@echo off
echo ===========================================
echo   CONSTRUCTION EXECUTABLE - VERSION FIXEE
echo ===========================================
echo.

echo [1/4] Installation des dependances requises...
pip install pyinstaller>=5.0
pip install pandas numpy openpyxl jinja2 xhtml2pdf mailjet-rest
if errorlevel 1 (
    echo ERREUR: Installation des dependances echouee
    pause
    exit /b 1
)

echo.
echo [2/4] Verification des imports...
python -c "import pandas, numpy, openpyxl, jinja2" 2>nul
if errorlevel 1 (
    echo ERREUR: Certaines dependances ne sont pas correctement installees
    echo Tentative de reinstallation...
    pip install --upgrade --force-reinstall pandas numpy openpyxl
)

echo.
echo [3/4] Nettoyage des anciens builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo [4/4] Construction de l'executable avec toutes les dependances...
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
    --hidden-import pandas._libs ^
    --hidden-import pandas._libs.tslibs ^
    --hidden-import pandas._libs.tslibs.base ^
    --hidden-import pandas.core ^
    --hidden-import pandas.core.common ^
    --hidden-import pandas.core.ops ^
    --hidden-import numpy ^
    --hidden-import numpy.core ^
    --hidden-import numpy.core._multiarray_umath ^
    --hidden-import numpy.core._multiarray_tests ^
    --hidden-import numpy.linalg ^
    --hidden-import numpy.fft ^
    --hidden-import numpy.random ^
    --hidden-import openpyxl ^
    --hidden-import openpyxl.workbook ^
    --hidden-import openpyxl.worksheet ^
    --hidden-import jinja2 ^
    --hidden-import jinja2.ext ^
    --hidden-import xhtml2pdf ^
    --hidden-import mailjet_rest ^
    --hidden-import pdf_generator ^
    --hidden-import jury_file_processor ^
    --hidden-import mailjet_bridge ^
    --hidden-import pytz ^
    --collect-all pandas ^
    --collect-all numpy ^
    --collect-all openpyxl ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module IPython ^
    --exclude-module jupyter ^
    main.py

if errorlevel 1 (
    echo.
    echo ERREUR: Construction echouee
    echo.
    echo DIAGNOSTIC POSSIBLE:
    echo - Verifiez que toutes les dependances sont installees
    echo - Essayez: pip install --upgrade pandas numpy openpyxl
    echo - Redemarrez votre terminal et re-essayez
    echo.
    pause
    exit /b 1
)

echo.
echo ===========================================
echo      CONSTRUCTION REUSSIE ! - VERSION FIXEE
echo ===========================================
echo.
echo Executable cree: dist\ConvocationGenerator.exe
echo.
echo IMPORTANT: Testez l'executable avant distribution
echo.
pause