#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer un exécutable stable de l'application ConvocationGenerator
Utilise PyInstaller avec une configuration optimisée pour Tkinter et les dépendances
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔧 {description}...")
    print(f"Commande: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout.strip():
                print(f"Sortie: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - Erreur")
            if result.stderr.strip():
                print(f"Erreur: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False
    
    return True

def check_python_version():
    """Vérifie la version de Python"""
    print(f"🐍 Version Python: {sys.version}")
    if sys.version_info < (3, 8):
        print("⚠️ Attention: Python 3.8+ recommandé pour PyInstaller")
    return True

def install_dependencies():
    """Installe les dépendances nécessaires"""
    dependencies = [
        "pyinstaller>=5.0",
        "auto-py-to-exe",  # Interface graphique optionnelle
    ]
    
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"Installation de {dep}"):
            return False
    
    return True

def create_spec_file():
    """Crée un fichier .spec personnalisé pour PyInstaller"""
    
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Chemin du projet
project_path = os.path.dirname(os.path.abspath(SPEC))

# Configuration pour l'analyse
a = Analysis(
    ['main.py'],
    pathex=[project_path],
    binaries=[],
    datas=[
        # Templates HTML
        ('templates', 'templates'),
        ('templates_fixed', 'templates_fixed'),
        
        # Assets (logos, images)
        ('assets', 'assets'),
        
        # Configuration et exemples
        ('*.json', '.'),
        ('*.xlsx', '.'),
        ('*.docx', '.'),
        ('*.svg', '.'),
        ('*.png', '.'),
        ('*.txt', '.'),
        
        # Documentation
        ('README.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        # Imports cachés pour Tkinter
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        
        # Imports cachés pour les dépendances principales
        'pandas',
        'openpyxl',
        'jinja2',
        'xhtml2pdf',
        'reportlab',
        'pathlib',
        'datetime',
        'json',
        'os',
        'sys',
        'traceback',
        'logging',
        
        # Imports cachés pour l'email
        'mailjet_rest',
        'requests',
        'cryptography',
        'keyring',
        
        # Imports cachés pour PDF
        'weasyprint',
        'html5lib',
        'six',
        'cssselect2',
        'tinycss2',
        'cairocffi',
        'cairosvg',
        
        # Modules de l'application
        'pdf_generator',
        'jury_file_processor',
        'mailjet_bridge',
        'email_auth',
        'oauth_auth',
        'oauth_email_sender',
        'oauth_entraid',
        'oauth_login_dialog',
        'login_dialog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclusions pour réduire la taille
        'matplotlib',
        'numpy',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'unittest',
    ],
    noarchive=False,
    optimize=0,
)

# Configuration des fichiers Python compilés
pyz = PYZ(a.pure)

# Configuration de l'exécutable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ConvocationGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compression UPX si disponible
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Application avec interface graphique
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

# Configuration pour une application avec interface graphique
app = BUNDLE(
    exe,
    name='ConvocationGenerator.app',
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    bundle_identifier='com.alliancefrancaise.convocationgenerator',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Excel Files',
                'CFBundleTypeExtensions': ['xlsx', 'xls'],
                'CFBundleTypeRole': 'Editor',
            }
        ]
    },
)
"""
    
    with open('convocation_generator.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier .spec créé")
    return True

def create_icon():
    """Crée un icône pour l'application si nécessaire"""
    icon_path = Path('assets/icon.ico')
    
    if not icon_path.exists():
        print("ℹ️ Aucun icône trouvé - l'exécutable utilisera l'icône par défaut")
        
        # Optionnel: Convertir un logo existant en icône
        logo_svg = Path('logoAF.svg')
        if logo_svg.exists():
            print("ℹ️ Logo SVG trouvé - vous pouvez le convertir en .ico avec un outil en ligne")
    else:
        print("✅ Icône trouvé pour l'application")
    
    return True

