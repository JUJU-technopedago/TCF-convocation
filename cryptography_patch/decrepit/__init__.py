# Module de remplacement pour cryptography.hazmat.decrepit
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
