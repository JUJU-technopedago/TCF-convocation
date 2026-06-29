#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour générer plusieurs PDFs de test TCF (tous les types)
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

def generer_pdfs_tous_types_tcf():
    """Générer des PDFs de test pour tous les types de TCF"""
    
    print("🚀 GÉNÉRATION PDFs POUR TOUS LES TYPES TCF")
    print("=" * 50)
    
    try:
        # 1. Charger les données TCF
        print("1. Chargement des données TCF...")
        processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
        processor.load_tcf_data()
        candidates = processor.get_all_candidates()
        
        if not candidates:
            print("❌ Aucun candidat trouvé")
            return False
        
        # Configuration commune
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
        
        generator = ReportLabPDFGenerator(config)
        
        # Types de TCF à tester
        types_tcf = ['TCF CANADA', 'TCF TP COMPLET', 'TCF IRN']
        
        pdfs_generes = []
        
        for tcf_type in types_tcf:
            print(f"\n2. Recherche d'un candidat {tcf_type}...")
            
            # Trouver un candidat de ce type
            candidate = None
            for c in candidates:
                if c['tcf_type'] == tcf_type:
                    candidate = c
                    break
            
            if not candidate:
                print(f"❌ Aucun candidat trouvé pour {tcf_type}")
                continue
            
            print(f"Candidat trouvé: {candidate['prenom']} {candidate['nom']}")
            
            # Préparer les données pour le template
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
            
            # Nom du fichier de sortie
            output_filename = f"convocation_{candidate['tcf_type'].replace(' ', '_')}_{candidate['nom']}.pdf"
            
            print(f"3. Génération du PDF: {output_filename}")
            print(f"   Durée collective: {template_data['duree_collective']}")
            print(f"   Durée individuelle: {template_data['duree_individual']}")
            
            # Générer le PDF
            success = generator.generate_convocation(
                template_data,
                output_filename,
                template_name="convocation_tcf_template_modele.html"
            )
            
            if success:
                print(f"✅ PDF généré: {output_filename}")
                pdfs_generes.append(output_filename)
            else:
                print(f"❌ Erreur génération: {output_filename}")
        
        print(f"\n🎉 GÉNÉRATION TERMINÉE!")
        print(f"PDFs générés ({len(pdfs_generes)}):")
        for pdf in pdfs_generes:
            print(f"  📄 {pdf}")
            
        return len(pdfs_generes) > 0
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generer_pdfs_tous_types_tcf()
    
    if success:
        print("\n✨ TOUS LES PDFs TCF ONT ÉTÉ GÉNÉRÉS AVEC SUCCÈS!")
        print("Vous pouvez maintenant comparer les différents types de convocations TCF.")
    else:
        print("\n❌ ÉCHEC DE LA GÉNÉRATION DES PDFs")