@echo off
rem Script pour générer les convocations avec le template HTML spécifique
echo Générateur de convocations avec TEMPLATE HTML
echo ===============================================
echo.

rem Définir le fichier Excel à utiliser
set EXCEL_FILE=juries_20250820_192410.xlsx
set OUTPUT_DIR=output_html_template

rem Vérifier si un fichier Excel a été spécifié
if not "%~1"=="" (
  set EXCEL_FILE=%~1
)

rem Vérifier si un répertoire de sortie a été spécifié
if not "%~2"=="" (
  set OUTPUT_DIR=%~2
)

echo Fichier Excel: %EXCEL_FILE%
echo Template HTML: templates\convocation_delf_template_modele.html
echo Répertoire de sortie: %OUTPUT_DIR%
echo.

rem Vérifier que le fichier Excel existe
if not exist "%EXCEL_FILE%" (
  echo ERREUR: Le fichier Excel '%EXCEL_FILE%' n'existe pas.
  goto :end
)

rem Vérifier que le template HTML existe
if not exist "templates\convocation_delf_template_modele.html" (
  echo ERREUR: Le template HTML 'templates\convocation_delf_template_modele.html' n'existe pas.
  goto :end
)

echo DÉMARRAGE DE LA GÉNÉRATION DES CONVOCATIONS...
echo.

python generate_with_html_template.py "%EXCEL_FILE%" "%OUTPUT_DIR%"

echo.
echo ===============================================
echo Traitement terminé.
echo.
echo Appuyez sur une touche pour quitter...

:end
pause