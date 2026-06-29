#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC INTERFACE - Trouve pourquoi l'interface montre 36 candidats INCONNU
"""

import os
import json
import sys

def main():
    print("DIAGNOSTIC INTERFACE CONVOCATION TCF")
    print("=" * 50)
    
    # Dossier de travail
    current_dir = os.getcwd()
    print(f"Dossier courant: {current_dir}")
    
    # Vérifier tous les fichiers JSON dans le dossier
    print("\nFICHIERS JSON TROUVES:")
    json_files = []
    for file in os.listdir(current_dir):
        if file.endswith('.json'):
            json_files.append(file)
            file_path = os.path.join(current_dir, file)
            file_size = os.path.getsize(file_path)
            print(f"   - {file} ({file_size} bytes)")
    
    # Analyser chaque fichier JSON
    for json_file in json_files:
        print(f"\n" + "="*30)
        print(f"ANALYSE: {json_file}")
        print("="*30)
        
        try:
            file_path = os.path.join(current_dir, json_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, dict):
                print(f"Type: Dictionnaire avec {len(data)} éléments")
                
                # Vérifier si c'est un registre de candidats
                if len(data) > 0:
                    sample_key = list(data.keys())[0]
                    sample_value = data[sample_key]
                    
                    print(f"Exemple de clé: {sample_key}")
                    print(f"Exemple de valeur: {sample_value}")
                    
                    # Vérifier structure candidat
                    if isinstance(sample_value, dict):
                        if 'nom' in sample_value and 'email' in sample_value:
                            print("STRUCTURE CANDIDAT DETECTEE!")
                            
                            # Compter les candidats INCONNU
                            inconnu_count = 0
                            total_candidates = len(data)
                            
                            for candidate_id, info in data.items():
                                nom = info.get('nom', 'INCONNU')
                                if nom == 'INCONNU':
                                    inconnu_count += 1
                                    print(f"   INCONNU trouvé: {candidate_id}")
                            
                            print(f"Total candidats: {total_candidates}")
                            print(f"Candidats INCONNU: {inconnu_count}")
                            print(f"Candidats avec nom: {total_candidates - inconnu_count}")
                            
                            # Montrer quelques exemples
                            print("\nECHANTILLON:")
                            for i, (candidate_id, info) in enumerate(list(data.items())[:3]):
                                nom = info.get('nom', 'INCONNU')
                                prenom = info.get('prenom', '')
                                email = info.get('email', 'N/A')
                                print(f"   {i+1}. {candidate_id}: {prenom} {nom} ({email})")
                            
            elif isinstance(data, list):
                print(f"Type: Liste avec {len(data)} éléments")
                if len(data) > 0:
                    print(f"Premier élément: {data[0]}")
            else:
                print(f"Type: {type(data)}")
                print(f"Contenu: {data}")
                
        except Exception as e:
            print(f"ERREUR lors de l'analyse de {json_file}: {str(e)}")
    
    # Vérifier si l'interface utilise un autre répertoire
    print(f"\n" + "="*50)
    print("VERIFICATION DES REPERTOIRES POSSIBLES")
    print("="*50)
    
    possible_dirs = [
        current_dir,
        os.path.join(current_dir, "output"),
        os.path.join(current_dir, "convocations"),
        os.path.join(current_dir, "pdfs"),
    ]
    
    for dir_path in possible_dirs:
        if os.path.exists(dir_path):
            print(f"\nDossier: {dir_path}")
            for file in os.listdir(dir_path):
                if file.endswith('.json'):
                    full_path = os.path.join(dir_path, file)
                    size = os.path.getsize(full_path)
                    print(f"   JSON: {file} ({size} bytes)")

if __name__ == "__main__":
    main()