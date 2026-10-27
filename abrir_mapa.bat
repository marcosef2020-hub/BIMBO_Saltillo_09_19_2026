@echo off
REM Inicia un servidor local y abre el mapa en el navegador.
REM Cierra esta ventana para detener el servidor.
cd /d "%~dp0"
start "" http://localhost:8000
python -m http.server 8000
