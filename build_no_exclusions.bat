@echo off
echo ===========================================
echo   BUILD SANS EXCLUSIONS (PLUS SUR)
echo ===========================================
echo.

call .venv\Scripts\activate.bat

echo Test des imports...
python -c "import pandas, numpy, jinja2, mailjet_rest; print('Tous les imports OK')"

echo.
echo Nettoyage...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo Construction SANS exclusions...
pyinstaller --onefile --windowed main.py ^
    --name "ConvocationGenerator" ^
    --add-data "templates;templates" ^
    --add-data "assets;assets" ^
    --add-data "*.json;." ^
    --add-data "*.svg;." ^
    --add-data "*.png;."

echo.
if exist "dist\ConvocationGenerator.exe" (
    echo ✅ SUCCES ! 
    echo 📁 Fichier: dist\ConvocationGenerator.exe
) else (
    echo ❌ ECHEC
)

pause