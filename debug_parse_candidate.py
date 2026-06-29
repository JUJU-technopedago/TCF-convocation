import pandas as pd
from jury_excel_processor import JuryExcelProcessor

def debug_parse_candidate_row():
    """Débogue le traitement de la ligne de SIANO Marco"""
    
    # Créer une instance du processeur
    processor = JuryExcelProcessor("JURYS.xlsx")
    
    # Lire l'onglet B2
    df = pd.read_excel("JURYS.xlsx", sheet_name="Niveau B2", header=None, engine='openpyxl')
    
    # Obtenir la ligne 9 (index 8)
    row_values = df.iloc[8].tolist()
    
    # Informations sur l'épreuve collective (ligne 1)
    first_row = df.iloc[0].tolist()
    epreuve_collective = {
        'date': processor._parse_date(first_row[3]) if len(first_row) > 3 else None,
        'debut': str(first_row[5]).strip() if len(first_row) > 5 else '',
        'fin_standard': str(first_row[7]).strip() if len(first_row) > 7 else '',
        'fin_besoins_speciaux': str(first_row[9]).strip() if len(first_row) > 9 else ''
    }
    
    # Informations sur le jury
    current_jury = {
        'numero': 'Jury 1',
        'date': None,
        'candidats': []
    }
    
    # Traiter manuellement la ligne
    print(f"Traitement de la ligne de SIANO Marco...")
    print(f"Valeurs: {row_values}")
    
    # Afficher les détails pour le débogage
    print("\nColonne G (index 6):")
    if len(row_values) > 6:
        print(f"Valeur: '{row_values[6]}'")
        if isinstance(row_values[6], str):
            print(f"Type: {type(row_values[6])}")
            print(f"Lowercase: '{row_values[6].lower()}'")
            print(f"Contient 'oui': {('oui' in row_values[6].lower())}")
    else:
        print("Pas de valeur disponible")
    
    # Tenter d'appeler la méthode de parsing
    print("\nTentative de parsing avec _parse_candidate_row...")
    try:
        candidat = processor._parse_candidate_row(row_values, "B2", None, epreuve_collective, current_jury)
        
        if candidat:
            print("Candidat créé avec succès:")
            for key, value in sorted(candidat.items()):
                print(f"  - {key}: {value}")
            
            # Vérifier spécifiquement les champs importants
            print("\nChamps spécifiques:")
            print(f"  besoins_speciaux: {candidat.get('besoins_speciaux', False)}")
            print(f"  tiers_temps: {candidat.get('tiers_temps', False)}")
            print(f"  fin_ep_coll: {candidat.get('fin_ep_coll', 'Non définie')}")
            print(f"  fin_ep_coll_affichage: {candidat.get('fin_ep_coll_affichage', 'Non définie')}")
        else:
            print("Le parsing a échoué: aucun candidat retourné")
    
    except Exception as e:
        print(f"Erreur lors du parsing: {e}")
    
    # Appliquer le cas spécial manuellement
    print("\nApplication manuelle du cas spécial...")
    if candidat:
        try:
            candidat_fixed = processor._apply_special_case_fixes(candidat)
            
            print("Candidat après application du cas spécial:")
            for key, value in sorted(candidat_fixed.items()):
                if key in ['besoins_speciaux', 'tiers_temps', 'fin_ep_coll', 'fin_ep_coll_affichage']:
                    print(f"  - {key}: {value}")
        except Exception as e:
            print(f"Erreur lors de l'application du cas spécial: {e}")

if __name__ == "__main__":
    debug_parse_candidate_row()