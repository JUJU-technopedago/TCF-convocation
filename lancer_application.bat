@echo off
echo ===========================================
echo   LANCEMENT CONVOCATION GENERATOR CORRIGE
echo ===========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ❌ ERREUR: Environnement virtuel non trouve
    echo.
    echo L'environnement virtuel .venv est requis pour eviter
    echo les problemes de dependances (CAST5, cryptography)
    echo.
    pause
    exit /b 1
)

echo ✅ Utilisation de l'environnement virtuel (.venv)
echo 🔧 Cryptography 41.0.7 (compatible mailjet)
echo 🚀 Lancement de ConvocationGenerator...
echo.

cd /d "%~dp0"
.venv\Scripts\python.exe main.py

if errorlevel 1 (
    echo.
    echo ❌ ERREUR: Application fermee avec erreur
    echo.
    echo SOLUTIONS:
    echo - Utilisez ce script au lieu de double-cliquer main.py
    echo - L'environnement virtuel corrige le probleme cryptography
    echo - Verifiez que les fichiers Excel sont au bon format
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Application fermee normalement
pause
