@echo off
echo ===================================================
echo Création d'un template HTML fixé dans les templates
echo ===================================================
echo.
echo Ce script crée une version corrigée du template HTML
echo pour éviter les erreurs de génération de PDF.
echo.

powershell.exe -Command "& python creer_template_fixe.py"

echo.
echo Appuyez sur une touche pour quitter...
pause > nul