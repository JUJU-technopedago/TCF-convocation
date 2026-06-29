#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour générer un PDF de test TCF
"""

import os
import sys
import logging
from datetime import datetime

# Ajouter le répertoire actuel au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tcf_excel_processor import TCFExcelProcessor
from reportlab_pdf_generator import ReportLabPDFGenerator

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

def generer_pdf_test_tcf():
    """Générer un PDF de test pour un candidat TCF"""
    
    print("🚀 GÉNÉRATION PDF DE TEST TCF")
    print("=" * 40)
    
    try:
        # 1. Charger les données TCF
        print("1. Chargement des données TCF...")
        processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
        processor.load_tcf_data()
        candidates = processor.get_all_candidates()
        
        if not candidates:
            print("❌ Aucun candidat trouvé")
            return False
        
        # Prendre le premier candidat TCF CANADA
        candidate = None
        for c in candidates:
            if c['tcf_type'] == 'TCF CANADA':
                candidate = c
                break
        
        if not candidate:
            candidate = candidates[0]
        
        print(f"Candidat sélectionné: {candidate['prenom']} {candidate['nom']} ({candidate['tcf_type']})")
        
        # 2. Préparer les données pour le générateur PDF
        print("2. Préparation des données...")
        
        # Configuration pour le générateur PDF
        config = {
            'institution_name': 'Alliance Française de Bruxelles-Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_postal': '1000',
            'institution_city': 'Bruxelles',
            'institution_country': 'Belgique',
            'institution_phone': '+32 2 788 21 60',
            'institution_email': 'info@alliancefrancaise.be',
            'logo_af_path': 'assets/logoAF.png',
            'logo_tcf_path': 'assets/logoTCF.png',
            'access_code': 'AF2025'
        }
        
        # Données du candidat pour le template
        template_data = {
            'nom': candidate['nom'],
            'prenom': candidate['prenom'],
            'date_naissance': candidate['date_naissance'],
            'email': candidate['email'],
            'tcf_type': candidate['tcf_type'],
            'date_examen': candidate['date_examen'],
            
            # Dates formatées
            'date_collective_format': candidate['date_ep_coll'].strftime("%d/%m/%Y") if candidate['date_ep_coll'] else "",
            'date_individual_format': candidate['date_ep_ind'].strftime("%d/%m/%Y") if candidate['date_ep_ind'] else "",
            
            # Épreuves
            'has_collective_exams': candidate['tcf_type'] != 'TCF TP OBLIGATOIRE',
            'has_individual_exam': True,
            'heure_collective': candidate['debut_ep_coll'],
            'heure_individual': candidate['heure_preparation'],
            'duree_collective': candidate['duree_collective'],
            'duree_individual': candidate['duree_individuelle'],
            
            # Salles
            'salle_collective': candidate['salle_collective'],
            'salle_individuelle': candidate['salle_individuelle'],
            'lieu': config['institution_address'],
            
            # Configuration
            **config
        }
        
        print("Données préparées:")
        print(f"  Type TCF: {template_data['tcf_type']}")
        print(f"  Date examen: {template_data['date_collective_format']}")
        print(f"  Épreuves collectives: {template_data['has_collective_exams']}")
        print(f"  Durée collective: {template_data['duree_collective']}")
        print(f"  Durée individuelle: {template_data['duree_individual']}")
        
        # 3. Générer le PDF
        print("3. Génération du PDF...")
        
        generator = ReportLabPDFGenerator(config)
        
        # Nom du fichier de sortie
        output_filename = f"test_convocation_{candidate['tcf_type'].replace(' ', '_')}_{candidate['nom']}.pdf"
        
        # Générer le PDF avec le template TCF
        success = generator.generate_convocation(
            template_data,
            output_filename,
            template_name="convocation_tcf_template_modele.html"
        )
        
        if success:
            print(f"✅ PDF généré avec succès: {output_filename}")
            print(f"📄 Chemin complet: {os.path.abspath(output_filename)}")
            return True
        else:
            print("❌ Erreur lors de la génération du PDF")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generer_pdf_test_tcf()
    
    if success:
        print("\n🎉 PDF DE TEST GÉNÉRÉ AVEC SUCCÈS!")
        print("Vous pouvez maintenant ouvrir le fichier PDF pour vérifier la convocation TCF.")
    else:
        print("\n❌ ÉCHEC DE LA GÉNÉRATION DU PDF")