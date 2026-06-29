try:
    from cryptography.hazmat.decrepit.ciphers.algorithms import ARC4
    print("Import ARC4 réussi !")
    print(f"ARC4: {ARC4}")
    print(f"ARC4.__module__: {ARC4.__module__}")
    arc4 = ARC4(b"test")
    print(f"arc4.key_size: {arc4.key_size}")
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    import sys
    print(f"sys.path: {sys.path}")
    
    # Vérifier si le module est bien présent dans site-packages
    import os
    expected_path = os.path.join("site-packages", "cryptography", "hazmat", "decrepit", "ciphers", "algorithms", "arc4.py")
    for path in sys.path:
        full_path = os.path.join(path, "cryptography", "hazmat", "decrepit", "ciphers", "algorithms", "arc4.py")
        if os.path.exists(full_path):
            print(f"Le fichier arc4.py existe à: {full_path}")
            with open(full_path, 'r') as f:
                print(f"Contenu de arc4.py:\n{f.read()}")
        else:
            if "site-packages" in path:
                print(f"Le fichier arc4.py n'existe pas à: {full_path}")
                
    # Vérifier le contenu du __init__.py
    for path in sys.path:
        init_path = os.path.join(path, "cryptography", "hazmat", "decrepit", "ciphers", "algorithms", "__init__.py")
        if os.path.exists(init_path):
            print(f"Le fichier __init__.py existe à: {init_path}")
            with open(init_path, 'r') as f:
                print(f"Contenu de __init__.py:\n{f.read()}")
except Exception as e:
    print(f"Autre erreur: {e}")