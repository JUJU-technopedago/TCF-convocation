@echo off
echo ===========================================
echo   BUILD FINAL AVEC NUMPY INCLUS
echo ===========================================
echo.

echo [1/5] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

echo.
echo [2/5] Installation des dependances manquantes...
pip install numpy --quiet
pip install pyinstaller>=5.0 --quiet

echo.
echo [3/5] Test des imports critiques...
python -c "import numpy; print('✅ NumPy OK')" 2>nul
python -c "import pandas; print('✅ Pandas OK')" 2>nul
python -c "import mailjet_rest; print('✅ Mailjet OK')" 2>nul

echo.
echo [4/5] Nettoyage...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo [5/5] Construction avec NUMPY inclus...
pyinstaller --onefile --windowed --name "ConvocationGenerator" ^
    --add-data "templates;templates" ^
    --add-data "templates_fixed;templates_fixed" ^
    --add-data "assets;assets" ^
    --add-data "*.json;." ^
    --add-data "*.xlsx;." ^
    --add-data "*.svg;." ^
    --add-data "*.png;." ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.filedialog ^
    --hidden-import tkinter.messagebox ^
    --hidden-import pandas ^
    --hidden-import numpy ^
    --hidden-import numpy.core ^
    --hidden-import numpy.core._multiarray_umath ^
    --hidden-import openpyxl ^
    --hidden-import jinja2 ^
    --hidden-import xhtml2pdf ^
    --hidden-import mailjet_rest ^
    --hidden-import pdf_generator ^
    --hidden-import jury_file_processor ^
    --hidden-import mailjet_bridge ^
    --collect-all pandas ^
    --collect-all numpy ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module numba ^
    main.py

if errorlevel 1 (
    echo.
    echo ❌ ERREUR: Construction echouee
    pause
    exit /b 1
)

echo.
echo ===========================================
echo        ✅ CONSTRUCTION REUSSIE !
echo ===========================================
echo.
echo 📁 Executable: dist\ConvocationGenerator.exe
echo 🔧 NumPy inclus pour pandas
echo 💡 Toutes les dependances incluses
echo.

REM Test rapide de l'executable
echo 🧪 Test rapide de l'executable...
if exist "dist\ConvocationGenerator.exe" (
    echo ✅ Fichier executable cree
    for %%I in ("dist\ConvocationGenerator.exe") do (
        set size=%%~zI
        set /a sizeMB=!size!/1048576
        echo 📊 Taille: !sizeMB! MB
    )
) else (
    echo ❌ Fichier executable non trouve
)

echo.
echo 🎯 IMPORTANT: Testez l'executable avant distribution
echo.
pause