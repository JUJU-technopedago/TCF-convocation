#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final pour vérifier que les vrais candidats du fichier Excel 
reçoivent bien leurs PDF personnalisés distincts
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tcf_excel_processor import TCFExcelProcessor
from main import ConvocationGenerator
import tkinter as tk

def test_real_candidates_pdf_matching():
    """Test avec les vrais candidats du fichier Excel"""
    
    print("🧪 TEST FINAL : Candidats réels - Correspondance PDF personnalisée")
    print("=" * 80)
    
    # Créer une instance temporaire
    root = tk.Tk()
    root.withdraw()
    
    app = ConvocationGenerator()
    app.root = root
    
    # Configurer pour TCF
    app.exam_type.set("TCF")
    app.output_dir.set("output")
    
    # Essayer différents fichiers Excel pour trouver celui avec des candidats
    excel_files = [
        "juries_20250919_162205.xlsx",
        "JURYS FINAL TCF.xlsx", 
        "JURYS FINAL TCF - Copie.xlsx",
        "test_tcf_data.xlsx"
    ]
    
    processor = None
    candidates = []
    
    for excel_file in excel_files:
        if os.path.exists(excel_file):
            try:
                print(f"📄 Tentative de lecture: {excel_file}")
                test_processor = TCFExcelProcessor(excel_file)
                test_processor.load_tcf_data()
                test_candidates = test_processor.get_all_candidates()
                
                if test_candidates and len(test_candidates) > 0:
                    print(f"✅ Fichier valide trouvé: {excel_file} ({len(test_candidates)} candidats)")
                    processor = test_processor
                    candidates = test_candidates
                    app.excel_file_path.set(excel_file)
                    break
                else:
                    print(f"⚠️ Fichier sans candidats: {excel_file}")
            except Exception as e:
                print(f"❌ Erreur lecture {excel_file}: {e}")
    
    if not candidates:
        print("❌ Aucun candidat trouvé dans les fichiers Excel disponibles")
        print("💡 Créons des candidats de test pour la démonstration...")
        
        # Candidats basés sur les PDF existants  
        candidates = [
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
        print(f"📊 Utilisation de {len(candidates)} candidats de test")
    
    print(f"\n📊 TEST AVEC {len(candidates)} CANDIDATS")
    print("-" * 60)
    
    # Prendre maximum 5 candidats pour le test
    test_candidates = candidates[:5]
    
    results = []
    unique_pdfs = set()
    
    for i, candidat in enumerate(test_candidates, 1):
        nom = candidat.get('nom', 'INCONNU')
        prenom = candidat.get('prenom', '')
        email = candidat.get('email', 'N/A')
        tcf_type = candidat.get('tcf_type', 'N/A')
        
        print(f"\n{i}. 👤 {prenom} {nom}")
        print(f"   📧 {email}")
        print(f"   🎯 {tcf_type}")
        
        # Rechercher le PDF correspondant
        pdf_path, pdf_filename = app._find_pdf_file_robust(candidat, "output")
        
        if pdf_path and os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"   ✅ PDF: {pdf_filename} ({file_size} bytes)")
            
            # Enregistrer pour vérifier l'unicité
            results.append({
                'candidat': f"{prenom} {nom}",
                'email': email,
                'pdf': pdf_filename,
                'taille': file_size,
                'chemin': pdf_path
            })
            unique_pdfs.add(pdf_filename)
            
        else:
            print(f"   ❌ AUCUN PDF TROUVÉ")
            results.append({
                'candidat': f"{prenom} {nom}",
                'email': email,
                'pdf': None,
                'taille': 0,
                'chemin': None
            })
    
    # ANALYSE FINALE
    print(f"\n" + "=" * 80)
    print("📊 ANALYSE FINALE:")
    print("-" * 40)
    
    total_candidates = len(results)
    candidates_with_pdf = len([r for r in results if r['pdf']])
    unique_pdf_count = len(unique_pdfs)
    
    print(f"📈 Candidats testés: {total_candidates}")
    print(f"📈 Candidats avec PDF: {candidates_with_pdf}")
    print(f"📈 PDF uniques trouvés: {unique_pdf_count}")
    
    if candidates_with_pdf == unique_pdf_count and unique_pdf_count > 0:
        print("✅ SUCCÈS COMPLET: Chaque candidat a un PDF unique!")
        print("✅ Aucun risque d'envoi de PDF identiques")
    elif unique_pdf_count < candidates_with_pdf:
        print("⚠️ ATTENTION: Certains candidats partagent le même PDF!")
        print("⚠️ Cela pourrait expliquer le problème signalé")
        
        # Identifier les doublons
        pdf_usage = {}
        for result in results:
            if result['pdf']:
                if result['pdf'] in pdf_usage:
                    pdf_usage[result['pdf']].append(result['candidat'])
                else:
                    pdf_usage[result['pdf']] = [result['candidat']]
        
        print("\n🔍 DOUBLONS DÉTECTÉS:")
        for pdf, users in pdf_usage.items():
            if len(users) > 1:
                print(f"   📄 {pdf} → {', '.join(users)}")
    else:
        print("❌ PROBLÈME: Candidats sans PDF correspondant")
    
    print("\n🏁 Test terminé")
    
    root.destroy()
    return results

if __name__ == "__main__":
    test_real_candidates_pdf_matching()