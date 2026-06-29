#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer la convocation de SIANO Marco avec besoins spéciaux
"""

import os
import sys
import pandas as pd
from datetime import datetime
from jury_excel_processor import JuryExcelProcessor
from pdf_generator import PDFGenerator

def generate_siano_convocation():
    """
    Génère spécifiquement la convocation pour SIANO Marco avec besoins spéciaux
    """
    print("=" * 60)
    print("GÉNÉRATEUR DE CONVOCATION POUR SIANO MARCO")
    print("=" * 60)
    
    # Créer un dossier de sortie avec horodatage
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output_siano_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Dossier de sortie: {output_dir}")
    print("-" * 60)
    
    # Créer manuellement les données pour SIANO Marco
    siano_data = {
        'numero_candidat': '032002032317',
        'nom': 'SIANO',
        'prenom': 'Marco',
        'date_naissance': '15/07/1995',
        'email': 'marco.siano@example.com',
        'niveau': 'B2',
        'matiere': 'DELF B2',
        'date_examen': '14/08/2025',
        'date_ep_coll': '14/08/2025',
        'debut_ep_coll': '15:00',
        'fin_ep_coll': '17:20',  # Avec tiers-temps
        'fin_ep_coll_affichage': '17:20 (tiers-temps)',
        'heure_debut': '09:00',
        'heure_preparation': '09:00',
        'heure_passage': '10:00',
        'besoins_speciaux': True,
        'tiers_temps': True,
        'institution_name': 'Alliance Française Bruxelles Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_city': 'Bruxelles',
        'institution_postal': '1000',
        'institution_phone': '+32 2 788 21 60',
        'contact_urgence': 'info@alliancefrancaise.be',
        'duree': '2h30 (collective) + 20min (individuelle)',
        'salle': 'Salle d\'examen'
    }
    
    # Définir les chemins
    template_path = "convocation_delf_template_modele.html"
    if not os.path.exists(template_path):
        template_path = "templates/convocation_delf_template_modele.html"
    
    # Vérifier les chemins des logos
    logo_af_path = "logoAF.svg"
    logo_delf_path = "logoDELF.svg"
    
    if not os.path.exists(logo_af_path):
        print(f"⚠️ Logo AF non trouvé à {logo_af_path}, utilisation du chemin par défaut")
        logo_af_path = "assets/logoAF.svg"
    
    if not os.path.exists(logo_delf_path):
        print(f"⚠️ Logo DELF non trouvé à {logo_delf_path}, utilisation du chemin par défaut")
        logo_delf_path = "assets/logoDELF.svg"
    
    # Initialiser le générateur PDF
    print("Initialisation du générateur PDF...")
    excel_path = "juries_20250825_181821.xlsx"  # Juste pour initialiser le générateur
    pdf_generator = PDFGenerator(
        excel_path=excel_path,
        template_path=template_path,
        logo_af_path=logo_af_path,
        logo_delf_path=logo_delf_path,
        output_dir=output_dir
    )
    
    # Générer le PDF pour SIANO Marco
    print("Génération de la convocation pour SIANO Marco...")
    
    try:
        # Format du nom de fichier: convocation_NOM_Prenom_Niveau.pdf
        nom_fichier = f"convocation_SIANO_Marco_B2.pdf"
        output_path = os.path.join(output_dir, nom_fichier)
        
        # Générer le PDF directement avec le processeur PDF
        pdf_path = pdf_generator.generate_pdf(siano_data)
        
        print(f"✅ Convocation générée avec succès: {pdf_path}")
        print(f"\nInformations pour SIANO Marco:")
        print(f"  - Niveau: {siano_data['niveau']}")
        print(f"  - Besoins spéciaux: {siano_data['besoins_speciaux']}")
        print(f"  - Tiers-temps: {siano_data['tiers_temps']}")
        print(f"  - Fin épreuve collective: {siano_data['fin_ep_coll_affichage']}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération de la convocation: {e}")
    
    print("\nTraitement terminé.")

if __name__ == "__main__":
    generate_siano_convocation()