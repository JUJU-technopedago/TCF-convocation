# Guide de Création d'Exécutable - Générateur de Convocations

## Solutions Disponibles

### 1. Lanceur Batch (Solution Immédiate)
Le fichier `lancer_application.bat` permet de lancer l'application directement :
- Double-cliquez sur `lancer_application.bat`
- L'application se lance automatiquement
- Nécessite Python installé sur le système

### 2. Création d'Exécutable avec PyInstaller

#### Prérequis
```bash
pip install pyinstaller
```

#### Commande Simple (Recommandée)
```bash
pyinstaller --onefile --windowed --name "Generateur_Convocations" main.py
```

#### Commande Complète (Avec toutes les dépendances)
```bash
pyinstaller --onefile --windowed --name "Generateur_Convocations" ^
    --add-data "templates;templates" ^
    --add-data "assets;assets" ^
    --hidden-import "tkinter" ^
    --hidden-import "pandas" ^
    --hidden-import "openpyxl" ^
    --hidden-import "jinja2" ^
    --hidden-import "xhtml2pdf" ^
    --hidden-import "PIL" ^
    --hidden-import "requests" ^
    --hidden-import "msal" ^
    main.py
```

#### Script Automatisé
Utilisez le fichier `build_exe.py` :
```bash
python build_exe.py
```

### 3. Vérification après Création

L'exécutable sera créé dans le dossier `dist/` :
- `dist/Generateur_Convocations.exe`

#### Structure requise pour l'exécutable
```
dist/
├── Generateur_Convocations.exe
├── templates/
│   └── *.html
├── assets/
│   └── *.png, *.ico
└── output/ (créé automatiquement)
```

### 4. Distribution

Pour distribuer l'application :
1. Copiez le dossier `dist/` complet
2. Incluez les dossiers `templates/` et `assets/`
3. L'utilisateur final peut lancer directement l'`.exe`

### 5. Dépannage

#### Erreur "Module not found"
- Ajoutez `--hidden-import nom_du_module` à la commande PyInstaller

#### L'exécutable ne se lance pas
- Testez d'abord avec `python main.py`
- Vérifiez que tous les fichiers sont présents

#### Processus trop long
- PyInstaller peut prendre 5-10 minutes pour une application complexe
- Utilisez le lanceur batch en attendant

### 6. Alternative : Distribution avec Python

Créez un package complet avec :
1. `requirements.txt` - Liste des dépendances
2. `install.bat` - Script d'installation
3. `lancer_application.bat` - Lanceur
4. Tous les fichiers source

L'utilisateur installe Python puis lance `install.bat` puis `lancer_application.bat`.

## Notes Techniques

- Taille de l'exécutable : ~50-100 MB (normal pour une app Tkinter)
- Temps de démarrage : 2-5 secondes (chargement des bibliothèques)
- Compatibilité : Windows 10/11 x64

## Support

En cas de problème :
1. Vérifiez que Python 3.8+ est installé
2. Installez les dépendances : `pip install -r requirements.txt`
3. Testez avec : `python main.py`
4. Puis créez l'exécutable avec PyInstaller
