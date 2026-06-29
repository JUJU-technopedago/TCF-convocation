#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECTIF REGISTRE - Copie le registre complet vers le dossier output
"""

import json
import os
import shutil

def main():
    print("CORRECTIF REGISTRE - Copie vers dossier output")
    print("=" * 50)
    
    # Chemins des fichiers
    source_registry = r"C:\Users\JMM\Desktop\convoc generator TCF\candidate_pdf_registry.json"
    output_dir = r"C:\Users\JMM\Desktop\convoc generator TCF\output"
    target_registry = os.path.join(output_dir, "candidate_pdf_registry.json")
    
    # Créer le dossier output s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    # Vérifier que le fichier source existe
    if not os.path.exists(source_registry):
        print(f"ERREUR: Fichier source non trouvé: {source_registry}")
        return False
    
    # Charger et analyser le fichier source
    with open(source_registry, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    
    print(f"Source: {len(source_data)} candidats dans {source_registry}")
    
    # Vérifier la qualité des données source
    candidats_valides = 0
    for candidate_id, info in source_data.items():
        nom = info.get('nom', 'INCONNU')
        if nom != 'INCONNU':
            candidats_valides += 1
    
    print(f"Candidats valides dans source: {candidats_valides}/{len(source_data)}")
    
    if candidats_valides == 0:
        print("ERREUR: Aucun candidat valide dans le fichier source!")
        return False
    
    # Sauvegarder l'ancien fichier output s'il existe
    if os.path.exists(target_registry):
        backup_path = target_registry + ".backup"
        shutil.copy2(target_registry, backup_path)
        print(f"Sauvegarde créée: {backup_path}")
    
    # Copier le registre source vers output
    shutil.copy2(source_registry, target_registry)
    print(f"Copie réussie: {source_registry} -> {target_registry}")
    
    # Vérifier la copie
    with open(target_registry, 'r', encoding='utf-8') as f:
        target_data = json.load(f)
    
    print(f"Vérification: {len(target_data)} candidats copiés")
    
    # Échantillon pour vérification
    print("\nECHANTILLON DES CANDIDATS COPIES:")
    for i, (candidate_id, info) in enumerate(list(target_data.items())[:3]):
        nom = info.get('nom', 'INCONNU')
        prenom = info.get('prenom', '')
        email = info.get('email', 'N/A')
        print(f"   {i+1}. {candidate_id}: {prenom} {nom} ({email})")
    
    print(f"\nSUCCES: {len(target_data)} candidats maintenant disponibles dans output")
    print("L'interface devrait maintenant afficher les vrais noms des candidats!")
    
    return True

if __name__ == "__main__":
    main()