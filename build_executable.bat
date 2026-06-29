@echo off
echo ===========================================
echo   CONSTRUCTION EXECUTABLE CONVOCATION
echo ===========================================
echo.

echo [1/3] Installation de PyInstaller...
pip install pyinstaller>=5.0
if errorlevel 1 (
    echo ERREUR: Installation de PyInstaller echouee
    pause
    exit /b 1
)

echo.
echo [2/3] Nettoyage des anciens builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo [3/3] Construction de l'executable...
pyinstaller --onefile ^
    --windowed ^
    --name "ConvocationGenerator" ^
    --add-data "templates;templates" ^
    --add-data "templates_fixed;templates_fixed" ^
    --add-data "assets;assets" ^
    --add-data "*.json;." ^
    --add-data "*.xlsx;." ^
    --add-data "*.docx;." ^
    --add-data "*.svg;." ^
    --add-data "*.png;." ^
    --add-data "requirements.txt;." ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.filedialog ^
    --hidden-import tkinter.messagebox ^
    --hidden-import pandas ^
    --hidden-import numpy ^
    --hidden-import openpyxl ^
    --hidden-import jinja2 ^
    --hidden-import xhtml2pdf ^
    --hidden-import mailjet_rest ^
    --hidden-import pdf_generator ^
    --hidden-import jury_file_processor ^
    --hidden-import mailjet_bridge ^
    --hidden-import pytz ^
    --collect-all pandas ^
    --collect-all numpy ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    main.py

if errorlevel 1 (
    echo.
    echo ERREUR: Construction echouee
    echo Verifiez les messages d'erreur ci-dessus
    pause
    exit /b 1
)

echo.
echo ===========================================
echo          CONSTRUCTION REUSSIE !
echo ===========================================
echo.
echo Executable cree: dist\ConvocationGenerator.exe
echo.
echo Instructions:
echo 1. Testez l'executable dans le dossier 'dist'
echo 2. Copiez ConvocationGenerator.exe ou vous voulez
echo 3. L'executable est portable (pas d'installation)
echo.
pause