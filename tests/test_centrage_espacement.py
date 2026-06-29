#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du centrage vertical du titre et de l'espacement doublé
"""

import os
import sys
from datetime import datetime

# Ajouter le répertoire parent au chemin Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_generator import PDFGenerator

def test_centrage_espacement():
    """Test du centrage vertical et de l'espacement"""
    
    print("=== Test du centrage vertical et espacement ===")
    
    # Données de test
    test_data = {
        'nom': 'CENTRAGE',
        'prenom': 'Vertical',
        'date_naissance': '15/03/1990',
        'numero_candidat': 'CENTRAGE2025001',
        'date_examen': '25/08/2025',
        'heure_debut': '09:00',
        'niveau': 'B1',
        'exam_type': 'DELF',
        'date_ep_coll': '25/08/2025',
        'debut_ep_coll': '09:00',
        'date_ep_ind': '25/08/2025',
        'heure_preparation': '14:00',
        'institution_name': 'Alliance Française de Bruxelles-Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_postal': '1000',
        'institution_city': 'Bruxelles',
        'access_code': '1234ABCD'
    }
    
    # Configuration des chemins
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    template_path = "templates/convocation_delf_template_modele.html"
    logo_af_path = "assets/logoAF.png"
    logo_delf_path = "assets/logoDELF.png"
    
    # Vérifier que les fichiers existent
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return False
    
    if not os.path.exists(logo_af_path):
        print(f"❌ Logo AF non trouvé: {logo_af_path}")
        return False
    
    if not os.path.exists(logo_delf_path):
        print(f"❌ Logo DELF non trouvé: {logo_delf_path}")
        return False
    
    # Générer le PDF
    try:
        pdf_generator = PDFGenerator(
            excel_path="exemple_candidats.xlsx",  # Fichier requis mais pas utilisé ici
            template_path=template_path,
            logo_af_path=logo_af_path,
            logo_delf_path=logo_delf_path,
            output_dir=output_dir,
            access_code=test_data['access_code']
        )
        
        filename = pdf_generator.generate_pdf(test_data)
        
        print(f"✅ PDF généré avec succès: {filename}")
        print("🎯 Vérifications à effectuer dans le PDF:")
        print("   - Le texte 'CONVOCATION À UN EXAMEN' est centré verticalement dans le cadre")
        print("   - L'espacement entre le titre et le nom du candidat est doublé")
        print("   - Le code d'accès apparaît en bas: '1234ABCD'")
        print("   - La bordure du titre fait 1px d'épaisseur")
        print("   - Le padding vertical du titre fait 2px au-dessus et au-dessous")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_centrage_espacement()
    if success:
        print("\n✅ Test terminé avec succès!")
    else:
        print("\n❌ Test échoué!")
    
    input("\nAppuyez sur Entrée pour continuer...")
