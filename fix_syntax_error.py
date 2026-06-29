import pandas as pd
import os

def fix_parse_candidate_row():
    """Crée un correctif pour la méthode _parse_candidate_row de JuryExcelProcessor"""
    
    # Lire le fichier original
    with open("jury_excel_processor.py", "r", encoding="utf-8") as f:
        original_code = f.read()
    
    # Rechercher la ligne problématique et la corriger
    if "print(f\"INFO: Détection directe - Candidat {candidat_name} - Valeur en colonne G: '{row_values[6]}' => Besoins spéciaux: {besoins_speciaux}\")                    break" in original_code:
        # Corriger la ligne problématique
        corrected_code = original_code.replace(
            "print(f\"INFO: Détection directe - Candidat {candidat_name} - Valeur en colonne G: '{row_values[6]}' => Besoins spéciaux: {besoins_speciaux}\")                    break",
            "print(f\"INFO: Détection directe - Candidat {candidat_name} - Valeur en colonne G: '{row_values[6]}' => Besoins spéciaux: {besoins_speciaux}\")\n                    break"
        )
        
        # Écrire le code corrigé
        with open("jury_excel_processor.py", "w", encoding="utf-8") as f:
            f.write(corrected_code)
        
        print("Correction de l'erreur de syntaxe réussie")
    else:
        print("Ligne problématique non trouvée")

if __name__ == "__main__":
    fix_parse_candidate_row()