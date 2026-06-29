#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Ajouter le répertoire courant au path pour importer les modules locaux
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_email_convocation_matching():
    """Test pour vérifier que les bonnes convocations sont envoyées aux bonnes adresses email"""
    
    print("=== TEST CORRESPONDANCE EMAIL <-> CONVOCATION ===")
    print("=" * 60)
    
    try:
        from tcf_excel_processor import TCFExcelProcessor
        from mailjet_bridge import MailjetEmailSender
        
        # 1. Charger les données TCF
        print("1. Chargement des données Excel TCF...")
        processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
        
        if not processor.load_tcf_data():
            print("❌ Erreur lors du chargement des données TCF")
            return False
        
        # 2. Obtenir tous les candidats
        candidates = processor.get_all_candidates()
        if not candidates:
            print("❌ Aucun candidat trouvé")
            return False
        
        print(f"✅ {len(candidates)} candidats trouvés")
        
        # 3. Créer une instance du sender email (sans vraies clés API)
        sender = MailjetEmailSender(api_key="test", secret_key="test")
        
        # 4. Tester quelques candidats représentatifs
        test_results = []
        test_candidates = candidates[:5]  # Prendre les 5 premiers pour le test
        
        print(f"\n2. Test de correspondance pour {len(test_candidates)} candidats...")
        print("-" * 60)
        
        for i, candidate in enumerate(test_candidates, 1):
            print(f"\n--- TEST {i}: {candidate['prenom']} {candidate['nom']} ---")
            
            # Informations du candidat
            nom = candidate['nom']
            prenom = candidate['prenom']
            email = candidate['email']
            tcf_type = candidate['tcf_type']
            date_examen = candidate['date_examen']
            
            print(f"📧 Email destinataire: {email}")
            print(f"📋 Type TCF: {tcf_type}")
            print(f"📅 Date examen: {date_examen}")
            
            # Générer le contenu email
            try:
                email_content = sender._create_email_content(candidate)
                
                # Vérifications de correspondance
                checks = {
                    'nom_in_html': nom.upper() in email_content['html_content'].upper(),
                    'prenom_in_html': prenom.upper() in email_content['html_content'].upper(),
                    'nom_in_text': nom.upper() in email_content['text_content'].upper(),
                    'prenom_in_text': prenom.upper() in email_content['text_content'].upper(),
                    'tcf_in_subject': 'TCF' in email_content['subject'],
                    'tcf_in_html': 'TCF' in email_content['html_content'],
                    'tcf_in_text': 'TCF' in email_content['text_content'],
                    'date_in_html': date_examen in email_content['html_content'] if date_examen else True,
                    'date_in_text': date_examen in email_content['text_content'] if date_examen else True,
                    'mailto_in_html': 'mailto:examens@alliancefr.be' in email_content['html_content'],
                    'contact_in_text': 'examens@alliancefr.be' in email_content['text_content']
                }
                
                # Résultats
                all_checks_passed = all(checks.values())
                
                print(f"✉️  Sujet: {email_content['subject']}")
                print(f"📝 Vérifications:")
                print(f"   ✅ Nom/Prénom dans HTML: {checks['nom_in_html'] and checks['prenom_in_html']}")
                print(f"   ✅ Nom/Prénom dans TEXTE: {checks['nom_in_text'] and checks['prenom_in_text']}")
                print(f"   ✅ TCF dans sujet: {checks['tcf_in_subject']}")
                print(f"   ✅ TCF dans contenu: {checks['tcf_in_html'] and checks['tcf_in_text']}")
                print(f"   ✅ Date examen dans contenu: {checks['date_in_html'] and checks['date_in_text']}")
                print(f"   ✅ Lien contact présent: {checks['mailto_in_html'] and checks['contact_in_text']}")
                
                if all_checks_passed:
                    print("   🎯 CORRESPONDANCE PARFAITE!")
                    status = "✅ SUCCÈS"
                else:
                    print("   ⚠️  Problèmes détectés!")
                    status = "❌ ÉCHEC"
                    
                test_results.append({
                    'candidat': f"{prenom} {nom}",
                    'email': email,
                    'tcf_type': tcf_type,
                    'status': status,
                    'all_checks': all_checks_passed,
                    'checks': checks
                })
                
            except Exception as e:
                print(f"❌ Erreur lors de la génération de l'email: {e}")
                test_results.append({
                    'candidat': f"{prenom} {nom}",
                    'email': email,
                    'tcf_type': tcf_type,
                    'status': "❌ ERREUR",
                    'all_checks': False,
                    'error': str(e)
                })
        
        # 5. Résumé des résultats
        print(f"\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS DE CORRESPONDANCE")
        print("=" * 60)
        
        success_count = sum(1 for result in test_results if result['all_checks'])
        
        print(f"Total candidats testés: {len(test_results)}")
        print(f"Correspondances parfaites: {success_count}")
        print(f"Problèmes détectés: {len(test_results) - success_count}")
        print(f"Taux de succès: {success_count/len(test_results)*100:.1f}%")
        
        print(f"\n📋 Détail des résultats:")
        for result in test_results:
            print(f"  {result['status']} {result['candidat']} ({result['email']}) - {result['tcf_type']}")
        
        # 6. Vérification spécifique des emails
        print(f"\n" + "=" * 60)
        print("🔍 VÉRIFICATION SPÉCIFIQUE DES ADRESSES EMAIL")
        print("=" * 60)
        
        email_issues = []
        for candidate in candidates:
            email = candidate.get('email', '').strip()
            if not email:
                email_issues.append(f"❌ {candidate['prenom']} {candidate['nom']}: Email manquant")
            elif '@' not in email:
                email_issues.append(f"❌ {candidate['prenom']} {candidate['nom']}: Email invalide '{email}'")
            elif not email.endswith(('.com', '.fr', '.be', '.org', '.net', '.edu')):
                email_issues.append(f"⚠️  {candidate['prenom']} {candidate['nom']}: Email suspect '{email}'")
        
        if email_issues:
            print(f"Problèmes d'email détectés ({len(email_issues)}):")
            for issue in email_issues[:10]:  # Afficher max 10 problèmes
                print(f"  {issue}")
            if len(email_issues) > 10:
                print(f"  ... et {len(email_issues) - 10} autres problèmes")
        else:
            print("✅ Toutes les adresses email semblent valides")
        
        # Résultat final
        if success_count == len(test_results) and not email_issues:
            print(f"\n🎉 SUCCÈS COMPLET: Toutes les correspondances sont correctes!")
            return True
        else:
            print(f"\n⚠️  ATTENTION: Des problèmes ont été détectés")
            return False
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Vérifiez que tous les modules nécessaires sont disponibles")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def test_email_uniqueness():
    """Test pour vérifier l'unicité des adresses email"""
    
    print(f"\n" + "=" * 60)
    print("🔄 TEST D'UNICITÉ DES ADRESSES EMAIL")
    print("=" * 60)
    
    try:
        from tcf_excel_processor import TCFExcelProcessor
        
        processor = TCFExcelProcessor("JURYS FINAL TCF.xlsx")
        if not processor.load_tcf_data():
            return False
        
        candidates = processor.get_all_candidates()
        
        # Collecter toutes les adresses email
        emails = []
        email_to_candidates = {}
        
        for candidate in candidates:
            email = candidate.get('email', '').strip().lower()
            if email:
                emails.append(email)
                if email not in email_to_candidates:
                    email_to_candidates[email] = []
                email_to_candidates[email].append(f"{candidate['prenom']} {candidate['nom']}")
        
        # Vérifier les doublons
        duplicates = {email: names for email, names in email_to_candidates.items() if len(names) > 1}
        
        print(f"Total emails collectés: {len(emails)}")
        print(f"Emails uniques: {len(set(emails))}")
        print(f"Doublons détectés: {len(duplicates)}")
        
        if duplicates:
            print(f"\n⚠️  DOUBLONS D'ADRESSES EMAIL:")
            for email, names in duplicates.items():
                print(f"  📧 {email}: {', '.join(names)}")
            return False
        else:
            print(f"\n✅ Toutes les adresses email sont uniques")
            return True
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LANCEMENT DES TESTS DE CORRESPONDANCE EMAIL/CONVOCATION")
    
    # Test 1: Correspondance email <-> convocation
    success1 = test_email_convocation_matching()
    
    # Test 2: Unicité des emails
    success2 = test_email_uniqueness()
    
    print(f"\n" + "=" * 80)
    print("🏁 RÉSULTATS FINAUX")
    print("=" * 80)
    
    if success1 and success2:
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        print("✅ Les bonnes convocations seront envoyées aux bonnes adresses")
    else:
        print("⚠️  DES PROBLÈMES ONT ÉTÉ DÉTECTÉS")
        print("❌ Vérifiez les erreurs ci-dessus avant d'envoyer les emails")