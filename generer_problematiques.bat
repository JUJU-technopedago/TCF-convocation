@echo off
echo ==========================================
echo Générateur de convocations - Template Fixé
echo ==========================================
echo.
echo Génération avec les candidats problématiques...
echo.

powershell.exe -Command "& python generate_with_fixed_template.py problematic"

echo.
echo Appuyez sur une touche pour quitter...
pause > nul