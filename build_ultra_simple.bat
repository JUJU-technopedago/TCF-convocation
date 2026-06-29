@echo off
echo ===========================================
echo   BUILD ULTRA SIMPLE SANS WARNINGS
echo ===========================================
echo.

call .venv\Scripts\activate.bat

echo Nettoyage...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo Construction sans modules de tests...
pyinstaller --onefile --windowed main.py ^
    --name "ConvocationGenerator" ^
    --add-data "templates;templates" ^
    --add-data "assets;assets" ^
    --add-data "*.json;." ^
    --add-data "*.svg;." ^
    --add-data "*.png;." ^
    --hidden-import pandas ^
    --hidden-import numpy ^
    --hidden-import openpyxl ^
    --hidden-import jinja2 ^
    --hidden-import xhtml2pdf ^
    --hidden-import mailjet_rest ^
    --exclude-module pytest ^
    --exclude-module pandas.tests ^
    --exclude-module numpy.tests ^
    --exclude-module numpy.f2py.tests ^
    --exclude-module pandas.tests.extension.base ^
    --collect-all pandas ^
    --collect-all numpy

if exist "dist\ConvocationGenerator.exe" (
    echo.
    echo ✅ CONSTRUCTION REUSSIE !
    echo 📁 Fichier: dist\ConvocationGenerator.exe
    
    REM Taille du fichier
    for %%I in ("dist\ConvocationGenerator.exe") do (
        set size=%%~zI
        set /a sizeMB=!size!/1048576
        echo 📊 Taille: !sizeMB! MB
    )
    
    echo.
    echo 🧪 TEST RAPIDE DE L'EXECUTABLE...
    echo (Lancement de 3 secondes pour tester)
    timeout /t 1 /nobreak >nul
    start /wait /b dist\ConvocationGenerator.exe
    
) else (
    echo ❌ ECHEC - Fichier non créé
)

echo.
echo Terminé !
pause