@echo off
echo ===============================================
echo   CREATION EXECUTABLE CONVOCATION GENERATOR
echo          VERSION STABLE FINALE
echo ===============================================
echo.

REM Verification des prerequis
echo [1/8] Verification de l'environnement...
if not exist ".venv\Scripts\python.exe" (
    echo ❌ ERREUR: Environnement virtuel non trouve
    echo Creez d'abord un venv: python -m venv .venv
    pause
    exit /b 1
)

echo ✅ Environnement virtuel trouve
call .venv\Scripts\activate.bat

echo.
echo [2/8] Test de l'application stable...
echo Test rapide des imports critiques...

REM Creation d'un script temporaire pour les tests
echo import main > test_imports_temp.py
echo import tkinter >> test_imports_temp.py
echo import pandas >> test_imports_temp.py
echo import numpy >> test_imports_temp.py
echo import cryptography >> test_imports_temp.py
echo import mailjet_rest >> test_imports_temp.py
echo import jinja2 >> test_imports_temp.py
echo import xhtml2pdf >> test_imports_temp.py
echo print('✅ Tous les imports fonctionnent!') >> test_imports_temp.py

.venv\Scripts\python.exe test_imports_temp.py
set TEST_RESULT=%errorlevel%
del test_imports_temp.py 2>nul

if %TEST_RESULT% neq 0 (
    echo ❌ Probleme avec les imports
    echo Verifiez que l'application fonctionne avec: lancer_application.bat
    pause
    exit /b 1
)

echo ✅ Application stable confirmee

echo.
echo [3/8] Installation/mise a jour de PyInstaller...
pip install --upgrade pyinstaller>=6.0

echo.
echo [4/8] Sauvegarde et nettoyage...
if exist "dist" (
    if exist "dist_backup" rmdir /s /q "dist_backup"
    move "dist" "dist_backup"
    echo ✅ Ancienne version sauvegardee dans dist_backup
)

if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"
echo ✅ Nettoyage termine

echo.
echo [5/8] Verification des ressources...
if not exist "templates" (
    echo ❌ ATTENTION: Dossier templates manquant
)
if not exist "assets" (
    echo ❌ ATTENTION: Dossier assets manquant
)
if not exist "logoAF.svg" (
    echo ⚠️  logoAF.svg non trouve
)
if not exist "logoDELF.svg" (
    echo ⚠️  logoDELF.svg non trouve
)

echo.
echo [6/8] Creation de l'executable...
echo (Ceci peut prendre 5-10 minutes selon votre machine)
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "ConvocationGenerator" ^
    --icon="assets\logo.ico" ^
    --add-data "templates;templates" ^
    --add-data "templates_fixed;templates_fixed" ^
    --add-data "assets;assets" ^
    --add-data "logoAF.svg;." ^
    --add-data "logoDELF.svg;." ^
    --add-data "modele_convocation.docx;." ^
    --add-data "graphics_config.json;." ^
    --add-data "*.json;." ^
    --add-data "requirements.txt;." ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.filedialog ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.font ^
    --hidden-import pandas ^
    --hidden-import pandas.core ^
    --hidden-import numpy ^
    --hidden-import numpy.core ^
    --hidden-import numpy.core._multiarray_umath ^
    --hidden-import openpyxl ^
    --hidden-import openpyxl.workbook ^
    --hidden-import openpyxl.worksheet ^
    --hidden-import jinja2 ^
    --hidden-import jinja2.ext ^
    --hidden-import xhtml2pdf ^
    --hidden-import xhtml2pdf.default ^
    --hidden-import mailjet_rest ^
    --hidden-import cryptography ^
    --hidden-import reportlab ^
    --hidden-import reportlab.graphics ^
    --hidden-import reportlab.graphics.barcode ^
    --hidden-import reportlab.graphics.barcode.code128 ^
    --hidden-import pdf_generator ^
    --hidden-import jury_file_processor ^
    --hidden-import mailjet_bridge ^
    --hidden-import email_auth ^
    --hidden-import oauth_auth ^
    --hidden-import login_dialog ^
    --collect-all pandas ^
    --collect-all numpy ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module IPython ^
    --exclude-module jupyter ^
    --exclude-module pytest ^
    --exclude-module sphinx ^
    --exclude-module numba ^
    main.py

