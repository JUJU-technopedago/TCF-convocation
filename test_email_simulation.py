#!/usr/bin/env python3
"""
Simulation d'envoi d'emails sans dépendances cryptography
"""

import pandas as pd
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EmailSimulator:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.logger = logging.getLogger(__name__)
    
    def _is_jury_file(self) -> bool:
        """Vérifie si le fichier Excel est un fichier de jurys DELF/DALF"""
        try:
            xl = pd.ExcelFile(self.excel_path)
            sheet_names = [sheet.strip().upper() for sheet in xl.sheet_names]
            
            # Vérifier la présence d'un onglet ADMIN et de niveaux DELF
            has_admin_sheet = 'ADMIN' in sheet_names
            niveau_sheets = [s for s in sheet_names if any(niveau in s for niveau in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])]
            
            # Minimum 2 niveaux et un onglet ADMIN
            return len(niveau_sheets) >= 2 and has_admin_sheet
            
        except Exception:
            return False
    
    def _convert_jury_file_to_candidates(self) -> pd.DataFrame:
        """Convertit un fichier de jurys DELF/DALF en format candidats avec emails extraits"""
        try:
            xl = pd.ExcelFile(self.excel_path)
            all_candidates = []
            
            for sheet_name in xl.sheet_names:
                if sheet_name.upper() == 'ADMIN':
                    continue
                    
                self.logger.info(f"📋 Traitement de l'onglet: {sheet_name}")
                
                try:
                    # Lire l'onglet
                    df = pd.read_excel(self.excel_path, sheet_name=sheet_name, engine='openpyxl')
                    
                    # Chercher la ligne d'en-tête (qui contient "Email")
                    header_row = None
                    for idx, row in df.iterrows():
                        row_values = row.tolist()
                        if any('Email' in str(cell) for cell in row_values):
                            header_row = idx
                            break
                    
                    if header_row is not None:
                        # Lire à partir de la ligne d'en-tête
                        df_data = pd.read_excel(self.excel_path, sheet_name=sheet_name, 
                                              header=header_row, engine='openpyxl')
                        
                        # Les emails sont dans la colonne 5 (index 5) selon la structure observée
                        email_col_idx = 5  # Index de la colonne Email
                        nom_prenom_idx = 3  # Index de la colonne "NOM et Prénom"
                        
                        if len(df_data.columns) > email_col_idx:
                            candidates_count = 0
                            
                            # Traiter chaque ligne de données
                            for idx, row in df_data.iterrows():
                                row_values = row.tolist()
                                
                                # Extraire les données
                                if len(row_values) > email_col_idx:
                                    email = str(row_values[email_col_idx]) if pd.notna(row_values[email_col_idx]) else ''
                                    nom_prenom = str(row_values[nom_prenom_idx]) if len(row_values) > nom_prenom_idx and pd.notna(row_values[nom_prenom_idx]) else ''
                                    
                                    # Ignorer la ligne d'en-tête (contient "Email" ou "NOM et Prénom")
                                    if email == 'Email' or nom_prenom == 'NOM et Prénom':
                                        continue
                                    
                                    # Séparer nom et prénom si possible
                                    if nom_prenom and ' ' in nom_prenom:
                                        parts = nom_prenom.split(' ', 1)
                                        nom = parts[0]
                                        prenom = parts[1] if len(parts) > 1 else ''
                                    else:
                                        nom = nom_prenom
                                        prenom = ''
                                    
                                    # Vérifier que l'email est valide
                                    if email and email.strip() and '@' in email and email.strip() != 'nan':
                                        candidate_data = {
                                            'nom': nom,
                                            'prenom': prenom,
                                            'email': email.strip(),
                                            'niveau': sheet_name,
                                            'type_examen': 'DELF',
                                            'date_examen': '15/10/2025',
                                            'heure_examen': '09:00',
                                            'salle': 'Salle A'
                                        }
                                        
                                        all_candidates.append(candidate_data)
                                        candidates_count += 1
                            
                            self.logger.info(f"✅ {candidates_count} candidats trouvés dans {sheet_name}")
                        
                except Exception as e:
                    self.logger.error(f"❌ Erreur lors du traitement de l'onglet {sheet_name}: {e}")
            
            if all_candidates:
                df = pd.DataFrame(all_candidates)
                self.logger.info(f"✅ Total: {len(df)} candidats avec emails valides chargés")
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la conversion: {e}")
            return pd.DataFrame()
    
    def _create_email_content(self, candidate_data, pdf_path=None):
        """Crée le contenu personnalisé de l'email pour DELF"""
        prenom = candidate_data.get('prenom', '').capitalize()
        nom = candidate_data.get('nom', '').upper()
        niveau = candidate_data.get('niveau', 'DELF')
        date_exam = candidate_data.get('date_examen', '15/10/2025')
        
        # Contenu spécialisé pour DELF
        content = f"""Bonjour {prenom} {nom},

Vous trouverez en pièce jointe votre convocation à l'examen {niveau} prévu le {date_exam}.

L'examen aura lieu sur ordinateur.

Cordialement,

L'Alliance Française de Bruxelles-Europe
Pôle des Certifications DELF, DALF, TCF et DFP"""
        
        return content
    
    def simulate_email_sending(self):
        """Simule l'envoi d'emails"""
        try:
            # Charger les données
            if self._is_jury_file():
                data = self._convert_jury_file_to_candidates()
            else:
                self.logger.error("❌ Fichier non reconnu comme fichier de jurys")
                return
            
            if len(data) == 0:
                self.logger.error("❌ Aucun candidat trouvé")
                return
            
            self.logger.info(f"📧 Simulation d'envoi d'emails pour {len(data)} candidats")
            
            # Simuler l'envoi pour chaque candidat
            for idx, candidate in data.iterrows():
                email = candidate['email']
                nom = candidate['nom']
                prenom = candidate['prenom']
                niveau = candidate['niveau']
                
                # Créer le contenu de l'email
                email_content = self._create_email_content(candidate)
                
                # Simuler l'envoi
                subject = f"Votre examen {niveau} du {candidate['date_examen']}"
                
                print(f"\n📧 EMAIL SIMULÉ #{idx+1}")
                print(f"Destinataire: {email}")
                print(f"Sujet: {subject}")
                print(f"Contenu:")
                print("=" * 50)
                print(email_content)
                print("=" * 50)
                
                self.logger.info(f"✅ Email simulé envoyé à {prenom} {nom} ({email})")
            
            self.logger.info(f"🎉 Simulation terminée: {len(data)} emails envoyés")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la simulation: {e}")

if __name__ == "__main__":
    excel_file = 'juries_20250919_162205.xlsx'
    
    simulator = EmailSimulator(excel_file)
    simulator.simulate_email_sending()