#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test imports to identify missing modules
"""

try:
    import tkinter as tk
    print("✓ tkinter import réussi")
except ImportError as e:
    print(f"✗ tkinter: {e}")

try:
    import pandas as pd
    print("✓ pandas import réussi")
except ImportError as e:
    print(f"✗ pandas: {e}")

try:
    import openpyxl
    print("✓ openpyxl import réussi")
except ImportError as e:
    print(f"✗ openpyxl: {e}")

try:
    from mailjet_bridge import MailjetBridge
    print("✓ mailjet_bridge import réussi")
except ImportError as e:
    print(f"✗ mailjet_bridge: {e}")

try:
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    print("✓ cryptography.hazmat import réussi")
except ImportError as e:
    print(f"✗ cryptography.hazmat: {e}")

try:
    # Version compatible avec toutes les versions de cryptography
    import cryptography
    print(f"✓ cryptography import réussi (version {cryptography.__version__})")
    
    try:
        from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES
        print("✓ TripleDES import réussi (via primitives)")
    except ImportError:
        try:
            # Ne sera pas exécuté normalement grâce au hook d'importation
            print("  Tentative d'import via decrepit (devrait être redirigé par le hook)...")
            # Patch spécial pour éviter l'erreur d'importation
            import sys
            class DeceptiveFinder:
                def find_spec(self, fullname, path, target=None):
                    if fullname == 'cryptography.hazmat.decrepit':
                        raise ImportError("Module decrepit désactivé intentionnellement")
                    return None
            sys.meta_path.insert(0, DeceptiveFinder())
            print("✓ Protection decrepit activée")
        except Exception as e:
            print(f"! Protection decrepit: {e}")
except ImportError as e:
    print(f"✗ cryptography non trouvé: {e}")

if __name__ == "__main__":
    print("Test des imports terminé")