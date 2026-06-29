#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour vérifier la modification du template TCF sans dépendances
"""

from jinja2 import Template
import os

def test_template_simple():
    """Test simple du template TCF modifié"""
    
    print("🧪 Test simple des déclinaisons TCF")
    print("=" * 50)
    
    # Lire le template
    template_path = 'templates/convocation_tcf_template_simple.html'
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
        
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Créer le template Jinja2
    template = Template(template_content)
    
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
    
    # Données de base pour le template
    base_data = {
        'nom': 'TEST',
        'prenom': 'Candidat',
        'date_naissance': '01/01/1990',
        'numero_candidat': '12345',
        'adresse': '123 Rue Test\n1000 Bruxelles',
        'numero_convocation': 'TCF001',
        'date_collective_format': '15 octobre 2024',
        'debut_ep_coll': '09:00',
        'duree_collective': '2h47',
        'salle_collective': 'Salle 1',
        'date_individual_format': '16 octobre 2024', 
        'heure_preparation': '14:00',
        'duree_individual': '12 minutes',
        'salle_individual': 'Salle 2',
        'logo_delf_path': 'assets/logoTCF_IRN.png'
    }
    
    # Test pour chaque type TCF
    success_count = 0
    for i, test_case in enumerate(test_cases):
        print(f"\n{i+1}. Test {test_case['tcf_type']}")
        print(f"   Attendu: {test_case['expected']}")
        
        try:
            # Préparer les données avec le type TCF
            data = base_data.copy()
            data['tcf_type'] = test_case['tcf_type']
            
            # Rendre le template
            html_output = template.render(**data)
            
            # Vérifier que le bon texte est présent
            if test_case['expected'] in html_output:
                print(f"   ✅ Correct: {test_case['expected']} trouvé")
                success_count += 1
            else:
                print(f"   ❌ Erreur: {test_case['expected']} non trouvé")
                # Chercher ce qui est affiché à la place
                import re
                exam_matches = re.findall(r'Examen [^<\n]+', html_output)
                if exam_matches:
                    print(f"      Trouvé à la place: {exam_matches}")
                    
        except Exception as e:
            print(f"   ❌ Erreur lors du test: {e}")
    
    print(f"\n{'='*50}")
    print(f"✅ Test terminé: {success_count}/{len(test_cases)} réussis")
    
    if success_count == len(test_cases):
        print("🎉 Toutes les déclinaisons TCF fonctionnent correctement!")
    else:
        print(f"⚠️  {len(test_cases) - success_count} échecs détectés")

if __name__ == "__main__":
    test_template_simple()