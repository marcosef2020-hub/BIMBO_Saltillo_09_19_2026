# Mapa de árboles

Mapa web interactivo del inventario de árboles levantado en campo con QField.

- Cada árbol se muestra con su foto como símbolo.
- Al pasar el puntero aparece una tarjeta con la foto grande y el nombre.
- Al hacer clic se abre un popup con la foto y los datos (fecha, notas).
- Los árboles muy cercanos se agrupan; al acercar el zoom se separan.

## Estructura

| Archivo / carpeta | Para qué sirve |
|---|---|
| `index.html` | La página del mapa (Leaflet + MarkerCluster). |
| `datos/arboles.geojson` | Los 58 árboles con nombre, nota, fecha y archivo de foto. |
| `fotos/` | Fotos reducidas (900 px) que se ven en la tarjeta y el popup. |
| `fotos/mini/` | Miniaturas (120 px) que se usan como símbolo. |
| `exportar.py` | Genera `datos/` y `fotos/` desde el proyecto de QField. Solo funciona en la computadora que tiene `notes.gpkg` en la carpeta superior. |
| `abrir_mapa.bat` | Abre el mapa en local (Windows, requiere Python). |
| `.nojekyll` | Le indica a GitHub Pages que sirva los archivos tal cual. |

## Ver el mapa en local

Abre `index.html` con doble clic **no funciona** (el navegador bloquea la lectura del GeoJSON).
Usa `abrir_mapa.bat`, o ejecuta en esta carpeta:

```
python -m http.server 8000
```

y abre http://localhost:8000.

## Actualizar los datos

1. Copia el proyecto actualizado de QField junto a la carpeta `mapa_web`.
2. Ejecuta `python exportar.py` (requiere `pip install pillow`).
3. Sube los cambios a GitHub.

## Créditos

Mapa base © colaboradores de OpenStreetMap. Hecho con Leaflet.
