# 🐍 Installation de Python pour le Générateur de Convocations

## ⚠️ Python n'est pas installé sur votre système

Pour utiliser l'application de génération de convocations, vous devez d'abord installer Python.

## 📥 Installation de Python

### Étape 1 : Télécharger Python
1. Allez sur le site officiel : **https://python.org**
2. Cliquez sur "Downloads"
3. Téléchargez la dernière version de Python 3 (recommandé : Python 3.11 ou 3.12)

### Étape 2 : Installer Python
1. **IMPORTANT** : Lors de l'installation, cochez impérativement la case **"Add Python to PATH"**
2. Choisissez "Install Now" pour une installation standard
3. Attendez la fin de l'installation

### Étape 3 : Vérifier l'installation
1. Ouvrez une nouvelle invite de commande (CMD) ou PowerShell
2. Tapez : `python --version`
3. Vous devriez voir quelque chose comme : `Python 3.11.x`

## 🚀 Après l'installation de Python

Une fois Python installé, vous pourrez :

### Option 1 : Installation automatique
```bash
.\install.bat
```

### Option 2 : Installation manuelle
```bash
pip install -r requirements.txt
python main.py
```

## 📋 Dépendances qui seront installées

L'application nécessite ces bibliothèques Python :
- `pandas` : Lecture des fichiers Excel
- `openpyxl` : Support Excel moderne
- `weasyprint` : Génération de PDF
- `jinja2` : Templates HTML
- `pywin32` : Intégration Outlook
- `pillow` : Traitement d'images

## 🔧 Dépannage

### Si "python" n'est pas reconnu après installation
1. Redémarrez votre ordinateur
2. Ou ajoutez manuellement Python au PATH :
   - Cherchez "Variables d'environnement" dans Windows
   - Ajoutez le chemin d'installation de Python au PATH

### Chemins typiques de Python
- `C:\Users\[VotreNom]\AppData\Local\Programs\Python\Python311\`
- `C:\Python311\`

## ✅ Une fois Python installé

Revenez dans ce répertoire et exécutez :
```bash
python main.py
```

L'interface graphique de l'application s'ouvrira et vous pourrez commencer à générer vos convocations !

---

**Note** : Cette application fonctionne uniquement sur Windows avec Microsoft Outlook installé.
