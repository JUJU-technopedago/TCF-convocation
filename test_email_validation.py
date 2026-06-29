#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_email_validation_detailed():
    """Test détaillé de validation des emails sans dépendance cryptographie"""
    
    print("=== VALIDATION DÉTAILLÉE DES EMAILS TCF ===")
    print("=" * 50)
    
    try:
        from tcf_excel_processor import TCFExcelProcessor
        
        # 1. Charger les données TCF
        processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
        
        if not processor.load_tcf_data():
            print("❌ Erreur lors du chargement des données TCF")
            return False
        
        candidates = processor.get_all_candidates()
        print(f"✅ {len(candidates)} candidats chargés")
        
        # 2. Analyse détaillée des emails
        print(f"\n📧 ANALYSE DES ADRESSES EMAIL")
        print("-" * 50)
        
        email_stats = {
            'total': 0,
            'valides': 0,
            'invalides': 0,
            'manquants': 0,
            'doublons': 0,
            'suspects': 0
        }
        
        email_to_candidates = {}
        problematic_emails = []
        
        for candidate in candidates:
            email_stats['total'] += 1
            
            nom = candidate['nom']
            prenom = candidate['prenom']
            email = candidate.get('email', '').strip()
            tcf_type = candidate['tcf_type']
            jury = candidate['jury_name']
            
            # Identifier le candidat
            candidat_id = f"{prenom} {nom} ({tcf_type} - {jury})"
            
            if not email:
                email_stats['manquants'] += 1
                problematic_emails.append(f"❌ EMAIL MANQUANT: {candidat_id}")
                continue
            
            # Collecter pour analyse des doublons
            email_lower = email.lower()
            if email_lower not in email_to_candidates:
                email_to_candidates[email_lower] = []
            email_to_candidates[email_lower].append(candidat_id)
            
            # Validation de base
            if '@' not in email:
                email_stats['invalides'] += 1
                problematic_emails.append(f"❌ EMAIL INVALIDE (pas de @): {candidat_id} → {email}")
                continue
            
            # Vérification du domaine
            parts = email.split('@')
            if len(parts) != 2 or not parts[0] or not parts[1]:
                email_stats['invalides'] += 1
                problematic_emails.append(f"❌ EMAIL INVALIDE (format): {candidat_id} → {email}")
                continue
            
            domain = parts[1].lower()
            
            # Domaines suspects ou tests
            if domain in ['example.com', 'test.com', 'temp.com', 'fake.com']:
                email_stats['suspects'] += 1
                problematic_emails.append(f"⚠️  EMAIL SUSPECT (domaine test): {candidat_id} → {email}")
            elif domain.endswith('.alliancefr.be'):
                email_stats['suspects'] += 1
                problematic_emails.append(f"⚠️  EMAIL INTERNE AF: {candidat_id} → {email}")
            elif not any(domain.endswith(ext) for ext in ['.com', '.fr', '.be', '.org', '.net', '.edu', '.gov', '.co.uk', '.de', '.it', '.es']):
                email_stats['suspects'] += 1
                problematic_emails.append(f"⚠️  DOMAINE INHABITUEL: {candidat_id} → {email}")
            else:
                email_stats['valides'] += 1
        
        # 3. Analyse des doublons
        print(f"\n🔍 ANALYSE DES DOUBLONS")
        print("-" * 50)
        
        duplicates = {email: candidates for email, candidates in email_to_candidates.items() if len(candidates) > 1}
        email_stats['doublons'] = len(duplicates)
        
        if duplicates:
            print(f"❌ {len(duplicates)} adresses email en doublon détectées:")
            for email, candidate_list in duplicates.items():
                print(f"\n📧 {email} ({len(candidate_list)} candidats):")
                for candidat in candidate_list:
                    print(f"    • {candidat}")
                
                # Suggestions
                if len(candidate_list) > 1:
                    print(f"  💡 SUGGESTION: Vérifier si c'est le même candidat ou corriger les emails")
        else:
            print("✅ Aucun doublon détecté")
        
        # 4. Résumé statistique
        print(f"\n📊 STATISTIQUES EMAILS")
        print("-" * 50)
        print(f"Total candidats: {email_stats['total']}")
        print(f"✅ Emails valides: {email_stats['valides']} ({email_stats['valides']/email_stats['total']*100:.1f}%)")
        print(f"❌ Emails invalides: {email_stats['invalides']} ({email_stats['invalides']/email_stats['total']*100:.1f}%)")
        print(f"🚫 Emails manquants: {email_stats['manquants']} ({email_stats['manquants']/email_stats['total']*100:.1f}%)")
        print(f"⚠️  Emails suspects: {email_stats['suspects']} ({email_stats['suspects']/email_stats['total']*100:.1f}%)")
        print(f"🔄 Emails en doublon: {email_stats['doublons']}")
        
        # 5. Liste des problèmes
        if problematic_emails:
            print(f"\n⚠️  PROBLÈMES DÉTECTÉS ({len(problematic_emails)}):")
            print("-" * 50)
            for problem in problematic_emails[:15]:  # Afficher max 15 problèmes
                print(f"  {problem}")
            if len(problematic_emails) > 15:
                print(f"  ... et {len(problematic_emails) - 15} autres problèmes")
        
        # 6. Vérification correspondance nom/email
        print(f"\n🎯 VÉRIFICATION CORRESPONDANCE NOM/EMAIL")
        print("-" * 50)
        
        correspondance_issues = []
        for candidate in candidates[:10]:  # Tester les 10 premiers
            nom = candidate['nom'].lower()
            prenom = candidate['prenom'].lower()
            email = candidate.get('email', '').lower()
            
            if email:
                # Vérifier si le nom ou prénom apparaît dans l'email
                nom_in_email = any(part in email for part in nom.split() if len(part) > 2)
                prenom_in_email = any(part in email for part in prenom.split() if len(part) > 2)
                
                if not nom_in_email and not prenom_in_email:
                    correspondance_issues.append(f"⚠️  {candidate['prenom']} {candidate['nom']} → {email} (aucune correspondance nom/email)")
        
        if correspondance_issues:
            print(f"Problèmes de correspondance nom/email détectés:")
            for issue in correspondance_issues:
                print(f"  {issue}")
        else:
            print("✅ Correspondances nom/email semblent correctes (échantillon testé)")
        
        # 7. Conclusion
        print(f"\n" + "=" * 60)
        print("🏁 CONCLUSION")
        print("=" * 60)
        
        critical_issues = email_stats['invalides'] + email_stats['manquants'] + email_stats['doublons']
        
        if critical_issues == 0:
            print("🎉 EXCELLENT: Tous les emails sont prêts pour l'envoi!")
            print("✅ Aucun problème critique détecté")
            return True
        else:
            print(f"⚠️  ATTENTION: {critical_issues} problèmes critiques détectés")
            print("❌ Il faut corriger ces problèmes avant d'envoyer les emails")
            
            print(f"\n🔧 ACTIONS RECOMMANDÉES:")
            if email_stats['manquants'] > 0:
                print(f"  • Obtenir les emails manquants ({email_stats['manquants']} candidats)")
            if email_stats['invalides'] > 0:
                print(f"  • Corriger les emails invalides ({email_stats['invalides']} candidats)")
            if email_stats['doublons'] > 0:
                print(f"  • Résoudre les doublons d'emails ({email_stats['doublons']} adresses)")
            
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LANCEMENT DE LA VALIDATION DES EMAILS TCF")
    test_email_validation_detailed()