@echo off
echo ========================================
echo  Installation des dependances Mailjet
echo ========================================
echo.

echo Installation en cours...
pip install mailjet-rest==1.3.4
pip install requests==2.31.0
pip install cryptography==41.0.7

echo.
echo ========================================
echo  Installation terminee!
echo ========================================
echo.
echo Le bridge Mailjet est maintenant pret a utiliser.
echo Lancez l'application et cliquez sur le bouton MAILJET.
echo.
pause
