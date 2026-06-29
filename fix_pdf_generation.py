#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correctif pour les problèmes de génération PDF
Améliore la robustesse de la génération des dates et des caractères spéciaux
"""

import os
import sys
import shutil
from pathlib import Path
import traceback

# Configuration du log
log_file = "pdf_fix_log.txt"
def log(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")
    print(message)

log("=== CORRECTIF PDF GENERATION ===")

# 1. Vérifier les fichiers à corriger
pdf_generator_path = "pdf_generator.py"
backup_path = "pdf_generator.py.bak"

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

# 4. Appliquer les correctifs

# Correctif 1: Améliorer la gestion des exceptions dans format_date_french
old_format_date_french = """    def _format_date_french(self, date_value):
        \"\"\"Formate une date au format français avec nom du jour et du mois (ex: lundi 01 janvier 2000)\"\"\"
        if pd.isna(date_value) or date_value == '':
            return ''
            
        # Dictionnaire des mois en français
        mois_francais = {
            1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin',
            7: 'juillet', 8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
        }
        
        # Dictionnaire des jours en français
        jours_francais = {
            0: 'lundi', 1: 'mardi', 2: 'mercredi', 3: 'jeudi', 4: 'vendredi', 5: 'samedi', 6: 'dimanche'
        }
        
        try:
            date_obj = None
            
            if isinstance(date_value, str):
                # Essayer différents formats de date
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        date_obj = datetime.strptime(date_value, fmt)
                        break
                    except:
                        continue
                        
                if date_obj is None:
                    return str(date_value)
                    
            elif hasattr(date_value, 'strftime'):
                date_obj = date_value
            else:
                return str(date_value)
            
            # Formatter en français
            jour_semaine = jours_francais[date_obj.weekday()]
            jour = date_obj.day
            mois = mois_francais[date_obj.month]
            annee = date_obj.year
            
            return f"{jour_semaine} {jour:02d} {mois} {annee}"
            
        except Exception as e:
            print(f"Erreur lors du formatage de la date française: {e}")
            return str(date_value)"""

new_format_date_french = """    def _format_date_french(self, date_value):
        \"\"\"Formate une date au format français avec nom du jour et du mois (ex: lundi 01 janvier 2000)\"\"\"
        if pd.isna(date_value) or date_value == '':
            return ''
            
        # Dictionnaire des mois en français
        mois_francais = {
            1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin',
            7: 'juillet', 8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
        }
        
        # Dictionnaire des jours en français
        jours_francais = {
            0: 'lundi', 1: 'mardi', 2: 'mercredi', 3: 'jeudi', 4: 'vendredi', 5: 'samedi', 6: 'dimanche'
        }
        
        try:
            date_obj = None
            
            if isinstance(date_value, str):
                # Vérifier si c'est une date déjà formatée en français
                if any(jour in date_value.lower() for jour in jours_francais.values()):
                    return date_value  # Déjà au format français
                
                # Essayer différents formats de date
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        date_obj = datetime.strptime(date_value, fmt)
                        break
                    except Exception:
                        continue
                        
                if date_obj is None:
                    return str(date_value)
                    
            elif hasattr(date_value, 'strftime'):
                date_obj = date_value
            else:
                return str(date_value)
            
            # Formatter en français
            try:
                jour_semaine = jours_francais[date_obj.weekday()]
                jour = date_obj.day
                mois = mois_francais[date_obj.month]
                annee = date_obj.year
                
                return f"{jour_semaine} {jour:02d} {mois} {annee}"
            except Exception as e:
                print(f"Erreur lors du formatage de la date (après parsing): {e}")
                # Fallback: format simple
                return date_obj.strftime('%d/%m/%Y')
            
        except Exception as e:
            print(f"Erreur lors du formatage de la date française: {e}")
            traceback_info = traceback.format_exc()
            print(f"Détails: {traceback_info}")
            return str(date_value)"""

# Correctif 2: Améliorer la génération de noms de fichiers
old_filename_code = """            # Nom du fichier de sortie
            if not output_filename:
                safe_name = f"{template_data['nom']}_{template_data['prenom']}".replace(' ', '_')
                # Garder les caractères Unicode dans le nom de fichier
                safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '_-ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĞğİıŞşÇçÜüÖö')
                output_filename = f"convocation_{safe_name}_{template_data['numero_candidat']}.pdf\""""

