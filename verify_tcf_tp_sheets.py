#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérification détaillée des onglets TCF TP dans JURYS FINAL TCF.xlsx
"""

import pandas as pd
import os

def verify_tcf_tp_sheets():
    """Vérifie en détail les onglets TCF TP"""
    
    excel_path = 'JURYS FINAL TCF.xlsx'
    
    print('🔍 VÉRIFICATION DÉTAILLÉE DES ONGLETS TCF TP')
    print('=' * 70)
    print(f'Fichier: {excel_path}\n')
    
    if not os.path.exists(excel_path):
        print(f"❌ Fichier non trouvé: {excel_path}")
        return
    
    sheets_to_check = [
        'TCF TP OBLIGATOIRE',
        'TCF TP EE',
        'TCF TP EO'
    ]
    
    for sheet_name in sheets_to_check:
        print(f'\n📋 ONGLET: {sheet_name}')
        print('-' * 70)
        
        try:
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None, engine='openpyxl')
            
            print(f'📐 Dimensions: {len(df)} lignes x {len(df.columns)} colonnes\n')
            print('📄 Contenu brut (premières lignes):')
            print('-' * 70)
            
            # Afficher les 15 premières lignes
            for idx in range(min(15, len(df))):
                row = df.iloc[idx]
                # Afficher seulement les 4 premières colonnes pour plus de clarté
                values = []
                for i in range(min(4, len(row))):
                    val = row[i]
                    if pd.notna(val):
                        val_str = str(val).strip()
                        if len(val_str) > 30:
                            val_str = val_str[:27] + '...'
                        values.append(val_str)
                    else:
                        values.append('')
                
                print(f'   Ligne {idx:2d}: {" | ".join(values)}')
            
            # Analyse spécifique
            print(f'\n🔎 Analyse des candidats:')
            print('-' * 70)
            
            current_jury = None
            candidates = []
            
            for idx in range(len(df)):
                row = df.iloc[idx]
                
                if pd.isna(row[0]):
                    continue
                
                cell_value = str(row[0]).strip()
                
                # Détection jury
                if 'Jury' in cell_value and cell_value.startswith('Jury'):
                    current_jury = cell_value
                    date = str(row[1]).strip() if len(row) > 1 and pd.notna(row[1]) else 'N/A'
                    print(f'   🏛️ {current_jury} - Date: {date}')
                    continue
                
                # Détection candidat (heure de passage)
                if 'h' in cell_value and len(cell_value) <= 6:
                    heure = cell_value
                    
                    if len(row) > 1 and pd.notna(row[1]):
                        nom = str(row[1]).strip()
                        
                        # Filtrer en-têtes
                        if nom in ['NOM et Prénom', 'Pass.', 'Jury'] or len(nom) <= 3:
                            continue
                        
                        salle = str(row[2]).strip() if len(row) > 2 and pd.notna(row[2]) else ''
                        besoin = str(row[3]).strip() if len(row) > 3 and pd.notna(row[3]) else ''
                        
                        candidates.append({
                            'jury': current_jury or 'N/A',
                            'heure': heure,
                            'nom': nom,
                            'salle': salle,
                            'besoin': besoin
                        })
                        
                        print(f'      ✅ {heure} - {nom}' + 
                              (f' (Salle: {salle})' if salle else '') +
                              (f' [Besoin: {besoin}]' if besoin else ''))
            
            print(f'\n📊 Total candidats détectés: {len(candidates)}')
            
        except Exception as e:
            print(f'❌ Erreur lors de la lecture: {e}')
            import traceback
            print(traceback.format_exc())
    
    print('\n' + '=' * 70)

if __name__ == "__main__":
    verify_tcf_tp_sheets()
