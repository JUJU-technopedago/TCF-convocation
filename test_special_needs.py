import pandas as pd
import sys
import os

# Ajouter le répertoire parent au chemin de recherche Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer notre classe JuryExcelProcessor
from jury_excel_processor import JuryExcelProcessor

def test_special_needs():
    """Teste spécifiquement la détection des besoins spéciaux pour SIANO Marco"""
    print("Test de détection des besoins spéciaux pour SIANO Marco")
    print("-" * 50)
    
    # Utiliser notre processeur de fichiers Excel
    processor = JuryExcelProcessor("JURYS.xlsx")
    processor.load_jury_data()
    
    # Obtenir tous les candidats
    candidates = processor.get_all_candidates()
    print(f"Total de {len(candidates)} candidats trouvés")
    
    # Chercher SIANO Marco
    siano_found = False
    for candidate in candidates:
        if "SIANO" in candidate.get('nom', '') and "Marco" in candidate.get('prenom', ''):
            siano_found = True
            print("\nInformations sur SIANO Marco:")
            print(f"Nom: {candidate['nom']} {candidate['prenom']}")
            print(f"Niveau: {candidate['niveau']}")
            print(f"Besoins spéciaux: {candidate.get('besoins_speciaux', 'Non défini')}")
            print(f"Tiers-temps: {candidate.get('tiers_temps', 'Non défini')}")
            print(f"Heure de fin collective: {candidate.get('fin_ep_coll', 'Non défini')}")
            print(f"Affichage heure de fin: {candidate.get('fin_ep_coll_affichage', 'Non défini')}")
            
            # Afficher toutes les infos disponibles
            print("\nToutes les informations disponibles:")
            for key, value in candidate.items():
                if key not in ['nom', 'prenom', 'niveau', 'besoins_speciaux', 'tiers_temps', 'fin_ep_coll', 'fin_ep_coll_affichage']:
                    print(f"  {key}: {value}")
            
            break
    
    if not siano_found:
        print("⚠️  SIANO Marco n'a pas été trouvé dans la liste des candidats!")
        print("Premiers candidats disponibles (pour vérification):")
        for i, candidate in enumerate(candidates[:3]):
            print(f"  {i+1}. {candidate.get('nom', 'N/A')} {candidate.get('prenom', 'N/A')}")

if __name__ == "__main__":
    test_special_needs()