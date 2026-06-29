#!/usr/bin/env python3
"""
Test de l'hyperlien mailto ajouté
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

def test_mailto_link():
    bridge = MailjetBridge('JURYS FINAL TCF - Copie.xlsx', '.')
    
    # Test avec un candidat TCF
    test_candidate = {
        'nom': 'MARTINEZ',
        'prenom': 'Julien',
        'matiere': 'TCF CANADA',
        'tcf_type': 'TCF CANADA'
    }
    
    subject, body_html, body_text = bridge._create_email_content(test_candidate)
    
    print("📧 VÉRIFICATION HYPERLIEN MAILTO :")
    print("=" * 50)
    
    # Vérifier version HTML
    if 'mailto:examens@alliancefr.be' in body_html:
        print("✅ Hyperlien mailto présent dans HTML")
    else:
        print("❌ Hyperlien mailto manquant dans HTML")
    
    # Vérifier version texte
    if 'examens@alliancefr.be' in body_text:
        print("✅ Email présent dans version texte")
    else:
        print("❌ Email manquant dans version texte")
    
    # Extraire et afficher la ligne concernée
    print("\n📋 EXTRAITS :")
    
    # HTML
    import re
    if 'En cas de question' in body_html:
        match = re.search(r'<p>En cas de question[^<]*<a[^>]*>[^<]*</a>[^<]*</p>', body_html)
        if match:
            print(f"HTML: {match.group()}")
    
    # Texte
    if 'En cas de question' in body_text:
        lines = body_text.split('\n')
        for line in lines:
            if 'En cas de question' in line:
                print(f"TEXTE: {line.strip()}")
                break
    
    print("=" * 50)
    print("🎯 L'hyperlien mailto:examens@alliancefr.be doit être présent !")

if __name__ == "__main__":
    test_mailto_link()