#!/usr/bin/env python3
"""
Test des objets d'emails corrigés
"""

import sys
import types

# Patcher le module cryptography avant l'import
class MockFernet:
    def __init__(self, key): pass
    def encrypt(self, data): return b'mock'
    def decrypt(self, data): return b'mock'

mock_fernet = types.ModuleType('cryptography.fernet')
mock_fernet.Fernet = MockFernet
mock_fernet.Fernet.generate_key = lambda: b'key'
sys.modules['cryptography.fernet'] = mock_fernet

from mailjet_bridge import MailjetBridge

def test_email_subjects():
    bridge = MailjetBridge('JURYS FINAL TCF - Copie.xlsx', '.')
    
    print("� TEST URGENT - TOUS LES EMAILS DOIVENT DIRE TCF !")
    print("=" * 60)
    
    # Test pour un candidat ex-DELF B2 (doit maintenant dire TCF B2)
    test_candidate_delf = {
        'nom': 'MARTIN',
        'prenom': 'Pierre',
        'matiere': 'DELF B2',
        'date_ep_coll': '2025-10-20'
    }
    
    subject_delf, _, _ = bridge._create_email_content(test_candidate_delf)
    print(f"❌ Ex-DELF B2: {subject_delf}")
    
    # Test pour un candidat ex-DALF C1 (doit maintenant dire TCF C1)
    test_candidate_dalf = {
        'nom': 'DUPONT',
        'prenom': 'Marie',
        'matiere': 'DALF C1',
        'date_ep_coll': '2025-10-22'
    }
    
    subject_dalf, _, _ = bridge._create_email_content(test_candidate_dalf)
    print(f"❌ Ex-DALF C1: {subject_dalf}")
    
    # Test pour un candidat TCF CANADA
    test_candidate_tcf = {
        'nom': 'MARTINEZ-MONNIELLI',
        'prenom': 'Julien',
        'matiere': 'TCF CANADA',
        'tcf_type': 'TCF CANADA',
        'date_collective_format': 'le mercredi 16 octobre 2025'
    }
    
    subject_tcf, _, _ = bridge._create_email_content(test_candidate_tcf)
    print(f"✅ TCF CANADA: {subject_tcf}")
    
    print("=" * 60)
    print("🎯 RÉSULTAT: Tout doit maintenant dire 'TCF' !")
    print("Plus jamais de DELF ou DALF dans les objets !")
    
    # Vérification
    if 'DALF' in subject_delf or 'DELF' in subject_delf:
        print("❌ ERREUR: Il y a encore du DELF/DALF !")
    else:
        print("✅ PARFAIT: Plus de DELF/DALF dans les objets !")

if __name__ == "__main__":
    test_email_subjects()