#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple du template Jinja2 sans PDF
"""

from jinja2 import Template, FileSystemLoader, Environment
import os

def test_template_simple():
    """Test simple du template modifié"""
    
    print("🧪 Test simple du template TCF")
    print("=" * 50)
    
    template_path = 'templates/convocation_tcf_template_simple.html'
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
    
    # Lire le template
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Créer le template Jinja2
    template = Template(template_content)
    
    # Données de test pour TCF CANADA
    test_data = {
        'nom': 'ALEXANDER',
        'prenom': 'Thomas Robert',
        'date_naissance': '13/08/1985',
        'numero_candidat': '12345',
        'adresse': '123 Rue Test\n1000 Bruxelles',
        'numero_convocation': 'TCF001',
        'tcf_type': 'TCF CANADA',  # IMPORTANT !
        
        # Données d'examen
        'date_collective_format': '15 octobre 2024',
        'debut_ep_coll': '09:00',
        'duree_collective': '2h47',
        'salle_collective': 'Salle 1',
        'date_individual_format': '16 octobre 2024', 
        'heure_preparation': '14:00',
        'duree_individual': '12 minutes',
        'salle_individual': 'Salle 2',
        'logo_delf_path': 'assets/logoTCF_CANADA.png'
    }
    
    print(f"📋 Données de test:")
    print(f"   Type TCF: {test_data['tcf_type']}")
    print(f"   Nom: {test_data['nom']} {test_data['prenom']}")
    
    try:
        # Générer le HTML
        html_output = template.render(**test_data)
        
        # Sauvegarder pour inspection
        with open('test_template_output.html', 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print("✅ HTML généré: test_template_output.html")
        
        # Chercher le titre d'examen
        if 'Examen TCF CANADA' in html_output:
            print("✅ SUCCÈS: 'Examen TCF CANADA' trouvé dans le HTML")
        elif 'Examen TCF' in html_output:
            print("⚠️  PROBLÈME: Trouvé seulement 'Examen TCF' générique")
            
            # Chercher ce qui est affiché exactement
            import re
            exam_matches = re.findall(r'Examen[^<\n]*', html_output)
            print(f"🔍 Titres trouvés: {exam_matches}")
        else:
            print("❌ ERREUR: Aucun titre d'examen trouvé")
            
        # Vérifier la condition Jinja2
        if "{% if tcf_type == 'TCF CANADA' %}" in template_content:
            print("✅ Condition 'TCF CANADA' trouvée dans le template")
        else:
            print("❌ Condition 'TCF CANADA' manquante dans le template")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_template_simple()