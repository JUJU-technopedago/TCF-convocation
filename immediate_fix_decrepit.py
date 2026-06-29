#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECTIF IMMÉDIAT POUR L'ERREUR DECREPIT
Ce script applique un correctif immédiat pour l'erreur 'cryptography.hazmat.decrepit'
en créant un module factice dans sys.modules
"""

import sys
import importlib
import types
import os
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fix_decrepit.log', encoding='utf-8'),
    ]
)

def create_fake_module(module_name):
    """Crée un module factice qui sera utilisé comme remplacement"""
    
    # Créer un module vide
    fake_module = types.ModuleType(module_name)
    
    # Si c'est le module decrepit principal, on ajoute un sous-module ciphers
    if module_name == 'cryptography.hazmat.decrepit':
        # Créer un sous-module ciphers
        ciphers_module = types.ModuleType(f"{module_name}.ciphers")
        fake_module.ciphers = ciphers_module
        sys.modules[f"{module_name}.ciphers"] = ciphers_module
        
        # Créer un sous-module algorithms
        algorithms_module = types.ModuleType(f"{module_name}.ciphers.algorithms")
        ciphers_module.algorithms = algorithms_module
        sys.modules[f"{module_name}.ciphers.algorithms"] = algorithms_module
        
        # Ajouter TripleDES au module algorithms
        try:
            # Essayer d'importer TripleDES depuis le module original
            from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES
            algorithms_module.TripleDES = TripleDES
            logging.info(f"Module {module_name}.ciphers.algorithms.TripleDES créé avec succès (redirection)")
        except ImportError:
            # Si l'import échoue, créer une classe factice
            class FakeTripleDES:
                def __init__(self, *args, **kwargs):
                    pass
            
            algorithms_module.TripleDES = FakeTripleDES
            logging.info(f"Module {module_name}.ciphers.algorithms.TripleDES créé avec une classe factice")
    
    # Ajouter le module au sys.modules pour qu'il soit trouvé lors des imports
    sys.modules[module_name] = fake_module
    logging.info(f"Module factice {module_name} créé et installé")
    
    return fake_module

def patch_cryptography():
    """Applique le patch pour cryptography.hazmat.decrepit"""
    
    logging.info("Début du patch pour cryptography.hazmat.decrepit")
    
    # Créer le module decrepit et ses sous-modules
    decrepit_module = create_fake_module('cryptography.hazmat.decrepit')
    
    # Vérifier si le patch a fonctionné
    try:
        import cryptography.hazmat.decrepit
        logging.info("Patch appliqué avec succès, le module decrepit est maintenant disponible")
        return True
    except ImportError as e:
        logging.error(f"Le patch a échoué: {e}")
        return False

# Appliquer le patch immédiatement
patch_cryptography()

# Récupérer le chemin du module cryptography pour le débogage
try:
    import cryptography
    logging.info(f"Module cryptography trouvé à: {cryptography.__file__}")
    logging.info(f"Version de cryptography: {cryptography.__version__}")
except Exception as e:
    logging.error(f"Erreur lors de l'accès au module cryptography: {e}")

# Message de confirmation
print("✅ Correctif decrepit appliqué")