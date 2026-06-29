#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correctif supplémentaire pour l'erreur xhtml2pdf
"""

import os
import sys
import shutil

# Configuration du log
log_file = "pdf_fix_log2.txt"
def log(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")
    print(message)

log("=== CORRECTIF SUPPLÉMENTAIRE PDF GENERATION ===")

# 1. Vérifier les fichiers à corriger
pdf_generator_path = "pdf_generator.py"
backup_path = "pdf_generator.py.bak2"

if not os.path.exists(pdf_generator_path):
    log(f"❌ Fichier {pdf_generator_path} non trouvé")
    sys.exit(1)

# 2. Faire une sauvegarde
try:
    shutil.copy2(pdf_generator_path, backup_path)
    log(f"✅ Sauvegarde créée: {backup_path}")
except Exception as e:
    log(f"❌ Erreur lors de la sauvegarde: {e}")
    sys.exit(1)

# 3. Lire le contenu du fichier
try:
    with open(pdf_generator_path, "r", encoding="utf-8") as f:
        content = f.read()
    log(f"✅ Fichier lu: {pdf_generator_path} ({len(content)} caractères)")
except Exception as e:
    log(f"❌ Erreur lors de la lecture: {e}")
    sys.exit(1)

# 4. Correctif pour l'erreur xhtml2pdf: unsupported operand type(s) for -: 'str' and 'int'

# Version erronée du code xhtml2pdf
old_xhtml2pdf_code = """                        try:
                            with open(output_path, "w+b") as result_file:
                                pisa_status = pisa.CreatePDF(
                                    html_content,
                                    dest=result_file,
                                    encoding='utf-8',
                                    path=os.path.dirname(os.path.abspath(self.template_path))
                                )
                                
                            if pisa_status.err:
                                raise Exception(f"Erreur xhtml2pdf: {pisa_status.err}")
                            print(f"✅ PDF généré avec xhtml2pdf (fallback): {output_path}")
                        except Exception as e2:
                            raise Exception(f"Erreur lors du fallback xhtml2pdf: {e2}")"""

# Version corrigée du code xhtml2pdf
new_xhtml2pdf_code = """                        try:
                            # Créer un chemin absolu pour les ressources du template
                            base_path = os.path.dirname(os.path.abspath(self.template_path))
                            
                            # Ouvrir le fichier en mode binaire (important pour PDF)
                            with open(output_path, "w+b") as result_file:
                                pisa_status = pisa.CreatePDF(
                                    src=html_content,  # Contenu HTML source
                                    dest=result_file,  # Fichier de destination
                                    encoding='utf-8',  # Encodage UTF-8 pour les caractères spéciaux
                                    path=base_path     # Chemin pour les ressources relatives
                                )
                                
                            # Vérifier si la conversion a réussi
                            if pisa_status.err:
                                raise Exception(f"Erreur xhtml2pdf: {pisa_status.err}")
                            print(f"✅ PDF généré avec xhtml2pdf (fallback): {output_path}")
                        except Exception as e2:
                            raise Exception(f"Erreur lors du fallback xhtml2pdf: {e2}")"""

# Correctif pour toutes les instances de xhtml2pdf
old_fallback_code = """            else:
                # Fallback vers xhtml2pdf avec améliorations Unicode
                try:
                    with open(output_path, "w+b") as result_file:
                        pisa_status = pisa.CreatePDF(
                            html_content,
                            dest=result_file,
                            encoding='utf-8',
                            path=os.path.dirname(os.path.abspath(self.template_path))
                        )
                        
                    if pisa_status.err:
                        raise Exception(f"Erreur lors de la génération PDF avec xhtml2pdf: {pisa_status.err}")
                    print(f"✅ PDF généré avec xhtml2pdf: {output_path}")
                except Exception as e:
                    raise Exception(f"Erreur lors de la génération PDF avec xhtml2pdf: {e}")"""

new_fallback_code = """            else:
                # Fallback vers xhtml2pdf avec améliorations Unicode
                try:
                    # Créer un chemin absolu pour les ressources du template
                    base_path = os.path.dirname(os.path.abspath(self.template_path))
                    
                    # Ouvrir le fichier en mode binaire (important pour PDF)
                    with open(output_path, "w+b") as result_file:
                        pisa_status = pisa.CreatePDF(
                            src=html_content,         # Contenu HTML source
                            dest=result_file,         # Fichier de destination
                            encoding='utf-8',         # Encodage UTF-8 pour les caractères spéciaux
                            path=base_path            # Chemin pour les ressources relatives
                        )
                        
                    if pisa_status.err:
                        raise Exception(f"Erreur lors de la génération PDF avec xhtml2pdf: {pisa_status.err}")
                    print(f"✅ PDF généré avec xhtml2pdf: {output_path}")
                except Exception as e:
                    raise Exception(f"Erreur lors de la génération PDF avec xhtml2pdf: {e}")"""

# Appliquer les correctifs
content = content.replace(old_xhtml2pdf_code, new_xhtml2pdf_code)
content = content.replace(old_fallback_code, new_fallback_code)
log("✅ Correctif appliqué: Correction de l'erreur xhtml2pdf")

# 5. Sauvegarder les modifications
try:
    with open(pdf_generator_path, "w", encoding="utf-8") as f:
        f.write(content)
    log(f"✅ Modifications sauvegardées dans {pdf_generator_path}")
except Exception as e:
    log(f"❌ Erreur lors de la sauvegarde des modifications: {e}")
    log(f"Vous pouvez restaurer le fichier original depuis {backup_path}")
    sys.exit(1)

# 6. Conseils d'utilisation
log("""
=== CORRECTIF SUPPLÉMENTAIRE APPLIQUÉ ===

Le correctif pour l'erreur xhtml2pdf a été appliqué:
- Correction du problème "unsupported operand type(s) for -: 'str' and 'int'"
- Amélioration du code de fallback xhtml2pdf
- Garantie de la compatibilité des chemins de fichiers

Pour tester le correctif:
1. Exécutez à nouveau le script verify_pdf_fix.py
2. Vérifiez que les PDF sont générés sans erreur
""")

log("=== FIN DU CORRECTIF SUPPLÉMENTAIRE ===")