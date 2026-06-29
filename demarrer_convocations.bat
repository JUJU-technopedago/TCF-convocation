@echo off
echo ======================================================
echo     DEMARRAGE DU GENERATEUR DE CONVOCATIONS SECURISE
echo ======================================================
echo.

REM Définir les variables d'environnement
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=utf-8

REM Vérifier si Python est disponible
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo Python non trouvé! Vérifiez l'installation de Python.
  pause
  exit /b 1
)

REM Démarrer l'application sécurisée
echo Démarrage du lanceur sécurisé...
python lancer_application.py

REM Gestion d'erreurs
if %ERRORLEVEL% NEQ 0 (
  echo.
  echo Une erreur est survenue lors de l'exécution de l'application.
  echo Code d'erreur: %ERRORLEVEL%
  pause
)