#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valide les emails du fichier candidats_pour_mailjet.xlsx pour Mailjet
Identifie et corrige les problèmes d'adresses email invalides
"""

import pandas as pd
import re
import os
from datetime import datetime

class EmailValidator:
    def __init__(self, excel_path):
        """
        Initialise le validateur d'emails
        
        Args:
            excel_path (str): Chemin vers le fichier Excel des candidats
        """
        self.excel_path = excel_path
        self.valid_emails = []
        self.invalid_emails = []
        self.corrected_emails = []
        
    def validate_email_format(self, email):
        """
        Valide le format d'une adresse email
        
        Args:
            email (str): Adresse email à valider
            
        Returns:
            bool: True si l'email est valide
        """
        if not email or pd.isna(email):
            return False
            
        email = str(email).strip()
        
        # Pattern regex pour validation email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        return re.match(pattern, email) is not None
    
    def clean_email(self, email):
        """
        Nettoie et corrige une adresse email
        
        Args:
            email (str): Email à nettoyer
            
        Returns:
            str: Email nettoyé ou None si non récupérable
        """
        if not email or pd.isna(email):
            return None
            
        email = str(email).strip().lower()
        
        # Corrections courantes
        corrections = {
            'gmial.com': 'gmail.com',
            'gmai.com': 'gmail.com',
            'gmail.co': 'gmail.com',
            'yahooo.com': 'yahoo.com',
            'yahoo.co': 'yahoo.com',
            'hotmial.com': 'hotmail.com',
            'hotmai.com': 'hotmail.com',
            'outlok.com': 'outlook.com',
            'outloo.com': 'outlook.com'
        }
        
        for wrong, correct in corrections.items():
            if wrong in email:
                email = email.replace(wrong, correct)
        
        # Supprimer les espaces et caractères invalides
        email = re.sub(r'\s+', '', email)
        
        # Vérifier si maintenant valide
        if self.validate_email_format(email):
            return email
            
        return None
    
    def validate_all_emails(self):
        """
        Valide tous les emails du fichier Excel
        
        Returns:
            dict: Résultats de la validation
        """
        print(f"📧 Validation des emails dans {self.excel_path}")
        
        try:
            # Charger le fichier Excel
            df = pd.read_excel(self.excel_path, engine='openpyxl')
            
            results = {
                'total_candidates': len(df),
                'valid_emails': [],
                'invalid_emails': [],
                'corrected_emails': [],
                'missing_emails': [],
                'duplicate_emails': [],
                'summary': {}
            }
            
            seen_emails = set()
            
            for index, row in df.iterrows():
                nom = str(row.get('nom', ''))
                prenom = str(row.get('prenom', ''))
                email = row.get('email', '')
                numero = str(row.get('numero_candidat', ''))
                
                candidate_info = {
                    'index': index + 1,
                    'nom': nom,
                    'prenom': prenom,
                    'numero_candidat': numero,
                    'email_original': str(email) if email else ''
                }
                
                # Vérifier si email manquant
                if not email or pd.isna(email) or str(email).strip() == '':
                    results['missing_emails'].append(candidate_info)
                    continue
                
                email_str = str(email).strip()
                
                # Vérifier si email valide
                if self.validate_email_format(email_str):
                    # Vérifier les doublons
                    if email_str.lower() in seen_emails:
                        candidate_info['email_clean'] = email_str.lower()
                        results['duplicate_emails'].append(candidate_info)
                    else:
                        seen_emails.add(email_str.lower())
                        candidate_info['email_clean'] = email_str
                        results['valid_emails'].append(candidate_info)
                else:
                    # Essayer de corriger l'email
                    corrected_email = self.clean_email(email_str)
                    
                    if corrected_email and self.validate_email_format(corrected_email):
                        if corrected_email in seen_emails:
                            candidate_info['email_clean'] = corrected_email
                            candidate_info['correction'] = f"{email_str} → {corrected_email}"
                            results['duplicate_emails'].append(candidate_info)
                        else:
                            seen_emails.add(corrected_email)
                            candidate_info['email_clean'] = corrected_email
                            candidate_info['correction'] = f"{email_str} → {corrected_email}"
                            results['corrected_emails'].append(candidate_info)
                    else:
                        candidate_info['email_clean'] = None
                        results['invalid_emails'].append(candidate_info)
            
            # Résumé
            results['summary'] = {
                'total': results['total_candidates'],
                'valid': len(results['valid_emails']),
                'corrected': len(results['corrected_emails']),
                'invalid': len(results['invalid_emails']),
                'missing': len(results['missing_emails']),
                'duplicates': len(results['duplicate_emails']),
                'sendable': len(results['valid_emails']) + len(results['corrected_emails'])
            }
            
            return results
            
        except Exception as e:
            raise Exception(f"Erreur lors de la validation: {e}")
    
    def create_corrected_file(self, results, output_path="candidats_emails_corriges.xlsx"):
        """
        Crée un fichier Excel avec les emails corrigés
        
        Args:
            results (dict): Résultats de la validation
            output_path (str): Chemin de sortie
        """
        try:
            # Charger le fichier original
            df = pd.read_excel(self.excel_path, engine='openpyxl')
            
            # Créer un mapping des corrections
            corrections = {}
            
            # Ajouter les emails valides
            for item in results['valid_emails']:
                corrections[item['index'] - 1] = item['email_clean']
            
            # Ajouter les emails corrigés
            for item in results['corrected_emails']:
                corrections[item['index'] - 1] = item['email_clean']
            
            # Appliquer les corrections
            for index, corrected_email in corrections.items():
                df.at[index, 'email'] = corrected_email
            
            # Marquer les emails invalides
            for item in results['invalid_emails']:
                df.at[item['index'] - 1, 'email'] = f"INVALIDE: {item['email_original']}"
            
            # Marquer les emails manquants
            for item in results['missing_emails']:
                df.at[item['index'] - 1, 'email'] = "EMAIL_MANQUANT"
            
            # Sauvegarder
            df.to_excel(output_path, index=False, engine='openpyxl')
            
            print(f"✅ Fichier corrigé créé: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Erreur lors de la création du fichier corrigé: {e}")
            return None
    
    def create_sendable_file(self, results, output_path="candidats_emails_valides.xlsx"):
        """
        Crée un fichier Excel avec seulement les candidats aux emails valides
        
        Args:
            results (dict): Résultats de la validation
            output_path (str): Chemin de sortie
        """
        try:
            # Charger le fichier original
            df = pd.read_excel(self.excel_path, engine='openpyxl')
            
            # Indices des candidats avec emails valides
            valid_indices = []
            
            # Ajouter les emails valides
            for item in results['valid_emails']:
                valid_indices.append(item['index'] - 1)
            
            # Ajouter les emails corrigés
            for item in results['corrected_emails']:
                valid_indices.append(item['index'] - 1)
                # Appliquer la correction
                df.at[item['index'] - 1, 'email'] = item['email_clean']
            
            # Filtrer le DataFrame
            df_valid = df.iloc[valid_indices].copy()
            
            # Sauvegarder
            df_valid.to_excel(output_path, index=False, engine='openpyxl')
            
            print(f"✅ Fichier des emails valides créé: {output_path}")
            print(f"📊 {len(df_valid)} candidats avec emails valides")
            return output_path
            
        except Exception as e:
            print(f"❌ Erreur lors de la création du fichier valide: {e}")
            return None
    
    def print_validation_report(self, results):
        """Affiche un rapport détaillé de la validation"""
        print(f"\n" + "="*70)
        print(f"📊 RAPPORT DE VALIDATION DES EMAILS")
        print(f"="*70)
        
        summary = results['summary']
        print(f"📁 Fichier analysé: {os.path.basename(self.excel_path)}")
        print(f"📅 Date de validation: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"👥 Total candidats: {summary['total']}")
        print(f"✅ Emails valides: {summary['valid']}")
        print(f"🔧 Emails corrigés: {summary['corrected']}")
        print(f"❌ Emails invalides: {summary['invalid']}")
        print(f"❓ Emails manquants: {summary['missing']}")
        print(f"🔄 Emails dupliqués: {summary['duplicates']}")
        print(f"📧 Emails envoyables: {summary['sendable']}")
        
        # Pourcentage de succès
        if summary['total'] > 0:
            success_rate = (summary['sendable'] / summary['total']) * 100
            print(f"📈 Taux de succès: {success_rate:.1f}%")
        
        # Détails des corrections
        if results['corrected_emails']:
            print(f"\n🔧 CORRECTIONS APPLIQUÉES:")
            for item in results['corrected_emails'][:10]:
                print(f"  • {item['nom']} {item['prenom']}: {item['correction']}")
            if len(results['corrected_emails']) > 10:
                print(f"  ... et {len(results['corrected_emails']) - 10} autres corrections")
        
        # Emails invalides
        if results['invalid_emails']:
            print(f"\n❌ EMAILS INVALIDES:")
            for item in results['invalid_emails'][:10]:
                print(f"  • {item['nom']} {item['prenom']}: '{item['email_original']}'")
            if len(results['invalid_emails']) > 10:
                print(f"  ... et {len(results['invalid_emails']) - 10} autres emails invalides")
        
        # Emails manquants
        if results['missing_emails']:
            print(f"\n❓ EMAILS MANQUANTS:")
            for item in results['missing_emails'][:10]:
                print(f"  • {item['nom']} {item['prenom']} ({item['numero_candidat']})")
            if len(results['missing_emails']) > 10:
                print(f"  ... et {len(results['missing_emails']) - 10} autres emails manquants")
        
        print(f"="*70)

def main():
    """Fonction principale"""
    excel_file = "candidats_pour_mailjet.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ Erreur: Le fichier {excel_file} n'existe pas.")
        return
    
    try:
        # Créer le validateur
        validator = EmailValidator(excel_file)
        
        # Valider tous les emails
        results = validator.validate_all_emails()
        
        # Afficher le rapport
        validator.print_validation_report(results)
        
        # Créer les fichiers corrigés
        corrected_file = validator.create_corrected_file(results)
        sendable_file = validator.create_sendable_file(results)
        
        print(f"\n💡 RECOMMANDATIONS POUR MAILJET:")
        print(f"   1. Utilisez le fichier '{sendable_file}' pour l'envoi Mailjet")
        print(f"   2. Ce fichier contient {results['summary']['sendable']} candidats avec emails valides")
        print(f"   3. Contactez manuellement les {results['summary']['invalid'] + results['summary']['missing']} candidats sans email valide")
        
        if results['summary']['sendable'] > 0:
            print(f"\n✅ Prêt pour l'envoi Mailjet avec {results['summary']['sendable']} candidats !")
        else:
            print(f"\n⚠️  Aucun email valide trouvé. Vérifiez vos données.")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
