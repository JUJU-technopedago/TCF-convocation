@echo off
rem Script pour générer les convocations avec le template HTML fixé
echo Générateur de convocations avec TEMPLATE HTML FIXÉ
echo ==================================================
echo.

rem Définir le fichier Excel à utiliser
set EXCEL_FILE=juries_20250820_192410.xlsx
set OUTPUT_DIR=output_fixed_template

rem Vérifier si un fichier Excel a été spécifié
if not "%~1"=="" (
  set EXCEL_FILE=%~1
)

rem Vérifier si un répertoire de sortie a été spécifié
if not "%~2"=="" (
  set OUTPUT_DIR=%~2
)

echo Fichier Excel: %EXCEL_FILE%
echo Répertoire de sortie: %OUTPUT_DIR%
echo.

rem Vérifier que le fichier Excel existe
if not exist "%EXCEL_FILE%" (
  echo ERREUR: Le fichier Excel '%EXCEL_FILE%' n'existe pas.
  goto :end
)

echo DÉMARRAGE DE LA GÉNÉRATION DES CONVOCATIONS...
echo.

powershell.exe -Command "& python generate_with_fixed_template.py '%EXCEL_FILE%' '%OUTPUT_DIR%'"

echo.
echo ==================================================
echo Traitement terminé.
echo.
echo Appuyez sur une touche pour quitter...

:end
pause