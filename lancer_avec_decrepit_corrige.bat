@echo off
echo ======================================================
echo     DEMARRAGE SECURISE AVEC MODULE DECREPIT CORRIGE
echo ======================================================
echo.

REM Définir les variables d'environnement
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=utf-8
set PYTHONPATH=%~dp0
set PYTHONDONTWRITEBYTECODE=1

REM Vérifier si Python est disponible
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo Python non trouve! Verifiez l'installation de Python.
  pause
  exit /b 1
)

REM Vérifier si le module decrepit est correctement installé
echo Verification du module decrepit...
python -c "import cryptography.hazmat.decrepit.ciphers.algorithms" 2>nul
if %ERRORLEVEL% NEQ 0 (
  echo Installation du module de remplacement...
  python installer_module_ascii.py
  if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors de l'installation du module de remplacement.
    pause
    exit /b 1
  )
)

REM Démarrer l'application principale
echo Demarrage de l'application...
python main.py

REM Gestion d'erreurs
if %ERRORLEVEL% NEQ 0 (
  echo.
  echo Une erreur est survenue lors de l'execution de l'application.
  echo Code d'erreur: %ERRORLEVEL%
  pause
)