if errorlevel 1 (
    echo.
    echo ❌ ERREUR: Creation de l'executable echouee
    echo.
    echo Solutions possibles:
    echo 1. Verifiez que l'application fonctionne: .\lancer_application.bat
    echo 2. Reinstallez PyInstaller: pip install --force-reinstall pyinstaller
    echo 3. Redemarrez et re-essayez
    echo.
    pause
    exit /b 1
)

echo.
echo [7/8] Verification de l'executable...
if exist "dist\ConvocationGenerator.exe" (
    echo ✅ Executable cree avec succes !
    
    REM Taille du fichier
    for %%I in ("dist\ConvocationGenerator.exe") do (
        set size=%%~zI
        set /a sizeMB=!size!/1048576
        echo 📊 Taille: !sizeMB! MB
        echo 📅 Date: %%~tI
    )
    
    REM Creation du package de distribution
    echo.
    echo [8/8] Creation du package de distribution...
    if not exist "distribution" mkdir "distribution"
    
    copy "dist\ConvocationGenerator.exe" "distribution\"
    copy "README.md" "distribution\LISEZMOI.txt" 2>nul
    
    REM Creation d'un fichier d'instructions
    echo Generateur de Convocations d'Examens > "distribution\INSTRUCTIONS.txt"
    echo ======================================= >> "distribution\INSTRUCTIONS.txt"
    echo. >> "distribution\INSTRUCTIONS.txt"
    echo UTILISATION: >> "distribution\INSTRUCTIONS.txt"
    echo 1. Double-cliquez sur ConvocationGenerator.exe >> "distribution\INSTRUCTIONS.txt"
    echo 2. L'application s'ouvrira automatiquement >> "distribution\INSTRUCTIONS.txt"
    echo 3. Suivez les instructions a l'ecran >> "distribution\INSTRUCTIONS.txt"
    echo. >> "distribution\INSTRUCTIONS.txt"
    echo REMARQUES: >> "distribution\INSTRUCTIONS.txt"
    echo - Aucune installation requise >> "distribution\INSTRUCTIONS.txt"
    echo - Fonctionne sur Windows 10/11 >> "distribution\INSTRUCTIONS.txt"
    echo - Portable: copiez le fichier .exe ou vous voulez >> "distribution\INSTRUCTIONS.txt"
    echo. >> "distribution\INSTRUCTIONS.txt"
    echo Version compilee le: %date% %time% >> "distribution\INSTRUCTIONS.txt"
    
    echo ✅ Package de distribution cree dans: distribution\
    
) else (
    echo ❌ ERREUR: Fichier executable non trouve
    exit /b 1
)

echo.
echo ===============================================
echo        ✅ CREATION REUSSIE !
echo ===============================================
echo.
echo 📁 Executable: dist\ConvocationGenerator.exe
echo 📦 Package: distribution\ConvocationGenerator.exe
echo.
echo 🧪 TESTS RECOMMANDES:
echo 1. Testez l'executable: dist\ConvocationGenerator.exe
echo 2. Verifiez l'ouverture des fichiers Excel
echo 3. Testez la generation de PDF
echo 4. Verifiez les images de niveaux
echo 5. Testez l'envoi d'emails (si configure)
echo.
echo 💡 DISTRIBUTION:
echo - Fichier portable: distribution\ConvocationGenerator.exe
echo - Aucune installation requise sur les autres PC
echo - Compatible Windows 10/11 64-bit
echo.
echo 🎯 L'executable est pret pour la distribution !
echo.
pause