def build_executable():
    """Construit l'exécutable avec PyInstaller"""
    
    # Nettoyer les anciens builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        print("🧹 Ancien dossier dist supprimé")
    
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("🧹 Ancien dossier build supprimé")
    
    # Construire avec le fichier .spec
    if not run_command("pyinstaller convocation_generator.spec", "Construction de l'exécutable"):
        return False
    
    # Vérifier que l'exécutable a été créé
    exe_path = Path('dist/ConvocationGenerator.exe')
    if exe_path.exists():
        print(f"✅ Exécutable créé: {exe_path.absolute()}")
        print(f"📁 Taille: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        return True
    else:
        print("❌ Exécutable non trouvé dans dist/")
        return False

def create_installer_script():
    """Crée un script d'installation simple"""
    
    installer_script = """@echo off
echo Installation de ConvocationGenerator
echo ====================================

echo.
echo Copie des fichiers...
if not exist "%USERPROFILE%\\ConvocationGenerator" mkdir "%USERPROFILE%\\ConvocationGenerator"

copy "ConvocationGenerator.exe" "%USERPROFILE%\\ConvocationGenerator\\"
copy "*.dll" "%USERPROFILE%\\ConvocationGenerator\\" 2>nul
xcopy "templates" "%USERPROFILE%\\ConvocationGenerator\\templates\\" /E /I /Y 2>nul
xcopy "assets" "%USERPROFILE%\\ConvocationGenerator\\assets\\" /E /I /Y 2>nul

echo.
echo Creation du raccourci sur le bureau...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\ConvocationGenerator.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\\ConvocationGenerator\\ConvocationGenerator.exe'; $Shortcut.WorkingDirectory = '%USERPROFILE%\\ConvocationGenerator'; $Shortcut.Description = 'Generateur de Convocations DELF'; $Shortcut.Save()"

echo.
echo ✅ Installation terminee!
echo Vous pouvez lancer l'application depuis le raccourci sur le bureau
echo ou depuis: %USERPROFILE%\\ConvocationGenerator\\ConvocationGenerator.exe
echo.
pause
"""
    
    with open('dist/installer.bat', 'w', encoding='utf-8') as f:
        f.write(installer_script)
    
    print("✅ Script d'installation créé")
    return True

def create_readme():
    """Crée un fichier README pour la distribution"""
    
    readme_content = """# ConvocationGenerator - Version Portable

## Installation

1. **Installation automatique** (recommandée):
   - Double-cliquez sur `installer.bat`
   - Suivez les instructions à l'écran
   - Un raccourci sera créé sur votre bureau

2. **Installation manuelle**:
   - Copiez le dossier entier où vous voulez
   - Lancez `ConvocationGenerator.exe`

## Utilisation

1. **Première utilisation**:
   - Configurez vos paramètres graphiques (logos, images de niveaux)
   - Configurez votre méthode d'envoi d'emails (Mailjet recommandé)

2. **Génération de convocations**:
   - Sélectionnez votre fichier Excel avec les candidats
   - Choisissez votre dossier de sortie
   - Cliquez sur "Générer PDF"

3. **Envoi d'emails**:
   - Connectez-vous à votre service email
   - Cliquez sur "Envoyer Emails"

## Configuration requise

- Windows 10/11 (64-bit)
- Aucune installation Python requise
- Connexion Internet pour l'envoi d'emails

## Support

Pour toute question ou problème:
1. Vérifiez que tous les fichiers sont présents
2. Vérifiez vos paramètres de configuration
3. Consultez les logs d'erreur dans l'application

## Fichiers importants

- `ConvocationGenerator.exe` : Application principale
- `templates/` : Modèles de convocations
- `assets/` : Logos et ressources graphiques
- Configuration automatiquement sauvegardée

Version: """ + f"{Path('main.py').stat().st_mtime}" + """
"""
    
    with open('dist/README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Documentation créée")
    return True

def main():
    """Fonction principale"""
    print("🚀 Construction d'un exécutable stable pour ConvocationGenerator")
    print("=" * 70)
    
    # Vérifications préliminaires
    if not check_python_version():
        return False
    
    # Installation des dépendances
    if not install_dependencies():
        print("❌ Échec de l'installation des dépendances")
        return False
    
    # Création des fichiers de configuration
    if not create_spec_file():
        print("❌ Échec de la création du fichier .spec")
        return False
    
    if not create_icon():
        print("❌ Échec de la gestion de l'icône")
        return False
    
    # Construction
    if not build_executable():
        print("❌ Échec de la construction de l'exécutable")
        return False
    
    # Scripts additionnels
    if not create_installer_script():
        print("❌ Échec de la création du script d'installation")
        return False
    
    if not create_readme():
        print("❌ Échec de la création de la documentation")
        return False
    
    print("\n" + "=" * 70)
    print("🎉 Construction terminée avec succès!")
    print("\n📂 Fichiers créés:")
    print("   └── dist/")
    print("       ├── ConvocationGenerator.exe")
    print("       ├── installer.bat")
    print("       └── README.txt")
    print("\n💡 Prochaines étapes:")
    print("   1. Testez l'exécutable: dist/ConvocationGenerator.exe")
    print("   2. Distribuez le dossier 'dist' complet")
    print("   3. Les utilisateurs peuvent utiliser installer.bat")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n❌ La construction a échoué")
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)
    else:
        print("\n✅ Construction réussie!")
        input("Appuyez sur Entrée pour fermer...")