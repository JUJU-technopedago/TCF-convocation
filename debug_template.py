#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de debug pour vérifier quel template est utilisé
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_generator import PDFGenerator

def test_template_usage():
    """Test pour vérifier quel template est utilisé"""
    
    print("🧪 Test de débug du template utilisé")
    print("=" * 50)
    
    # Données de test
    test_candidate = {
        'nom': 'TEST',
        'prenom': 'Debug',
        'date_naissance': '01/01/1990',
        'numero_candidat': '12345',
        'adresse': '123 Rue Test\n1000 Bruxelles',
        'numero_convocation': 'DEBUG001',
        'tcf_type': 'TCF CANADA',  # Type spécifique
        
        # Données d'examen
        'date_collective_format': '15 octobre 2024',
        'debut_ep_coll': '09:00',
        'duree_collective': '2h47',
        'salle_collective': 'Salle 1',
        'date_individual_format': '16 octobre 2024', 
        'heure_preparation': '14:00',
        'duree_individual': '12 minutes',
        'salle_individual': 'Salle 2',
    }
    
    # Test avec le template simple
    template_path = 'templates/convocation_tcf_template_simple.html'
    
    print(f"📄 Template testé: {template_path}")
    print(f"📋 Type TCF: {test_candidate['tcf_type']}")
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
    
    try:
        # Créer le générateur PDF
        generator = PDFGenerator(
            excel_path='',  # Pas besoin pour ce test
            template_path=template_path,
            logo_af_path='assets/logoAF.png',
            logo_delf_path='assets/logoTCF_CANADA.png',
            output_dir='debug_output'
        )
        
        # Générer le HTML pour voir le contenu
        template_data = generator._prepare_template_data(test_candidate)
        html_content = generator.template.render(**template_data)
        
        # Sauvegarder le HTML pour inspection
        with open('debug_template_output.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ HTML généré: debug_template_output.html")
        
        # Chercher le titre d'examen dans le HTML
        if 'Examen TCF CANADA' in html_content:
            print("✅ SUCCÈS: Trouvé 'Examen TCF CANADA' dans le HTML")
        elif 'Examen TCF' in html_content:
            print("⚠️  PROBLÈME: Trouvé seulement 'Examen TCF' générique")
        else:
            print("❌ ERREUR: Aucun titre d'examen trouvé")
            
        # Afficher un extrait du HTML autour du titre
        import re
        exam_match = re.search(r'<div[^>]*class="exam-title"[^>]*>(.*?)</div>', html_content, re.DOTALL)
        if exam_match:
            print(f"📝 Titre trouvé: {exam_match.group(1).strip()}")
        else:
            print("❌ Div exam-title non trouvée")
            
        # Chercher toutes les occurrences de "Examen"
        exam_matches = re.findall(r'Examen[^<\n]*', html_content)
        if exam_matches:
            print(f"🔍 Tous les titres d'examen trouvés: {exam_matches}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_template_usage()