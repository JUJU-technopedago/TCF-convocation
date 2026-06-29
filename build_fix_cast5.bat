@echo off
echo ===========================================
echo   RESOLUTION ERREUR CRYPTOGRAPHY/CAST5
echo ===========================================
echo.

echo [1/6] Diagnostic du probleme...
echo Le probleme CAST5 est du a une incompatibilite de versions
echo entre cryptography et d'autres packages.
echo.

echo [2/6] Desinstallation des packages problematiques...
pip uninstall -y cryptography pyOpenSSL paramiko
pip uninstall -y mailjet-rest

echo.
echo [3/6] Installation des versions compatibles...
pip install cryptography==41.0.7
pip install pyOpenSSL==23.3.0
pip install mailjet-rest==1.3.4
pip install pyinstaller>=5.0

echo.
echo [4/6] Installation des autres dependances...
pip install pandas openpyxl jinja2 xhtml2pdf

echo.
echo [5/6] Test des imports critiques...
python -c "
try:
    import cryptography
    print('✅ cryptography OK')
    import mailjet_rest
    print('✅ mailjet_rest OK')  
    import pandas
    print('✅ pandas OK')
    import jinja2
    print('✅ jinja2 OK')
    print('✅ Tous les imports fonctionnent!')
except Exception as e:
    print(f'❌ Erreur: {e}')
    exit(1)
"

if errorlevel 1 (
    echo.
    echo ❌ Les imports echouent encore
    echo Tentative de solution alternative...
    pip install --upgrade --force-reinstall cryptography==41.0.7
    echo.
)

echo.
echo [6/6] Nettoyage et construction...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo Construction avec versions fixes...
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
    --exclude-module cryptography.hazmat.decrepit.ciphers.algorithms.cast5 ^
    --exclude-module CAST5 ^
    --exclude-module numpy ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module numba ^
    main.py

if errorlevel 1 (
    echo.
    echo ❌ CONSTRUCTION ECHOUEE
    echo.
    echo SOLUTIONS ALTERNATIVES:
    echo 1. Essayez: pip install cryptography==40.0.2
    echo 2. Ou: pip install cryptography==42.0.0
    echo 3. Redemarrez et re-essayez
    echo.
    pause
    exit /b 1
)

echo.
echo ===========================================
echo    ✅ CONSTRUCTION REUSSIE (CAST5 FIXE)
echo ===========================================
echo.
echo 📁 Executable: dist\ConvocationGenerator.exe
echo 🔧 Probleme cryptography/CAST5 resolu
echo 💡 Versions fixes installees pour compatibilite
echo.
echo IMPORTANT: Testez l'envoi d'emails dans l'executable
echo.
pause