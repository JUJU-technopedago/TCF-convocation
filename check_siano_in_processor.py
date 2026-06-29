import os
import pandas as pd

def verify_siano_in_data():
    """Vérifie si SIANO Marco est dans les données traitées par JuryExcelProcessor"""
    
    from jury_excel_processor import JuryExcelProcessor
    
    # Initialiser le processeur
    processor = JuryExcelProcessor("JURYS.xlsx")
    
    # Charger les données
    print("Chargement des données...")
    processor.load_jury_data()
    
    # Récupérer tous les candidats
    print("Récupération de tous les candidats...")
    all_candidates = processor.get_all_candidates()
    
    # Vérifier si SIANO est présent
    siano = None
    for i, candidate in enumerate(all_candidates):
        if candidate.get('nom', '') == 'SIANO' and candidate.get('prenom', '') == 'Marco':
            siano = candidate
            print(f"\nSIANO Marco trouvé à l'index {i} sur {len(all_candidates)} candidats:")
            for key, value in sorted(candidate.items()):
                print(f"  - {key}: {value}")
    
    # Afficher le nombre total de candidats
    print(f"\nNombre total de candidats: {len(all_candidates)}")
    
    # Lister les candidats avec besoins spéciaux
    special_needs = [c for c in all_candidates if c.get('besoins_speciaux', False)]
    print(f"Candidats avec besoins spéciaux ({len(special_needs)}):")
    for i, candidate in enumerate(special_needs):
        print(f"  {i+1}. {candidate.get('nom', '')} {candidate.get('prenom', '')}: {candidate.get('niveau', '')}")
        print(f"     Tiers-temps: {candidate.get('tiers_temps', False)}")
        print(f"     Fin épreuve: {candidate.get('fin_ep_coll_affichage', candidate.get('fin_ep_coll', 'Non définie'))}")
    
    # Si SIANO n'est pas trouvé, rechercher des noms similaires
    if not siano:
        print("\nSIANO Marco n'a pas été trouvé. Recherche de noms similaires...")
        similar = []
        for candidate in all_candidates:
            nom = candidate.get('nom', '').lower()
            prenom = candidate.get('prenom', '').lower()
            if 'siano' in nom or 'marco' in prenom:
                similar.append(candidate)
        
        if similar:
            print(f"Trouvé {len(similar)} candidats avec des noms similaires:")
            for i, candidate in enumerate(similar):
                print(f"  {i+1}. {candidate.get('nom', '')} {candidate.get('prenom', '')}")
        else:
            print("Aucun candidat avec un nom similaire.")
    
    return siano is not None

if __name__ == "__main__":
    verify_siano_in_data()