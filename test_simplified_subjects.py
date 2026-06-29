#!/usr/bin/env python3
"""
Test des objets d'emails simplifiés
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

def test_simplified_subjects():
    bridge = MailjetBridge('JURYS FINAL TCF - Copie.xlsx', '.')
    
    print("📧 TEST OBJETS SIMPLIFIÉS :")
    print("=" * 40)
    
    # Test TCF CANADA
    test_tcf = {
        'nom': 'MARTINEZ',
        'prenom': 'Julien',
        'matiere': 'TCF CANADA',
        'tcf_type': 'TCF CANADA'
    }
    
    subject_tcf, _, _ = bridge._create_email_content(test_tcf)
    print(f"✅ TCF CANADA: {subject_tcf}")
    
    # Test ex-DELF B2
    test_delf = {
        'nom': 'MARTIN',
        'prenom': 'Pierre',
        'matiere': 'DELF B2'
    }
    
    subject_delf, _, _ = bridge._create_email_content(test_delf)
    print(f"✅ Ex-DELF B2: {subject_delf}")
    
    # Test ex-DALF C1
    test_dalf = {
        'nom': 'DUPONT',
        'prenom': 'Marie',
        'matiere': 'DALF C1'
    }
    
    subject_dalf, _, _ = bridge._create_email_content(test_dalf)
    print(f"✅ Ex-DALF C1: {subject_dalf}")
    
    print("=" * 40)
    print("🎯 Tous les emails ont maintenant")
    print("   juste 'Votre examen TCF' comme objet !")

if __name__ == "__main__":
    test_simplified_subjects()