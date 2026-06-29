#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VALIDATION DYNAMIQUE - Vérifie que le système s'adapte au nombre réel de candidats
"""

import json
import os
from datetime import datetime

def validate_dynamic_system():
    """Valide que le système fonctionne de manière dynamique"""
    
    print("VALIDATION SYSTÈME DYNAMIQUE")
    print("=" * 50)
    print(f"Date/Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Vérifier les candidats dans Excel
    try:
        from tcf_excel_processor import TCFExcelProcessor
        excel_path = r"C:\Users\JMM\Desktop\convoc generator TCF\JURYS FINAL TCF.xlsx"
        
        print(f"\n1. ANALYSE DU FICHIER EXCEL:")
        print(f"   Fichier: {excel_path}")
        
        processor = TCFExcelProcessor(excel_path)
        processor.load_tcf_data()
        excel_candidates = processor.get_all_candidates()
        
        print(f"   Candidats dans Excel: {len(excel_candidates)}")
        
        # Échantillon
        print(f"\n   Échantillon (premiers 3):")
        for i, candidate in enumerate(excel_candidates[:3], 1):
            nom = candidate.get('nom', 'INCONNU')
            prenom = candidate.get('prenom', '')
            email = candidate.get('email', 'N/A')
            print(f"      {i}. {prenom} {nom} ({email})")
        
    except Exception as e:
        print(f"   ERREUR Excel: {e}")
        excel_candidates = []
    
    # 2. Vérifier le registre dans output
    output_dir = r"C:\Users\JMM\Desktop\convoc generator TCF\output"
    registry_path = os.path.join(output_dir, "candidate_pdf_registry.json")
    
    print(f"\n2. ANALYSE DU REGISTRE OUTPUT:")
    print(f"   Fichier: {registry_path}")
    
    if os.path.exists(registry_path):
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            
            print(f"   Candidats dans registre: {len(registry)}")
            
            # Analyser la qualité
            valid_count = 0
            inconnu_count = 0
            
            for candidate_id, info in registry.items():
                nom = info.get('nom', 'INCONNU')
                if nom != 'INCONNU':
                    valid_count += 1
                else:
                    inconnu_count += 1
            
            print(f"   Candidats valides: {valid_count}")
            print(f"   Candidats INCONNU: {inconnu_count}")
            
            if len(registry) > 0:
                ratio = valid_count / len(registry) * 100
                print(f"   Ratio validité: {ratio:.1f}%")
            
        except Exception as e:
            print(f"   ERREUR Registre: {e}")
            registry = {}
    else:
        print(f"   Registre non trouvé")
        registry = {}
    
    # 3. Comparaison et validation
    print(f"\n3. VALIDATION DYNAMIQUE:")
    
    if len(excel_candidates) == 0:
        print("   ❌ PROBLÈME: Aucun candidat dans Excel")
        return False
    
    if len(registry) == 0:
        print("   ⚠️ NORMAL: Registre vide (génération PDF requise)")
        print(f"   📊 Le système devra traiter {len(excel_candidates)} candidats")
        return True
    
    # Comparer les nombres
    excel_count = len(excel_candidates)
    registry_count = len(registry)
    
    print(f"   Excel: {excel_count} candidats")
    print(f"   Registre: {registry_count} candidats")
    
    if excel_count == registry_count:
        print("   ✅ PARFAIT: Nombre cohérent Excel-Registre")
        
        if valid_count == registry_count:
            print("   ✅ PARFAIT: Tous les candidats du registre sont valides")
            print("   🎯 SYSTÈME OPTIMAL: Prêt pour envoi d'emails")
            return True
        else:
            ratio = valid_count / registry_count * 100
            if ratio >= 90:
                print(f"   ✅ BON: {ratio:.1f}% des candidats sont valides")
                return True
            elif ratio >= 50:
                print(f"   ⚠️ ACCEPTABLE: {ratio:.1f}% des candidats sont valides")
                print("   💡 Conseil: Régénération recommandée pour optimiser")
                return True
            else:
                print(f"   ❌ PROBLÈME: Seulement {ratio:.1f}% des candidats sont valides")
                return False
    else:
        diff = abs(excel_count - registry_count)
        print(f"   ⚠️ DIFFÉRENCE: {diff} candidats de différence")
        
        if registry_count < excel_count:
            print("   📊 Le registre contient moins de candidats que l'Excel")
            print("   💡 Conseil: Régénérez les PDFs pour traiter tous les candidats")
        else:
            print("   📊 Le registre contient plus de candidats que l'Excel")
            print("   💡 Possible: Données Excel mises à jour depuis la dernière génération")
        
        return True
    
    # 4. Recommandations
    print(f"\n4. RECOMMANDATIONS:")
    
    if len(registry) == 0:
        print("   1. Générer les PDFs pour créer le registre")
        print("   2. L'envoi d'emails sera alors possible")
    elif excel_count != registry_count:
        print("   1. Régénérer les PDFs pour synchroniser")
        print("   2. Cela videra output et recréera tout")
    elif valid_count < registry_count:
        print("   1. Régénérer les PDFs pour corriger les candidats INCONNU")
        print("   2. Améliorer la qualité du registre")
    else:
        print("   1. Système prêt pour envoi d'emails")
        print("   2. Aucune action requise")
    
    print(f"\n5. CONCLUSION:")
    print("   Le système est 100% dynamique et s'adapte automatiquement")
    print(f"   au nombre réel de candidats ({excel_count} dans ce cas)")
    
    return True

if __name__ == "__main__":
    validate_dynamic_system()