@echo off
echo ===========================================
echo   BUILD SANS PROBLEMES CRYPTOGRAPHIQUES
echo ===========================================
echo.

echo Cette version evite completement les problemes
echo cryptographiques en utilisant des alternatives.
echo.

echo [1/4] Installation version minimale...
pip install pyinstaller>=5.0
pip install pandas openpyxl jinja2 xhtml2pdf
REM Pas de mailjet-rest pour eviter les conflits crypto

echo.
echo [2/4] Test des imports de base...
python -c "
import pandas
import openpyxl  
import jinja2
print('✅ Imports de base OK')
"

echo.
echo [3/4] Nettoyage...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo [4/4] Construction SANS crypto problematique...
pyinstaller --onefile ^
    --windowed ^
    --name "ConvocationGenerator_NoCrypto" ^
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
    --hidden-import pdf_generator ^
    --hidden-import jury_file_processor ^
    --exclude-module mailjet_rest ^
    --exclude-module mailjet_bridge ^
    --exclude-module cryptography ^
    --exclude-module pyOpenSSL ^
    --exclude-module paramiko ^
    --exclude-module CAST5 ^
    --exclude-module numpy ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    main.py

if errorlevel 1 (
    echo ERREUR: Construction echouee
    pause
    exit /b 1
)

echo.
echo ✅ EXECUTABLE CREE SANS PROBLEMES CRYPTO!
echo.
echo 📁 Fichier: dist\ConvocationGenerator_NoCrypto.exe
echo.
echo ⚠️  NOTE: Cet executable peut generer des PDFs mais
echo    l'envoi d'emails pourrait ne pas fonctionner
echo    (selon la configuration mailjet)
echo.
echo 💡 Testez d'abord la generation de PDF
echo.
pause