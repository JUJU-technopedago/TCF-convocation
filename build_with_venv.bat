@echo off
echo ===========================================
echo   BUILD AVEC ENVIRONNEMENT VIRTUEL FIXE
echo ===========================================
echo.

echo [1/5] Activation de l'environnement virtuel...
if not exist ".venv\Scripts\activate.bat" (
    echo ERREUR: Environnement virtuel non trouve
    echo Creez d'abord un venv avec: python -m venv .venv
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

echo.
echo [2/5] Verification des versions...
python -c "import cryptography; print('Cryptography:', cryptography.__version__)"
python -c "import mailjet_rest; print('Mailjet-rest: OK')"

echo.
echo [3/5] Installation de PyInstaller dans le venv...
pip install pyinstaller>=5.0

echo.
echo [4/5] Nettoyage...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo [5/5] Construction avec environnement virtuel...
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
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.filedialog ^
    --hidden-import tkinter.messagebox ^
    --hidden-import pandas ^
    --hidden-import openpyxl ^
    --hidden-import jinja2 ^
    --hidden-import xhtml2pdf ^
    --hidden-import mailjet_rest ^
    --hidden-import pdf_generator ^
    --hidden-import jury_file_processor ^
    --hidden-import mailjet_bridge ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module numpy ^
    --exclude-module numba ^
    main.py

if errorlevel 1 (
    echo.
    echo ERREUR: Construction echouee
    pause
    exit /b 1
)

echo.
echo ✅ CONSTRUCTION REUSSIE AVEC VENV!
echo.
echo 📁 Executable: dist\ConvocationGenerator.exe
echo 🔧 Probleme CAST5 resolu avec cryptography 41.0.7
echo 💡 Construit avec l'environnement virtuel
echo.
echo IMPORTANT: L'executable est maintenant compatible
echo.
pause