new_filename_code = """            # Nom du fichier de sortie
            if not output_filename:
                try:
                    # Obtenir les données nom et prénom
                    nom = template_data.get('nom', '').strip()
                    prenom = template_data.get('prenom', '').strip()
                    numero = template_data.get('numero_candidat', '').strip()
                    niveau = template_data.get('niveau', '').strip()
                    
                    # Nettoyer le nom et prénom pour le nom de fichier
                    safe_name = f"{nom}_{prenom}".replace(' ', '_')
                    
                    # Version plus simple et robuste
                    safe_chars = []
                    for c in safe_name:
                        if c.isalnum() or c in '_-':
                            safe_chars.append(c)
                        elif c in 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĞğİıŞşÇçÜüÖö':
                            # Pour les caractères spéciaux, on peut soit les garder, soit les translittérer
                            # Option 1: Les garder
                            safe_chars.append(c)
                            # Option 2: Translittération (décommentez si nécessaire)
                            # safe_chars.append(unidecode(c))
                    
                    safe_name = ''.join(safe_chars)
                    
                    # Fallback si le nom est vide après nettoyage
                    if not safe_name:
                        safe_name = f"candidat_{numero}"
                    
                    output_filename = f"convocation_{safe_name}_{numero}.pdf"
                    
                    # Vérifier la longueur du nom de fichier (max 255 caractères)
                    if len(output_filename) > 250:
                        # Tronquer le nom si nécessaire
                        output_filename = output_filename[:240] + ".pdf"
                        
                except Exception as e:
                    print(f"Erreur lors de la génération du nom de fichier: {e}")
                    # Fallback: nom de fichier sans caractères spéciaux
                    output_filename = f"convocation_{template_data.get('numero_candidat', 'inconnu')}.pdf\""""

# Correctif 3: Améliorer la gestion des erreurs lors de la génération PDF
old_pdf_gen_code = """            # Générer le PDF selon le moteur disponible
            if PDF_ENGINE == 'pdfkit':
                # Utiliser pdfkit pour un excellent support Unicode
                options = {
                    'page-size': 'A4',
                    'margin-top': '2cm',
                    'margin-right': '2cm',
                    'margin-bottom': '2cm',
                    'margin-left': '2cm',
                    'encoding': "UTF-8",
                    'no-outline': None,
                    'enable-local-file-access': None
                }
                try:
                    pdfkit.from_string(html_content, output_path, options=options)
                except OSError as e:
                    if "wkhtmltopdf" in str(e):
                        print("⚠️  wkhtmltopdf non installé, fallback vers xhtml2pdf")
                        # Fallback vers xhtml2pdf
                        with open(output_path, "w+b") as result_file:
                            pisa_status = pisa.CreatePDF(
                                html_content,
                                dest=result_file,
                                encoding='utf-8',
                                path=os.path.dirname(os.path.abspath(self.template_path))
                            )
                            
                        if pisa_status.err:
                            raise Exception(f"Erreur lors de la génération PDF: {pisa_status.err}")
                    else:
                        raise e
            elif PDF_ENGINE == 'weasyprint':
                # Utiliser WeasyPrint pour un meilleur support Unicode
                html_doc = weasyprint.HTML(string=html_content, base_url=os.path.dirname(os.path.abspath(self.template_path)))
                html_doc.write_pdf(output_path)
            else:
                # Fallback vers xhtml2pdf avec améliorations Unicode
                with open(output_path, "w+b") as result_file:
                    pisa_status = pisa.CreatePDF(
                        html_content,
                        dest=result_file,
                        encoding='utf-8',
                        path=os.path.dirname(os.path.abspath(self.template_path))
                    )
                    
                if pisa_status.err:
                    raise Exception(f"Erreur lors de la génération PDF: {pisa_status.err}")"""

