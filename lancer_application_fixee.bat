@echo off
echo =====================================================================
echo Générateur de Convocations - Application principale avec template fixé
echo =====================================================================
echo.
echo Démarrage de l'application...
echo.

powershell.exe -Command "& python main.py"

echo.
echo Appuyez sur une touche pour quitter...
pause > nul