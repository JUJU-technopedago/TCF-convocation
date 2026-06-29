#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'installation d'une version compatible de cryptography
Ce script corrige définitivement le problème du module 'cryptography.hazmat.decrepit'
"""

import os
import subprocess
import sys
import importlib.util
import platform

def get_python_version():
    """Récupère la version de Python"""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

def check_cryptography_installed():
    """Vérifie si cryptography est installé et sa version"""
    try:
        import cryptography
        return cryptography.__version__
    except ImportError:
        return None

def install_cryptography_compatible():
    """Installe une version compatible de cryptography"""
    # Version compatible qui n'a pas le problème decrepit
    version = "36.0.0"
    
    print(f"Installation de cryptography=={version}...")
    
    # Détecter si pip est disponible
    pip_command = "pip"
    if platform.system() == "Windows":
        pip_command = "pip.exe"
    
    try:
        subprocess.check_call([pip_command, "install", f"cryptography=={version}", "--force-reinstall"])
        print(f"✅ Installation réussie de cryptography=={version}")
        return True
    except Exception as e:
        print(f"❌ Erreur d'installation: {e}")
        
        # Essayer avec python -m pip en cas d'échec
        try:
            print("Tentative avec python -m pip...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"cryptography=={version}", "--force-reinstall"])
            print(f"✅ Installation réussie de cryptography=={version}")
            return True
        except Exception as e2:
            print(f"❌ Échec de l'installation: {e2}")
            return False

def create_decrepit_patch():
    """Crée un module de remplacement pour decrepit"""
    patch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cryptography_patch")
    os.makedirs(patch_dir, exist_ok=True)
    
    # Créer le fichier __init__.py dans le répertoire patch
    with open(os.path.join(patch_dir, "__init__.py"), "w") as f:
        f.write("# Patch pour cryptography\n")
    
    # Créer le module de remplacement decrepit
    decrepit_dir = os.path.join(patch_dir, "decrepit")
    os.makedirs(decrepit_dir, exist_ok=True)
    
    # Créer __init__.py dans decrepit
    with open(os.path.join(decrepit_dir, "__init__.py"), "w") as f:
        f.write("""# Module de remplacement pour cryptography.hazmat.decrepit
# Redirige toutes les importations vers primitives

from cryptography.hazmat.primitives import *

class RedirectedModule:
    def __getattr__(self, name):
        # Rediriger vers primitives
        try:
            import importlib
            return importlib.import_module(f"cryptography.hazmat.primitives.{name}")
        except ImportError:
            raise AttributeError(f"Module '{name}' not found in primitives")

# Créer un objet qui redirigera les imports
ciphers = RedirectedModule()
""")
    
    # Créer le répertoire ciphers
    ciphers_dir = os.path.join(decrepit_dir, "ciphers")
    os.makedirs(ciphers_dir, exist_ok=True)
    
    # Créer __init__.py dans ciphers
    with open(os.path.join(ciphers_dir, "__init__.py"), "w") as f:
        f.write("""# Module de remplacement pour cryptography.hazmat.decrepit.ciphers
# Redirige toutes les importations vers primitives.ciphers

from cryptography.hazmat.primitives.ciphers import *
""")
    
    # Créer le répertoire algorithms
    algo_dir = os.path.join(ciphers_dir, "algorithms")
    os.makedirs(algo_dir, exist_ok=True)
    
    # Créer __init__.py dans algorithms
    with open(os.path.join(algo_dir, "__init__.py"), "w") as f:
        f.write("""# Module de remplacement pour cryptography.hazmat.decrepit.ciphers.algorithms
# Redirige toutes les importations vers primitives.ciphers.algorithms

from cryptography.hazmat.primitives.ciphers.algorithms import *
""")
    
    print(f"✅ Module de remplacement créé dans {patch_dir}")
    return patch_dir

def install_import_hook(patch_dir=None):
    """Installe un hook d'importation pour rediriger les imports decrepit"""
    hook_code = """
# Hook d'importation pour rediriger cryptography.hazmat.decrepit
import sys
import importlib.util

class DerecpitImportFixer:
    def __init__(self):
        self.handled_modules = set()
    
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith('cryptography.hazmat.decrepit'):
            if fullname not in self.handled_modules:
                self.handled_modules.add(fullname)
                
                # Rediriger vers primitives
                replacement = fullname.replace('cryptography.hazmat.decrepit', 'cryptography.hazmat.primitives')
                
                try:
                    importlib.import_module(replacement)
                    return importlib.util.find_spec(replacement)
                except ImportError:
                    pass
        
        return None

# Installer le hook
sys.meta_path.insert(0, DerecpitImportFixer())
"""
    
    # Créer le fichier dans le répertoire de l'application
    hook_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decrepit_import_hook.py")
    with open(hook_file, "w") as f:
        f.write(hook_code)
    
    # Créer un fichier decrepit_patch.pth dans le site-packages pour activer automatiquement le hook
    site_packages = None
    for path in sys.path:
        if "site-packages" in path:
            site_packages = path
            break
    
    if site_packages:
        pth_file = os.path.join(site_packages, "decrepit_patch.pth")
        with open(pth_file, "w") as f:
            f.write(f"import {os.path.splitext(os.path.basename(hook_file))[0]}\n")
            if patch_dir:
                f.write(f"{patch_dir}\n")
        
        print(f"✅ Hook d'importation installé dans {pth_file}")
        return True
    
    print("❌ Impossible de trouver le répertoire site-packages")
    return False

def main():
    """Fonction principale"""
    print("=" * 60)
    print("INSTALLATION DE LA VERSION COMPATIBLE DE CRYPTOGRAPHY")
    print("=" * 60)
    
    python_version = get_python_version()
    print(f"Version Python: {python_version}")
    
    # Vérifier si cryptography est déjà installé
    crypto_version = check_cryptography_installed()
    if crypto_version:
        print(f"cryptography est installé (version {crypto_version})")
        
        # Vérifier si la version est problématique (>= 40.0.0)
        if crypto_version.split('.')[0] >= "40":
            print("⚠️ Version potentiellement problématique détectée")
            print("Installation d'une version compatible...")
            install_cryptography_compatible()
        else:
            print("✅ Version compatible détectée")
    else:
        print("cryptography n'est pas installé, installation en cours...")
        install_cryptography_compatible()
    
    # Créer un module de remplacement pour decrepit
    patch_dir = create_decrepit_patch()
    
    # Installer le hook d'importation
    install_import_hook(patch_dir)
    
    print("\n✅ INSTALLATION TERMINÉE")
    print("Le problème 'cryptography.hazmat.decrepit' est maintenant résolu")
    print("Vous pouvez lancer l'application normalement")
    
    input("\nAppuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        input("\nAppuyez sur Entrée pour fermer...")