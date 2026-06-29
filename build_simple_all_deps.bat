@echo off
echo ===========================================
echo   BUILD SIMPLE AVEC TOUTES LES DEPS
echo ===========================================
echo.

call .venv\Scripts\activate.bat

echo Nettoyage...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo Construction avec toutes les dependances...
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
    --collect-all pandas ^
    --collect-all numpy

if errorlevel 1 (
    echo ERREUR
    pause
    exit /b 1
)

echo.
echo ✅ FINI ! Fichier: dist\ConvocationGenerator.exe
pause