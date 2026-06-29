import os
import sys
import importlib
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_module_info(module_name):
    """Affiche des informations détaillées sur un module."""
    try:
        module = importlib.import_module(module_name)
        logging.info(f"Module {module_name} importé avec succès")
        logging.info(f"Chemin du module: {getattr(module, '__file__', 'Module intégré')}")
        
        # Afficher les attributs du module
        attrs = dir(module)
        logging.info(f"Attributs de {module_name}: {', '.join(attrs)}")
        
        # Si c'est un package, afficher les sous-modules
        if hasattr(module, '__path__'):
            logging.info(f"{module_name} est un package avec __path__ = {module.__path__}")
            
    except ImportError as e:
        logging.error(f"Impossible d'importer {module_name}: {e}")
    except Exception as e:
        logging.error(f"Erreur lors de l'inspection de {module_name}: {e}")
        traceback.print_exc()

def inspect_decrepit_modules():
    """Inspecte en détail les modules decrepit."""
    modules_to_check = [
        'cryptography',
        'cryptography.hazmat',
        'cryptography.hazmat.decrepit',
        'cryptography.hazmat.decrepit.ciphers',
        'cryptography.hazmat.decrepit.ciphers.algorithms',
    ]
    
    # Vérifier les chemins d'importation
    logging.info(f"sys.path: {sys.path}")
    
    # Vérifier les modules
    for module_name in modules_to_check:
        print_module_info(module_name)
    
    # Tenter d'importer directement ARC4 et TripleDES
    try:
        from cryptography.hazmat.decrepit.ciphers.algorithms import ARC4, TripleDES
        logging.info(f"ARC4 importé avec succès: {ARC4}")
        logging.info(f"ARC4.__module__: {ARC4.__module__}")
        logging.info(f"TripleDES importé avec succès: {TripleDES}")
        logging.info(f"TripleDES.__module__: {TripleDES.__module__}")
    except ImportError as e:
        logging.error(f"Erreur d'importation directe: {e}")
        
    # Vérifier les fichiers
    for path in sys.path:
        if 'site-packages' in path:
            algo_path = os.path.join(path, 'cryptography', 'hazmat', 'decrepit', 'ciphers', 'algorithms')
            if os.path.exists(algo_path):
                logging.info(f"Répertoire algorithms trouvé: {algo_path}")
                logging.info(f"Contenu du répertoire: {os.listdir(algo_path)}")
                
                # Vérifier le contenu de __init__.py
                init_file = os.path.join(algo_path, '__init__.py')
                if os.path.exists(init_file):
                    with open(init_file, 'r') as f:
                        logging.info(f"Contenu de {init_file}:\n{f.read()}")
                        
                # Vérifier le contenu de arc4.py
                arc4_file = os.path.join(algo_path, 'arc4.py')
                if os.path.exists(arc4_file):
                    with open(arc4_file, 'r') as f:
                        logging.info(f"Contenu de {arc4_file}:\n{f.read()}")

    # Vérifier si sys.modules contient déjà des modules decrepit
    for module_name, module in sys.modules.items():
        if 'decrepit' in module_name:
            logging.info(f"Module decrepit trouvé dans sys.modules: {module_name}")
            if hasattr(module, '__file__'):
                logging.info(f"  Chemin: {module.__file__}")

if __name__ == "__main__":
    logging.info("Début du diagnostic des modules decrepit")
    inspect_decrepit_modules()
    logging.info("Fin du diagnostic")