#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour la génération de PDF avec données issues de fichier Excel
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# Importer tous les moteurs PDF possibles
from xhtml2pdf import pisa

try:
    import pdfkit
    PDF_ENGINE = 'pdfkit'
    print("✅ Utilisation de pdfkit pour un meilleur support Unicode")
except ImportError:
    try:
        import weasyprint
        PDF_ENGINE = 'weasyprint'
        print("✅ Utilisation de WeasyPrint pour un support Unicode complet")
    except ImportError:
        PDF_ENGINE = 'xhtml2pdf'
        print("⚠️ Utilisation de xhtml2pdf (support Unicode limité)")

# Configurer l'encodage pour les sorties
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Créer un dossier de test
output_dir = "output_test_dates"
os.makedirs(output_dir, exist_ok=True)

print("=== TEST DE GÉNÉRATION PDF AVEC DONNÉES EXCEL ===")

# HTML Template simplifié
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Convocation Test</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { text-align: center; margin-bottom: 20px; }
        .content { margin-bottom: 20px; }
        .footer { text-align: center; font-size: 0.8em; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Convocation à l'examen</h1>
        <h2>{{exam_type}} {{niveau}}</h2>
    </div>
    
    <div class="content">
        <p><strong>Candidat:</strong> {{prenom}} {{nom}}</p>
        <p><strong>Numéro de candidat:</strong> {{numero_candidat}}</p>
        <p><strong>Date de naissance:</strong> {{date_naissance}}</p>
        <p><strong>Email:</strong> {{email}}</p>
        
        <h3>Détails de l'examen</h3>
        <p><strong>Date épreuve collective:</strong> {{date_ep_coll}}</p>
        <p><strong>Heure de début:</strong> {{debut_ep_coll}}</p>
        <p><strong>Date épreuve individuelle:</strong> {{date_ep_ind}}</p>
        <p><strong>Heure de préparation:</strong> {{heure_preparation}}</p>
        
        <p><strong>Lieu:</strong> {{institution_name}}, {{institution_address}}, {{institution_city}} {{institution_postal}}</p>
    </div>
    
    <div class="footer">
        <p>Référence: {{reference}}</p>
        <p>Généré le: {{date_generation}}</p>
    </div>
</body>
</html>
"""

# Simuler des données de candidats
candidates = [
    {
        'nom': 'Dupont',
        'prenom': 'Jean',
        'numero_candidat': '123456',
        'date_naissance': '01/01/1990',
        'email': 'jean.dupont@example.com',
        'niveau': 'B2',
        'exam_type': 'DELF',
        'date_ep_coll': '2025-08-25',
        'debut_ep_coll': '09:00',
        'date_ep_ind': '2025-08-25',
        'heure_preparation': '14:00',
        'institution_name': 'Alliance Française Bruxelles Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_city': 'Bruxelles',
        'institution_postal': '1000'
    },
    {
        'nom': 'Müller',
        'prenom': 'Hans',
        'numero_candidat': '654321',
        'date_naissance': '02/02/1995',
        'email': 'hans.muller@example.com',
        'niveau': 'C1',
        'exam_type': 'DALF',
        'date_ep_coll': '2025-08-26',
        'debut_ep_coll': '09:30',
        'date_ep_ind': '2025-08-26',
        'heure_preparation': '14:30',
        'institution_name': 'Alliance Française Bruxelles Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_city': 'Bruxelles',
        'institution_postal': '1000'
    },
    {
        'nom': 'Martínez',
        'prenom': 'José',
        'numero_candidat': '789012',
        'date_naissance': '03/03/1985',
        'email': 'jose.martinez@example.com',
        'niveau': 'A2',
        'exam_type': 'DELF',
        'date_ep_coll': '2025-08-27',
        'debut_ep_coll': '10:00',
        'date_ep_ind': '2025-08-27',
        'heure_preparation': '15:00',
        'institution_name': 'Alliance Française Bruxelles Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_city': 'Bruxelles',
        'institution_postal': '1000'
    }
]

# Fonction pour formater les dates
def format_date_french(date_value):
    """Formate une date au format français avec nom du jour et du mois"""
    if not date_value:
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
        return str(date_value)

# Générer un PDF pour chaque candidat
for i, candidate in enumerate(candidates, 1):
    print(f"\nTest {i}: Génération PDF pour {candidate['prenom']} {candidate['nom']}")
    
    # Préparation des données
    data = candidate.copy()
    
    # Formatage des dates
    data['date_ep_coll'] = format_date_french(data['date_ep_coll'])
    data['date_ep_ind'] = format_date_french(data['date_ep_ind'])
    
    # Données système
    data['date_generation'] = datetime.now().strftime('%d/%m/%Y à %H:%M')
    data['reference'] = f"CONV-{data['numero_candidat']}-{datetime.now().strftime('%Y%m%d')}"
    
    # Remplacer les variables dans le template
    html_content = html_template
    for key, value in data.items():
        placeholder = '{{' + key + '}}'
        html_content = html_content.replace(placeholder, str(value))
    
    # Nom du fichier
    safe_name = f"{data['nom']}_{data['prenom']}".replace(' ', '_')
    # Garder les caractères Unicode dans le nom de fichier
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '_-ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĞğİıŞşÇçÜüÖö')
    output_filename = f"convocation_{safe_name}_{data['numero_candidat']}.pdf"
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"Nom du fichier: {output_filename}")
    
    # Générer le PDF selon le moteur disponible
    try:
        if PDF_ENGINE == 'pdfkit':
            # Utiliser pdfkit
            print("Utilisation de pdfkit...")
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
                print(f"✅ PDF généré avec pdfkit: {output_path} ({os.path.getsize(output_path)} bytes)")
            except OSError as e:
                if "wkhtmltopdf" in str(e):
                    print("⚠️ wkhtmltopdf non installé, fallback vers xhtml2pdf")
                    # Fallback vers xhtml2pdf
                    with open(output_path, "w+b") as result_file:
                        pisa_status = pisa.CreatePDF(
                            html_content,
                            dest=result_file,
                            encoding='utf-8'
                        )
                        
                    if pisa_status.err:
                        print(f"❌ Erreur avec xhtml2pdf: {pisa_status.err}")
                    else:
                        print(f"✅ PDF généré avec xhtml2pdf (fallback): {output_path} ({os.path.getsize(output_path)} bytes)")
                else:
                    raise e
        elif PDF_ENGINE == 'weasyprint':
            # Utiliser WeasyPrint
            print("Utilisation de WeasyPrint...")
            html_doc = weasyprint.HTML(string=html_content)
            html_doc.write_pdf(output_path)
            print(f"✅ PDF généré avec WeasyPrint: {output_path} ({os.path.getsize(output_path)} bytes)")
        else:
            # Fallback vers xhtml2pdf
            print("Utilisation de xhtml2pdf...")
            with open(output_path, "w+b") as result_file:
                pisa_status = pisa.CreatePDF(
                    html_content,
                    dest=result_file,
                    encoding='utf-8'
                )
                
            if pisa_status.err:
                print(f"❌ Erreur avec xhtml2pdf: {pisa_status.err}")
            else:
                print(f"✅ PDF généré avec xhtml2pdf: {output_path} ({os.path.getsize(output_path)} bytes)")
                
    except Exception as e:
        print(f"❌ Erreur lors de la génération PDF: {e}")

print("\n=== FIN DES TESTS ===")
print(f"Veuillez consulter le répertoire '{output_dir}' pour les fichiers PDF générés.")