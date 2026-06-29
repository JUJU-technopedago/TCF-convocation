#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer des convocations avec une version modifiée du template HTML
pour résoudre le problème de type 'str' et 'int' avec tous les candidats problématiques
"""

import os
import sys
import shutil
import pandas as pd
from pdf_generator import PDFGenerator

def print_progress(message):
    print(message)

def create_problematic_candidates_excel():
    """
    Crée un fichier Excel avec les candidats problématiques mentionnés dans les logs
    """
    # Liste des noms des candidats problématiques
    problematic_names = [
        "BRANKIN Ciara Marie Thérèse",
        "CHATZIS Alkis",
        "IONESCU Matei",
        "MENAND Maria",
        "STATHOPOULOS Miltiadis",
        "ANGELOPOULOS Spiros",
        "CHATZI Nefeli",
        "GARCIA MELER Ines",
        "KAMYA Michael",
        "SZYNDLAUER Emilia",
        "KODERAS Alexa"
    ]
    
    # Créer un DataFrame avec les données de base pour ces candidats
    data = []
    for i, full_name in enumerate(problematic_names):
        # Séparer le nom et le prénom
        parts = full_name.split(' ', 1)
        nom = parts[0]
        prenom = parts[1] if len(parts) > 1 else ""
        
        # Créer un enregistrement pour ce candidat
        data.append({
            'numero_candidat': f"0320020322{90+i}",
            'nom': nom,
            'prenom': prenom,
            'date_naissance': '01/01/2000',
            'email': f"{nom.lower()}.{prenom.lower().split()[0]}@email.com",
            'niveau': 'B2',
            'matiere': 'DELF B2',
            'date_examen': '20/09/2025',
            'heure_debut': '09:00',
            'heure_fin': '11:30',
            'duree': '2h30 (collective) + 20min (individuelle)',
            'salle': '1',
            'institution_name': 'Alliance Française Bruxelles Europe',
            'institution_address': 'Avenue des Arts 46',
            'institution_city': 'Bruxelles',
            'institution_postal': '1000',
            'besoins_speciaux': False,
            'tiers_temps': False
        })
    
    # Créer le DataFrame
    df = pd.DataFrame(data)
    
    # Chemin du fichier Excel
    excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "problematic_candidates.xlsx")
    
    # Sauvegarder le DataFrame dans un fichier Excel
    df.to_excel(excel_path, index=False)
    
    print(f"Fichier Excel créé avec {len(problematic_names)} candidats problématiques: {excel_path}")
    return excel_path

def generate_fixed_template():
    """
    Crée une version modifiée du template HTML pour éviter les erreurs de type
    """
    source_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               "templates", "convocation_delf_template_modele.html")
    
    if not os.path.exists(source_template):
        print(f"ERREUR: Le template HTML source '{source_template}' n'existe pas!")
        return None
    
    # Créer un répertoire pour la version fixée
    fixed_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates_fixed")
    os.makedirs(fixed_dir, exist_ok=True)
    
    # Chemin du template fixé
    fixed_template = os.path.join(fixed_dir, "convocation_delf_template_fixed.html")
    
    # Lire le contenu du template original
    with open(source_template, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer les valeurs problématiques (pourcentages dans les tables)
    fixed_content = content.replace('width: 50%;', 'width: 300px;')
    fixed_content = fixed_content.replace('width: 40%;', 'width: 250px;')
    fixed_content = fixed_content.replace('width: 60%;', 'width: 350px;')
    
    # Corriger d'autres valeurs qui pourraient causer des problèmes
    fixed_content = fixed_content.replace('height: 100%;', 'height: 100px;')
    fixed_content = fixed_content.replace('width: 100%;', 'width: 600px;')
    
    # Écrire le contenu modifié dans le nouveau fichier
    with open(fixed_template, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Template fixé créé: {fixed_template}")
    return fixed_template

def generate_convocations(excel_path, output_dir="output_fixed_template"):
    """
    Génère les convocations avec le template HTML modifié
    """
    # Créer le template fixé
    template_path = generate_fixed_template()
    if not template_path:
        return 0
        
    print(f"=== GÉNÉRATEUR DE CONVOCATIONS AVEC TEMPLATE HTML FIXÉ ===")
    print(f"Fichier Excel: {excel_path}")
    print(f"Template HTML fixé: {template_path}")
    print(f"Répertoire de sortie: {output_dir}")
    print(f"=========================================================")
    
    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    # Créer le générateur de PDF avec le template HTML fixé
    generator = PDFGenerator(
        excel_path=excel_path,
        template_path=template_path,
        logo_af_path="assets/logoAF.png",
        logo_delf_path="assets/logoDELF.png",
        output_dir=output_dir,
        access_code="1234"  # Remplacez par le code d'accès réel si nécessaire
    )
    
    # Générer les PDF
    print("\nDémarrage de la génération des PDF...")
    count = generator.generate_all_pdfs(print_progress)
    
    print(f"\n=== GÉNÉRATION TERMINÉE ===")
    print(f"{count} PDF générés avec succès dans {output_dir}")
    
    return count

if __name__ == "__main__":
    # Définir l'action par défaut
    action = "generate"
    
    # Si des arguments sont fournis
    if len(sys.argv) > 1:
        # Si le premier argument est "problematic", on crée le fichier Excel des candidats problématiques
        if sys.argv[1].lower() == "problematic":
            action = "problematic"
            excel_path = create_problematic_candidates_excel()
            output_dir = sys.argv[2] if len(sys.argv) > 2 else "output_problematic"
        else:
            # Sinon, on utilise le fichier Excel spécifié
            excel_path = sys.argv[1]
            output_dir = sys.argv[2] if len(sys.argv) > 2 else "output_fixed_template"
    else:
        # Si aucun argument n'est fourni, on affiche l'usage
        print("Usage: python generate_with_fixed_template.py <fichier_excel|problematic> [output_dir]")
        print("  - fichier_excel: chemin vers le fichier Excel contenant les candidats")
        print("  - problematic: génère un fichier Excel avec les candidats problématiques des logs")
        sys.exit(1)
    
    # Si on génère les convocations
    if action == "generate":
        # Vérifier que le fichier Excel existe
        if not os.path.exists(excel_path):
            print(f"ERREUR: Le fichier Excel '{excel_path}' n'existe pas.")
            sys.exit(1)
    
    # Générer les convocations
    try:
        generate_convocations(excel_path, output_dir)
    except Exception as e:
        print(f"ERREUR lors de la génération des convocations: {e}")
        sys.exit(1)