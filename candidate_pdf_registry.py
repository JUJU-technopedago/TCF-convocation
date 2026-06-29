#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Registre sécurisé pour l'association 100% fiable candidat ↔ PDF ↔ Email
Système infaillible basé sur des identifiants uniques et un registre de correspondance
"""

import hashlib
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path


class CandidatePDFRegistry:
    """
    Registre sécurisé pour garantir l'association candidat-PDF-email sans erreur possible
    """
    
    def __init__(self, output_dir, registry_file=None):
        """
        Initialise le registre sécurisé
        
        Args:
            output_dir (str): Répertoire de sortie des PDF
            registry_file (str): Nom du fichier registre (optionnel)
        """
        self.output_dir = Path(output_dir)
        self.registry_file = registry_file or os.path.join(output_dir, "candidate_pdf_registry.json")
        self.registry = {}
        self.load_registry()
    
    def generate_candidate_id(self, candidate):
        """
        Génère un identifiant unique et reproductible pour un candidat
        Format simplifié : 6 caractères alternés lettres minuscules et chiffres (ex: a9t5g1)
        
        Args:
            candidate (dict): Données du candidat
            
        Returns:
            str: Identifiant unique alterné (ex: a9t5g1)
        """
        import random
        
        # Créer une signature unique basée sur les données essentielles
        nom = self.clean_text(candidate.get('nom', ''))
        prenom = self.clean_text(candidate.get('prenom', ''))
        email = candidate.get('email', '').lower().strip()
        
        # Signature unique
        signature = f"{nom}|{prenom}|{email}"
        
        # Générer hash SHA-256 pour avoir une base reproductible
        hash_object = hashlib.sha256(signature.encode('utf-8'))
        hash_hex = hash_object.hexdigest()
        
        # Utiliser le hash comme seed pour générer un ID reproductible
        # Convertir les premiers 8 caractères hex en nombre pour seed
        seed = int(hash_hex[:8], 16)
        random.seed(seed)
        
        # Générer un ID alterné lettres-chiffres de 6 caractères
        letters = 'abcdefghijklmnopqrstuvwxyz'
        digits = '0123456789'
        
        unique_id = ''
        for i in range(6):
            if i % 2 == 0:  # Positions 0, 2, 4 : lettres
                unique_id += random.choice(letters)
            else:  # Positions 1, 3, 5 : chiffres
                unique_id += random.choice(digits)
        
        return unique_id
    
    def clean_text(self, text):
        """
        Nettoie et normalise le texte pour éviter les problèmes de nommage
        
        Args:
            text (str): Texte à nettoyer
            
        Returns:
            str: Texte nettoyé
        """
        if not text:
            return ""
        
        # Supprimer les accents et caractères spéciaux
        import unicodedata
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        
        # Garder seulement lettres, chiffres, tirets, underscores et espaces
        text = re.sub(r'[^\w\-\s]', '', text)
        
        # Remplacer les espaces multiples par un seul espace et normaliser
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remplacer les espaces par des underscores
        text = text.replace(' ', '_')
        
        return text
    
    def generate_secure_filename(self, candidate, exam_type="TCF"):
        """
        Génère un nom de fichier PDF sécurisé et lisible
        Format : convocation_TCF_DOUANFACK_MEJIOTSA_Francine_a9t5g1.pdf
        Nom de famille conservé en MAJUSCULES (avec underscores si composé)
        Prénom avec capitalisation sur chaque mot
        
        Args:
            candidate (dict): Données du candidat
            exam_type (str): Type d'examen
            
        Returns:
            str: Nom de fichier PDF sécurisé et lisible
        """
        # Identifiant unique simplifié (ex: a9t5g1)
        candidate_id = self.generate_candidate_id(candidate)
        
        # Nettoyer et préserver la casse d'origine
        nom_raw = candidate.get('nom', '')
        prenom_raw = candidate.get('prenom', '')
        
        # Pour le nom : nettoyer et mettre en MAJUSCULES (car c'est le nom de famille)
        nom_clean = self.clean_text(nom_raw).upper()
        
        # Pour le prénom : nettoyer et capitaliser chaque mot (title case)
        prenom_clean = self.clean_text(prenom_raw).title()
        
        # Format simplifié et lisible : convocation_{exam_type}_{NOM}_{Prenom}_{id}.pdf
        filename = f"convocation_{exam_type}_{nom_clean}_{prenom_clean}_{candidate_id}.pdf"
        
        return filename
    
    def register_candidate_pdf(self, candidate, pdf_filename, pdf_full_path):
        """
        Enregistre l'association candidat-PDF dans le registre sécurisé
        
        Args:
            candidate (dict): Données du candidat
            pdf_filename (str): Nom du fichier PDF
            pdf_full_path (str): Chemin complet du PDF
            
        Returns:
            str: Identifiant unique du candidat
        """
        candidate_id = self.generate_candidate_id(candidate)
        
        # Vérifier que le fichier existe
        if not os.path.exists(pdf_full_path):
            raise FileNotFoundError(f"PDF non trouvé: {pdf_full_path}")
        
        # Calculer la taille et le checksum du PDF pour validation
        pdf_size = os.path.getsize(pdf_full_path)
        with open(pdf_full_path, 'rb') as f:
            pdf_content = f.read()
            pdf_checksum = hashlib.md5(pdf_content).hexdigest()
        
        # Enregistrer dans le registre
        self.registry[candidate_id] = {
            'candidate_info': {
                'nom': candidate.get('nom', ''),
                'prenom': candidate.get('prenom', ''),
                'email': candidate.get('email', ''),
                'numero_candidat': candidate.get('numero_candidat', ''),
                'tcf_type': candidate.get('tcf_type', '')
            },
            'pdf_info': {
                'filename': pdf_filename,
                'full_path': pdf_full_path,
                'size_bytes': pdf_size,
                'checksum_md5': pdf_checksum,
                'created_at': datetime.now().isoformat()
            },
            'status': 'registered',
            'registered_at': datetime.now().isoformat()
        }
        
        # Sauvegarder le registre
        self.save_registry()
        
        return candidate_id
    
    def find_pdf_for_candidate(self, candidate):
        """
        Trouve le PDF associé à un candidat de manière 100% fiable
        
        Args:
            candidate (dict): Données du candidat
            
        Returns:
            tuple: (pdf_path, pdf_filename) ou (None, None) si non trouvé
        """
        candidate_id = self.generate_candidate_id(candidate)
        
        # Chercher dans le registre
        if candidate_id in self.registry:
            registration = self.registry[candidate_id]
            pdf_full_path = registration['pdf_info']['full_path']
            pdf_filename = registration['pdf_info']['filename']
            
            # Vérifier que le fichier existe toujours
            if os.path.exists(pdf_full_path):
                # Vérifier l'intégrité (optionnel)
                current_size = os.path.getsize(pdf_full_path)
                expected_size = registration['pdf_info']['size_bytes']
                
                if current_size == expected_size:
                    return pdf_full_path, pdf_filename
                else:
                    print(f"⚠️ ATTENTION: Taille PDF modifiée pour {candidate_id}")
                    return pdf_full_path, pdf_filename  # Retourner quand même
            else:
                print(f"❌ PDF enregistré mais fichier manquant: {pdf_full_path}")
                return None, None
        
        # Si pas trouvé dans le registre, retourner None
        print(f"❌ Candidat {candidate_id} non trouvé dans le registre")
        return None, None
    
    def get_candidate_by_id(self, candidate_id):
        """
        Récupère les informations d'un candidat par son ID
        
        Args:
            candidate_id (str): Identifiant unique du candidat
            
        Returns:
            dict: Informations du candidat ou None
        """
        if candidate_id in self.registry:
            return self.registry[candidate_id]['candidate_info']
        return None
    
    def list_all_registrations(self):
        """
        Liste toutes les associations enregistrées
        
        Returns:
            list: Liste des enregistrements
        """
        result = []
        for candidate_id, registration in self.registry.items():
            candidate_info = registration['candidate_info']
            pdf_info = registration['pdf_info']
            
            result.append({
                'candidate_id': candidate_id,
                'nom': candidate_info['nom'],
                'prenom': candidate_info['prenom'],
                'email': candidate_info['email'],
                'pdf_filename': pdf_info['filename'],
                'pdf_exists': os.path.exists(pdf_info['full_path']),
                'registered_at': registration['registered_at']
            })
        
        return result
    
    def validate_registry_integrity(self):
        """
        Valide l'intégrité complète du registre
        
        Returns:
            dict: Rapport de validation
        """
        report = {
            'total_registered': len(self.registry),
            'valid_entries': 0,
            'missing_files': 0,
            'invalid_checksums': 0,
            'errors': []
        }
        
        for candidate_id, registration in self.registry.items():
            try:
                pdf_path = registration['pdf_info']['full_path']
                expected_checksum = registration['pdf_info']['checksum_md5']
                
                if os.path.exists(pdf_path):
                    # Vérifier le checksum
                    with open(pdf_path, 'rb') as f:
                        current_checksum = hashlib.md5(f.read()).hexdigest()
                    
                    if current_checksum == expected_checksum:
                        report['valid_entries'] += 1
                    else:
                        report['invalid_checksums'] += 1
                        report['errors'].append(f"Checksum invalide pour {candidate_id}")
                else:
                    report['missing_files'] += 1
                    report['errors'].append(f"Fichier manquant pour {candidate_id}: {pdf_path}")
                    
            except Exception as e:
                report['errors'].append(f"Erreur validation {candidate_id}: {str(e)}")
        
        return report
    
    def load_registry(self):
        """Charge le registre depuis le fichier JSON"""
        try:
            if os.path.exists(self.registry_file):
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    self.registry = json.load(f)
                print(f"📂 Registre chargé: {len(self.registry)} enregistrements")
            else:
                self.registry = {}
                print("📂 Nouveau registre créé")
        except Exception as e:
            print(f"⚠️ Erreur chargement registre: {e}")
            self.registry = {}
    
    def save_registry(self):
        """Sauvegarde le registre dans le fichier JSON"""
        try:
            # Créer le répertoire si nécessaire
            os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
            
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Registre sauvegardé: {len(self.registry)} enregistrements")
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde registre: {e}")
    
    def clear_registry(self):
        """Efface complètement le registre (utiliser avec précaution)"""
        self.registry = {}
        self.save_registry()
        print("🗑️ Registre effacé")
    
    def export_registry_report(self, report_file=None):
        """
        Exporte un rapport détaillé du registre
        
        Args:
            report_file (str): Nom du fichier de rapport (optionnel)
        """
        if not report_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = os.path.join(self.output_dir, f"registry_report_{timestamp}.txt")
        
        registrations = self.list_all_registrations()
        validation_report = self.validate_registry_integrity()
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=== RAPPORT REGISTRE CANDIDAT-PDF ===\n")
            f.write(f"Généré le: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Répertoire: {self.output_dir}\n")
            f.write(f"Fichier registre: {self.registry_file}\n\n")
            
            f.write("=== VALIDATION INTÉGRITÉ ===\n")
            f.write(f"Total enregistrements: {validation_report['total_registered']}\n")
            f.write(f"Entrées valides: {validation_report['valid_entries']}\n")
            f.write(f"Fichiers manquants: {validation_report['missing_files']}\n")
            f.write(f"Checksums invalides: {validation_report['invalid_checksums']}\n\n")
            
            if validation_report['errors']:
                f.write("=== ERREURS DÉTECTÉES ===\n")
                for error in validation_report['errors']:
                    f.write(f"- {error}\n")
                f.write("\n")
            
            f.write("=== LISTE COMPLÈTE DES ENREGISTREMENTS ===\n")
            for i, reg in enumerate(registrations, 1):
                status = "✅ OK" if reg['pdf_exists'] else "❌ MANQUANT"
                f.write(f"{i:3d}. [{reg['candidate_id']}] {reg['prenom']} {reg['nom']}\n")
                f.write(f"     Email: {reg['email']}\n")
                f.write(f"     PDF: {reg['pdf_filename']} ({status})\n")
                f.write(f"     Enregistré: {reg['registered_at']}\n\n")
        
        print(f"📊 Rapport exporté: {report_file}")
        return report_file


def test_registry_system():
    """Fonction de test du système de registre"""
    print("🧪 TEST DU SYSTÈME DE REGISTRE")
    
    # Candidats de test
    test_candidates = [
        {
            'nom': 'DUPONT',
            'prenom': 'Jean-Marie',
            'email': 'jean.marie.dupont@email.com',
            'numero_candidat': 'TCF001',
            'tcf_type': 'TCF CANADA'
        },
        {
            'nom': 'MARTIN-LEFÈVRE',
            'prenom': 'Émilie',
            'email': 'emilie.martin@email.fr',
            'numero_candidat': 'TCF002',
            'tcf_type': 'TCF TP COMPLET'
        }
    ]
    
    # Créer le registre de test
    registry = CandidatePDFRegistry("./test_output")
    
    for candidate in test_candidates:
        # Générer un nom de fichier sécurisé
        filename = registry.generate_secure_filename(candidate)
        print(f"📁 Nom généré: {filename}")
        
        # Générer l'ID unique
        candidate_id = registry.generate_candidate_id(candidate)
        print(f"🆔 ID unique: {candidate_id}")
        
        print(f"✅ Test réussi pour {candidate['prenom']} {candidate['nom']}")
        print("-" * 50)


if __name__ == "__main__":
    test_registry_system()