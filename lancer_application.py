#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur sécurisé pour le Générateur de Convocations
Applique tous les correctifs nécessaires avant de lancer l'application
"""

import os
import sys
import importlib.util
import subprocess
import time

# Afficher le banner
print("=" * 80)
print("🚀 LANCEUR SÉCURISÉ - GÉNÉRATEUR DE CONVOCATIONS")
print("=" * 80)

# Vérifier si le module cryptography est accessible
try:
    import cryptography
    print(f"✅ Module cryptography trouvé (version {cryptography.__version__})")
except ImportError:
    print("❌ Module cryptography non trouvé")
    print("Installation en cours...")
    try:
        # Installer cryptography version 36.0.0 qui est connue pour fonctionner
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography==36.0.0"])
        print("✅ Installation réussie")
    except Exception as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)

# Appliquer le correctif decrepit
print("\n📋 Application des correctifs...")
fix_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "immediate_fix_decrepit.py")

if os.path.exists(fix_path):
    print(f"✅ Correctif trouvé: {fix_path}")
    try:
        # Charger le module de correctif
        spec = importlib.util.spec_from_file_location("immediate_fix_decrepit", fix_path)
        fix_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fix_module)
        print("✅ Correctif decrepit appliqué avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'application du correctif: {e}")
        print("⚠️ L'application peut ne pas fonctionner correctement")
else:
    print(f"❌ Correctif non trouvé: {fix_path}")
    print("⚠️ L'application peut ne pas fonctionner correctement")

# Vérifier si on a accès au module problématique maintenant
try:
    import sys.modules['cryptography.hazmat.decrepit']
    print("✅ Module decrepit factice accessible")
except Exception:
    # Si cela échoue, créer le module factice directement ici
    print("⚠️ Module decrepit non trouvé, création manuelle...")
    import types
    
    decrepit = types.ModuleType('cryptography.hazmat.decrepit')
    sys.modules['cryptography.hazmat.decrepit'] = decrepit
    
    ciphers = types.ModuleType('cryptography.hazmat.decrepit.ciphers')
    decrepit.ciphers = ciphers
    sys.modules['cryptography.hazmat.decrepit.ciphers'] = ciphers
    
    algorithms = types.ModuleType('cryptography.hazmat.decrepit.ciphers.algorithms')
    ciphers.algorithms = algorithms
    sys.modules['cryptography.hazmat.decrepit.ciphers.algorithms'] = algorithms
    
    # Tenter d'importer TripleDES depuis primitives
    try:
        from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES
        algorithms.TripleDES = TripleDES
    except ImportError:
        # Classe factice si l'import échoue
        class FakeTripleDES:
            def __init__(self, *args, **kwargs):
                pass
        algorithms.TripleDES = FakeTripleDES
    
    print("✅ Module decrepit créé manuellement")

# Lancement de l'application
print("\n🚀 Démarrage de l'application...")
time.sleep(1)  # Petite pause pour s'assurer que tout est en place

# Déterminer le chemin du fichier main.py
main_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

if not os.path.exists(main_script):
    print(f"❌ Script principal non trouvé: {main_script}")
    input("Appuyez sur Entrée pour quitter...")
    sys.exit(1)

# Lancer l'application
try:
    print(f"📂 Exécution de: {main_script}")
    exec(open(main_script, encoding='utf-8').read())
except Exception as e:
    print(f"❌ Erreur lors de l'exécution de l'application: {e}")
    input("Appuyez sur Entrée pour quitter...")
    sys.exit(1)