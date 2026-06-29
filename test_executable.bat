@echo off
echo ===========================================
echo   TEST DE L'EXECUTABLE CONVOCATION
echo ===========================================
echo.

if not exist "dist\ConvocationGenerator.exe" (
    echo ❌ ERREUR: Executable non trouve dans dist\
    echo.
    echo Verifiez que la construction s'est bien terminee
    pause
    exit /b 1
)

echo ✅ Executable trouve: dist\ConvocationGenerator.exe
echo.

REM Affichage des informations
for %%I in ("dist\ConvocationGenerator.exe") do (
    set size=%%~zI
    set /a sizeMB=!size!/1048576
    echo 📊 Taille: !sizeMB! MB
    echo 📅 Date: %%~tI
)

echo.
echo 🧪 TEST DE LANCEMENT...
echo.
echo IMPORTANT: 
echo - L'executable va se lancer
echo - Testez la generation de PDF
echo - Testez l'ouverture de fichier Excel
echo - Fermez l'application normalement
echo.
echo Appuyez sur une touche pour lancer le test...
pause >nul

echo.
echo Lancement de ConvocationGenerator.exe...
start "" "dist\ConvocationGenerator.exe"

echo.
echo ✅ Test lance !
echo.
echo 💡 Si l'application s'ouvre correctement, votre executable est pret !
echo 💡 Vous pouvez maintenant copier ConvocationGenerator.exe ou vous voulez
echo.
pause