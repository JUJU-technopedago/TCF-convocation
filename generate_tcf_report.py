#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rapport d'analyse complet du fichier JURYS FINAL TCF.xlsx
"""

import pandas as pd
import os

def generate_full_report():
    """Génère un rapport complet d'analyse"""
    
    excel_path = 'JURYS FINAL TCF.xlsx'
    
    print('📊 RAPPORT D\'ANALYSE COMPLET')
    print('=' * 70)
    print(f'Fichier: {excel_path}')
    print(f'Date: 17 novembre 2025\n')
    
    if not os.path.exists(excel_path):
        print(f"❌ Fichier non trouvé")
        return
    
    excel_file = pd.ExcelFile(excel_path, engine='openpyxl')
    
    print(f'✅ Fichier chargé avec succès')
    print(f'📋 Nombre d\'onglets: {len(excel_file.sheet_names)}\n')
    
    # 1. Liste des onglets
    print('1️⃣ ONGLETS PRÉSENTS:\n')
    for i, sheet in enumerate(excel_file.sheet_names, 1):
        is_new = sheet in ['TCF TP EE', 'TCF TP EO']
        marker = '🆕' if is_new else '✅'
        print(f'   {marker} {i}. {sheet}')
    
    # 2. Analyse de l'onglet ADMIN
    print('\n\n2️⃣ CONFIGURATION ADMIN:\n')
    
    admin_df = pd.read_excel(excel_path, sheet_name='ADMIN', header=None, engine='openpyxl')
    
    print('   📅 Durées collectives:')
    for i in range(1, 8):
        if i < len(admin_df):
            type_tcf = admin_df.iloc[i, 0]
            duree = admin_df.iloc[i, 1]
            if pd.notna(type_tcf):
                type_str = str(type_tcf).strip()
                duree_str = str(duree).strip() if pd.notna(duree) else 'NON DÉFINI'
                marker = '🆕' if any(x in type_str for x in ['EE', 'EO', 'Expression']) else '  '
                print(f'      {marker} {type_str}: {duree_str}')
    
    print('\n   ⏱️ Durées individuelles:')
    for i in range(10, 16):
        if i < len(admin_df):
            type_tcf = admin_df.iloc[i, 0]
            duree = admin_df.iloc[i, 1]
            if pd.notna(type_tcf):
                type_str = str(type_tcf).strip()
                duree_str = f'{str(duree).strip()} min' if pd.notna(duree) else 'NON DÉFINI'
                marker = '🆕' if any(x in type_str for x in ['EE', 'EO', 'Expression']) else '  '
                print(f'      {marker} {type_str}: {duree_str}')
    
    # 3. Analyse détaillée par onglet
    print('\n\n3️⃣ ANALYSE PAR ONGLET:\n')
    
    total_jurys = 0
    total_candidates = 0
    
    for sheet_name in excel_file.sheet_names:
        if sheet_name == 'ADMIN':
            continue
        
        df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None, engine='openpyxl')
        
        # Compter les jurys
        jury_count = 0
        candidate_count = 0
        jury_dates = []
        
        for idx in range(len(df)):
            row = df.iloc[idx]
            if pd.notna(row[0]):
                cell_value = str(row[0]).strip()
                
                # Détection jury
                if 'Jury' in cell_value and cell_value.startswith('Jury'):
                    jury_count += 1
                    # Récupérer la date si disponible
                    if len(row) > 1 and pd.notna(row[1]):
                        date_val = str(row[1]).strip()
                        if '/' in date_val or '-' in date_val:
                            jury_dates.append(date_val)
                
                # Détection candidat (heure de passage)
                elif 'h' in cell_value and len(cell_value) <= 6:
                    # Vérifier qu'il y a un nom dans la colonne suivante
                    if len(row) > 1 and pd.notna(row[1]):
                        name = str(row[1]).strip()
                        if len(name) > 3 and name not in ['NOM et Prénom', 'Pass.']:
                            candidate_count += 1
        
        total_jurys += jury_count
        total_candidates += candidate_count
        
        is_new = sheet_name in ['TCF TP EE', 'TCF TP EO']
        marker = '🆕' if is_new else '  '
        
        print(f'   {marker} {sheet_name}:')
        print(f'      📐 Dimensions: {len(df)} lignes x {len(df.columns)} colonnes')
        print(f'      👥 Jurys: {jury_count}')
        print(f'      📝 Candidats: {candidate_count}')
        
        if jury_dates:
            print(f'      📅 Dates: {", ".join(jury_dates[:3])}' + 
                  (f' (+{len(jury_dates)-3} autres)' if len(jury_dates) > 3 else ''))
        
        if is_new and candidate_count == 0:
            print(f'      ⚠️ Onglet vide (template)')
        
        print()
    
    # 4. Statistiques globales
    print('4️⃣ STATISTIQUES GLOBALES:\n')
    print(f'   👥 Total jurys: {total_jurys}')
    print(f'   📝 Total candidats: {total_candidates}')
    print(f'   📊 Moyenne candidats/jury: {total_candidates/total_jurys:.1f}' if total_jurys > 0 else '')
    
    # 5. Validation structure
    print('\n\n5️⃣ VALIDATION DE LA STRUCTURE:\n')
    
    required_sheets = [
        'TCF CANADA',
        'TCF TP COMPLET',
        'TCF TP OBLIGATOIRE',
        'TCF TP EE',
        'TCF TP EO',
        'TCF IRN',
        'ADMIN'
    ]
    
    all_present = True
    for sheet in required_sheets:
        if sheet in excel_file.sheet_names:
            is_new = sheet in ['TCF TP EE', 'TCF TP EO']
            marker = '🆕' if is_new else '✅'
            print(f'   {marker} {sheet}: Présent')
        else:
            print(f'   ❌ {sheet}: MANQUANT')
            all_present = False
    
    # 6. Recommandations
    print('\n\n6️⃣ RECOMMANDATIONS:\n')
    
    if all_present:
        print('   ✅ Structure complète à 7 onglets')
        print('   ✅ Compatible avec le nouveau système')
        print('   ✅ Prêt pour la génération de convocations')
        
        # Vérifier si les nouveaux onglets ont des candidats
        for sheet in ['TCF TP EE', 'TCF TP EO']:
            df = pd.read_excel(excel_path, sheet_name=sheet, header=None, engine='openpyxl')
            candidate_count = 0
            for idx in range(len(df)):
                row = df.iloc[idx]
                if pd.notna(row[0]):
                    cell_value = str(row[0]).strip()
                    if 'h' in cell_value and len(cell_value) <= 6:
                        if len(row) > 1 and pd.notna(row[1]):
                            name = str(row[1]).strip()
                            if len(name) > 3 and name not in ['NOM et Prénom', 'Pass.']:
                                candidate_count += 1
            
            if candidate_count == 0:
                print(f'   💡 {sheet}: Onglet vide - Ajoutez des candidats si nécessaire')
    else:
        print('   ⚠️ Onglets manquants - Ajoutez-les avant utilisation')
    
    # 7. Conclusion
    print('\n\n' + '=' * 70)
    print('📊 CONCLUSION:\n')
    
    if all_present:
        print('   🎉 Le fichier JURYS FINAL TCF.xlsx est parfaitement structuré!')
        print('   ✅ Contient les 7 onglets requis (5 originaux + 2 nouveaux)')
        print('   ✅ Configuration ADMIN présente')
        print(f'   ✅ {total_candidates} candidats répartis sur {total_jurys} jurys')
        print('   🚀 Prêt pour génération avec le système mis à jour')
        
        print('\n   💡 Prochaines étapes:')
        print('      1. Vérifier/compléter les onglets TCF TP EE et EO si nécessaire')
        print('      2. Lancer: python main.py')
        print('      3. Générer les convocations')
        print('      4. Envoyer les emails')
    else:
        print('   ⚠️ Structure incomplète - Ajoutez les onglets manquants')

if __name__ == "__main__":
    generate_full_report()