@echo off
echo ===========================================
echo   CONSTRUCTION EXECUTABLE - VERSION LEGERE
echo ===========================================
echo.
echo Cette version exclut numba et autres dependances lourdes
echo pour un executable plus petit et plus rapide.
echo.

echo [1/4] Installation minimale...
pip install pyinstaller>=5.0 pandas openpyxl jinja2 xhtml2pdf mailjet-rest

echo.
echo [2/4] Verification...
python -c "import pandas, openpyxl, jinja2; print('✅ Imports OK')"

echo.
echo [3/4] Nettoyage...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo [4/4] Construction legere (sans numba/numpy lourd)...
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
    --exclude-module numpy ^
    --exclude-module numba ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module dask ^
    --exclude-module bottleneck ^
    --exclude-module numexpr ^
    --exclude-module tables ^
    --exclude-module IPython ^
    --exclude-module jupyter ^
    main.py

if errorlevel 1 (
    echo ERREUR: Construction echouee
    pause
    exit /b 1
)

echo.
echo ✅ EXECUTABLE LEGER CREE !
echo 📁 Emplacement: dist\ConvocationGenerator.exe
echo 💡 Cette version devrait etre plus petite et plus rapide
echo.
pause