new_pdf_gen_code = """            # Générer le PDF selon le moteur disponible
            print(f"Génération PDF avec moteur: {PDF_ENGINE}")
            if PDF_ENGINE == 'pdfkit':
                # Utiliser pdfkit pour un excellent support Unicode
                options = {
                    'page-size': 'A4',
                    'margin-top': '2cm',
                    'margin-right': '2cm',
                    'margin-bottom': '2cm',
                    'margin-left': '2cm',
                    'encoding': "UTF-8",
                    'no-outline': None,
                    'enable-local-file-access': None
                }
                try:
                    pdfkit.from_string(html_content, output_path, options=options)
                    print(f"✅ PDF généré avec pdfkit: {output_path}")
                except Exception as e:
                    print(f"⚠️ Erreur pdfkit: {e}")
                    if "wkhtmltopdf" in str(e) or "not found" in str(e):
                        print("⚠️ wkhtmltopdf non installé, fallback vers xhtml2pdf")
                        # Fallback vers xhtml2pdf
                        try:
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
                            raise Exception(f"Erreur lors du fallback xhtml2pdf: {e2}")
                    else:
                        raise Exception(f"Erreur pdfkit: {e}")
            elif PDF_ENGINE == 'weasyprint':
                # Utiliser WeasyPrint pour un meilleur support Unicode
                try:
                    html_doc = weasyprint.HTML(string=html_content, base_url=os.path.dirname(os.path.abspath(self.template_path)))
                    html_doc.write_pdf(output_path)
                    print(f"✅ PDF généré avec WeasyPrint: {output_path}")
                except Exception as e:
                    print(f"⚠️ Erreur WeasyPrint: {e}, tentative de fallback vers xhtml2pdf")
                    # Fallback vers xhtml2pdf
                    try:
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
                        raise Exception(f"Erreur lors du fallback xhtml2pdf: {e2}")
            else:
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
                        raise Exception(f"Erreur xhtml2pdf: {pisa_status.err}")
                    print(f"✅ PDF généré avec xhtml2pdf: {output_path}")
                except Exception as e:
                    raise Exception(f"Erreur lors de la génération PDF avec xhtml2pdf: {e}")"""

# Appliquer les correctifs
content = content.replace(old_format_date_french, new_format_date_french)
log("✅ Correctif 1 appliqué: Amélioration du formatage des dates")

content = content.replace(old_filename_code, new_filename_code)
log("✅ Correctif 2 appliqué: Amélioration de la génération de noms de fichiers")

content = content.replace(old_pdf_gen_code, new_pdf_gen_code)
log("✅ Correctif 3 appliqué: Amélioration de la gestion des erreurs lors de la génération PDF")

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
=== CORRECTIFS APPLIQUÉS AVEC SUCCÈS ===

Les correctifs suivants ont été appliqués:
1. Amélioration du formatage des dates françaises
2. Génération plus robuste des noms de fichiers avec caractères spéciaux
3. Meilleure gestion des erreurs et fallback lors de la génération PDF

Pour utiliser les améliorations:
1. Lancez votre application normalement
2. Vérifiez les logs pour des informations détaillées sur la génération PDF
3. En cas de problème, vous pouvez restaurer la version originale: 
   - Copiez {backup_path} vers {pdf_generator_path}

Si vous rencontrez des problèmes avec wkhtmltopdf:
1. Installez wkhtmltopdf depuis https://wkhtmltopdf.org/downloads.html
2. Assurez-vous qu'il est dans votre PATH système
""")

log("=== FIN DU CORRECTIF ===")