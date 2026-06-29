#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérification des dépendances pour le Générateur de Convocations
Vérifie que tous les modules nécessaires sont installés et fonctionnels
"""

import sys
import importlib

# Liste des modules requis
REQUIRED_MODULES = [
    "tkinter",
    "pandas",
    "openpyxl",
    "mailjet_rest",
    "requests",
    "cryptography",
    "msal",
    "flask",
    "keyring"
]

# Modules avec imports spécifiques à vérifier
SPECIFIC_IMPORTS = [
    ("cryptography.fernet", "Fernet"),
    ("cryptography.hazmat.primitives", "hashes"),
    ("cryptography.hazmat.primitives.kdf.pbkdf2", "PBKDF2HMAC"),
    ("cryptography.hazmat.primitives.ciphers.algorithms", "TripleDES")
]

def check_module(module_name, attr_name=None):
    """Vérifie si un module est installé et accessible"""
    try:
        module = importlib.__import__(module_name)
        if attr_name:
            getattr(module, attr_name)
        print(f"✓ Module {module_name}{f'.{attr_name}' if attr_name else ''} disponible")
        return True
    except ImportError:
        print(f"✗ Module {module_name} non installé")
        return False
    except AttributeError:
        print(f"✗ Attribut {attr_name} non trouvé dans {module_name}")
        return False
    except Exception as e:
        print(f"✗ Erreur lors de l'importation de {module_name}: {e}")
        return False

def check_specific_import(module_path, attr_name):
    """Vérifie un import spécifique"""
    try:
        module = importlib.import_module(module_path)
        getattr(module, attr_name)
        print(f"✓ Import {module_path}.{attr_name} réussi")
        return True
    except ImportError as e:
        print(f"✗ Module {module_path} non trouvé: {e}")
        return False
    except AttributeError:
        print(f"✗ Attribut {attr_name} non trouvé dans {module_path}")
        return False
    except Exception as e:
        print(f"✗ Erreur lors de l'importation de {module_path}.{attr_name}: {e}")
        return False

def check_cryptography_version():
    """Vérifie la version de cryptography"""
    try:
        import cryptography
        version = cryptography.__version__
        print(f"✓ Version de cryptography: {version}")
        
        # Vérifier si la version est compatible
        if version.startswith("41."):
            print("✓ Version compatible avec votre application")
        else:
            print("⚠️ Version non testée avec votre application")
            print("   Recommandation: installer cryptography==41.0.5")
    except Exception as e:
        print(f"✗ Impossible de vérifier la version de cryptography: {e}")

def main():
    """Vérifie toutes les dépendances"""
    print("Vérification des dépendances pour le Générateur de Convocations")
    print("=" * 60)
    
    all_ok = True
    
    # Vérifier les modules de base
    print("\n1. Modules de base:")
    print("-" * 30)
    for module_name in REQUIRED_MODULES:
        if not check_module(module_name):
            all_ok = False
    
    # Vérifier les imports spécifiques
    print("\n2. Imports spécifiques:")
    print("-" * 30)
    for module_path, attr_name in SPECIFIC_IMPORTS:
        if not check_specific_import(module_path, attr_name):
            all_ok = False
    
    # Vérifier la version de cryptography
    print("\n3. Vérification des versions:")
    print("-" * 30)
    check_cryptography_version()
    
    # Résultat final
    print("\nRésultat:")
    print("-" * 30)
    if all_ok:
        print("✅ Toutes les dépendances sont correctement installées")
    else:
        print("❌ Certaines dépendances sont manquantes ou incorrectes")
        print("   Exécutez: pip install -r requirements.txt")
        print("   Pour cryptography spécifiquement: pip install cryptography==41.0.5")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())