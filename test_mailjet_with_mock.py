#!/usr/bin/env python3
"""
Script de contournement pour le problème cryptography
Remplace temporairement les imports cryptography pour permettre l'utilisation du mailjet_bridge
"""

import sys
import os

# Ajouter un module factice pour cryptography avant l'import
class MockFernet:
    def __init__(self, key):
        self.key = key
    
    def encrypt(self, data):
        return b"mock_encrypted_" + data
    
    def decrypt(self, data):
        if data.startswith(b"mock_encrypted_"):
            return data[15:]  # Retirer le préfixe mock
        return data

class MockCryptography:
    @staticmethod
    def generate_key():
        return b"mock_key_for_testing_purposes_32b"

# Patcher le module cryptography avant l'import
if 'cryptography.fernet' not in sys.modules:
    # Créer un module factice
    import types
    mock_fernet = types.ModuleType('cryptography.fernet')
    mock_fernet.Fernet = MockFernet
    mock_fernet.Fernet.generate_key = MockCryptography.generate_key
    sys.modules['cryptography.fernet'] = mock_fernet

# Maintenant on peut importer le bridge
from mailjet_bridge import MailjetBridge
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    excel_file = 'juries_20250919_162205.xlsx'
    
    print("🔧 Test avec contournement cryptography")
    
    try:
        bridge = MailjetBridge(excel_file)
        data = bridge._load_excel_data()
        
        print(f"✅ Chargement réussi: {len(data)} candidats")
        
        if len(data) > 0:
            print("Colonnes:", list(data.columns))
            print("Premiers emails:", data['email'].head(3).tolist())
            
            # Test de la méthode d'envoi (sans vraiment envoyer)
            print("\\n📧 Test de préparation d'emails:")
            for i, row in data.head(2).iterrows():
                email_content = bridge._create_email_content(row)
                print(f"Email pour {row['prenom']} {row['nom']}:")
                print(email_content[:100] + "...")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()