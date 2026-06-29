#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from tcf_excel_processor import TCFExcelProcessor
from jinja2 import Template, FileSystemLoader, Environment

def test_tcf_data_simple():
    """Test simple des données TCF sans génération PDF"""
    
    print("=== TEST SIMPLE DES DONNÉES TCF ===")
    print("=" * 40)
    
    # 1. Charger les données TCF
    print("1. Chargement des données TCF...")
    processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
    
    if not processor.load_tcf_data():
        print("❌ Erreur lors du chargement des données TCF")
        return False
        
    processor.print_summary()
    
    # 2. Tester les données de quelques candidats
    candidates = processor.get_all_candidates()
    if not candidates:
        print("❌ Aucun candidat trouvé")
        return False
    
    print(f"\n2. Test des données candidats...")
    
    # Prendre un candidat de chaque type TCF si possible
    test_candidates = []
    tcf_types_tested = set()
    
    for candidate in candidates:
        tcf_type = candidate.get('tcf_type')
        if tcf_type not in tcf_types_tested:
            test_candidates.append(candidate)
            tcf_types_tested.add(tcf_type)
            if len(test_candidates) >= 3:  # Limiter à 3 tests
                break
    
    for i, candidate in enumerate(test_candidates, 1):
        print(f"\n--- Candidat {i}: {candidate['prenom']} {candidate['nom']} ---")
        print(f"Type TCF: {candidate['tcf_type']}")
        print(f"Jury: {candidate['jury_name']}")
        print(f"Email: {candidate['email']}")
        print(f"Date naissance: {candidate['date_naissance']}")
        print(f"Date examen: {candidate['date_examen']}")
        print(f"Épreuve collective: {candidate['debut_ep_coll']} - {candidate['fin_ep_coll']}")
        if candidate.get('has_individual_exam'):
            print(f"Épreuve individuelle: {candidate['heure_preparation']}")
        else:
            print("Pas d'épreuve individuelle")
        print(f"Durée collective: {candidate['duree_collective']}")
        print(f"Durée individuelle: {candidate['duree_individuelle']}")
    
    return True

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
    
    candidate = candidates[0]
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
            'heure_preparation': candidate.get('heure_preparation'),
            'has_individual_exam': candidate['has_individual_exam'],
            'salle_collective': candidate['salle_collective'],
            'salle_individuelle': candidate['salle_individuelle'],
            'institution_name': candidate['institution_name'],
            'institution_address': candidate['institution_address'],
            'institution_postal': candidate['institution_postal'],
            'institution_city': candidate['institution_city'],
            'logo_af_path': 'assets/logoAF.png',
            'logo_tcf_path': 'assets/logoTCF.png',  # À définir plus tard
            'access_code': 'AF2025'
        }
        
        print("\nDonnées envoyées au template:")
        for key, value in template_data.items():
            print(f"  {key}: {value}")
        
        # Rendre le template
        html_content = template.render(**template_data)
        
        print(f"\n✅ Template rendu avec succès!")
        print(f"Taille HTML: {len(html_content)} caractères")
        
        # Sauvegarder le HTML pour inspection
        output_html = f"test_output_{candidate['tcf_type'].replace(' ', '_')}.html"
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML sauvegardé: {output_html}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du rendu du template: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LANCEMENT DES TESTS TCF SIMPLES")
    
    # Test 1: Données TCF
    if test_tcf_data_simple():
        print("\n" + "="*50)
        # Test 2: Rendu template
        test_template_rendering()
    else:
        print("❌ Échec du test des données TCF")