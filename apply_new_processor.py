import os
import shutil

def apply_fix():
    """Remplace le fichier jury_excel_processor.py par la version simplifiée"""
    try:
        # Créer une sauvegarde du fichier original si elle n'existe pas déjà
        if not os.path.exists("jury_excel_processor.py.original"):
            shutil.copy("jury_excel_processor.py", "jury_excel_processor.py.original")
            print("Sauvegarde du fichier original créée: jury_excel_processor.py.original")
        
        # Remplacer le fichier par la nouvelle version
        shutil.copy("jury_excel_processor_new.py", "jury_excel_processor.py")
        print("Fichier jury_excel_processor.py remplacé par la version simplifiée")
        
        # Tester la nouvelle version
        print("\nTest de la nouvelle version...")
        import jury_excel_processor
        
        processor = jury_excel_processor.JuryExcelProcessor("JURYS.xlsx")
        try:
            processor.load_jury_data()
            candidates = processor.get_all_candidates()
            print(f"Succès! {len(candidates)} candidats trouvés")
            
            # Vérifier si SIANO est correctement traité
            siano = None
            for candidate in candidates:
                if candidate.get('nom', '') == 'SIANO' and candidate.get('prenom', '') == 'Marco':
                    siano = candidate
                    break
            
            if siano:
                print("\nInformations pour SIANO Marco:")
                print(f"  - Besoins spéciaux: {siano.get('besoins_speciaux', False)}")
                print(f"  - Tiers-temps: {siano.get('tiers_temps', False)}")
                print(f"  - Fin épreuve: {siano.get('fin_ep_coll', 'Non définie')}")
                print(f"  - Affichage: {siano.get('fin_ep_coll_affichage', 'Non défini')}")
            else:
                print("\nSIANO Marco non trouvé dans les données")
            
        except Exception as e:
            print(f"Erreur lors du test: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du remplacement du fichier: {e}")
        return False

if __name__ == "__main__":
    if apply_fix():
        print("\nCorrection appliquée avec succès!")
    else:
        print("\nÉchec de la correction")