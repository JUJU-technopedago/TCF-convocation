#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérifie les PDF manquants pour les candidats des jurys
Identifie quels PDF doivent être générés avant l'envoi Mailjet
"""

import os
import pandas as pd
from datetime import datetime
import re

class PDFChecker:
    def __init__(self, excel_path, pdf_dir):
        """
        Initialise le vérificateur de PDF
        
        Args:
            excel_path (str): Chemin vers le fichier Excel des candidats
            pdf_dir (str): Répertoire des PDF
        """
        self.excel_path = excel_path
        self.pdf_dir = pdf_dir
        self.missing_pdfs = []
        self.found_pdfs = []
        
    def clean_filename(self, text):
        """Nettoie un texte pour créer un nom de fichier valide"""
        if not text:
            return ""
        
        # Remplacer les caractères spéciaux
        text = str(text).strip()
        
        # Remplacements spécifiques pour les caractères accentués
        replacements = {
            'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a', 'ã': 'a',
            'é': 'e', 'è': 'e', 'ë': 'e', 'ê': 'e',
            'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i',
            'ó': 'o', 'ò': 'o', 'ö': 'o', 'ô': 'o', 'õ': 'o',
            'ú': 'u', 'ù': 'u', 'ü': 'u', 'û': 'u',
            'ç': 'c', 'ñ': 'n',
            'Á': 'A', 'À': 'A', 'Ä': 'A', 'Â': 'A', 'Ã': 'A',
            'É': 'E', 'È': 'E', 'Ë': 'E', 'Ê': 'E',
            'Í': 'I', 'Ì': 'I', 'Ï': 'I', 'Î': 'I',
            'Ó': 'O', 'Ò': 'O', 'Ö': 'O', 'Ô': 'O', 'Õ': 'O',
            'Ú': 'U', 'Ù': 'U', 'Ü': 'U', 'Û': 'U',
            'Ç': 'C', 'Ñ': 'N'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Remplacer les espaces et caractères spéciaux par des underscores
        text = re.sub(r'[^\w\-_.]', '_', text)
        
        # Supprimer les underscores multiples
        text = re.sub(r'_+', '_', text)
        
        # Supprimer les underscores en début et fin
        text = text.strip('_')
        
        return text
    
    def find_pdf_patterns(self, candidate_data):
        """
        Génère tous les patterns possibles pour un candidat
        
        Args:
            candidate_data (dict): Données du candidat
            
        Returns:
            list: Liste des noms de fichiers possibles
        """
        nom = str(candidate_data.get('nom', ''))
        prenom = str(candidate_data.get('prenom', ''))
        numero = str(candidate_data.get('numero_candidat', ''))
        
        # Nettoyer les noms
        safe_nom = self.clean_filename(nom)
        safe_prenom = self.clean_filename(prenom)
        
        # Patterns possibles
        patterns = [
            f"convocation_{safe_nom}_{safe_prenom}_{numero}.pdf",
            f"convocation_{safe_nom}_{safe_prenom}.pdf",
            f"{safe_nom}_{safe_prenom}_{numero}.pdf",
            f"{safe_nom}_{safe_prenom}.pdf",
            f"convocation_{numero}.pdf",
            f"{numero}.pdf"
        ]
        
        # Ajouter des variantes avec espaces remplacés par des tirets
        nom_dash = nom.replace(' ', '-')
        prenom_dash = prenom.replace(' ', '-')
        safe_nom_dash = self.clean_filename(nom_dash)
        safe_prenom_dash = self.clean_filename(prenom_dash)
        
        patterns.extend([
            f"convocation_{safe_nom_dash}_{safe_prenom_dash}_{numero}.pdf",
            f"convocation_{safe_nom_dash}_{safe_prenom_dash}.pdf",
            f"{safe_nom_dash}_{safe_prenom_dash}_{numero}.pdf",
            f"{safe_nom_dash}_{safe_prenom_dash}.pdf"
        ])
        
        return patterns
    
    def find_pdf_file(self, candidate_data):
        """
        Trouve le fichier PDF correspondant au candidat
        
        Args:
            candidate_data (dict): Données du candidat
            
        Returns:
            str: Chemin vers le PDF trouvé ou None
        """
        patterns = self.find_pdf_patterns(candidate_data)
        
        # Chercher avec les patterns exacts
        for pattern in patterns:
            filepath = os.path.join(self.pdf_dir, pattern)
            if os.path.exists(filepath):
                return filepath
        
        # Chercher par correspondance partielle (insensible à la casse)
        if os.path.exists(self.pdf_dir):
            available_files = [f for f in os.listdir(self.pdf_dir) if f.endswith('.pdf')]
            
            nom = str(candidate_data.get('nom', '')).lower()
            prenom = str(candidate_data.get('prenom', '')).lower()
            numero = str(candidate_data.get('numero_candidat', ''))
            
            for available_file in available_files:
                file_lower = available_file.lower()
                
                # Vérifier si le nom et prénom sont dans le fichier
                if (nom in file_lower and prenom in file_lower) or numero in available_file:
                    return os.path.join(self.pdf_dir, available_file)
        
        return None
    
    def check_all_pdfs(self):
        """
        Vérifie tous les PDF pour les candidats
        
        Returns:
            dict: Résultats de la vérification
        """
        print(f"📄 Vérification des PDF dans {self.pdf_dir}")
        print(f"📊 Lecture des candidats depuis {self.excel_path}")
        
        try:
            df = pd.read_excel(self.excel_path, engine='openpyxl')
            total_candidates = len(df)
            
            print(f"👥 {total_candidates} candidats à vérifier")
            
            results = {
                'total_candidates': total_candidates,
                'found_pdfs': [],
                'missing_pdfs': [],
                'summary': {}
            }
            
            for index, row in df.iterrows():
                candidate_data = row.to_dict()
                
                nom = str(candidate_data.get('nom', ''))
                prenom = str(candidate_data.get('prenom', ''))
                email = str(candidate_data.get('email', ''))
                numero = str(candidate_data.get('numero_candidat', ''))
                
                print(f"[{index + 1}/{total_candidates}] {nom} {prenom}")
                
                pdf_path = self.find_pdf_file(candidate_data)
                
                candidate_info = {
                    'index': index + 1,
                    'nom': nom,
                    'prenom': prenom,
                    'email': email,
                    'numero_candidat': numero,
                    'pdf_path': pdf_path,
                    'expected_patterns': self.find_pdf_patterns(candidate_data)[:3]  # Top 3 patterns
                }
                
                if pdf_path:
                    print(f"  ✅ PDF trouvé: {os.path.basename(pdf_path)}")
                    results['found_pdfs'].append(candidate_info)
                else:
                    print(f"  ❌ PDF manquant")
                    results['missing_pdfs'].append(candidate_info)
            
            # Résumé
            results['summary'] = {
                'total': total_candidates,
                'found': len(results['found_pdfs']),
                'missing': len(results['missing_pdfs']),
                'success_rate': (len(results['found_pdfs']) / total_candidates * 100) if total_candidates > 0 else 0
            }
            
            return results
            
        except Exception as e:
            raise Exception(f"Erreur lors de la vérification des PDF: {e}")
    
    def print_detailed_report(self, results):
        """Affiche un rapport détaillé"""
        print("\n" + "="*70)
        print("📄 RAPPORT DE VÉRIFICATION DES PDF")
        print("="*70)
        
        summary = results['summary']
        print(f"📁 Répertoire PDF: {self.pdf_dir}")
        print(f"📊 Fichier candidats: {os.path.basename(self.excel_path)}")
        print(f"📅 Date de vérification: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"👥 Total candidats: {summary['total']}")
        print(f"✅ PDF trouvés: {summary['found']}")
        print(f"❌ PDF manquants: {summary['missing']}")
        print(f"📈 Taux de succès: {summary['success_rate']:.1f}%")
        
        if results['missing_pdfs']:
            print(f"\n❌ PDF MANQUANTS ({len(results['missing_pdfs'])}):")
            for item in results['missing_pdfs']:
                print(f"\n  👤 {item['nom']} {item['prenom']}")
                print(f"     📧 {item['email']}")
                print(f"     🔢 {item['numero_candidat']}")
                print(f"     📄 Patterns attendus:")
                for pattern in item['expected_patterns']:
                    print(f"       - {pattern}")
        
        if results['found_pdfs']:
            print(f"\n✅ ÉCHANTILLON PDF TROUVÉS:")
            for item in results['found_pdfs'][:5]:  # Afficher les 5 premiers
                pdf_name = os.path.basename(item['pdf_path'])
                print(f"  • {item['nom']} {item['prenom']} → {pdf_name}")
            
            if len(results['found_pdfs']) > 5:
                print(f"  ... et {len(results['found_pdfs']) - 5} autres PDF trouvés")
        
        print("="*70)
    
    def create_missing_pdfs_list(self, results, output_file="pdf_manquants.txt"):
        """Crée un fichier avec la liste des PDF manquants"""
        if not results['missing_pdfs']:
            print("✅ Aucun PDF manquant, pas de fichier à créer")
            return None
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Liste des PDF manquants pour les candidats des jurys DELF\n")
            f.write(f"# Généré le {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"# Total: {len(results['missing_pdfs'])} PDF manquants\n\n")
            
            for item in results['missing_pdfs']:
                f.write(f"Candidat: {item['nom']} {item['prenom']}\n")
                f.write(f"Email: {item['email']}\n")
                f.write(f"Numéro: {item['numero_candidat']}\n")
                f.write(f"Patterns attendus:\n")
                for pattern in item['expected_patterns']:
                    f.write(f"  - {pattern}\n")
                f.write("\n" + "-"*50 + "\n\n")
        
        print(f"📄 Liste des PDF manquants sauvegardée: {output_file}")
        return output_file

def main():
    """Fonction principale"""
    excel_file = "candidats_emails_valides.xlsx"
    pdf_dir = "output"
    
    # Vérifications
    if not os.path.exists(excel_file):
        print(f"❌ Fichier Excel non trouvé: {excel_file}")
        print("💡 Exécutez d'abord validate_emails_for_mailjet.py")
        return
    
    if not os.path.exists(pdf_dir):
        print(f"❌ Répertoire PDF non trouvé: {pdf_dir}")
        print("💡 Générez d'abord les PDF avec votre générateur de convocations")
        return
    
    try:
        # Créer le vérificateur
        checker = PDFChecker(excel_file, pdf_dir)
        
        # Vérifier tous les PDF
        results = checker.check_all_pdfs()
        
        # Afficher le rapport
        checker.print_detailed_report(results)
        
        # Créer la liste des PDF manquants
        missing_file = checker.create_missing_pdfs_list(results)
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        
        if results['missing_pdfs']:
            print(f"   1. Générez les {len(results['missing_pdfs'])} PDF manquants avec votre générateur")
            print(f"   2. Consultez le fichier '{missing_file or 'pdf_manquants.txt'}' pour les détails")
            print(f"   3. Relancez l'envoi Mailjet après génération des PDF")
        else:
            print(f"   ✅ Tous les PDF sont présents, vous pouvez lancer l'envoi Mailjet !")
            print(f"   🚀 Utilisez: python send_emails_standalone.py")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
