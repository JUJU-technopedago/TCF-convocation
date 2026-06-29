#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validateur de fichier Excel TCF - Vérification de la structure à 7 onglets
"""

import pandas as pd
import os
import sys

def validate_tcf_excel_structure(excel_path):
    """
    Valide qu'un fichier Excel TCF contient la structure requise avec 7 onglets
    
    Args:
        excel_path (str): Chemin vers le fichier Excel à valider
        
    Returns:
        tuple: (bool, list) - (succès, liste des erreurs/avertissements)
    """
    
    print("🔍 VALIDATION DU FICHIER EXCEL TCF")
    print("=" * 60)
    print(f"📁 Fichier : {excel_path}\n")
    
    errors = []
    warnings = []
    
    # 1. Vérifier que le fichier existe
    if not os.path.exists(excel_path):
        errors.append(f"❌ Le fichier n'existe pas : {excel_path}")
        return False, errors
    
    try:
        # 2. Charger le fichier Excel
        excel_file = pd.ExcelFile(excel_path, engine='openpyxl')
        
        print(f"✅ Fichier Excel chargé avec succès")
        print(f"📊 Nombre d'onglets : {len(excel_file.sheet_names)}\n")
        
        # 3. Vérifier les onglets requis
        required_sheets = [
            'TCF CANADA',
            'TCF TP COMPLET',
            'TCF TP OBLIGATOIRE',
            'TCF TP EE',
            'TCF TP EO',
            'TCF IRN',
            'ADMIN'
        ]
        
        print("📋 VÉRIFICATION DES ONGLETS REQUIS:")
        
        all_sheets_present = True
        for sheet_name in required_sheets:
            if sheet_name in excel_file.sheet_names:
                is_new = sheet_name in ['TCF TP EE', 'TCF TP EO']
                marker = "🆕" if is_new else "✅"
                print(f"   {marker} {sheet_name} : Présent")
            else:
                print(f"   ❌ {sheet_name} : MANQUANT")
                errors.append(f"Onglet manquant : {sheet_name}")
                all_sheets_present = False
        
        # 4. Vérifier les onglets supplémentaires
        extra_sheets = [s for s in excel_file.sheet_names if s not in required_sheets]
        if extra_sheets:
            print(f"\n⚠️ ONGLETS SUPPLÉMENTAIRES (seront ignorés):")
            for sheet in extra_sheets:
                print(f"   ⚪ {sheet}")
                warnings.append(f"Onglet supplémentaire ignoré : {sheet}")
        
        # 5. Vérifier l'onglet ADMIN
        print(f"\n⚙️ VÉRIFICATION DE L'ONGLET ADMIN:")
        
        if 'ADMIN' in excel_file.sheet_names:
            admin_df = pd.read_excel(excel_path, sheet_name='ADMIN', header=None, engine='openpyxl')
            
            # Vérifier les durées collectives
            print(f"   📅 Durées collectives:")
            collective_types = ['TCF CANADA', 'TCF TP COMPLET', 'TCF TP OBLIGATOIRE', 'TCF TP EE', 'TCF IRN']
            found_collective = 0
            
            for i in range(1, 6):  # lignes 2 à 6
                if i < len(admin_df):
                    type_tcf = admin_df.iloc[i, 0]
                    duree = admin_df.iloc[i, 1]
                    
                    if pd.notna(type_tcf):
                        type_str = str(type_tcf).strip()
                        duree_str = str(duree).strip() if pd.notna(duree) else "MANQUANT"
                        
                        # Vérifier chaque type
                        for ct in collective_types:
                            if ct in type_str or ct.replace(' ', '') in type_str.replace(' ', ''):
                                is_new = ct == 'TCF TP EE'
                                marker = "🆕" if is_new else "✅"
                                print(f"      {marker} {ct} : {duree_str}")
                                found_collective += 1
                                break
            
            if found_collective < len(collective_types):
                msg = f"Seulement {found_collective}/{len(collective_types)} durées collectives trouvées"
                warnings.append(msg)
                print(f"      ⚠️ {msg}")
            
            # Vérifier les durées individuelles
            print(f"\n   ⏱️ Durées individuelles:")
            individual_types = ['TCF CANADA', 'TCF TP COMPLET', 'TCF TP EO', 'TCF IRN']
            found_individual = 0
            
            for i in range(10, 15):  # lignes 11 à 15
                if i < len(admin_df):
                    type_tcf = admin_df.iloc[i, 0]
                    duree = admin_df.iloc[i, 1]
                    
                    if pd.notna(type_tcf):
                        type_str = str(type_tcf).strip()
                        duree_str = f"{str(duree).strip()} minutes" if pd.notna(duree) else "MANQUANT"
                        
                        # Vérifier chaque type
                        for it in individual_types:
                            if it in type_str or it.replace(' ', '') in type_str.replace(' ', ''):
                                is_new = it == 'TCF TP EO'
                                marker = "🆕" if is_new else "✅"
                                print(f"      {marker} {it} : {duree_str}")
                                found_individual += 1
                                break
            
            if found_individual < len(individual_types):
                msg = f"Seulement {found_individual}/{len(individual_types)} durées individuelles trouvées"
                warnings.append(msg)
                print(f"      ⚠️ {msg}")
        
        # 6. Vérifier les nouveaux onglets TCF TP EE et EO
        print(f"\n🆕 VÉRIFICATION DES NOUVEAUX ONGLETS:")
        
        for new_sheet in ['TCF TP EE', 'TCF TP EO']:
            if new_sheet in excel_file.sheet_names:
                df = pd.read_excel(excel_path, sheet_name=new_sheet, header=None, engine='openpyxl')
                rows = len(df)
                print(f"   ✅ {new_sheet} : {rows} lignes")
                
                if rows < 3:
                    warnings.append(f"{new_sheet} : Très peu de données ({rows} lignes)")
            else:
                print(f"   ⚪ {new_sheet} : Absent (optionnel)")
        
        # 7. Résumé
        print(f"\n📊 RÉSUMÉ DE LA VALIDATION:")
        print(f"   ✅ Onglets requis : {7 - len([e for e in errors if 'Onglet manquant' in e])}/7")
        print(f"   ⚠️ Avertissements : {len(warnings)}")
        print(f"   ❌ Erreurs : {len(errors)}")
        
        if len(errors) == 0 and len(warnings) == 0:
            print(f"\n🎉 VALIDATION COMPLÈTE RÉUSSIE !")
            print(f"   ✅ Le fichier est correctement structuré")
            print(f"   ✅ Tous les onglets requis sont présents")
            print(f"   ✅ Aucun problème détecté")
            return True, []
        elif len(errors) == 0:
            print(f"\n⚠️ VALIDATION RÉUSSIE AVEC AVERTISSEMENTS")
            print(f"   ✅ Le fichier peut être utilisé")
            print(f"   ⚠️ Quelques avertissements à considérer:")
            for warning in warnings:
                print(f"      • {warning}")
            return True, warnings
        else:
            print(f"\n❌ VALIDATION ÉCHOUÉE")
            print(f"   ❌ Le fichier présente des erreurs:")
            for error in errors:
                print(f"      • {error}")
            if warnings:
                print(f"   ⚠️ Avertissements additionnels:")
                for warning in warnings:
                    print(f"      • {warning}")
            return False, errors + warnings
            
    except Exception as e:
        error_msg = f"Erreur lors de la lecture du fichier : {str(e)}"
        print(f"\n❌ {error_msg}")
        errors.append(error_msg)
        return False, errors

def main():
    """Fonction principale"""
    
    print("🧪 VALIDATEUR DE FICHIER EXCEL TCF")
    print("=" * 60)
    print("Vérifie la structure à 7 onglets\n")
    
    # Vérifier si un fichier est spécifié en argument
    if len(sys.argv) > 1:
        excel_path = sys.argv[1]
    else:
        # Utiliser le fichier par défaut
        excel_path = "JURYS FINAL TCF.xlsx"
        print(f"💡 Aucun fichier spécifié, utilisation du fichier par défaut:")
        print(f"   {excel_path}\n")
    
    # Valider le fichier
    success, issues = validate_tcf_excel_structure(excel_path)
    
    # Afficher les instructions
    print(f"\n💡 UTILISATION:")
    print(f"   python validate_tcf_excel.py [chemin_vers_fichier.xlsx]")
    print(f"\n💡 EXEMPLE:")
    print(f"   python validate_tcf_excel.py \"JURYS FINAL TCF.xlsx\"")
    
    # Code de sortie
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())