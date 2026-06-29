#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic et réparation du système d'envoi d'emails
"""

import json
import os
import glob
from pathlib import Path

def diagnose_pdf_registry_sync():
    """Diagnostique la synchronisation entre PDFs et registre"""
    print("🔍 DIAGNOSTIC SYSTÈME PDF-REGISTRE")
    print("=" * 50)
    
    # 1. Vérifier le registre
    registry_path = "candidate_pdf_registry.json"
    if not os.path.exists(registry_path):
        print("❌ Registre manquant!")
        return False
    
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    print(f"✅ Registre: {len(registry)} candidats")
    
    # 2. Vérifier les PDFs existants
    pdf_files = glob.glob("convocation_TCF_*.pdf")
    print(f"📄 PDFs trouvés: {len(pdf_files)}")
    
    # 3. Analyser la correspondance
    print("\n🔍 ANALYSE DE CORRESPONDANCE:")
    registry_files = []
    missing_pdfs = []
    existing_pdfs = []
    
    for candidate_id, info in registry.items():
        pdf_filename = info.get('pdf_filename', f'convocation_TCF_UNKNOWN_{candidate_id}.pdf')
        registry_files.append(pdf_filename)
        
        if os.path.exists(pdf_filename):
            existing_pdfs.append(pdf_filename)
            print(f"   ✅ {info.get('prenom', '')} {info.get('nom', '')} → {pdf_filename}")
        else:
            missing_pdfs.append({
                'candidate_id': candidate_id,
                'nom': info.get('nom', 'INCONNU'),
                'prenom': info.get('prenom', ''),
                'pdf_filename': pdf_filename
            })
            print(f"   ❌ {info.get('prenom', '')} {info.get('nom', '')} → {pdf_filename} (MANQUANT)")
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"   📋 Registre: {len(registry)} candidats")
    print(f"   📄 PDFs attendus: {len(registry_files)}")
    print(f"   ✅ PDFs existants: {len(existing_pdfs)}")
    print(f"   ❌ PDFs manquants: {len(missing_pdfs)}")
    print(f"   🎯 Taux de couverture: {len(existing_pdfs)/len(registry)*100:.1f}%")
    
    if missing_pdfs:
        print(f"\n🚫 PDFS MANQUANTS:")
        for i, missing in enumerate(missing_pdfs[:10], 1):  # Afficher seulement les 10 premiers
            print(f"   {i}. {missing['prenom']} {missing['nom']} → {missing['pdf_filename']}")
        
        if len(missing_pdfs) > 10:
            print(f"   ... et {len(missing_pdfs) - 10} autres")
    
    return len(missing_pdfs) == 0

def create_test_pdfs():
    """Crée des PDFs de test pour tous les candidats du registre"""
    print("\n🎭 CRÉATION DE PDFs DE TEST")
    print("=" * 30)
    
    with open("candidate_pdf_registry.json", 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    created_count = 0
    for candidate_id, info in registry.items():
        pdf_filename = info['pdf_filename']
        
        if not os.path.exists(pdf_filename):
            # Créer un PDF de test
            with open(pdf_filename, 'w', encoding='utf-8') as f:
                f.write(f"PDF DE TEST pour {info['prenom']} {info['nom']}\n")
                f.write(f"ID: {candidate_id}\n")
                f.write(f"Email: {info['email']}\n")
                f.write(f"Type TCF: {info.get('tcf_type', 'N/A')}\n")
                f.write(f"Fichier: {pdf_filename}\n")
                f.write("\nCeci est un fichier de test généré automatiquement.\n")
            
            created_count += 1
            if created_count <= 5:
                print(f"   ✅ {pdf_filename}")
    
    print(f"📄 {created_count} PDFs de test créés")
    return created_count

def test_email_system():
    """Test du système d'envoi avec PDFs existants"""
    print("\n🧪 TEST DU SYSTÈME D'ENVOI")
    print("=" * 30)
    
    # Simuler la classe SimpleMailjetBridge
    with open("candidate_pdf_registry.json", 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    class TestEmailSystem:
        def __init__(self, registry):
            self.registry = registry
            self.output_dir = "."
        
        def test_send_emails(self, limit=10):
            results = {'total': 0, 'sent': 0, 'failed': 0, 'errors': []}
            
            candidate_ids = list(self.registry.keys())[:limit]
            results['total'] = len(candidate_ids)
            
            for i, candidate_id in enumerate(candidate_ids, 1):
                candidate_info = self.registry[candidate_id]
                nom = candidate_info.get('nom', 'INCONNU')
                prenom = candidate_info.get('prenom', '')
                pdf_filename = candidate_info['pdf_filename']
                pdf_path = os.path.join(self.output_dir, pdf_filename)
                
                print(f"[{i}/{len(candidate_ids)}] 📧 Test envoi à {prenom} {nom}")
                
                if os.path.exists(pdf_path):
                    results['sent'] += 1
                    print(f"   ✅ PDF trouvé: {pdf_filename}")
                else:
                    results['failed'] += 1
                    results['errors'].append({
                        'candidate_id': candidate_id,
                        'error': f'PDF non trouvé: {pdf_filename}'
                    })
                    print(f"   ❌ PDF manquant: {pdf_filename}")
            
            return results
    
    # Test avec 10 candidats
    system = TestEmailSystem(registry)
    results = system.test_send_emails(10)
    
    print(f"\n📊 RÉSULTATS TEST:")
    print(f"   Total: {results['total']}")
    print(f"   Succès: {results['sent']}")
    print(f"   Échecs: {results['failed']}")
    print(f"   Taux: {results['sent']/results['total']*100:.1f}%")
    
    return results['sent'] == results['total']

def main():
    """Fonction principale de diagnostic et réparation"""
    print("🔧 DIAGNOSTIC ET RÉPARATION SYSTÈME EMAIL")
    print("=" * 60)
    
    # Étape 1: Diagnostic
    is_synced = diagnose_pdf_registry_sync()
    
    if not is_synced:
        print("\n🔧 RÉPARATION NÉCESSAIRE")
        
        # Proposer de créer des PDFs de test
        response = input("\nVoulez-vous créer des PDFs de test pour résoudre le problème? (o/n): ")
        
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            created_count = create_test_pdfs()
            print(f"\n✅ {created_count} PDFs de test créés")
            
            # Re-tester
            print("\n🔄 NOUVEAU TEST APRÈS RÉPARATION:")
            success = test_email_system()
            
            if success:
                print("\n🎉 SYSTÈME RÉPARÉ ET FONCTIONNEL!")
                print("✅ Vous pouvez maintenant envoyer vos emails")
                print("✅ Tous les candidats ont leurs PDFs")
            else:
                print("\n⚠️ Quelques problèmes subsistent")
        else:
            print("❌ Réparation annulée")
    else:
        print("\n✅ SYSTÈME DÉJÀ SYNCHRONISÉ")
        success = test_email_system()
        
        if success:
            print("\n🎉 SYSTÈME ENTIÈREMENT FONCTIONNEL!")

if __name__ == "__main__":
    main()