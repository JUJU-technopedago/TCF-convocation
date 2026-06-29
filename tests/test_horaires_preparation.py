#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test spécifique pour vérifier la lecture des horaires de préparation individuelle
dans TOUS les onglets du fichier Excel
"""

from jury_excel_processor import JuryExcelProcessor

def test_horaires_preparation():
    """Test de la lecture des horaires de préparation individuelle"""
    
    print("=== TEST LECTURE HORAIRES PRÉPARATION INDIVIDUELLE ===\n")
    
    processor = JuryExcelProcessor('juries_20250820_192410.xlsx')
    
    try:
        processor.load_jury_data()
        
        print("Vérification des horaires de préparation par niveau:")
        
        for niveau, data in processor.data.items():
            print(f"\n--- NIVEAU {niveau} ---")
            
            # Vérifier les candidats de ce niveau
            candidats = processor.get_candidates_by_level(niveau)
            
            if not candidats:
                print(f"  ❌ Aucun candidat trouvé pour le niveau {niveau}")
                continue
            
            print(f"  Nombre de candidats: {len(candidats)}")
            
            # Vérifier les horaires pour les premiers candidats
            for i, candidat in enumerate(candidats[:3]):  # Premiers 3 candidats
                nom_complet = f"{candidat['nom']} {candidat['prenom']}"
                heure_prep = candidat.get('heure_preparation', 'N/A')
                heure_pass = candidat.get('heure_passage', 'N/A')
                
                print(f"  Candidat {i+1}: {nom_complet}")
                print(f"    Heure préparation: {heure_prep}")
                print(f"    Heure passage: {heure_pass}")
                
                # Vérifier si les horaires sont vides ou "nan"
                if heure_prep in ['', 'N/A', 'nan', None] or heure_pass in ['', 'N/A', 'nan', None]:
                    print(f"    ❌ PROBLÈME: Horaires manquants pour {nom_complet}")
                else:
                    print(f"    ✅ Horaires OK pour {nom_complet}")
        
        # Résumé global
        print("\n=== RÉSUMÉ GLOBAL ===")
        all_candidates = processor.get_all_candidates()
        
        problemes_par_niveau = {}
        
        for candidat in all_candidates:
            niveau = candidat['niveau']
            heure_prep = candidat.get('heure_preparation', 'N/A')
            heure_pass = candidat.get('heure_passage', 'N/A')
            
            if niveau not in problemes_par_niveau:
                problemes_par_niveau[niveau] = {'total': 0, 'problemes': 0}
            
            problemes_par_niveau[niveau]['total'] += 1
            
            if heure_prep in ['', 'N/A', 'nan', None] or heure_pass in ['', 'N/A', 'nan', None]:
                problemes_par_niveau[niveau]['problemes'] += 1
        
        for niveau, stats in problemes_par_niveau.items():
            total = stats['total']
            problemes = stats['problemes']
            pourcentage = (problemes / total * 100) if total > 0 else 0
            
            if problemes > 0:
                print(f"❌ {niveau}: {problemes}/{total} candidats avec horaires manquants ({pourcentage:.1f}%)")
            else:
                print(f"✅ {niveau}: Tous les horaires OK ({total} candidats)")
        
        return True
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_horaires_preparation()
