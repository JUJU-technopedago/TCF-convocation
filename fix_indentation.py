import re

def fix_indentation_error():
    """
    Corrige l'erreur d'indentation dans jury_excel_processor.py
    """
    try:
        # Lire le contenu du fichier
        with open("jury_excel_processor.py", "r", encoding="utf-8") as f:
            content = f.readlines()
        
        # Identifier la ligne 274 et ajuster son indentation
        if len(content) >= 274:
            line_274 = content[273]  # les indices commencent à 0
            
            # Vérifier si c'est bien la ligne problématique
            if "candidat_name = str(row_values[i + 1])" in line_274:
                # Déterminer le niveau d'indentation correct
                # Vérifier les lignes précédentes pour comprendre le contexte
                correct_indentation = ""
                for i in range(273, 250, -1):
                    if "besoins_speciaux" in content[i]:
                        # Trouver l'indentation de cette ligne
                        match = re.match(r"(\s+)", content[i])
                        if match:
                            correct_indentation = match.group(1)
                            break
                
                # Si on n'a pas trouvé d'indentation, utiliser une valeur par défaut
                if not correct_indentation:
                    correct_indentation = "                    "  # 20 espaces
                
                # Corriger l'indentation de la ligne 274
                stripped_line = line_274.lstrip()
                content[273] = correct_indentation + stripped_line
                
                print(f"Indentation corrigée pour la ligne 274")
                print(f"Ancienne: '{line_274}'")
                print(f"Nouvelle: '{content[273]}'")
            else:
                print(f"La ligne 274 ne correspond pas à la ligne attendue:")
                print(f"Contenu: '{line_274}'")
        else:
            print(f"Le fichier a seulement {len(content)} lignes (moins que 274)")
        
        # Écrire le fichier corrigé
        with open("jury_excel_processor.py", "w", encoding="utf-8") as f:
            f.writelines(content)
        
        print("Fichier corrigé sauvegardé")
        
    except Exception as e:
        print(f"Erreur lors de la correction: {e}")
        
    # Tenter une autre approche si nécessaire
    try:
        # Lire tout le contenu du fichier
        with open("jury_excel_processor.py", "r", encoding="utf-8") as f:
            full_content = f.read()
        
        # Chercher le motif problématique
        pattern = r'print\(f"INFO: Détection directe - Candidat \{candidat_name\} - Valeur en colonne G: \'\{row_values\[6\]\}\' => Besoins spéciaux: \{besoins_speciaux\}"\)\s+candidat_name = '
        
        # Remplacer par la version correcte
        fixed_content = re.sub(pattern, 'print(f"INFO: Détection directe - Candidat {candidat_name} - Valeur en colonne G: \'{row_values[6]}\' => Besoins spéciaux: {besoins_speciaux}")\n                    candidat_name = ', full_content)
        
        # Écrire le fichier corrigé
        with open("jury_excel_processor.py", "w", encoding="utf-8") as f:
            f.write(fixed_content)
        
        print("Deuxième tentative de correction appliquée")
        
    except Exception as e:
        print(f"Erreur lors de la deuxième tentative: {e}")

if __name__ == "__main__":
    fix_indentation_error()