@echo off
echo ===========================================
echo   VERIFICATION ENVIRONNEMENT CONVOCATION
echo ===========================================
echo.

echo [1/5] Verification environnement virtuel...
if exist ".venv\Scripts\python.exe" (
    echo ✅ Environnement virtuel trouve
) else (
    echo ❌ Environnement virtuel manquant
    echo.
    echo Pour creer l'environnement virtuel:
    echo python -m venv .venv
    echo.
    pause
    exit /b 1
)

echo.
echo [2/5] Test des imports critiques...
.venv\Scripts\python.exe -c "
try:
    import cryptography
    print(f'✅ cryptography: {cryptography.__version__}')
    import mailjet_rest
    print('✅ mailjet_rest: OK')
    import pandas
    print(f'✅ pandas: {pandas.__version__}')
    import numpy
    print(f'✅ numpy: {numpy.__version__}')
    import jinja2
    print('✅ jinja2: OK')
    import xhtml2pdf
    print('✅ xhtml2pdf: OK')
except Exception as e:
    print(f'❌ Erreur import: {e}')
    exit(1)
"

if errorlevel 1 (
    echo.
    echo ❌ Probleme avec les imports
    echo Reinstallez les dependances:
    echo .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo [3/5] Verification des fichiers requis...
if exist "main.py" (
    echo ✅ main.py trouve
) else (
    echo ❌ main.py manquant
)

if exist "templates" (
    echo ✅ Dossier templates trouve
) else (
    echo ❌ Dossier templates manquant
)

if exist "assets" (
    echo ✅ Dossier assets trouve
) else (
    echo ❌ Dossier assets manquant
)

echo.
echo [4/5] Test de lancement rapide...
echo (Test de 2 secondes)
timeout /t 1 /nobreak >nul
.venv\Scripts\python.exe -c "
import sys
sys.path.append('.')
try:
    import main
    print('✅ Module main importable')
except Exception as e:
    print(f'❌ Erreur module main: {e}')
    exit(1)
"

if errorlevel 1 (
    echo ❌ Probleme avec main.py
    pause
    exit /b 1
)

echo.
echo [5/5] Verification builds...
if exist "dist\ConvocationGenerator.exe" (
    echo ✅ Executable trouve: dist\ConvocationGenerator.exe
    for %%I in ("dist\ConvocationGenerator.exe") do (
        set size=%%~zI
        set /a sizeMB=!size!/1048576
        echo   📊 Taille: !sizeMB! MB
    )
) else (
    echo ⚠️  Executable non construit (utilisez build_simple_all_deps.bat)
)

echo.
echo ===========================================
echo        ✅ VERIFICATION TERMINEE
echo ===========================================
echo.
echo 🎯 RECOMMANDATIONS:
echo   - Utilisez lancer_application.bat (pas main.py direct)
echo   - Pour l'executable: build_simple_all_deps.bat
echo   - En cas de probleme CAST5: utilisez toujours le .bat
echo.
pause