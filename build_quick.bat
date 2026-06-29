@echo off
echo ===========================================
echo   BUILD RAPIDE ET DIRECT
echo ===========================================
echo.

echo Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

echo.
echo Nettoyage rapide...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo Construction directe...
pyinstaller --onefile --windowed --name "ConvocationGenerator" ^
    --add-data "templates;templates" ^
    --add-data "assets;assets" ^
    --add-data "*.json;." ^
    --add-data "*.svg;." ^
    --add-data "*.png;." ^
    --hidden-import tkinter ^
    --hidden-import pandas ^
    --hidden-import openpyxl ^
    --hidden-import jinja2 ^
    --hidden-import xhtml2pdf ^
    --hidden-import mailjet_rest ^
    --exclude-module numpy ^
    --exclude-module matplotlib ^
    main.py

if errorlevel 1 (
    echo ERREUR: Construction echouee
    pause
    exit /b 1
)

echo.
echo ✅ CONSTRUCTION TERMINEE !
echo 📁 Fichier: dist\ConvocationGenerator.exe
echo.
pause