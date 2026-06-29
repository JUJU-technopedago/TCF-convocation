import pandas as pd
import os

def fix_parse_candidate_row():
    """Crée un correctif pour la méthode _parse_candidate_row de JuryExcelProcessor"""
    
    # Lire le fichier original
    with open("jury_excel_processor.py", "r", encoding="utf-8") as f:
        original_code = f.read()
    
    # Trouver la section problématique
    start_marker = "                    # Vérifier si candidat à besoins spéciaux (colonne G)"
    end_marker = "                    break"
    
    # Extraire la section à corriger
    start_pos = original_code.find(start_marker)
    end_pos = original_code.find(end_marker, start_pos)
    
    if start_pos == -1 or end_pos == -1:
        print("Impossible de trouver la section à modifier")
        return
    
    section_to_replace = original_code[start_pos:end_pos]
    
    # Créer la nouvelle section
    new_section = """                    # Vérifier si candidat à besoins spéciaux (colonne G)
                    besoins_speciaux = False
                    if i + 6 < len(row_values) and row_values[i + 6]:  # Colonne G (index i+6) après le numéro de candidat
                        besoins_speciaux_str = str(row_values[i + 6]).strip().lower()
                        # Détection plus robuste: accepte "oui", "OUI", "Oui", "o", "yes", "1", "true", etc.
                        valid_values = ["oui", "o", "yes", "y", "1", "true", "vrai", "x"]
                        besoins_speciaux = False
                        
                        # Vérification explicite
                        for valid_value in valid_values:
                            if valid_value in besoins_speciaux_str:
                                besoins_speciaux = True
                                break
                        
                        # Afficher les informations pour le débogage
                        candidat_name = str(row_values[i + 1]) if i + 1 < len(row_values) else "inconnu"
                        print(f"INFO: Candidat {candidat_name} - Valeur en colonne G: '{row_values[i + 6]}' ('{besoins_speciaux_str}') => Besoins spéciaux: {besoins_speciaux}")
                    
                    # Solution alternative pour SIANO Marco : vérifier directement à l'index 6 (colonne G)
                    # Cette solution est plus directe mais moins générale
                    if not besoins_speciaux and len(row_values) > 6 and isinstance(row_values[6], str) and "oui" in row_values[6].lower():
                        besoins_speciaux = True
                        candidat_name = str(row_values[3]) if len(row_values) > 3 else "inconnu"
                        print(f"INFO: Détection directe - Candidat {candidat_name} - Valeur en colonne G: '{row_values[6]}' => Besoins spéciaux: {besoins_speciaux}")"""
    
    # Remplacer la section
    new_code = original_code.replace(section_to_replace, new_section)
    
    # Écrire dans un nouveau fichier pour vérification
    with open("jury_excel_processor_fixed.py", "w", encoding="utf-8") as f:
        f.write(new_code)
    
    print("Fichier jury_excel_processor_fixed.py créé avec succès")
    print("Ce fichier contient une version corrigée de la méthode _parse_candidate_row")
    print("La correction ajoute une détection alternative des besoins spéciaux directement à l'index 6")

if __name__ == "__main__":
    fix_parse_candidate_row()