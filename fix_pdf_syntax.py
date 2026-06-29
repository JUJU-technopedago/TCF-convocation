#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correctif pour l'erreur de syntaxe dans le fichier pdf_generator.py
"""

import os
import sys
import shutil

# Configuration du log
log_file = "pdf_fix_syntax_log.txt"
def log(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")
    print(message)

log("=== CORRECTIF ERREUR SYNTAXE PDF GENERATOR ===")

# 1. Restaurer depuis la sauvegarde
pdf_generator_path = "pdf_generator.py"
backup_path = "pdf_generator_fixed.py"  # Utiliser la version fixed au lieu de l'original

if not os.path.exists(backup_path):
    log(f"❌ Fichier de sauvegarde {backup_path} non trouvé")
    sys.exit(1)

try:
    # Créer une sauvegarde de la version actuelle (avec erreur)
    shutil.copy2(pdf_generator_path, f"{pdf_generator_path}.error")
    log(f"✅ Sauvegarde de la version avec erreur: {pdf_generator_path}.error")
    
    # Copier la version correcte
    shutil.copy2(backup_path, pdf_generator_path)
    log(f"✅ Restauration depuis {backup_path} réussie")
except Exception as e:
    log(f"❌ Erreur lors de la restauration: {e}")
    sys.exit(1)

log("=== FIN DU CORRECTIF ERREUR SYNTAXE ===")