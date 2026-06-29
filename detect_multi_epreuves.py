#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour détecter les candidats inscrits à plusieurs épreuves TCF TP
Uniquement pour: TCF TP OBLIGATOIRE, TCF TP EE, TCF TP EO
"""

import pandas as pd
import os
from collections import defaultdict
import json

def normalize_name(name):
    """Normalise un nom pour la comparaison (minuscules, sans espaces superflus)"""
    if pd.isna(name):
        return ""
    return str(name).strip().lower()

def extract_candidates_from_sheet(excel_path, sheet_name):
    """
    Extrait les candidats d'un onglet spécifique
    Retourne: dict {nom_normalisé: {nom_original, date_jury, heure, autres_infos}}
    """
    candidates = {}
    
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None, engine='openpyxl')
    except Exception as e:
        print(f"❌ Erreur lecture {sheet_name}: {e}")
        return candidates
    
    current_jury_date = None
    in_candidate_section = False
    
    for idx in range(len(df)):
        row = df.iloc[idx]
        
        if pd.isna(row[0]) and (pd.isna(row[1]) if len(row) > 1 else True):
            continue
        
        # Colonne 0 (Pass. ou heure)
        cell_value_0 = str(row[0]).strip() if pd.notna(row[0]) else ""
        # Colonne 1 (NOM et Prénom)
        cell_value_1 = str(row[1]).strip() if len(row) > 1 and pd.notna(row[1]) else ""
        
        # Détection ligne Jury pour récupérer la date
        if 'Jury' in cell_value_0 and cell_value_0.startswith('Jury'):
            if len(row) > 1 and pd.notna(row[1]):
                date_val = str(row[1]).strip()
                if '/' in date_val or '-' in date_val:
                    current_jury_date = date_val
            in_candidate_section = False
            continue
        
        # Détection ligne d'en-tête (Pass. | NOM et Prénom)
        if cell_value_0 in ['Pass.', 'Pass'] or cell_value_1 == 'NOM et Prénom':
            in_candidate_section = True
            continue
        
        # Si on est dans la section candidats, chercher les noms
        if in_candidate_section and cell_value_1:
            nom = cell_value_1
            
            # Filtrer les en-têtes résiduels
            if nom in ['NOM et Prénom', 'Pass.', 'Jury', 'Pass']:
                continue
            
            # Vérifier que c'est un nom valide (plus de 3 caractères)
            if len(nom) > 3:
                nom_normalized = normalize_name(nom)
                
                # Détecter l'heure si présente en colonne 0
                heure = cell_value_0 if ('h' in cell_value_0 and len(cell_value_0) <= 6) else ""
                
                # Colonnes supplémentaires
                date_naissance = str(row[2]).strip() if len(row) > 2 and pd.notna(row[2]) else ""
                email = str(row[3]).strip() if len(row) > 3 and pd.notna(row[3]) else ""
                
                candidates[nom_normalized] = {
                    'nom_original': nom,
                    'date_jury': current_jury_date,
                    'heure': heure,
                    'date_naissance': date_naissance,
                    'email': email,
                    'sheet': sheet_name
                }
    
    return candidates

def detect_multi_epreuves(excel_path='JURYS FINAL TCF.xlsx'):
    """
    Détecte les candidats inscrits à plusieurs épreuves
    """
    
    print('🔍 DÉTECTION DES CANDIDATS MULTI-ÉPREUVES')
    print('=' * 70)
    print(f'Fichier: {excel_path}\n')
    
    if not os.path.exists(excel_path):
        print(f"❌ Fichier non trouvé: {excel_path}")
        return
    
    # Onglets à analyser
    sheets_to_check = [
        'TCF TP OBLIGATOIRE',
        'TCF TP EE',
        'TCF TP EO'
    ]
    
    # Extraction des candidats par onglet
    print('📋 Extraction des candidats par onglet...\n')
    
    all_candidates = {}  # {sheet_name: {nom_normalisé: infos}}
    
    for sheet in sheets_to_check:
        candidates = extract_candidates_from_sheet(excel_path, sheet)
        all_candidates[sheet] = candidates
        print(f'   ✅ {sheet}: {len(candidates)} candidat(s)')
    
    # Détection des doublons
    print('\n\n🔎 Analyse des candidats présents dans plusieurs onglets...\n')
    
    # Regrouper par nom normalisé
    name_to_sheets = defaultdict(list)
    
    for sheet, candidates in all_candidates.items():
        for name_normalized, info in candidates.items():
            name_to_sheets[name_normalized].append({
                'sheet': sheet,
                'info': info
            })
    
    # Filtrer les candidats présents dans plusieurs onglets
    multi_epreuves = {}
    
    for name_normalized, occurrences in name_to_sheets.items():
        if len(occurrences) > 1:
            multi_epreuves[name_normalized] = occurrences
    
    # Affichage des résultats
    if not multi_epreuves:
        print('   ℹ️ Aucun candidat inscrit à plusieurs épreuves')
        print('\n' + '=' * 70)
        return {}
    
    print(f'   🎯 {len(multi_epreuves)} candidat(s) inscrit(s) à plusieurs épreuves\n')
    
    # Statistiques par combinaison
    combinations_stats = defaultdict(int)
    
    for name_normalized, occurrences in multi_epreuves.items():
        sheets = sorted([occ['sheet'] for occ in occurrences])
        combination_key = ' + '.join([s.replace('TCF TP ', '') for s in sheets])
        combinations_stats[combination_key] += 1
    
    print('📊 Répartition par type de combinaison:\n')
    for combo, count in sorted(combinations_stats.items()):
        print(f'   • {combo}: {count} candidat(s)')
    
    # Détail par candidat
    print('\n\n👥 DÉTAIL PAR CANDIDAT:')
    print('=' * 70)
    
    for idx, (name_normalized, occurrences) in enumerate(sorted(multi_epreuves.items(), key=lambda x: x[1][0]['info']['nom_original']), 1):
        nom_original = occurrences[0]['info']['nom_original']
        
        print(f'\n{idx}. {nom_original}')
        print('   ' + '-' * 66)
        
        for occ in sorted(occurrences, key=lambda x: x['sheet']):
            sheet = occ['sheet']
            info = occ['info']
            
            sheet_display = sheet.replace('TCF TP ', '')
            
            print(f'   📌 {sheet_display}')
            print(f'      📅 Date: {info["date_jury"] or "Non définie"}')
            if info['heure']:
                print(f'      ⏰ Heure: {info["heure"]}')
            if info.get('date_naissance'):
                print(f'      🎂 Date naissance: {info["date_naissance"]}')
            if info.get('email'):
                print(f'      📧 Email: {info["email"]}')
    
    # Sauvegarde en JSON
    output_file = 'candidats_multi_epreuves.json'
    
    export_data = {}
    for name_normalized, occurrences in multi_epreuves.items():
        nom_original = occurrences[0]['info']['nom_original']
        
        export_data[nom_original] = {
            'epreuves': []
        }
        
        for occ in occurrences:
            sheet = occ['sheet']
            info = occ['info']
            
            export_data[nom_original]['epreuves'].append({
                'type_epreuve': sheet.replace('TCF TP ', ''),
                'date_jury': info['date_jury'],
                'heure': info['heure'],
                'date_naissance': info.get('date_naissance', ''),
                'email': info.get('email', '')
            })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print('\n\n' + '=' * 70)
    print(f'💾 Résultats sauvegardés dans: {output_file}')
    print('=' * 70)
    
    return export_data

def generate_combination_summary(excel_path='JURYS FINAL TCF.xlsx'):
    """
    Génère un résumé des combinaisons possibles
    """
    multi_epreuves = detect_multi_epreuves(excel_path)
    
    if not multi_epreuves:
        return
    
    print('\n\n📋 TYPES DE CONVOCATIONS À GÉNÉRER:')
    print('=' * 70)
    
    combinations = defaultdict(list)
    
    for nom, data in multi_epreuves.items():
        epreuves_types = sorted([ep['type_epreuve'] for ep in data['epreuves']])
        combo_key = ' + '.join(epreuves_types)
        combinations[combo_key].append(nom)
    
    for combo, names in sorted(combinations.items()):
        print(f'\n🎯 {combo} ({len(names)} candidat(s)):')
        for name in sorted(names):
            print(f'   • {name}')
    
    print('\n' + '=' * 70)
    print('💡 PROCHAINES ÉTAPES:')
    print('=' * 70)
    print('1. Générer des convocations combinées pour ces candidats')
    print('2. Fusionner les horaires et dates sur un seul document')
    print('3. Indiquer clairement les différentes épreuves')
    print('=' * 70)

if __name__ == "__main__":
    generate_combination_summary()
