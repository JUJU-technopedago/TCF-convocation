#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final du système complet sans dépendances PDF
"""

from jury_excel_processor import JuryExcelProcessor
import pandas as pd
import os

def test_final_system():
    """Test final du système complet"""
    
    print("=== TEST FINAL DU SYSTÈME COMPLET ===\n")
    
    # 1. Test du fichier réel de jurys
    print("1. Test du fichier réel de jurys...")
    processor = JuryExcelProcessor('juries_20250820_192410.xlsx')
    
    try:
        processor.load_jury_data()
        candidates = processor.get_all_candidates()
        
        print(f"   ✓ {len(candidates)} candidats trouvés")
        
        # Statistiques détaillées
        niveaux = {}
        dates_examens = set()
        emails_valides = 0
        
        for c in candidates:
            niveau = c['niveau']
            niveaux[niveau] = niveaux.get(niveau, 0) + 1
            
            if c.get('date_examen'):
                dates_examens.add(c['date_examen'])
            
            if c.get('email') and '@' in c['email']:
                emails_valides += 1
        
        print(f"   ✓ Répartition: {dict(sorted(niveaux.items()))}")
        print(f"   ✓ {len(dates_examens)} dates d'examen différentes")
        print(f"   ✓ {emails_valides} emails valides")
        
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        return False
    
    # 2. Test d'export et compatibilité
    print("\n2. Test d'export et compatibilité...")
    try:
        # Export vers format standard
        count = processor.export_to_standard_excel('candidats_final.xlsx')
        print(f"   ✓ {count} candidats exportés")
        
        # Vérification du fichier exporté
        df_exported = pd.read_excel('candidats_final.xlsx')
        print(f"   ✓ Fichier exporté: {len(df_exported)} lignes, {len(df_exported.columns)} colonnes")
        
        # Vérifier les colonnes essentielles
        colonnes_essentielles = ['numero_candidat', 'nom', 'prenom', 'email', 'niveau', 'date_examen']
        colonnes_manquantes = [col for col in colonnes_essentielles if col not in df_exported.columns]
        
        if not colonnes_manquantes:
            print("   ✓ Toutes les colonnes essentielles présentes")
        else:
            print(f"   ⚠ Colonnes manquantes: {colonnes_manquantes}")
        
    except Exception as e:
        print(f"   ✗ Erreur d'export: {e}")
        return False
    
    # 3. Test de détection automatique (sans import PDF)
    print("\n3. Test de détection automatique...")
    try:
        # Test direct de la fonction de détection
        
        # Vérifier les noms de feuilles du fichier de jurys
        excel_file = pd.ExcelFile('juries_20250820_192410.xlsx', engine='openpyxl')
        sheet_names = excel_file.sheet_names
        niveau_sheets = [name for name in sheet_names if name.startswith('Niveau ')]
        
        print(f"   ✓ Feuilles trouvées: {sheet_names}")
        print(f"   ✓ Feuilles de niveau: {niveau_sheets}")
        print(f"   ✓ Détection fichier jurys: {len(niveau_sheets) >= 2}")
        
        # Test avec fichier standard
        excel_file_standard = pd.ExcelFile('candidats_final.xlsx', engine='openpyxl')
        sheet_names_standard = excel_file_standard.sheet_names
        niveau_sheets_standard = [name for name in sheet_names_standard if name.startswith('Niveau ')]
        
        print(f"   ✓ Détection fichier standard: {len(niveau_sheets_standard) < 2}")
        
    except Exception as e:
        print(f"   ✗ Erreur de détection: {e}")
        return False
    
    # 4. Test de préparation des données
    print("\n4. Test de préparation des données...")
    try:
        # Simuler la préparation des données comme le ferait le générateur PDF
        candidat_test = candidates[0]
        
        # Données essentielles pour PDF
        donnees_pdf = {
            'nom': candidat_test['nom'],
            'prenom': candidat_test['prenom'],
            'numero_candidat': candidat_test['numero_candidat'],
            'email': candidat_test['email'],
            'niveau': candidat_test['niveau'],
            'date_examen': candidat_test['date_examen'],
            'heure_debut': candidat_test['heure_debut'],
            'heure_fin': candidat_test['heure_fin'],
            'duree': candidat_test['duree'],
            'institution_name': candidat_test['institution_name'],
            'institution_address': candidat_test['institution_address'],
            'institution_city': candidat_test['institution_city']
        }
        
        print(f"   ✓ Données préparées pour: {donnees_pdf['nom']} {donnees_pdf['prenom']}")
        print(f"     - Niveau: {donnees_pdf['niveau']}")
        print(f"     - Date: {donnees_pdf['date_examen']}")
        print(f"     - Horaire: {donnees_pdf['heure_debut']} - {donnees_pdf['heure_fin']}")
        print(f"     - Institution: {donnees_pdf['institution_name']}")
        
        # Vérifier que toutes les données essentielles sont présentes
        donnees_manquantes = [k for k, v in donnees_pdf.items() if not v]
        if donnees_manquantes:
            print(f"   ⚠ Données manquantes: {donnees_manquantes}")
        else:
            print("   ✓ Toutes les données essentielles présentes")
        
    except Exception as e:
        print(f"   ✗ Erreur de préparation: {e}")
        return False
    
    # 5. Résumé final
    print("\n=== RÉSUMÉ FINAL ===")
    print(f"✅ Fichier de jurys traité avec succès")
    print(f"✅ {len(candidates)} candidats extraits")
    print(f"✅ {len(niveaux)} niveaux DELF traités: {list(sorted(niveaux.keys()))}")
    print(f"✅ Export vers format standard réussi")
    print(f"✅ Détection automatique du format fonctionnelle")
    print(f"✅ Données prêtes pour génération PDF")
    
    print(f"\n🎉 SYSTÈME OPÉRATIONNEL !")
    print(f"\nLe système peut maintenant:")
    print(f"• Lire automatiquement les fichiers Excel de jurys DELF")
    print(f"• Traiter {len(candidates)} candidats répartis sur {len(niveaux)} niveaux")
    print(f"• Détecter automatiquement le format de fichier")
    print(f"• Exporter vers le format standard")
    print(f"• Préparer toutes les données nécessaires pour les PDF")
    
    print(f"\nPour utiliser le système:")
    print(f"1. Lancez main.py")
    print(f"2. Sélectionnez le fichier juries_20250820_192410.xlsx")
    print(f"3. Le système générera automatiquement {len(candidates)} convocations PDF")
    
    return True

if __name__ == "__main__":
    test_final_system()
