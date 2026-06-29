#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégrateur de solution pour le problème de génération PDF
Ce script corrige le template HTML pour éviter l'erreur de type 'str' - 'int'
"""

import os
import shutil
import re

def ensure_templates_dir_exists():
    """Vérifie que le répertoire templates_fixed existe"""
    templates_fixed_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates_fixed")
    os.makedirs(templates_fixed_dir, exist_ok=True)
    return templates_fixed_dir

def create_fixed_template():
    """
    Crée une version modifiée du template HTML pour éviter les erreurs de type
    """
    source_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               "templates", "convocation_delf_template_modele.html")
    
    if not os.path.exists(source_template):
        print(f"ERREUR: Le template HTML source '{source_template}' n'existe pas!")
        return None
    
    # Créer un répertoire pour la version fixée
    fixed_dir = ensure_templates_dir_exists()
    
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
    fixed_content = fixed_content.replace('height: 100%;', 'height: 120px;')
    fixed_content = fixed_content.replace('width: 100%;', 'width: 600px;')
    
    # Ajuster la largeur de la cellule QR code pour correspondre à l'image
    fixed_content = fixed_content.replace('width: 150px;', 'width: 120px;')
    
    # Fixer la taille du texte dans le cadre de titre de manière permanente
    fixed_content = fixed_content.replace('font-size: 35pt;', 'font-size: 15pt;')
    
    # Supprimer la couleur de fond du titre d'examen
    fixed_content = fixed_content.replace('background-color: #e8e8e8;', 'background-color: #ffffff;')
    
    # Réduire l'espace entre le QR code et le bloc adresse
    fixed_content = fixed_content.replace('padding: 0 0 0 20px;', 'padding: 0 0 0 7px;')
    
    # Supprimer toutes les bordures grises légères
    fixed_content = fixed_content.replace('border: 1px solid #cccccc;', 'border: none;')
    fixed_content = fixed_content.replace('border: 1px solid #e6e6e6;', 'border: none;')
    
    # Ajuster la hauteur de l'espace entre les logos et le titre
    fixed_content = fixed_content.replace('padding: 15px 0; margin-top: 10px;', 'padding: 20px 0; margin-top: 20px;')
    # Mettre à jour aussi les valeurs intermédiaires
    fixed_content = fixed_content.replace('padding: 30px 0; margin-top: 20px;', 'padding: 20px 0; margin-top: 20px;')
    fixed_content = fixed_content.replace('padding: 60px 0; margin-top: 40px;', 'padding: 20px 0; margin-top: 20px;')
    fixed_content = fixed_content.replace('padding: 40px 0; margin-top: 40px;', 'padding: 20px 0; margin-top: 20px;')
    
    # S'assurer que le style de tr a une bordure nulle
    if 'tr style="height: 120px;' in fixed_content:
        fixed_content = fixed_content.replace('tr style="height: 120px;\n        border: 1px solid #e6e6e6;"', 
                                             'tr style="height: 120px;\n        border: none;"')
    
    # Conserver uniquement la bordure noire pour le titre
    if '.exam-title-box {' in fixed_content:
        fixed_content = fixed_content.replace('.exam-title-box {\n            background-color: #ffffff;\n            border: none;',
                                            '.exam-title-box {\n            background-color: #ffffff;\n            border: 2px solid #000;')
    
    # Ajuster la hauteur sans ajouter de bordure
    if 'height: 100px;' in fixed_content:
        fixed_content = fixed_content.replace('height: 100px;', 'height: 120px;')
    
    # Définir l'espace entre le titre et le nom du candidat égal à l'espace au-dessus du titre
    if 'margin: 30px 0 5px 0;' in fixed_content:
        fixed_content = fixed_content.replace('margin: 30px 0 5px 0;', 'margin: 20px 0 5px 0;')
    if 'margin: 15px 0 5px 0;' in fixed_content:
        fixed_content = fixed_content.replace('margin: 15px 0 5px 0;', 'margin: 20px 0 5px 0;')
    
    # Ajouter la structure de table pour les informations d'examen
    # Vérifions d'abord si le nouveau modèle de table existe déjà
    if '<table class="exam-info-table">' not in fixed_content:
        # Si pas de nouvelle structure, remplacer l'ancienne structure par la nouvelle
        pattern_old_exam_format = r'<div class="exam-title-container">.*?<div class="exam-info"><strong>Salle</strong> : {{ salle_individuelle }}</div>\s*</div>'
        
        new_table_structure = '''    <!-- Nouvelle table structurée pour les informations d'examen -->
    <table class="exam-info-table">
        <!-- Ligne 1 avec titre fusionné -->
        <tr class="exam-title-row">
            <td colspan="3" class="exam-title">
                Examen {{ exam_type or "DELF" }}, Niveau {{ niveau or "B1" }} du CECRL
            </td>
        </tr>
        <!-- Ligne 2 avec numéros et première épreuve -->
        <tr>
            <td class="exam-number-cell">1</td>
            <td class="exam-details-cell">
                {% if (date_ep_coll and date_ep_ind and (date_ep_coll < date_ep_ind)) or 
                    (date_ep_coll and date_ep_ind and date_ep_coll == date_ep_ind and debut_ep_coll < heure_preparation) or
                    (not date_ep_ind) %}
                <div class="exam-section-title">Épreuves collectives :</div>
                <div class="exam-info"><strong>Date</strong> : <span style="background-color: #ffff00;">{{ date_ep_coll or date_examen }}</span></div>
                <div class="exam-info"><strong>Début de l'épreuve</strong> : {{ debut_ep_coll or heure_debut }}</div>
                <div class="exam-info"><strong>Fin de l'épreuve</strong> : {{ fin_ep_coll_affichage or fin_ep_coll or "Selon durée du niveau" }}</div>
                <div class="exam-info"><strong>Salle</strong> : {{ salle_collective or salle }}</div>
                {% else %}
                <div class="exam-section-title">Épreuve individuelle :</div>
                <div class="exam-info"><strong>Date</strong> : <span style="background-color: #ffff00;">{{ date_ep_ind or date_examen }}</span></div>
                <div class="exam-info"><strong>Heure de préparation</strong> : {{ heure_preparation or heure_debut }}</div>
                <div class="exam-info"><strong>Salle</strong> : {{ salle_individuelle }}</div>
                {% endif %}
            </td>
            <td class="empty-cell" rowspan="4"></td>
        </tr>
        <!-- Ligne de séparation minimale -->
        <tr class="separator-row">
            <td style="height: 5px; padding: 0;"></td>
            <td style="height: 5px; padding: 0;"></td>
        </tr>
        <!-- Ligne 3 avec numéro et seconde épreuve -->
        <tr>
            <td class="exam-number-cell">2</td>
            <td class="exam-details-cell">
                {% if (date_ep_coll and date_ep_ind and (date_ep_coll < date_ep_ind)) or 
                    (date_ep_coll and date_ep_ind and date_ep_coll == date_ep_ind and debut_ep_coll < heure_preparation) or
                    (not date_ep_ind) %}
                <div class="exam-section-title">Épreuve individuelle :</div>
                <div class="exam-info"><strong>Date</strong> : <span style="background-color: #ffff00;">{{ date_ep_ind or date_examen }}</span></div>
                <div class="exam-info"><strong>Heure de préparation</strong> : {{ heure_preparation or heure_debut }}</div>
                <div class="exam-info"><strong>Salle</strong> : {{ salle_individuelle }}</div>
                {% else %}
                <div class="exam-section-title">Épreuves collectives :</div>
                <div class="exam-info"><strong>Date</strong> : <span style="background-color: #ffff00;">{{ date_ep_coll or date_examen }}</span></div>
                <div class="exam-info"><strong>Début de l'épreuve</strong> : {{ debut_ep_coll or heure_debut }}</div>
                <div class="exam-info"><strong>Fin de l'épreuve</strong> : {{ fin_ep_coll_affichage or fin_ep_coll or "Selon durée du niveau" }}</div>
                <div class="exam-info"><strong>Salle</strong> : {{ salle_collective or salle }}</div>
                {% endif %}
            </td>
        </tr>
    </table>'''
        
        # Remplacer l'ancien format par le nouveau
        if re.search(pattern_old_exam_format, fixed_content, re.DOTALL):
            fixed_content = re.sub(pattern_old_exam_format, new_table_structure, fixed_content, flags=re.DOTALL)
            
        # Ajouter les styles CSS nécessaires s'ils n'existent pas déjà
        if '.exam-info-table {' not in fixed_content:
            new_css = '''
        /* Styles pour la nouvelle table d'examen */
        .exam-info-table {
            width: 600px;
            border-collapse: collapse;
            margin: 15px 0 20px 0;
            border: 1px solid #000;
        }
        
        .exam-info-table td {
            border: 1px solid #000;
            padding: 8px;
            vertical-align: top;
        }
        
        .exam-title-row td {
            background-color: #ffffff;
            font-weight: bold;
            text-align: center;
            padding: 8px;
            font-size: 12pt;
        }
        
        .exam-number-cell {
            width: 30px;
            text-align: center;
            font-weight: bold;
            font-size: 14pt;
            background-color: #f2f2f2; /* Arrière-plan grisé */
            border: 1px solid #cccccc; /* Bordure légère */
        }
        
        .exam-details-cell {
            width: 370px;
        }
        
        .empty-cell {
            width: 200px;
            border-left: 1px solid #000;
        }
        
        /* Style pour réduire l'interligne dans les cellules d'examen */
        .exam-details-cell .exam-info {
            margin: 1px 0;
            line-height: 1.2;
        }
        
        /* Style pour la ligne de séparation minimale */
        .separator-row {
            height: 5px;
        }'''
            
            # Insérer les nouveaux styles CSS avant la fin de la section style
            fixed_content = fixed_content.replace('    </style>', new_css + '\n    </style>')
    
    # Gérer le bloc d'adresse pour qu'il apparaisse après la table des épreuves
    pattern_address_block = r'<div class="address-text">L\'examen se déroulera à l\'adresse suivante :</div>.*?</table>'
    
    # Si le pattern est trouvé, déplacer le bloc d'adresse après la table d'examen
    if re.search(pattern_address_block, fixed_content, re.DOTALL) and '<table class="exam-info-table">' in fixed_content:
        # Extraire le bloc d'adresse
        address_block = re.search(pattern_address_block, fixed_content, re.DOTALL).group(0)
        
        # Supprimer le bloc adresse de sa position originale s'il est avant la table d'examen
        pattern_check = r'<div class="address-text">.*?</table>\s*<table class="exam-info-table">'
        if re.search(pattern_check, fixed_content, re.DOTALL):
            fixed_content = re.sub(pattern_address_block + r'\s*<table class="exam-info-table">', 
                                  '<table class="exam-info-table">', fixed_content, flags=re.DOTALL)
            
            # Insérer le bloc d'adresse après la table d'examen
            fixed_content = fixed_content.replace('</table>\n\n    {% if tiers_temps %}', 
                                               '</table>\n\n    ' + address_block + '\n\n    {% if tiers_temps %}')
    
    # Écrire le contenu modifié dans le nouveau fichier
    with open(fixed_template, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Template fixé créé: {fixed_template}")
    return fixed_template

def fix_main_template():
    """
    Corrige le template pour éviter les erreurs de type dans main.py
    Doit être appelé depuis main.py
    """
    # Créer le template fixé
    fixed_template = create_fixed_template()
    if not fixed_template:
        return "templates/convocation_delf_template_modele.html"  # Retourner le template original en cas d'échec
    
    return fixed_template

# Pour des tests directs
if __name__ == "__main__":
    fixed_template_path = create_fixed_template()
    print(f"Template fixé: {fixed_template_path}")