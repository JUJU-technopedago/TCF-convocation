#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Ajouter le répertoire courant au path pour importer les modules locaux
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mailjet_bridge import MailjetEmailSender

def test_tcf_email_with_mailto():
    """Test que les emails TCF contiennent bien les liens mailto"""
    
    # Données de test pour un candidat TCF
    test_data = {
        'nom': 'Dupont',
        'prenom': 'Marie',
        'email': 'marie.dupont@example.com',
        'matiere': 'TCF CANADA',
        'date_examen': '2024-01-15',
        'heure_debut': '14:00'
    }
    
    # Créer une instance du sender
    sender = MailjetEmailSender(api_key="test", secret_key="test")
    
    # Générer le contenu email
    email_content = sender._create_email_content(test_data)
    
    print("=== Test du contenu email TCF avec mailto ===")
    print(f"Sujet: {email_content['subject']}")
    print("\n=== Version HTML ===")
    print(email_content['html_content'])
    print("\n=== Version TEXTE ===")
    print(email_content['text_content'])
    
    # Vérifier la présence des liens mailto
    html_has_mailto = 'mailto:examens@alliancefr.be' in email_content['html_content']
    text_has_mailto = 'examens@alliancefr.be' in email_content['text_content']
    
    print(f"\n=== Résultats ===")
    print(f"Version HTML contient mailto: {html_has_mailto}")
    print(f"Version TEXTE contient email: {text_has_mailto}")
    
    if html_has_mailto and text_has_mailto:
        print("✅ SUCCESS: Les liens mailto sont présents dans les deux versions!")
    else:
        print("❌ FAIL: Les liens mailto sont manquants")
        
    return html_has_mailto and text_has_mailto

if __name__ == "__main__":
    test_tcf_email_with_mailto()