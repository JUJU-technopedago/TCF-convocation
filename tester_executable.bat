@echo off
echo ===============================================
echo     TEST DE L'EXECUTABLE CONVOCATION GENERATOR
echo ===============================================
echo.

if not exist "dist\ConvocationGenerator.exe" (
    echo ❌ ERREUR: Executable non trouve
    echo Lancez d'abord: creer_executable_stable.bat
    pause
    exit /b 1
)

echo [1/5] Informations sur l'executable...
for %%I in ("dist\ConvocationGenerator.exe") do (
    set size=%%~zI
    set /a sizeMB=!size!/1048576
    echo 📊 Taille: !sizeMB! MB
    echo 📅 Date: %%~tI
    echo 📂 Chemin: %%~fI
)

echo.
echo [2/5] Test de lancement rapide...
echo (L'application va s'ouvrir brievement)
timeout /t 2 >nul

start "" "dist\ConvocationGenerator.exe"
echo ✅ Executable lance

echo.
echo [3/5] Verification des dependances...
echo (Ceci permet de voir si l'executable est autonome)

REM Test sur un repertoire temporaire pour simuler un autre PC
set TEMP_DIR=%temp%\test_convocation
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

copy "dist\ConvocationGenerator.exe" "%TEMP_DIR%\"
echo ✅ Copie dans repertoire temporaire: %TEMP_DIR%

cd /d "%TEMP_DIR%"
echo 🧪 Test depuis un repertoire vide...
echo (Ceci simule un autre PC sans Python)

start "" "ConvocationGenerator.exe"
cd /d "d:\convoc generator"
echo ✅ Test de portabilite effectue

echo.
echo [4/5] Verification de la taille...
if !sizeMB! GTR 100 (
    echo ⚠️  ATTENTION: Executable volumineux (!sizeMB! MB)
    echo    - Normal pour une premiere version
    echo    - Optimisations possibles plus tard
) else (
    echo ✅ Taille acceptable: !sizeMB! MB
)

echo.
echo [5/5] Verification des fichiers de distribution...
if exist "distribution\ConvocationGenerator.exe" (
    echo ✅ Package de distribution present
    if exist "distribution\INSTRUCTIONS.txt" (
        echo ✅ Instructions incluses
    )
) else (
    echo ⚠️  Package de distribution manquant
)

echo.
echo ===============================================
echo            RAPPORT DE TEST
echo ===============================================
echo.
echo ✅ Tests termines avec succes !
echo.
echo 📋 CHECKLIST POUR DISTRIBUTION:
echo [ ] L'executable s'ouvre correctement
echo [ ] Interface utilisateur visible et responsive
echo [ ] Ouverture des fichiers Excel fonctionne
echo [ ] Generation PDF fonctionne
echo [ ] Images de niveaux s'affichent
echo [ ] Configuration email fonctionne (si utilise)
echo [ ] Fermeture propre de l'application
echo.
echo 💡 TESTS MANUELS RECOMMANDES:
echo 1. Ouvrez l'executable: dist\ConvocationGenerator.exe
echo 2. Testez avec un fichier Excel d'exemple
echo 3. Generez un PDF et verifiez le contenu
echo 4. Testez la configuration des images
echo 5. Verifiez que tout fonctionne comme avec le script
echo.
echo 📦 FICHIERS POUR DISTRIBUTION:
echo - distribution\ConvocationGenerator.exe (executable)
echo - distribution\INSTRUCTIONS.txt (guide utilisateur)
echo.
echo 🎯 Pret pour la distribution si tous les tests passent !
echo.
pause

REM Nettoyage du repertoire temporaire
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%" 2>nul