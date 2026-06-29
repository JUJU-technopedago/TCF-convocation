#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test du nouveau format d'email DELF/DALF
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mailjet_bridge import MailjetBridge

def test_email_format():
    """Test le nouveau format d'email sans authentification"""
    
    print("=" * 60)
    print("TEST DU NOUVEAU FORMAT D'EMAIL DELF/DALF")
    print("=" * 60)
    
    # Créer une instance sans authentification
    bridge = MailjetBridge(
        excel_path="candidats_pour_mailjet.xlsx",
        pdf_dir="output",
        sender_email="test@example.com",
        sender_name="Alliance Française Bruxelles Europe"
    )
    
    # Données de test pour un candidat DELF A1
    test_candidate_delf = {
        'nom': 'andersson',
        'prenom': 'erik',
        'matiere': 'DELF A1',
        'email': 'erik.andersson@email.com',
        'date_examen': '2025-08-14',
        'heure_debut': '09:00',
        'date_collective': '2025-08-14',
        'heure_collective': '09:00',
        'date_individuelle': '2025-08-14',
        'heure_individuelle': '14:30',
        'numero_candidat': '32002032261'
    }
    
    # Données de test pour un candidat DALF C1
    test_candidate_dalf = {
        'nom': 'martin',
        'prenom': 'sophie',
        'matiere': 'DALF C1',
        'email': 'sophie.martin@email.com',
        'date_examen': '2025-08-15',
        'heure_debut': '08:30',
        'date_collective': '2025-08-15',
        'heure_collective': '08:30',
        'date_individuelle': '2025-08-15',
        'heure_individuelle': '15:00',
        'numero_candidat': '32002033333'
    }
    
    print("\n1. TEST FORMAT DELF A1")
    print("-" * 40)
    
    try:
        subject, body_html, body_text = bridge._create_email_content(test_candidate_delf)
        
        print(f"✓ Sujet: {subject}")
        print(f"✓ Décodage HTML: {'✓' if 'd\\'examen' in subject else '✗'}")
        print(f"✓ Format nom: {'✓' if 'ANDERSSON' in body_html else '✗'}")
        print(f"✓ Type DELF: {'✓' if 'DELF A1' in body_html else '✗'}")
        print(f"✓ Date française: {'✓' if 'jeudi 14 août 2025' in body_html else '✗'}")
        print(f"✓ 30 minutes: {'✓' if '30 minutes avant' in body_html else '✗'}")
        print(f"✓ Couleur rouge: {'✓' if '#da002e' in body_html else '✗'}")
        print(f"✓ Épreuves séparées: {'✓' if 'ÉPREUVES COLLECTIVES' in body_html and 'ÉPREUVE INDIVIDUELLE' in body_html else '✗'}")
        
        # Afficher un extrait du contenu
        print("\nExtrait du contenu HTML:")
        lines = body_html.split('\n')
        for i, line in enumerate(lines):
            if 'Bonjour' in line or 'DELF' in line or 'ÉPREUVES COLLECTIVES' in line or '[IMPORTANT]' in line:
                print(f"  {line.strip()}")
                
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    print("\n2. TEST FORMAT DALF C1")
    print("-" * 40)
    
    try:
        subject, body_html, body_text = bridge._create_email_content(test_candidate_dalf)
        
        print(f"✓ Sujet: {subject}")
        print(f"✓ Format nom: {'✓' if 'MARTIN' in body_html else '✗'}")
        print(f"✓ Type DALF: {'✓' if 'DALF C1' in body_html else '✗'}")
        print(f"✓ Date française: {'✓' if 'vendredi 15 août 2025' in body_html else '✗'}")
        
        # Afficher un extrait du contenu
        print("\nExtrait du contenu HTML:")
        lines = body_html.split('\n')
        for i, line in enumerate(lines):
            if 'Bonjour' in line or 'DALF' in line:
                print(f"  {line.strip()}")
                
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    print("\n3. TEST VERSION TEXTE")
    print("-" * 40)
    
    try:
        subject, body_html, body_text = bridge._create_email_content(test_candidate_delf)
        
        print("Version texte (extrait):")
        lines = body_text.split('\n')
        for line in lines[:15]:  # Afficher les 15 premières lignes
            if line.strip():
                print(f"  {line}")
                
    except Exception as e:
        print(f"✗ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("✅ TEST DU NOUVEAU FORMAT TERMINÉ")
    print("=" * 60)

if __name__ == "__main__":
    test_email_format()
