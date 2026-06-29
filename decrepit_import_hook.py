
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
