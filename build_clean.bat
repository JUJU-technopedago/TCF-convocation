@echo off
echo ===========================================
echo   BUILD PROPRE SANS WARNINGS DECREPIT
echo ===========================================
echo.

echo [1/6] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

echo.
echo [2/6] Nettoyage des fichiers problematiques...
if exist ".venv\Lib\site-packages\decrepit_patch.pth" (
    echo Suppression du fichier decrepit_patch.pth problematique...
    del ".venv\Lib\site-packages\decrepit_patch.pth"
)

echo.
echo [3/6] Verification des versions (sans warnings)...
python -c "import cryptography; print('✅ Cryptography:', cryptography.__version__)" 2>nul
python -c "import mailjet_rest; print('✅ Mailjet-rest: OK')" 2>nul
python -c "import pandas; print('✅ Pandas: OK')" 2>nul
python -c "import jinja2; print('✅ Jinja2: OK')" 2>nul

echo.
echo [4/6] Installation de PyInstaller...
pip install pyinstaller>=5.0 --quiet

echo.
echo [5/6] Nettoyage des anciens builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo [6/6] Construction de l'executable...
echo (Ceci peut prendre quelques minutes...)
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
    --exclude-module decrepit_import_hook ^
    main.py

if errorlevel 1 (
    echo.
    echo ❌ ERREUR: Construction echouee
    echo.
    echo Verifiez les messages d'erreur ci-dessus
    pause
    exit /b 1
)

echo.
echo ===========================================
echo        ✅ CONSTRUCTION REUSSIE !
echo ===========================================
echo.
echo 📁 Executable cree: dist\ConvocationGenerator.exe
echo.

REM Affichage de la taille
for %%I in ("dist\ConvocationGenerator.exe") do (
    set size=%%~zI
    set /a sizeMB=!size!/1048576
    echo 📊 Taille: !sizeMB! MB
)

echo.
echo 🎯 TESTS RECOMMANDES:
echo    1. Testez: dist\ConvocationGenerator.exe
echo    2. Verifiez la generation de PDF
echo    3. Testez l'envoi d'emails (si configure)
echo    4. Verifiez les images de niveau
echo.
echo 💡 L'executable est portable et pret a distribuer
echo.
pause