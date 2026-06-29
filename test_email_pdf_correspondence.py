#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour simuler l'envoi d'emails et vérifier la correspondance PDF-candidat
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tcf_excel_processor import TCFExcelProcessor
from main import ConvocationGenerator
import tkinter as tk

def test_email_pdf_matching():
    """Test la correspondance PDF-candidat lors de l'envoi d'emails"""
    
    print("🧪 TEST : Correspondance PDF-candidat pour envoi emails")
    print("=" * 70)
    
    # Créer une instance temporaire
    root = tk.Tk()
    root.withdraw()
    
    app = ConvocationGenerator()
    app.root = root
    
    # Configurer pour TCF
    app.exam_type.set("TCF")
    app.output_dir.set("output")
    
    # Créer des candidats fictifs basés sur les PDF existants
    test_candidates = [
        {
            'nom': 'BIDON',
            'prenom': 'Marc',
            'email': 'marc.bidon@test.com',
            'numero_candidat': 'TCF2025000001',
            'tcf_type': 'TCF CANADA'
        },
        {
            'nom': 'BROOT',
            'prenom': '',
            'email': 'broot@test.com',
            'numero_candidat': 'TCF2025000002',
            'tcf_type': 'TCF TP COMPLET'
        },
        {
            'nom': 'TARTAMPION',
            'prenom': 'John',
            'email': 'john.tartampion@test.com',
            'numero_candidat': 'TCF2025000003',
            'tcf_type': 'TCF IRN'
        }
    ]
    
    print(f"📊 Test avec {len(test_candidates)} candidats fictifs")
    print("-" * 50)
    
    all_match = True
    
    for i, candidat in enumerate(test_candidates, 1):
        nom = candidat['nom']
        prenom = candidat['prenom']
        email = candidat['email']
        
        print(f"\n{i}. Candidat: {prenom} {nom}")
        print(f"   Email: {email}")
        print(f"   Type TCF: {candidat['tcf_type']}")
        
        # Tester la fonction de recherche PDF
        pdf_path, pdf_filename = app._find_pdf_file_robust(candidat, "output")
        
        if pdf_path and os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"   ✅ PDF trouvé: {pdf_filename}")
            print(f"   📁 Chemin: {pdf_path}")
            print(f"   📊 Taille: {file_size} bytes")
            
            # Vérifier que c'est le bon PDF pour ce candidat
            expected_filename = f"convocation_tcf_{nom}_{prenom}.pdf"
            if pdf_filename == expected_filename:
                print(f"   ✅ CORRESPONDANCE PARFAITE: {expected_filename}")
            else:
                print(f"   ⚠️ CORRESPONDANCE DIFFÉRENTE:")
                print(f"      Attendu: {expected_filename}")
                print(f"      Trouvé:  {pdf_filename}")
                all_match = False
                
        else:
            print(f"   ❌ AUCUN PDF TROUVÉ pour ce candidat")
            all_match = False
            
            # Afficher les patterns testés pour debug
            print(f"   🔍 Patterns qui auraient dû marcher:")
            print(f"      - convocation_tcf_{nom}_{prenom}.pdf")
            print(f"      - convocation_tcf_{nom.upper()}_{prenom}.pdf")
    
    print(f"\n" + "=" * 70)
    print("📋 RÉSUMÉ DU TEST:")
    
    if all_match:
        print("✅ SUCCÈS: Tous les candidats ont leur PDF correspondant")
        print("✅ Le système de correspondance fonctionne correctement")
    else:
        print("❌ ÉCHEC: Certains candidats n'ont pas leur PDF correspondant")
        print("❌ Il y a un problème dans la logique de correspondance")
    
    print("🏁 Test terminé")
    
    root.destroy()
    return all_match

if __name__ == "__main__":
    test_email_pdf_matching()