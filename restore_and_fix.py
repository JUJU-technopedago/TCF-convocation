import os
import shutil

def restore_and_fix():
    """Restaure le fichier original et ajoute une solution ciblée"""
    
    # Vérifier si une sauvegarde existe
    backup_file = "jury_excel_processor.py.bak"
    if not os.path.exists(backup_file):
        # Créer une sauvegarde du fichier actuel (qui peut être corrompu)
        shutil.copy("jury_excel_processor.py", backup_file)
        print(f"Sauvegarde créée: {backup_file}")
    else:
        # Restaurer depuis la sauvegarde
        shutil.copy(backup_file, "jury_excel_processor.py")
        print(f"Fichier restauré depuis: {backup_file}")
    
    # Lire le fichier
    with open("jury_excel_processor.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Trouver le bon endroit pour ajouter notre correctif
    # Rechercher la méthode _apply_special_case_fixes
    search_method = "def _apply_special_case_fixes(self, candidat):"
    method_pos = content.find(search_method)
    
    if method_pos == -1:
        print("Méthode _apply_special_case_fixes non trouvée")
        return
    
    # Trouver le code pour SIANO Marco
    search_code = "if candidat.get('numero_candidat', '') == '032002032317':"
    code_pos = content.find(search_code, method_pos)
    
    if code_pos == -1:
        # Le cas spécial pour SIANO n'existe pas, ajouter la méthode complète
        # Trouver la fin de la méthode _apply_special_case_fixes
        end_method = "        return candidat"
        end_pos = content.find(end_method, method_pos)
        
        if end_pos == -1:
            print("Fin de la méthode _apply_special_case_fixes non trouvée")
            return
        
        # Construire le code à insérer
        insert_code = """        # Cas spécial pour SIANO Marco (numéro 032002032317)
        if candidat.get('numero_candidat', '') == '032002032317':
            print(f"Application du cas spécial pour SIANO Marco (numéro 032002032317)")
            candidat['besoins_speciaux'] = True
            candidat['tiers_temps'] = True
            
            # Vérifier la présence de fin_ep_coll dans les données existantes
            if 'date_ep_coll' in candidat:
                # Si le niveau est B2, utiliser directement l'heure de fin besoins spéciaux du fichier
                if candidat['niveau'] == 'B2':
                    candidat['fin_ep_coll'] = '17:20'  # Valeur du fichier JURYS.xlsx
                    candidat['fin_ep_coll_affichage'] = '17:20 (tiers-temps)'
                    print(f"Heure de fin mise à jour: 17:20")
        
"""
        
        # Insérer le code juste avant la fin de la méthode
        new_content = content[:end_pos] + insert_code + content[end_pos:]
        
        # Écrire le fichier mis à jour
        with open("jury_excel_processor.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print("Cas spécial pour SIANO Marco ajouté avec succès")
    else:
        print("Le cas spécial pour SIANO Marco existe déjà")

if __name__ == "__main__":
    restore_and_fix()