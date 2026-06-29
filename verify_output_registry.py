#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE VÉRIFICATION - S'assure que le registre output est toujours cohérent
"""

import json
import os
from datetime import datetime

def verify_output_registry():
    """Vérifie la cohérence du registre dans output"""
    
    print("VÉRIFICATION REGISTRE OUTPUT")
    print("=" * 40)
    print(f"Date/Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Chemins
    output_dir = r"C:\Users\JMM\Desktop\convoc generator TCF\output"
    registry_path = os.path.join(output_dir, "candidate_pdf_registry.json")
    
    print(f"\nDossier output: {output_dir}")
    print(f"Registre attendu: {registry_path}")
    
    # Vérifier l'existence du dossier
    if not os.path.exists(output_dir):
        print("❌ ERREUR: Dossier output n'existe pas!")
        return False
    
    # Lister tous les fichiers dans output
    all_files = os.listdir(output_dir)
    pdf_files = [f for f in all_files if f.endswith('.pdf')]
    json_files = [f for f in all_files if f.endswith('.json')]
    other_files = [f for f in all_files if not f.endswith('.pdf') and not f.endswith('.json')]
    
    print(f"\nCONTENU DU DOSSIER OUTPUT:")
    print(f"   Total fichiers: {len(all_files)}")
    print(f"   PDFs: {len(pdf_files)}")
    print(f"   JSON: {len(json_files)}")
    print(f"   Autres: {len(other_files)}")
    
    # Vérifier le registre
    if not os.path.exists(registry_path):
        print("\n❌ ERREUR: candidate_pdf_registry.json manquant!")
        if json_files:
            print(f"   Autres JSON trouvés: {json_files}")
        return False
    
    # Charger et analyser le registre
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
        
        print(f"\n✅ REGISTRE CHARGÉ AVEC SUCCÈS")
        print(f"   Candidats dans registre: {len(registry)}")
        
        # Vérifier la cohérence avec les PDFs
        expected_pdfs = []
        missing_pdfs = []
        inconnu_candidates = 0
        
        for candidate_id, info in registry.items():
            nom = info.get('nom', 'INCONNU')
            prenom = info.get('prenom', '')
            email = info.get('email', 'N/A')
            pdf_filename = info.get('pdf_filename', 'MANQUANT')
            
            if nom == 'INCONNU':
                inconnu_candidates += 1
            
            expected_pdfs.append(pdf_filename)
            
            # Vérifier si le PDF existe
            pdf_path = os.path.join(output_dir, pdf_filename)
            if not os.path.exists(pdf_path):
                missing_pdfs.append(pdf_filename)
        
        print(f"\nCOHÉRENCE PDF-REGISTRE:")
        print(f"   PDFs attendus: {len(expected_pdfs)}")
        print(f"   PDFs présents: {len(pdf_files)}")
        print(f"   PDFs manquants: {len(missing_pdfs)}")
        print(f"   Candidats INCONNU: {inconnu_candidates}")
        
        # Échantillon des candidats
        print(f"\nÉCHANTILLON (premiers 3 candidats):")
        for i, (candidate_id, info) in enumerate(list(registry.items())[:3]):
            nom = info.get('nom', 'INCONNU')
            prenom = info.get('prenom', '')
            email = info.get('email', 'N/A')
            pdf_filename = info.get('pdf_filename', 'MANQUANT')
            print(f"   {i+1}. {candidate_id}: {prenom} {nom}")
            print(f"      Email: {email}")
            print(f"      PDF: {pdf_filename}")
        
        # Évaluation finale
        print(f"\nÉVALUATION:")
        
        success = True
        if inconnu_candidates > 0:
            print(f"   ⚠️ {inconnu_candidates} candidats sans nom (INCONNU)")
            success = False
        
        if missing_pdfs:
            print(f"   ⚠️ {len(missing_pdfs)} PDFs manquants")
            success = False
        
        if len(registry) == 0:
            print(f"   ❌ Registre vide!")
            success = False
        
        if success:
            print(f"   ✅ REGISTRE PARFAITEMENT COHÉRENT!")
            print(f"   📊 {len(registry)} candidats avec noms valides")
            print(f"   📄 {len(pdf_files)} PDFs présents")
            print(f"   🎯 Prêt pour envoi d'emails")
        
        return success
        
    except Exception as e:
        print(f"\n❌ ERREUR lors de l'analyse du registre: {e}")
        return False

if __name__ == "__main__":
    verify_output_registry()