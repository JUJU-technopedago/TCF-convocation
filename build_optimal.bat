@echo off
echo ===========================================
echo   CONSTRUCTION EXECUTABLE - VERSION OPTIMALE
echo ===========================================
echo.

echo [1/5] Installation des dependances principales...
pip install pyinstaller>=5.0
pip install pandas openpyxl jinja2 xhtml2pdf mailjet-rest
if errorlevel 1 (
    echo ERREUR: Installation des dependances principales echouee
    pause
    exit /b 1
)

echo.
echo [2/5] Installation des dependances optionnelles (pour eviter les warnings)...
pip install numba pytz python-dateutil six
echo Note: Les erreurs ci-dessus sont normales si certains packages ne sont pas compatibles

echo.
echo [3/5] Verification des imports critiques...
python -c "import pandas, openpyxl, jinja2; print('Imports critiques: OK')" 2>nul
if errorlevel 1 (
    echo ERREUR: Les imports critiques echouent
    echo Reinstallation forcee...
    pip install --upgrade --force-reinstall pandas openpyxl jinja2
)

echo.
echo [4/5] Nettoyage des anciens builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo [5/5] Construction de l'executable optimise...
pyinstaller --onefile ^
    --windowed ^
    --name "ConvocationGenerator" ^
    --icon=logoAF.ico ^
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
    --hidden-import pandas._libs.tslibs.base ^
    --hidden-import pandas.core ^
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
    --hidden-import six ^
    --hidden-import dateutil ^
    --collect-all pandas ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module IPython ^
    --exclude-module jupyter ^
    --exclude-module numba ^
    --exclude-module dask ^
    --exclude-module bottleneck ^
    --exclude-module numexpr ^
    --exclude-module tables ^
    --exclude-module xlsxwriter ^
    --exclude-module xlrd ^
    --exclude-module pytest ^
    --exclude-module sphinx ^
    main.py

if errorlevel 1 (
    echo.
    echo ERREUR: Construction echouee
    echo.
    echo SOLUTIONS POSSIBLES:
    echo 1. Redemarrez votre terminal en tant qu'administrateur
    echo 2. Essayez: pip install --upgrade pip setuptools wheel
    echo 3. Verifiez que Python est dans votre PATH
    echo.
    pause
    exit /b 1
)

echo.
echo ===========================================
echo      CONSTRUCTION REUSSIE ! 🎉
echo ===========================================
echo.
echo ✅ Executable cree: dist\ConvocationGenerator.exe
echo.

REM Verification de la taille du fichier
for %%I in ("dist\ConvocationGenerator.exe") do (
    set /a size=%%~zI/1048576
    echo 📊 Taille: !size! MB environ
)

echo.
echo 🚀 INSTRUCTIONS:
echo    1. Testez: dist\ConvocationGenerator.exe
echo    2. L'executable est portable (aucune installation requise)
echo    3. Copiez-le ou vous voulez l'utiliser
echo.
echo ⚠️  IMPORTANT: Testez toutes les fonctionnalites avant distribution
echo.
pause