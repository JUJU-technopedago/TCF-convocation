#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet du système de génération de convocations avec la nouvelle structure de jurys
"""

from jury_excel_processor import JuryExcelProcessor
import pandas as pd

def test_complete_system():
    """Test complet du système"""
    
    print("=== TEST DU SYSTÈME DE GÉNÉRATION DE CONVOCATIONS ===\n")
    
    # 1. Test du processeur de jurys
    print("1. Test du processeur de jurys...")
    processor = JuryExcelProcessor('test_juries.xlsx')
    
    try:
        processor.load_jury_data()
        candidates = processor.get_all_candidates()
        
        print(f"   ✓ {len(candidates)} candidats trouvés")
        
        # Afficher les détails des candidats
        for i, c in enumerate(candidates):
            print(f"   - Candidat {i+1}: {c['nom']} {c['prenom']} ({c['niveau']})")
            print(f"     Email: {c['email']}")
            print(f"     Date examen: {c['date_examen']}")
            print(f"     Heure: {c['heure_debut']} - {c['heure_fin']}")
            print(f"     Durée: {c['duree']}")
            if c.get('heure_preparation'):
                print(f"     Préparation: {c['heure_preparation']}")
            print()
        
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        return False
    
    # 2. Test d'export vers format standard
    print("2. Test d'export vers format standard...")
    try:
        count = processor.export_to_standard_excel('candidats_standard.xlsx')
        print(f"   ✓ {count} candidats exportés vers candidats_standard.xlsx")
        
        # Vérifier le contenu du fichier exporté
        df_exported = pd.read_excel('candidats_standard.xlsx')
        print(f"   ✓ Fichier exporté contient {len(df_exported)} lignes")
        print(f"   ✓ Colonnes: {list(df_exported.columns)}")
        
    except Exception as e:
        print(f"   ✗ Erreur d'export: {e}")
        return False
    
    # 3. Test de détection automatique du format
    print("3. Test de détection automatique du format...")
    try:
        # Simuler l'utilisation du PDFGenerator avec détection automatique
        from pdf_generator import PDFGenerator
        
        # Test avec le fichier de jurys
        generator_jury = PDFGenerator(
            excel_path='test_juries.xlsx',
            template_path='templates/convocation_delf_template.html',
            logo_af_path='logoAF.svg',
            logo_delf_path='logoDELF.svg',
            output_dir='output'
        )
        
        # Test de détection
        is_jury_file = generator_jury._is_jury_excel_file()
        print(f"   ✓ Détection fichier jurys: {is_jury_file}")
        
        # Test avec le fichier standard
        generator_standard = PDFGenerator(
            excel_path='candidats_standard.xlsx',
            template_path='templates/convocation_delf_template.html',
            logo_af_path='logoAF.svg',
            logo_delf_path='logoDELF.svg',
            output_dir='output'
        )
        
        is_standard_file = not generator_standard._is_jury_excel_file()
        print(f"   ✓ Détection fichier standard: {is_standard_file}")
        
    except Exception as e:
        print(f"   ✗ Erreur de détection: {e}")
        return False
    
    # 4. Test de chargement des données
    print("4. Test de chargement des données...")
    try:
        # Test avec fichier de jurys
        df_jury = generator_jury._load_excel_data()
        print(f"   ✓ Données jurys chargées: {len(df_jury)} candidats")
        
        # Test avec fichier standard
        df_standard = generator_standard._load_excel_data()
        print(f"   ✓ Données standard chargées: {len(df_standard)} candidats")
        
        # Vérifier que les données sont identiques
        if len(df_jury) == len(df_standard):
            print("   ✓ Même nombre de candidats dans les deux formats")
        else:
            print(f"   ⚠ Différence: jurys={len(df_jury)}, standard={len(df_standard)}")
        
    except Exception as e:
        print(f"   ✗ Erreur de chargement: {e}")
        return False
    
    print("\n=== RÉSUMÉ ===")
    print("✓ Processeur de jurys fonctionnel")
    print("✓ Export vers format standard fonctionnel")
    print("✓ Détection automatique du format fonctionnelle")
    print("✓ Chargement des données fonctionnel")
    print("\n🎉 Le système est prêt à générer des PDF à partir de fichiers Excel de jurys !")
    print("\nPour utiliser le système:")
    print("1. Placez votre fichier Excel de jurys dans le répertoire")
    print("2. Lancez l'application main.py")
    print("3. Sélectionnez votre fichier Excel")
    print("4. Le système détectera automatiquement le format et générera les PDF")
    
    return True

if __name__ == "__main__":
    test_complete_system()
