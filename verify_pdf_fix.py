#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification des correctifs PDF
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import traceback

# Configuration pour sortie UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Importer le générateur PDF
from pdf_generator import PDFGenerator

# Créer un dossier de test
output_dir = "output_test_fix"
os.makedirs(output_dir, exist_ok=True)

print("=== TEST DES CORRECTIFS PDF ===")

# Créer un petit fichier Excel de test
test_excel_path = os.path.join(output_dir, "test_candidats.xlsx")

# Données de test
candidates = [
    {
        'nom': 'Dupont',
        'prenom': 'Jean',
        'numero_candidat': '123456',
        'date_naissance': '01/01/1990',
        'email': 'jean.dupont@example.com',
        'niveau': 'B2',
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

# Créer un DataFrame et sauvegarder en Excel
df = pd.DataFrame(candidates)
df.to_excel(test_excel_path, index=False)
print(f"✅ Fichier Excel de test créé: {test_excel_path}")

# Créer un générateur PDF
try:
    # Trouver le template HTML
    template_path = None
    
    # Chercher d'abord dans templates/
    if os.path.exists("templates"):
        for file in os.listdir("templates"):
            if file.endswith(".html"):
                template_path = os.path.join("templates", file)
                break
    
    # Si pas trouvé, chercher dans le dossier courant
    if not template_path:
        for file in os.listdir("."):
            if file.endswith(".html") and "template" in file.lower():
                template_path = file
                break
    
    # Utiliser un template par défaut si aucun n'est trouvé
    if not template_path:
        print("⚠️ Aucun template HTML trouvé, création d'un template de base")
        default_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Convocation DELF/DALF</title>
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
                <h2>{{ exam_type }} {{ niveau }}</h2>
            </div>
            
            <div class="content">
                <p><strong>Candidat:</strong> {{ prenom }} {{ nom }}</p>
                <p><strong>Numéro de candidat:</strong> {{ numero_candidat }}</p>
                <p><strong>Date de naissance:</strong> {{ date_naissance }}</p>
                <p><strong>Email:</strong> {{ email }}</p>
                
                <h3>Détails de l'examen</h3>
                <p><strong>Date épreuve collective:</strong> {{ date_ep_coll }}</p>
                <p><strong>Heure de début:</strong> {{ debut_ep_coll }}</p>
                <p><strong>Date épreuve individuelle:</strong> {{ date_ep_ind }}</p>
                <p><strong>Heure de préparation:</strong> {{ heure_preparation }}</p>
                
                <p><strong>Lieu:</strong> {{ institution_name }}, {{ institution_address }}, {{ institution_city }} {{ institution_postal }}</p>
            </div>
            
            <div class="footer">
                <p>Référence: {{ reference }}</p>
                <p>Généré le: {{ date_generation }}</p>
            </div>
        </body>
        </html>
        """
        template_path = os.path.join(output_dir, "default_template.html")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(default_template)
    
    print(f"✅ Template HTML: {template_path}")
    
    # Trouver les logos
    logo_af_path = None
    logo_delf_path = None
    
    # Chercher dans assets/
    if os.path.exists("assets"):
        for file in os.listdir("assets"):
            if file.lower() == "logoaf.svg" or file.lower() == "logoaf.png":
                logo_af_path = os.path.join("assets", file)
            elif file.lower() == "logodelf.svg" or file.lower() == "logodelf.png":
                logo_delf_path = os.path.join("assets", file)
    
    # Si pas trouvé, chercher dans le dossier courant
    if not logo_af_path:
        for file in os.listdir("."):
            if file.lower() == "logoaf.svg" or file.lower() == "logoaf.png":
                logo_af_path = file
                break
    
    if not logo_delf_path:
        for file in os.listdir("."):
            if file.lower() == "logodelf.svg" or file.lower() == "logodelf.png":
                logo_delf_path = file
                break
    
    if logo_af_path:
        print(f"✅ Logo AF: {logo_af_path}")
    else:
        print("⚠️ Logo AF non trouvé, utilisation d'un placeholder")
        logo_af_path = "logoAF.svg"
    
    if logo_delf_path:
        print(f"✅ Logo DELF: {logo_delf_path}")
    else:
        print("⚠️ Logo DELF non trouvé, utilisation d'un placeholder")
        logo_delf_path = "logoDELF.svg"
    
    # Initialiser le générateur PDF
    generator = PDFGenerator(
        excel_path=test_excel_path,
        template_path=template_path,
        logo_af_path=logo_af_path,
        logo_delf_path=logo_delf_path,
        output_dir=output_dir,
        access_code="1234"
    )
    
    # Définir la fonction de callback pour la progression
    def print_progress(message):
        print(message)
    
    # Générer les PDF
    try:
        print("\n=== GÉNÉRATION PDF ===")
        count = generator.generate_all_pdfs(print_progress)
        print(f"\n✅ Génération terminée! {count} PDF générés dans {output_dir}")
    except Exception as e:
        print(f"\n❌ Erreur lors de la génération: {e}")
        traceback_info = traceback.format_exc()
        print(f"Détails: {traceback_info}")
    
except Exception as e:
    print(f"\n❌ Erreur générale: {e}")
    traceback_info = traceback.format_exc()
    print(f"Détails: {traceback_info}")

print("\n=== FIN DU TEST ===")
print(f"Veuillez consulter le répertoire '{output_dir}' pour les fichiers PDF générés.")