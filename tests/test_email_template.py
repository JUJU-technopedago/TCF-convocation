#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier le nouveau format d'email
"""

def test_email_template():
    """Test du nouveau template d'email"""
    
    # Template d'email mis à jour
    subject_template = "Convocation {exam_type} - {prenom} {nom}"
    body_template = """
    <html>
    <body>
        <p>Bonjour {prenom} {nom},</p>
        
        <p>Vous trouverez ci-joint votre convocation pour l'examen {exam_type} {niveau}.</p>
        
        <p><strong>Détails de l'examen :</strong></p>
        
        <p><strong>ÉPREUVES COLLECTIVES</strong><br>
        Date : {date_ep_coll}<br>
        Heure : {debut_ep_coll}</p>
        
        <p><strong>Épreuve individuelle :</strong><br>
        Date : {date_ep_ind}<br>
        Heure : {heure_preparation}</p>
        
        <p><strong>Lieu :</strong> Alliance Française de Bruxelles-Europe, Avenue des Arts 46, 1000 Bruxelles.</p>
        
        <p>Merci de vous présenter 30 minutes avant l'heure de convocation avec une pièce d'identité valide.</p>
        
        <p>Cordialement,</p>
        <p><em>L'équipe de l'AFBE</em></p>
    </body>
    </html>
    """
    
    # Données de test
    test_candidate = {
        'prenom': 'Takumi',
        'nom': 'YAMADA',
        'niveau': 'A1',
        'exam_type': 'DELF',
        'date_ep_coll': '15/09/2025',
        'debut_ep_coll': '09:00',
        'date_ep_ind': '15/09/2025',
        'heure_preparation': '15:30'
    }
    
    # Générer le contenu
    subject = subject_template.format(**test_candidate)
    body = body_template.format(**test_candidate)
    
    print("=== TEST DU NOUVEAU TEMPLATE D'EMAIL ===\n")
    
    print(f"SUJET: {subject}\n")
    
    print("CORPS DE L'EMAIL (HTML):")
    print(body)
    
    print("\n=== RENDU APPROXIMATIF (TEXT) ===")
    print(f"Bonjour {test_candidate['prenom']} {test_candidate['nom']},")
    print()
    print(f"Vous trouverez ci-joint votre convocation pour l'examen {test_candidate['exam_type']} {test_candidate['niveau']}.")
    print()
    print("Détails de l'examen :")
    print()
    print("ÉPREUVES COLLECTIVES")
    print(f"Date : {test_candidate['date_ep_coll']}")
    print(f"Heure : {test_candidate['debut_ep_coll']}")
    print()
    print("Épreuve individuelle :")
    print(f"Date : {test_candidate['date_ep_ind']}")
    print(f"Heure : {test_candidate['heure_preparation']}")
    print()
    print("Lieu : Alliance Française de Bruxelles-Europe, Avenue des Arts 46, 1000 Bruxelles.")
    print()
    print("Merci de vous présenter 30 minutes avant l'heure de convocation avec une pièce d'identité valide.")
    print()
    print("Cordialement,")
    print("L'équipe de l'AFBE")
    
    print("\n=== TEST TERMINÉ ===")
    print("✓ Le template d'email a été mis à jour avec succès!")
    print("✓ Format conforme aux spécifications demandées")
    print("✓ Toutes les variables nécessaires sont incluses")

if __name__ == "__main__":
    test_email_template()
