#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de nettoyage final pour organiser les fichiers
"""

import os
import shutil

def cleanup_files():
    """Nettoie et organise les fichiers restants"""
    
    print("🧹 Nettoyage final en cours...")
    
    # Fichiers à déplacer vers archive
    archive_files = [
        'login_dialog.py',
        'secure_email_sender.py', 
        'launch_safe.py',
        'build_exe.py',
        'jury_excel_processor.py'
    ]
    
    # Créer le dossier archive s'il n'existe pas
    os.makedirs('archive', exist_ok=True)
    
    moved_count = 0
    for file in archive_files:
        if os.path.exists(file):
            try:
                shutil.move(file, f'archive/{file}')
                print(f"   ✅ {file} → archive/")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Erreur pour {file}: {e}")
    
    print(f"\n📊 Résumé du nettoyage:")
    print(f"   - {moved_count} fichiers déplacés vers archive/")
    
    # Afficher l'état final
    print(f"\n📁 Structure finale:")
    print(f"   📂 Racine (fichiers principaux):")
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    for file in sorted(py_files):
        print(f"      - {file}")
    
    print(f"\n   📂 tests/ : {len([f for f in os.listdir('tests') if f.endswith('.py')])} fichiers de test")
    print(f"   📂 scripts/ : {len([f for f in os.listdir('scripts') if f.endswith('.py')])} scripts utilitaires")
    print(f"   📂 docs/ : {len([f for f in os.listdir('docs') if f.endswith('.md')])} fichiers de documentation")
    print(f"   📂 archive/ : {len([f for f in os.listdir('archive') if f.endswith('.py')])} fichiers archivés")
    
    print(f"\n✅ Nettoyage terminé!")

if __name__ == "__main__":
    cleanup_files()
