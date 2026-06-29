#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de lecture des emails depuis le fichier Excel TCF
"""

from tcf_excel_processor import TCFExcelProcessor

# Charger les données
processor = TCFExcelProcessor('JURYS FINAL TCF 11-18.xlsx')
processor.load_tcf_data()

# Vérifier les emails
candidates = processor.get_all_candidates()
print(f"\n{'='*80}")
print(f"TEST DE LECTURE DES EMAILS")
print(f"{'='*80}\n")

total = len(candidates)
with_email = sum(1 for c in candidates if c.get('email') and '@' in c.get('email', ''))
without_email = total - with_email

print(f"Total candidats: {total}")
print(f"Avec email valide: {with_email}")
print(f"Sans email valide: {without_email}")
print(f"\nTaux de réussite: {(with_email/total*100):.1f}%")

print(f"\n{'='*80}")
print(f"ÉCHANTILLON DE CANDIDATS:")
print(f"{'='*80}\n")

# Afficher les 10 premiers candidats
for i, candidate in enumerate(candidates[:10], 1):
    nom = candidate.get('nom', 'N/A')
    prenom = candidate.get('prenom', 'N/A')
    email = candidate.get('email', 'N/A')
    tcf_type = candidate.get('tcf_type', 'N/A')
    
    email_status = "✅" if email and '@' in email else "❌"
    
    print(f"{i}. {prenom} {nom}")
    print(f"   Type: {tcf_type}")
    print(f"   Email: {email_status} {email}")
    print()

# Afficher les candidats SANS email
print(f"\n{'='*80}")
print(f"CANDIDATS SANS EMAIL (tous):")
print(f"{'='*80}\n")

no_email_candidates = [c for c in candidates if not c.get('email') or '@' not in c.get('email', '')]
for i, candidate in enumerate(no_email_candidates, 1):
    nom = candidate.get('nom', 'N/A')
    prenom = candidate.get('prenom', 'N/A')
    tcf_type = candidate.get('tcf_type', 'N/A')
    
    print(f"{i}. {prenom} {nom} ({tcf_type})")
