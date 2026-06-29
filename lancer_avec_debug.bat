@echo off
echo ===========================================
echo   LANCEMENT AVEC DEBUG COMPLET
echo ===========================================
echo.

echo Test rapide de l'environnement...
.venv\Scripts\python.exe -c "import tkinter; print('✅ Tkinter OK')"

echo.
echo Lancement de l'application avec debug...
echo (La fenetre devrait apparaitre maintenant)
echo.

.venv\Scripts\python.exe -c "
import sys
import main

print('Création de l\'application...')
app = main.ConvocationGenerator()
print('Application créée')

print('Configuration de l\'interface...')
if hasattr(app, 'root'):
    print(f'Fenêtre root: {app.root}')
    print(f'Géométrie: {app.root.geometry()}')
    app.root.lift()  # Met la fenêtre au premier plan
    app.root.attributes('-topmost', True)  # Force au-dessus
    app.root.after(100, lambda: app.root.attributes('-topmost', False))  # Remet normal après 100ms
    print('Fenêtre forcée au premier plan')

print('Démarrage de la boucle principale...')
app.run()
print('Application fermée')
"

echo.
echo Application terminee
pause