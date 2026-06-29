#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que la modification du template TCF fonctionne
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_generator import PDFGenerator
from tcf_excel_processor import TCFExcelProcessor

def test_tcf_template_modification():
    """Test pour vérifier les déclinaisons TCF dans le template"""
    
    print("🧪 Test des déclinaisons TCF dans le template")
    print("=" * 50)
    
    # Données de test pour chaque type TCF
    test_cases = [
        {
            'tcf_type': 'TCF CANADA',
            'expected': 'Examen TCF CANADA'
        },
        {
            'tcf_type': 'TCF TP COMPLET', 
            'expected': 'Examen TCF TOUT PUBLIC'
        },
        {
            'tcf_type': 'TCF IRN',
            'expected': 'Examen TCF INTÉGRATION, RÉSIDENCE & NATIONALITÉ'
        },
        {
            'tcf_type': 'TCF TP OBLIGATOIRE',
            'expected': 'Examen TCF TOUT PUBLIC'
        }
    ]
    
    # Candidat de test
    base_candidate = {
        'nom': 'TEST',
        'prenom': 'Candidat',
        'date_naissance': '01/01/1990',
        'numero_candidat': '12345',
        'adresse': '123 Rue Test\n1000 Bruxelles',
        'numero_convocation': 'TCF001'
    }
    
    # Test pour chaque type TCF
    for i, test_case in enumerate(test_cases):
        print(f"\n{i+1}. Test {test_case['tcf_type']}")
        print(f"   Attendu: {test_case['expected']}")
        
        # Préparer les données du candidat
        candidate = base_candidate.copy()
        candidate['tcf_type'] = test_case['tcf_type']
        
        # Données du template
        template_data = {
            'nom': candidate['nom'],
            'prenom': candidate['prenom'],
            'date_naissance': candidate['date_naissance'],
            'numero_candidat': candidate['numero_candidat'],
            'adresse': candidate['adresse'],
            'numero_convocation': candidate['numero_convocation'],
            'tcf_type': candidate['tcf_type'],
            
            # Données d'examen exemple
            'date_collective_format': '15 octobre 2024',
            'debut_ep_coll': '09:00',
            'duree_collective': '2h47',
            'salle_collective': 'Salle 1',
            'date_individual_format': '16 octobre 2024', 
            'heure_preparation': '14:00',
            'duree_individual': '12 minutes',
            'salle_individual': 'Salle 2',
            
            # Logo
            'logo_delf_path': 'assets/logoTCF_IRN.png'
        }
        
        try:
            # Générer le HTML pour vérifier le contenu
            pdf_gen = PDFGenerator()
            html_content = pdf_gen.render_html_template('convocation_tcf_template_simple.html', template_data)
            
            # Vérifier que le bon texte est présent
            if test_case['expected'] in html_content:
                print(f"   ✅ Correct: {test_case['expected']} trouvé")
            else:
                print(f"   ❌ Erreur: {test_case['expected']} non trouvé")
                # Chercher ce qui est affiché à la place
                import re
                exam_match = re.search(r'<div class="exam-title">\s*([^<]+)', html_content)
                if exam_match:
                    found_text = exam_match.group(1).strip()
                    print(f"      Trouvé à la place: {found_text}")
                    
        except Exception as e:
            print(f"   ❌ Erreur lors du test: {e}")
    
    print(f"\n{'='*50}")
    print("✅ Test des déclinaisons TCF terminé")

if __name__ == "__main__":
    test_tcf_template_modification()