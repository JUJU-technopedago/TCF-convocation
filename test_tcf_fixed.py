#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test simple du processeur TCF et du template
"""

import os
import sys
import logging
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Ajouter le répertoire actuel au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tcf_excel_processor import TCFExcelProcessor

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

def test_tcf_data_simple():
    """Test simple des données TCF sans génération PDF"""
    
    print("=== TEST SIMPLE DES DONNÉES TCF ===")
    print("=" * 40)
    
    # 1. Charger les données TCF
    print("1. Chargement des données TCF...")
    processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
    
    try:
        processor.load_tcf_data()
        print(f"\n=== RÉSUMÉ DES DONNÉES TCF ===")
        print(f"Fichier: JURYS FINAL TCF.xlsx")
        print(f"Total candidats: {len(processor.get_all_candidates())}")
        
        # Statistiques par type de TCF
        stats = {}
        for candidate in processor.get_all_candidates():
            tcf_type = candidate['tcf_type']
            stats[tcf_type] = stats.get(tcf_type, 0) + 1
        
        for tcf_type, count in stats.items():
            print(f"  {tcf_type}: {count} candidats")
        
        print(f"\nJurys détectés: {len(processor.jurys)}")
        for jury_name, jury_info in processor.jurys.items():
            print(f"  {jury_name} ({jury_info['tcf_type']}): {jury_info['date_examen']} - {jury_info['debut_ep_coll']}-{jury_info['fin_ep_coll']}")
        
        # 2. Afficher quelques candidats
        print("\n2. Test des données candidats...")
        candidates = processor.get_all_candidates()[:3]  # Premiers 3 candidats
        
        for i, candidate in enumerate(candidates, 1):
            print(f"\n--- Candidat {i}: {candidate['prenom']} {candidate['nom']} ---")
            print(f"Type TCF: {candidate['tcf_type']}")
            print(f"Jury: {candidate['jury_name']}")
            print(f"Email: {candidate['email']}")
            print(f"Date naissance: {candidate['date_naissance']}")
            print(f"Date examen: {candidate['date_examen']}")
            print(f"Épreuve collective: {candidate['debut_ep_coll']} - {candidate['fin_ep_coll']}")
            print(f"Épreuve individuelle: {candidate['heure_preparation']}")
            print(f"Durée collective: {candidate['duree_collective']}")
            print(f"Durée individuelle: {candidate['duree_individuelle']}")
            
        print("\n" + "=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement TCF: {e}")
        return False

def test_template_rendering():
    """Test du rendu du template TCF"""
    
    print("\n=== TEST DU RENDU TEMPLATE TCF ===")
    print("=" * 40)
    
    # Charger un candidat
    processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
    processor.load_tcf_data()
    candidates = processor.get_all_candidates()
    
    if not candidates:
        print("❌ Aucun candidat trouvé")
        return False
    
    # Trouver un candidat TCF TP COMPLET pour tester
    candidate = None
    for c in candidates:
        if c['tcf_type'] == 'TCF TP COMPLET':
            candidate = c
            break
    
    # Si pas de TCF TP COMPLET, prendre TCF CANADA 
    if not candidate:
        for c in candidates:
            if c['tcf_type'] == 'TCF CANADA':
                candidate = c
                break
    
    if not candidate:
        candidate = candidates[0]  # Fallback sur le premier candidat
    print(f"Test avec: {candidate['prenom']} {candidate['nom']} ({candidate['tcf_type']})")
    
    # Charger le template TCF
    template_path = "templates/convocation_tcf_template_modele.html"
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return False
    
    try:
        # Charger le template Jinja2
        template_dir = os.path.dirname(template_path)
        template_name = os.path.basename(template_path)
        
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)
        
        print(f"✅ Template chargé: {template_name}")
        
        # Préparer les données pour le template
        template_data = {
            'nom': candidate['nom'],
            'prenom': candidate['prenom'],
            'date_naissance': candidate['date_naissance'],
            'email': candidate['email'],
            'tcf_type': candidate['tcf_type'],
            'date_examen': candidate['date_examen'],
            'date_ep_coll': candidate['date_ep_coll'],
            'date_ep_ind': candidate['date_ep_ind'],
            'debut_ep_coll': candidate['debut_ep_coll'],
            'fin_ep_coll': candidate['fin_ep_coll'],
            'heure_preparation': candidate['heure_preparation'],
            # Nouvelles variables TCF
            'has_collective_exams': candidate['tcf_type'] != 'TCF TP OBLIGATOIRE',
            'has_individual_exam': True,
            'date_collective_format': candidate['date_ep_coll'].strftime("%d/%m/%Y") if candidate['date_ep_coll'] else "",
            'date_individual_format': candidate['date_ep_ind'].strftime("%d/%m/%Y") if candidate['date_ep_ind'] else "",
            'heure_collective': candidate['debut_ep_coll'],
            'heure_individual': candidate['heure_preparation'],
            'duree_collective': candidate['duree_collective'],
            'duree_individual': candidate['duree_individuelle'],
            'salle_collective': candidate['salle_collective'],
            'salle_individuelle': candidate['salle_individuelle'],
            # Lieu et informations standard
            'lieu': 'Avenue des Arts 46',
            'institution_name': 'Alliance Française de Bruxelles-Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_postal': '1000',
            'institution_city': 'Bruxelles',
            'logo_af_path': 'assets/logoAF.png',
            'logo_tcf_path': 'assets/logoTCF.png',
            'access_code': 'AF2025'
        }
        
        print("\nDonnées envoyées au template:")
        for key, value in template_data.items():
            print(f"  {key}: {value}")
        
        # Générer le HTML
        html_content = template.render(**template_data)
        
        print("\n✅ Template rendu avec succès!")
        print(f"Taille HTML: {len(html_content)} caractères")
        
        # Sauvegarder le HTML pour vérification
        output_file = f"test_output_{candidate['tcf_type'].replace(' ', '_')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML sauvegardé: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur template: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 LANCEMENT DES TESTS TCF SIMPLES")
    
    # Test des données
    success_data = test_tcf_data_simple()
    
    # Test du template
    success_template = test_template_rendering()
    
    if success_data and success_template:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
    else:
        print("\n❌ Certains tests ont échoué")