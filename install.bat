@echo off
echo ========================================
echo Installation du Generateur de Convocations
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo Veuillez installer Python depuis https://python.org
    echo Assurez-vous de cocher "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

echo Python detecte:
python --version
echo.

REM Vérifier si pip est disponible
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: pip n'est pas disponible
    echo.
    pause
    exit /b 1
)

echo pip detecte:
pip --version
echo.

echo Installation des dependances Python...
echo.

REM Installer les dépendances
pip install pandas==2.1.4
if %errorlevel% neq 0 (
    echo ERREUR lors de l'installation de pandas
    pause
    exit /b 1
)

pip install openpyxl==3.1.2
if %errorlevel% neq 0 (
    echo ERREUR lors de l'installation de openpyxl
    pause
    exit /b 1
)

pip install weasyprint==60.2
if %errorlevel% neq 0 (
    echo ERREUR lors de l'installation de weasyprint
    pause
    exit /b 1
)

pip install jinja2==3.1.2
if %errorlevel% neq 0 (
    echo ERREUR lors de l'installation de jinja2
    pause
    exit /b 1
)

pip install pywin32==306
if %errorlevel% neq 0 (
    echo ERREUR lors de l'installation de pywin32
    pause
    exit /b 1
)

pip install pillow==10.1.0
if %errorlevel% neq 0 (
    echo ERREUR lors de l'installation de pillow
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation terminee avec succes!
echo ========================================
echo.

REM Créer les répertoires nécessaires
if not exist "templates" mkdir templates
if not exist "assets" mkdir assets
if not exist "output" mkdir output

echo Repertoires crees:
echo - templates/
echo - assets/
echo - output/
echo.

REM Créer un logo SVG simple si il n'existe pas
if not exist "assets\logo.svg" (
    echo Creation d'un logo d'exemple...
    echo ^<?xml version="1.0" encoding="UTF-8"?^> > assets\logo.svg
    echo ^<svg width="200" height="80" viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg"^> >> assets\logo.svg
    echo   ^<rect width="200" height="80" fill="#0066cc" rx="8"/^> >> assets\logo.svg
    echo   ^<text x="100" y="30" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="18" font-weight="bold"^>UNIVERSITE^</text^> >> assets\logo.svg
    echo   ^<text x="100" y="50" text-anchor="middle" fill="#e6f3ff" font-family="Arial, sans-serif" font-size="12"^>DE PARIS^</text^> >> assets\logo.svg
    echo   ^<circle cx="30" cy="40" r="15" fill="none" stroke="white" stroke-width="2"/^> >> assets\logo.svg
    echo   ^<circle cx="30" cy="40" r="8" fill="white"/^> >> assets\logo.svg
    echo   ^<polygon points="170,25 185,40 170,55" fill="white"/^> >> assets\logo.svg
    echo ^</svg^> >> assets\logo.svg
    echo Logo d'exemple cree dans assets\logo.svg
)

echo.
echo Pour lancer l'application, executez:
echo python main.py
echo.
echo Ou double-cliquez sur run.bat
echo.

REM Créer un script de lancement
echo @echo off > run.bat
echo echo Lancement du Generateur de Convocations... >> run.bat
echo python main.py >> run.bat
echo pause >> run.bat

echo Script de lancement cree: run.bat
echo.
echo Installation complete!
pause
