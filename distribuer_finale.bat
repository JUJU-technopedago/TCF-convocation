@echo off
echo ===============================================
echo       PREPARATION DISTRIBUTION FINALE
echo    CONVOCATION GENERATOR - VERSION STABLE
echo ===============================================
echo.

if not exist "dist\ConvocationGenerator.exe" (
    echo ❌ ERREUR: Executable non trouve
    echo Lancez d'abord: creer_executable_stable.bat
    pause
    exit /b 1
)

echo [1/4] Creation du package de distribution finale...

REM Nom avec date pour versioning
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set RELEASE_DATE=%datetime:~0,8%
set PACKAGE_NAME=ConvocationGenerator_v%RELEASE_DATE%

if exist "%PACKAGE_NAME%" rmdir /s /q "%PACKAGE_NAME%"
mkdir "%PACKAGE_NAME%"

echo ✅ Dossier de release: %PACKAGE_NAME%

echo.
echo [2/4] Copie des fichiers essentiels...

REM Executable principal
copy "dist\ConvocationGenerator.exe" "%PACKAGE_NAME%\"
echo ✅ Executable copie

REM Documentation
if exist "README.md" (
    copy "README.md" "%PACKAGE_NAME%\LISEZMOI.txt"
    echo ✅ Documentation copiee
)

REM Creation du guide utilisateur complet
echo Creation du guide utilisateur...
(
echo GENERATEUR DE CONVOCATIONS D'EXAMENS
echo =====================================
echo Version stable compilee le: %date%
echo.
echo INSTALLATION:
echo Aucune installation requise ! Ce programme est portable.
echo.
echo UTILISATION:
echo 1. Double-cliquez sur ConvocationGenerator.exe
echo 2. L'interface s'ouvrira automatiquement
echo 3. Suivez les instructions a l'ecran
echo.
echo FONCTIONNALITES:
echo - Import de fichiers Excel avec donnees jury/candidats
echo - Generation automatique de PDF de convocations
echo - Insertion automatique d'images selon le niveau ^(A1, A2, B1, B2, C1, C2^)
echo - Configuration graphique personnalisable
echo - Envoi d'emails automatique ^(si configure^)
echo - Sauvegarde des preferences
echo.
echo FORMAT FICHIER EXCEL REQUIS:
echo Le fichier Excel doit contenir les colonnes:
echo - Nom, Prenom, Email des candidats
echo - Date, Heure, Lieu de l'examen
echo - Niveau ^(A1, A2, B1, B2, C1, C2^)
echo.
echo CONFIGURATION DES IMAGES:
echo Via le menu "Configuration Graphique":
echo - Selectionnez les images pour chaque niveau
echo - Ajustez l'opacite ^(recommande: 30%%^)
echo - Les images sont automatiquement centrees ^(200x200px^)
echo.
echo CONFIGURATION EMAIL:
echo Pour l'envoi automatique:
echo - Configurez vos parametres SMTP/OAuth
echo - Testez l'envoi avant utilisation en masse
echo.
echo DEPANNAGE:
echo - Si l'application ne s'ouvre pas: redemarrez Windows
echo - Si erreur PDF: verifiez le format du fichier Excel
echo - Si probleme email: verifiez votre configuration reseau
echo.
echo COMPATIBILITE:
echo - Windows 10 et 11 ^(64-bit^)
echo - Aucune installation Python requise
echo - Fonctionne sans connexion internet ^(sauf pour emails^)
echo.
echo SUPPORT:
echo Pour assistance technique, contactez l'administrateur
echo avec le fichier de log ^(si genere^).
echo.
echo =====================================
echo Version: %PACKAGE_NAME%
echo Compile avec: Python + PyInstaller
echo =====================================
) > "%PACKAGE_NAME%\GUIDE_UTILISATEUR.txt"

echo ✅ Guide utilisateur cree

REM Script de lancement alternatif (si problemes)
(
echo @echo off
echo echo Lancement du Generateur de Convocations...
echo echo Si la fenetre ne s'ouvre pas, attendez quelques secondes.
echo echo.
echo start "" "ConvocationGenerator.exe"
echo echo.
echo echo Si probleme persistant:
echo echo 1. Redemarrez Windows
echo echo 2. Verifiez que Windows Defender n'a pas bloque le fichier
echo echo 3. Lancez en tant qu'administrateur si necessaire
echo echo.
echo pause
) > "%PACKAGE_NAME%\LANCER_APPLICATION.bat"

echo ✅ Script de lancement alternatif cree

echo.
echo [3/4] Verification finale de l'executable...

for %%I in ("%PACKAGE_NAME%\ConvocationGenerator.exe") do (
    set size=%%~zI
    set /a sizeMB=!size!/1048576
    echo 📊 Taille finale: !sizeMB! MB
)

echo ✅ Verification terminee

echo.
echo [4/4] Creation de l'archive de distribution...

REM Creation d'un ZIP si 7zip est disponible
where 7z >nul 2>&1
if %errorlevel%==0 (
    7z a -tzip "%PACKAGE_NAME%.zip" "%PACKAGE_NAME%\*"
    echo ✅ Archive ZIP creee: %PACKAGE_NAME%.zip
) else (
    echo ℹ️  Archive ZIP non creee ^(7zip non installe^)
    echo   Le dossier %PACKAGE_NAME% contient tous les fichiers
)

echo.
echo ===============================================
echo          🎉 DISTRIBUTION PRETE !
echo ===============================================
echo.
echo 📁 Package: %PACKAGE_NAME%\
echo 📋 Contient:
echo    - ConvocationGenerator.exe (executable principal)
echo    - GUIDE_UTILISATEUR.txt (documentation complete)
echo    - LANCER_APPLICATION.bat (lancement alternatif)
if exist "%PACKAGE_NAME%.zip" echo    - %PACKAGE_NAME%.zip (archive pour distribution)
echo.
echo 🚀 PROCHAINES ETAPES:
echo 1. Testez l'executable: %PACKAGE_NAME%\ConvocationGenerator.exe
echo 2. Verifiez toutes les fonctionnalites
echo 3. Distribuez le dossier %PACKAGE_NAME% ou l'archive ZIP
echo.
echo 💡 CONSEILS DISTRIBUTION:
echo - Partagez tout le dossier (pas seulement l'exe)
echo - Informez les utilisateurs du guide utilisateur
echo - Testez sur une machine vierge si possible
echo.
echo ✅ Votre application est prete pour la distribution !
echo.
pause