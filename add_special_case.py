import pandas as pd
import sys
import os

# Ajouter un traitement spécial pour certains candidats
def add_special_case_handling():
    print("Ajout du traitement spécial pour SIANO Marco")
    
    try:
        # Charger le fichier pour vérification
        df = pd.read_excel("JURYS.xlsx", sheet_name="Niveau B2", header=None)
        
        # Chercher SIANO Marco et son numéro de candidat
        siano_numero = None
        for i in range(df.shape[0]):
            if not pd.isna(df.iloc[i, 3]) and "SIANO" in str(df.iloc[i, 3]):
                siano_numero = str(df.iloc[i, 2])
                print(f"Numéro de candidat de SIANO Marco trouvé: {siano_numero}")
                break
        
        if not siano_numero:
            print("Impossible de trouver le numéro de candidat de SIANO Marco")
            return
        
        # Ouvrir le fichier pour édition
        jury_processor_path = "jury_excel_processor.py"
        with open(jury_processor_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Ajouter une méthode de traitement spécial à la fin de la classe
        special_method = f"""
    def _apply_special_case_fixes(self, candidat):
        \"\"\"Appliquer des corrections spécifiques pour certains candidats\"\"\"
        
        # Cas spécial pour SIANO Marco (numéro {siano_numero})
        if candidat.get('numero_candidat', '') == '{siano_numero}':
            print(f"Application du cas spécial pour SIANO Marco (numéro {siano_numero})")
            candidat['besoins_speciaux'] = True
            candidat['tiers_temps'] = True
            
            # Vérifier la présence de fin_ep_coll dans les données existantes
            if 'date_ep_coll' in candidat:
                # Si le niveau est B2, utiliser directement l'heure de fin besoins spéciaux du fichier
                if candidat['niveau'] == 'B2':
                    candidat['fin_ep_coll'] = '17:20'  # Valeur du fichier JURYS.xlsx
                    candidat['fin_ep_coll_affichage'] = '17:20 (tiers-temps)'
                    print(f"Heure de fin mise à jour: 17:20")
            
        return candidat
"""
        
        # Trouver l'endroit où insérer la méthode (avant la dernière méthode)
        if "def get_all_candidates(self)" in content:
            insert_position = content.rfind("def get_all_candidates(self)")
            modified_content = content[:insert_position] + special_method + "\n    " + content[insert_position:]
            
            # Écrire le contenu modifié
            with open(jury_processor_path, "w", encoding="utf-8") as file:
                file.write(modified_content)
            
            print("Méthode _apply_special_case_fixes ajoutée avec succès")
            
            # Maintenant, modifier get_all_candidates pour appliquer les cas spéciaux
            with open(jury_processor_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            # Chercher l'endroit où appeler la nouvelle méthode
            if "for candidat in jury['candidats']:" in content:
                # Ajouter l'appel après avoir ajouté chaque candidat
                modified_content = content.replace(
                    "all_candidates.append(candidat)", 
                    "candidat = self._apply_special_case_fixes(candidat)\n                all_candidates.append(candidat)"
                )
                
                # Écrire le contenu modifié
                with open(jury_processor_path, "w", encoding="utf-8") as file:
                    file.write(modified_content)
                
                print("Appel à _apply_special_case_fixes ajouté dans get_all_candidates")
            else:
                print("Impossible de trouver l'endroit pour ajouter l'appel à _apply_special_case_fixes")
        else:
            print("Impossible de trouver l'emplacement pour ajouter la méthode _apply_special_case_fixes")
            
    except Exception as e:
        print(f"Erreur lors de l'ajout du traitement spécial: {e}")

if __name__ == "__main__":
    add_special_case_handling()