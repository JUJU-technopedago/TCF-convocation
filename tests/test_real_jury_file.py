#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du fichier réel de jurys corrigé
"""

from jury_excel_processor import JuryExcelProcessor

def test_real_jury_file():
    """Test du fichier réel de jurys"""
    
    print("=== TEST DU FICHIER RÉEL DE JURYS ===\n")
    
    processor = JuryExcelProcessor('juries_20250820_192410.xlsx')
    
    try:
        print("Chargement des données...")
        processor.load_jury_data()
        candidates = processor.get_all_candidates()
        
        print(f"✓ {len(candidates)} candidats trouvés au total\n")
        
        # Statistiques par niveau
        niveaux = {}
        for c in candidates:
            niveau = c['niveau']
            if niveau not in niveaux:
                niveaux[niveau] = 0
            niveaux[niveau] += 1
        
        print("Répartition par niveau:")
        for niveau, count in sorted(niveaux.items()):
            print(f"  - {niveau}: {count} candidats")
        
        print("\nPremiers candidats de chaque niveau:")
        for niveau in sorted(niveaux.keys()):
            candidats_niveau = [c for c in candidates if c['niveau'] == niveau]
            if candidats_niveau:
                c = candidats_niveau[0]
                print(f"  {niveau}: {c['nom']} {c['prenom']} - {c['email']}")
                if c.get('date_examen'):
                    print(f"       Date: {c['date_examen']}")
                if c.get('heure_preparation'):
                    print(f"       Préparation: {c['heure_preparation']}")
        
        # Test d'export
        print(f"\nExport vers fichier standard...")
        count = processor.export_to_standard_excel('candidats_real.xlsx')
        print(f"✓ {count} candidats exportés vers candidats_real.xlsx")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_real_jury_file()
