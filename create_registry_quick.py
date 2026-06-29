#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de création rapide du registre sécurisé pour corriger l'envoi d'emails
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire courant au path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def create_registry_with_existing_pdfs():
    """Crée le registre sécurisé en analysant les PDFs existants"""
    
    print("🔧 CRÉATION REGISTRE SÉCURISÉ POUR CORRECTION MAILJET")
    print("=" * 60)
    
    try:
        from tcf_excel_processor import TCFExcelProcessor
        from candidate_pdf_registry import CandidatePDFRegistry
        print("✅ Imports des modules TCF réussis")
    except Exception as e:
        print(f"❌ Erreur import modules: {e}")
        return False
    
    # 1. Charger les candidats depuis le fichier Excel
    excel_file = "JURYS FINAL TCF.xlsx"
    output_dir = "."
    
    try:
        processor = TCFExcelProcessor(excel_file)
        processor.load_tcf_data()
        candidates = processor.get_all_candidates()
        
        if not candidates:
            print("❌ Aucun candidat trouvé dans le fichier Excel")
            return False
            
        print(f"📊 {len(candidates)} candidats trouvés dans Excel")
        
    except Exception as e:
        print(f"❌ Erreur chargement Excel: {e}")
        return False
    
    # 2. Initialiser le registre sécurisé
    registry = CandidatePDFRegistry(output_dir)
    print("🔒 Registre sécurisé initialisé")
    
    # 3. Chercher tous les PDFs TCF existants
    import glob
    pdf_files = glob.glob(os.path.join(output_dir, "convocation_TCF_*.pdf"))
    print(f"📄 {len(pdf_files)} PDFs TCF trouvés sur disque")
    
    if pdf_files:
        for pdf_file in pdf_files:
            print(f"   - {os.path.basename(pdf_file)}")
    
    # 4. Créer les associations candidates-PDFs pour le registre
    registered_count = 0
    fallback_count = 0
    
    for i, candidate in enumerate(candidates, 1):
        try:
            nom = candidate.get('nom', 'INCONNU')
            prenom = candidate.get('prenom', '')
            email = candidate.get('email', 'N/A')
            
            # Générer nom de fichier sécurisé
            secure_filename = registry.generate_secure_filename(candidate, "TCF")
            candidate_id = registry.generate_candidate_id(candidate)
            
            # Vérifier si un PDF existe pour ce candidat
            pdf_found = False
            pdf_path = None
            
            # Recherche dans les PDFs existants
            for pdf_file in pdf_files:
                pdf_name = os.path.basename(pdf_file)
                
                # Vérifier si ce PDF correspond au candidat
                if (nom.upper() in pdf_name.upper() and prenom.upper() in pdf_name.upper()) or \
                   secure_filename in pdf_name:
                    pdf_found = True
                    pdf_path = pdf_file
                    break
            
            if pdf_found:
                # Enregistrer dans le registre
                registry.register_candidate_pdf(candidate, os.path.basename(pdf_path), pdf_path)
                registered_count += 1
                print(f"[{i}/{len(candidates)}] ✅ {prenom} {nom} → {os.path.basename(pdf_path)}")
            else:
                # Créer une entrée de fallback avec le nom de fichier attendu
                expected_pdf = secure_filename
                expected_path = os.path.join(output_dir, expected_pdf)
                
                # Enregistrer quand même pour que le système de fallback fonctionne
                registry.register_candidate_pdf(candidate, expected_pdf, expected_path)
                fallback_count += 1
                print(f"[{i}/{len(candidates)}] ⚠️ {prenom} {nom} → {expected_pdf} (fallback)")
                
        except Exception as e:
            print(f"   ❌ Erreur candidat {nom}: {e}")
    
    # 5. Sauvegarder le registre
    registry.save_registry()
    
    print(f"\n✅ REGISTRE CRÉÉ AVEC SUCCÈS !")
    print(f"📊 Candidats avec PDF existant: {registered_count}")
    print(f"🔄 Candidats en fallback: {fallback_count}")
    print(f"📋 Total enregistré: {registered_count + fallback_count}/{len(candidates)}")
    print(f"💾 Registre sauvegardé dans: {registry.registry_file}")
    
    return True

if __name__ == "__main__":
    create_registry_with_existing_pdfs()