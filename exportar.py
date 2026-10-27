"""
exportar.py - Convierte los datos de QField en los archivos que usa el mapa web.

Qué hace:
  1. Lee los árboles de notes.gpkg (un GeoPackage es una base de datos SQLite).
  2. Busca la foto de cada árbol en la tabla notes_attachments.
  3. Guarda datos/arboles.geojson con nombre, nota, fecha y foto.
  4. Crea copias reducidas de las fotos (grandes y miniaturas).

Cómo ejecutarlo:  python exportar.py   (necesita Pillow: pip install pillow)
Si agregas más árboles en QField, vuelve a copiar el proyecto y ejecútalo otra vez.
"""
import sqlite3, json, struct
from pathlib import Path
from PIL import Image, ImageOps

AQUI = Path(__file__).resolve().parent      # carpeta mapa_web
PROYECTO = AQUI.parent                      # carpeta del proyecto QField

TAM_FOTO = 900    # ancho máximo (px) de la foto grande (popup y tarjeta)
TAM_MINI = 120    # lado (px) de la miniatura que se usa como símbolo

# ---------- 1. Leer la geometría de un GeoPackage ----------
def leer_punto(blob):
    """GeoPackage guarda cada geometría con una cabecera + formato WKB.
    Devuelve (longitud, latitud)."""
    flags = blob[3]
    tam_envolvente = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(flags >> 1) & 0b111]
    inicio = 8 + tam_envolvente                      # donde empieza el WKB
    orden = '<' if blob[inicio] == 1 else '>'        # little o big endian
    x, y = struct.unpack(orden + 'dd', blob[inicio + 5: inicio + 21])
    return x, y

# ---------- 2. Redimensionar fotos ----------
def procesar_foto(origen, nombre):
    """Genera fotos/nombre (grande) y fotos/mini/nombre (miniatura cuadrada)."""
    img = Image.open(origen)
    img = ImageOps.exif_transpose(img)               # respeta la orientación del celular
    img = img.convert('RGB')
    grande = img.copy()
    grande.thumbnail((TAM_FOTO, TAM_FOTO))
    grande.save(AQUI / 'fotos' / nombre, quality=82, optimize=True)
    mini = ImageOps.fit(img, (TAM_MINI, TAM_MINI))   # recorte cuadrado centrado
    mini.save(AQUI / 'fotos' / 'mini' / nombre, quality=80, optimize=True)

# ---------- 3. Construir el GeoJSON ----------
con = sqlite3.connect(PROYECTO / 'notes.gpkg')
fotos = dict(con.execute('SELECT note_uuid, media FROM notes_attachments'))

features, sin_foto = [], []
for fid, geom, uuid, titulo, nota, fecha in con.execute(
        'SELECT fid, geom, uuid, title, note, timestamp FROM notes_point ORDER BY fid'):
    lon, lat = leer_punto(geom)

    # Un punto se capturó con el nombre en el campo "nota": lo usamos como nombre.
    nombre = (titulo or nota or f'Punto {fid}').strip()
    nota_extra = nota.strip() if (titulo and nota) else None

    archivo = None
    ruta = fotos.get(uuid)                           # p. ej. 'DCIM/JPEG_2026....jpg'
    if ruta:
        archivo = Path(ruta).name
        procesar_foto(PROYECTO / ruta, archivo)
    else:
        sin_foto.append(nombre)

    features.append({
        'type': 'Feature',
        'properties': {'nombre': nombre, 'nota': nota_extra,
                       'fecha': (fecha or '')[:10], 'foto': archivo},
        'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
    })

salida = AQUI / 'datos' / 'arboles.geojson'
salida.write_text(json.dumps({'type': 'FeatureCollection', 'features': features},
                             ensure_ascii=False, indent=1), encoding='utf-8')

print(f'{len(features)} árboles exportados -> {salida}')
print('Sin foto:', sin_foto or 'ninguno')
