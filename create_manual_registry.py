#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de création manuelle du registre pour corriger l'envoi d'emails
"""

import json
import os
import sys
from pathlib import Path

# Ajouter le répertoire courant au path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def create_manual_registry():
    """Crée manuellement le registre sécurisé pour que Mailjet trouve les candidats"""
    
    print("🔧 CRÉATION MANUELLE DU REGISTRE SÉCURISÉ")
    print("=" * 50)
    
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
            print("❌ Aucun candidats trouvés")
            return False
            
        print(f"📊 {len(candidates)} candidats trouvés")
        
    except Exception as e:
        print(f"❌ Erreur chargement Excel: {e}")
        return False
    
    # 2. Créer un registre vide et l'alimenter manuellement
    registry = CandidatePDFRegistry(output_dir)
    
    # 3. Créer le registre manuellement avec un format JSON simple
    registry_data = {}
    
    for i, candidate in enumerate(candidates, 1):
        try:
            nom = candidate.get('nom', 'INCONNU')
            prenom = candidate.get('prenom', '')
            email = candidate.get('email', 'N/A')
            
            # Générer ID unique avec la méthode du registre
            candidate_id = registry.generate_candidate_id(candidate)
            secure_filename = registry.generate_secure_filename(candidate, "TCF")
            
            # Ajouter au registre
            registry_data[candidate_id] = {
                "nom": nom,
                "prenom": prenom,
                "email": email,
                "pdf_filename": secure_filename,
                "pdf_path": os.path.join(output_dir, secure_filename),
                "tcf_type": candidate.get('tcf_type', 'TCF'),
                "jury": candidate.get('jury_info', {}),
                "date_ep_coll": str(candidate.get('date_ep_coll', '')),
                "debut_ep_coll": str(candidate.get('debut_ep_coll', '')),
                "registered_at": "2025-10-01T11:00:00"
            }
            
            print(f"[{i}/{len(candidates)}] ✅ {prenom} {nom} (ID: {candidate_id}) → {secure_filename}")
            
        except Exception as e:
            print(f"   ❌ Erreur candidat {nom}: {e}")
    
    # 4. Sauvegarder le registre manuellement
    registry_file = os.path.join(output_dir, "candidate_pdf_registry.json")
    
    try:
        with open(registry_file, 'w', encoding='utf-8') as f:
            json.dump(registry_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ REGISTRE CRÉÉ AVEC SUCCÈS !")
        print(f"📋 Total enregistré: {len(registry_data)}/{len(candidates)}")
        print(f"💾 Registre sauvegardé dans: {registry_file}")
        
        # 5. Vérifier le contenu
        print(f"\n🔍 Vérification du registre:")
        with open(registry_file, 'r', encoding='utf-8') as f:
            verification_data = json.load(f)
        print(f"   📊 Enregistrements trouvés: {len(verification_data)}")
        
        # Afficher quelques exemples
        example_count = min(3, len(verification_data))
        for i, (candidate_id, data) in enumerate(verification_data.items()):
            if i < example_count:
                print(f"   📝 Exemple {i+1}: {data['prenom']} {data['nom']} (ID: {candidate_id})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return False

if __name__ == "__main__":
    create_manual_registry()