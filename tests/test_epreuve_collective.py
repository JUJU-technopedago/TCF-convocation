#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la lecture des informations d'épreuve collective
"""

from jury_excel_processor import JuryExcelProcessor

def test_epreuve_collective():
    """Test de la lecture des informations d'épreuve collective"""
    
    print("=== TEST LECTURE ÉPREUVE COLLECTIVE ===\n")
    
    processor = JuryExcelProcessor('juries_20250820_192410.xlsx')
    
    try:
        processor.load_jury_data()
        
        print("Informations d'épreuve collective par niveau:")
        for niveau, data in processor.data.items():
            epreuve_coll = data['epreuve_collective']
            date = epreuve_coll.get('date', 'N/A')
            heure = epreuve_coll.get('debut', 'N/A')
            print(f"  {niveau}: date={date}, heure={heure}")
        
        # Test avec quelques candidats pour voir si les infos sont bien transmises
        print("\nTest avec candidats (premiers de chaque niveau):")
        candidates = processor.get_all_candidates()
        
        niveaux_vus = set()
        for candidat in candidates:
            niveau = candidat['niveau']
            if niveau not in niveaux_vus:
                niveaux_vus.add(niveau)
                print(f"  {niveau} - {candidat['nom']} {candidat['prenom']}:")
                print(f"    Date épreuve collective: {candidat.get('date_ep_coll', 'N/A')}")
                print(f"    Heure épreuve collective: {candidat.get('debut_ep_coll', 'N/A')}")
                print(f"    Date examen individuel: {candidat.get('date_examen', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_epreuve_collective()
