#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correctif pour le problème 'cryptography.hazmat.decrepit'
Ce script applique un patch pour résoudre l'erreur d'importation 'No module named cryptography.hazmat.decrepit'
en redirigeant les imports vers les chemins d'importation compatibles avec la version installée de cryptography
"""

import os
import sys
import re
import importlib
import glob

def check_cryptography_version():
    """Vérifie la version de cryptography installée"""
    try:
        import cryptography
        version = cryptography.__version__
        print(f"Version de cryptography installée: {version}")
        return version
    except ImportError:
        print("❌ Module cryptography non installé")
        return None

def get_all_py_files(directory='.'):
    """Récupère tous les fichiers Python dans le répertoire et ses sous-répertoires"""
    return [f for f in glob.glob(f"{directory}/**/*.py", recursive=True)]

def patch_file(file_path):
    """Applique un patch au fichier pour résoudre l'erreur decrepit"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le fichier contient des références à decrepit
    if 'cryptography.hazmat.decrepit' not in content:
        return False
    
    # Pattern pour trouver les imports de decrepit
    patterns = [
        r'from\s+cryptography\.hazmat\.decrepit\.ciphers\.algorithms\s+import\s+([A-Za-z0-9_,\s]+)',
        r'from\s+cryptography\.hazmat\.decrepit\s+import\s+([A-Za-z0-9_,\s]+)',
        r'import\s+cryptography\.hazmat\.decrepit'
    ]
    
    modified = False
    
    for pattern in patterns:
        matches = re.findall(pattern, content)
        if matches:
            if pattern.endswith('algorithms\\s+import\\s+([A-Za-z0-9_,\\s]+)'):
                # Remplacer par l'import depuis primitives
                for match in matches:
                    imports = [item.strip() for item in match.split(',')]
                    for imp in imports:
                        old_import = f"from cryptography.hazmat.decrepit.ciphers.algorithms import {imp}"
                        new_import = f"from cryptography.hazmat.primitives.ciphers.algorithms import {imp}  # Patched import"
                        content = content.replace(old_import, new_import)
                        modified = True
                        print(f"  - Remplacé: {old_import}")
                        print(f"  - Par     : {new_import}")
            elif pattern.endswith('decrepit\\s+import\\s+([A-Za-z0-9_,\\s]+)'):
                # Cas spécial pour les imports directs depuis decrepit
                old_import = f"from cryptography.hazmat.decrepit import {matches[0]}"
                # Patch spécial: On simule un module decrepit vide
                new_import = f"# Patched import: decrepit modules moved to primitives\n" \
                             f"try:\n" \
                             f"    from cryptography.hazmat.decrepit import {matches[0]}\n" \
                             f"except ImportError:\n" \
                             f"    # Fallback import pour compatibilité\n" \
                             f"    from cryptography.hazmat.primitives import {matches[0]}"
                content = content.replace(old_import, new_import)
                modified = True
                print(f"  - Patché: {old_import}")
            else:
                # Import général de decrepit
                old_import = "# Patched: decrepit import removed
# import cryptography.hazmat.decrepit"
                new_import = "# Patched: decrepit import removed\n" \
                             "# # Patched: decrepit import removed
# import cryptography.hazmat.decrepit"
                content = content.replace(old_import, new_import)
                modified = True
                print(f"  - Commenté: {old_import}")
    
    # Sauvegarder les modifications
    if modified:
        # Faire une sauvegarde du fichier original
        backup_path = f"{file_path}.bak"
        if not os.path.exists(backup_path):
            with open(backup_path, 'w', encoding='utf-8') as f:
                with open(file_path, 'r', encoding='utf-8') as original:
                    f.write(original.read())
            print(f"  - Sauvegarde créée: {backup_path}")
        
        # Écrire le fichier patché
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def create_import_hook():
    """Crée un hook d'importation pour rediriger dynamiquement les imports decrepit"""
    class DerecpitImportFixer:
        def __init__(self):
            # Modules déjà traités
            self.handled_modules = set()
        
        def find_spec(self, fullname, path, target=None):
            # Si on demande à importer cryptography.hazmat.decrepit
            if fullname.startswith('cryptography.hazmat.decrepit'):
                # Si c'est un module qu'on n'a pas encore traité
                if fullname not in self.handled_modules:
                    self.handled_modules.add(fullname)
                    
                    # Déterminer le module de remplacement (primitives au lieu de decrepit)
                    replacement = fullname.replace('cryptography.hazmat.decrepit', 'cryptography.hazmat.primitives')
                    
                    try:
                        # Essayer d'importer le module de remplacement
                        importlib.import_module(replacement)
                        print(f"Import redirigé: {fullname} → {replacement}")
                        
                        # Retourner le spec du module de remplacement
                        return importlib.util.find_spec(replacement)
                    except ImportError:
                        pass
            
            # Laisser le système d'import standard gérer les autres cas
            return None
    
    # Installer le hook
    sys.meta_path.insert(0, DerecpitImportFixer())
    print("✅ Hook d'importation installé pour rediriger decrepit → primitives")

def main():
    """Fonction principale du script"""
    print("=" * 60)
    print("CORRECTIF POUR L'ERREUR 'cryptography.hazmat.decrepit'")
    print("=" * 60)
    
    # Vérifier la version de cryptography
    version = check_cryptography_version()
    if not version:
        print("❌ Installez d'abord cryptography avec: pip install cryptography==41.0.5")
        return 1
    
    # Créer un hook d'importation pour rediriger les imports
    create_import_hook()
    
    # Scanner tous les fichiers Python
    print("\nRecherche des fichiers Python à patcher:")
    files = get_all_py_files()
    print(f"Trouvé {len(files)} fichiers Python")
    
    # Appliquer le patch
    print("\nApplication du patch pour 'cryptography.hazmat.decrepit':")
    patched_files = 0
    for file_path in files:
        print(f"Vérification de {os.path.basename(file_path)}...")
        if patch_file(file_path):
            patched_files += 1
    
    print(f"\nOpération terminée: {patched_files} fichiers patchés")
    
    print("\nETAPE SUIVANTE: Redémarrez votre application")
    
    if patched_files == 0:
        print("\n⚠️  Aucun fichier n'a été modifié. Il est possible que le problème vienne:")
        print("   - D'un import dynamique pendant l'exécution")
        print("   - D'une dépendance indirecte non visible dans les fichiers")
        print("   - D'un fichier compilé (.pyc) qui utilise le module")
        
        print("\n💡 Solution alternative: Installez une ancienne version de cryptography:")
        print("   pip install cryptography==36.0.0")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())