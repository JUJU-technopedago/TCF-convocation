#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier le contenu HTML généré pour la convocation de SIANO Marco
"""

import os
import sys
from datetime import datetime
from jinja2 import Template, FileSystemLoader, Environment

def verify_html_template():
    """
    Vérifie le contenu HTML généré pour la convocation de SIANO Marco
    """
    print("=" * 60)
    print("VÉRIFICATION DU MODÈLE HTML POUR SIANO MARCO")
    print("=" * 60)
    
    # Créer manuellement les données pour SIANO Marco
    siano_data = {
        'numero_candidat': '032002032317',
        'nom': 'SIANO',
        'prenom': 'Marco',
        'date_naissance': '15/07/1995',
        'email': 'marco.siano@example.com',
        'niveau': 'B2',
        'matiere': 'DELF B2',
        'date_examen': '14/08/2025',
        'date_ep_coll': '14/08/2025',
        'debut_ep_coll': '15:00',
        'fin_ep_coll': '17:20',  # Avec tiers-temps
        'fin_ep_coll_affichage': '17:20 (tiers-temps)',
        'heure_debut': '09:00',
        'heure_preparation': '09:00',
        'heure_passage': '10:00',
        'besoins_speciaux': True,
        'tiers_temps': True,
        'institution_name': 'Alliance Française Bruxelles Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_city': 'Bruxelles',
        'institution_postal': '1000',
        'institution_phone': '+32 2 788 21 60',
        'contact_urgence': 'info@alliancefrancaise.be',
        'duree': '2h30 (collective) + 20min (individuelle)',
        'salle': 'Salle d\'examen',
        'exam_type': 'DELF',
        'logo_af_path': 'logoAF.svg',
        'logo_delf_path': 'logoDELF.svg',
        'access_code': ''
    }
    
    # Définir le chemin du template
    template_path = "templates/convocation_delf_template_modele.html"
    if not os.path.exists(template_path):
        template_path = "convocation_delf_template_modele.html"
        if not os.path.exists(template_path):
            print(f"❌ Erreur: Fichier template non trouvé: {template_path}")
            sys.exit(1)
    
    print(f"Utilisation du template: {template_path}")
    
    # Charger le template Jinja2
    template_dir = os.path.dirname(template_path)
    template_name = os.path.basename(template_path)
    
    # Si le chemin est vide (fichier dans le répertoire courant)
    if not template_dir:
        template_dir = "."
    
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    
    # Générer le HTML
    html_content = template.render(**siano_data)
    
    # Rechercher le texte spécifique dans le HTML généré
    search_string = "(Candidat bénéficiaire d'un aménagement spécifique)"
    old_string = "(Aménagement tiers-temps)"
    
    if search_string in html_content:
        print(f"✅ SUCCÈS: Le texte '{search_string}' a été trouvé dans le HTML généré.")
        print("\nExtrait du HTML où le texte apparaît:")
        
        # Trouver l'extrait pertinent
        index = html_content.find(search_string)
        start = max(0, index - 100)
        end = min(len(html_content), index + len(search_string) + 100)
        extract = html_content[start:end]
        
        # Mettre en évidence le texte recherché
        highlighted_extract = extract.replace(search_string, f"\033[1;32m{search_string}\033[0m")
        print(f"\n{highlighted_extract}\n")
        
    elif old_string in html_content:
        print(f"❌ ÉCHEC: L'ancien texte '{old_string}' est toujours présent dans le HTML généré.")
        print("Le remplacement n'a pas été effectif.")
    else:
        print(f"❌ ÉCHEC: Ni le nouveau texte '{search_string}' ni l'ancien texte '{old_string}' n'ont été trouvés.")
        print("Vérifiez que le candidat a bien le statut 'tiers_temps' à True.")
    
    # Créer un fichier HTML pour vérification
    output_dir = "output_html_verification"
    os.makedirs(output_dir, exist_ok=True)
    
    html_file = os.path.join(output_dir, "verification_siano.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\nFichier HTML de vérification créé: {html_file}")
    print("\nVérification terminée.")

if __name__ == "__main__":
    verify_html_template()