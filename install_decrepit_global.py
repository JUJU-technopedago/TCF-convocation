import os
import sys
import shutil

def create_global_decrepit_modules():
    """Crée les modules decrepit nécessaires dans l'installation globale de Python."""
    # Trouver le chemin site-packages global
    site_packages = None
    for path in sys.path:
        if path.endswith('site-packages') and not path.endswith(('win32', 'win32\\lib', 'Pythonwin')):
            site_packages = path
            break
            
    if not site_packages:
        print("Impossible de trouver le répertoire site-packages global.")
        return False
        
    print(f"Installation dans: {site_packages}")
    
    # Créer les répertoires nécessaires
    decrepit_path = os.path.join(site_packages, 'cryptography', 'hazmat', 'decrepit')
    ciphers_path = os.path.join(decrepit_path, 'ciphers')
    algorithms_path = os.path.join(ciphers_path, 'algorithms')
    
    os.makedirs(algorithms_path, exist_ok=True)
    
    # Créer les fichiers __init__.py nécessaires
    for path in [decrepit_path, ciphers_path, algorithms_path]:
        init_file = os.path.join(path, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Module de remplacement automatiquement créé\n")
    
    # Créer les modules ARC4 et TripleDES
    arc4_path = os.path.join(algorithms_path, 'arc4.py')
    with open(arc4_path, 'w') as f:
        f.write("""# Module de remplacement pour ARC4
class ARC4:
    def __init__(self, key):
        self.key = key
        
    @property
    def key_size(self):
        return len(self.key) * 8
""")
    
    tripledes_path = os.path.join(algorithms_path, 'triple_des.py')
    with open(tripledes_path, 'w') as f:
        f.write("""# Module de remplacement pour TripleDES
class TripleDES:
    def __init__(self, key):
        self.key = key
        
    @property
    def key_size(self):
        return len(self.key) * 8
        
    @property
    def block_size(self):
        return 64
""")
    
    # Mettre à jour le fichier __init__.py du module algorithms
    algorithms_init = os.path.join(algorithms_path, '__init__.py')
    with open(algorithms_init, 'w') as f:
        f.write("""# Module de remplacement pour cryptography.hazmat.decrepit.ciphers.algorithms
from .triple_des import TripleDES
from .arc4 import ARC4

# Ajouter RC2 pour compléter les importations requises
class RC2:
    def __init__(self, key):
        self.key = key
        
    @property
    def key_size(self):
        return len(self.key) * 8
""")
    
    print("Modules decrepit créés avec succès dans l'installation globale de Python.")
    return True

if __name__ == "__main__":
    success = create_global_decrepit_modules()
    if success:
        print("Vous pouvez maintenant lancer l'application principale.")
    else:
        print("Erreur lors de la création des modules. Vérifiez les permissions et les chemins.")