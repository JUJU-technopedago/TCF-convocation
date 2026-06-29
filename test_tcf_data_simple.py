#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour vérifier les données TCF sans générer de PDF
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tcf_excel_processor import TCFExcelProcessor

def test_tcf_data_only():
    """Test simple pour vérifier les données TCF sans générer de PDF"""
    
    print("🔍 TEST SIMPLE : Vérification des données TCF uniquement")
    print("=" * 60)
    
    try:
        # Charger les candidats TCF
        processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
        processor.load_tcf_data()
        candidates = processor.get_all_candidates()
        
        print(f"📊 Total candidats chargés: {len(candidates)}")
        
        # Prendre les 5 premiers candidats
        test_candidates = candidates[:5]
        
        print(f"\n📋 DONNÉES DES 5 PREMIERS CANDIDATS:")
        print("-" * 50)
        
        for i, candidate in enumerate(test_candidates, 1):
            print(f"\n{i}. Candidat:")
            print(f"   nom: '{candidate.get('nom', 'N/A')}'")
            print(f"   prenom: '{candidate.get('prenom', 'N/A')}'")
            print(f"   email: '{candidate.get('email', 'N/A')}'")
            print(f"   tcf_type: '{candidate.get('tcf_type', 'N/A')}'")
            print(f"   numero_candidat: '{candidate.get('numero_candidat', 'N/A')}'")
        
        print(f"\n🔍 ANALYSE DE L'UNICITÉ:")
        print("-" * 30)
        
        # Vérifier l'unicité des données
        noms = [c.get('nom', 'N/A') for c in test_candidates]
        prenoms = [c.get('prenom', 'N/A') for c in test_candidates]
        emails = [c.get('email', 'N/A') for c in test_candidates]
        tcf_types = [c.get('tcf_type', 'N/A') for c in test_candidates]
        
        print(f"Noms uniques: {len(set(noms))} sur {len(noms)}")
        print(f"Prénoms uniques: {len(set(prenoms))} sur {len(prenoms)}")
        print(f"Emails uniques: {len(set(emails))} sur {len(emails)}")
        print(f"Types TCF uniques: {len(set(tcf_types))} sur {len(tcf_types)}")
        
        if len(set(noms)) == len(noms):
            print("✅ Tous les noms sont différents")
        else:
            print("⚠️ Il y a des noms en double")
            
        if len(set(emails)) == len(emails):
            print("✅ Tous les emails sont différents")
        else:
            print("⚠️ Il y a des emails en double")
        
        print(f"\n📂 SIMULATION NOMS DE FICHIERS PDF:")
        print("-" * 40)
        
        # Simuler la génération des noms de fichiers PDF
        pdf_names = []
        for candidate in test_candidates:
            nom = candidate.get('nom', 'INCONNU')
            prenom = candidate.get('prenom', '')
            pdf_filename = f"convocation_tcf_{nom}_{prenom}.pdf".replace(" ", "_")
            pdf_names.append(pdf_filename)
            print(f"PDF: {pdf_filename}")
        
        if len(set(pdf_names)) == len(pdf_names):
            print("✅ Tous les noms de fichiers PDF seraient uniques")
        else:
            print("⚠️ Certains noms de fichiers PDF seraient identiques")
        
        print(f"\n💡 CONCLUSION:")
        if len(set(noms)) == len(noms) and len(set(emails)) == len(emails):
            print("✅ Les données sources sont bien distinctes")
            print("🔍 Le problème vient probablement de la génération PDF ou du template")
        else:
            print("⚠️ Il y a des données en double dans la source")
            print("🔍 Vérifiez le fichier Excel ou le processeur TCF")
            
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tcf_data_only()