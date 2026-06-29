#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST NETTOYAGE OUTPUT - Vérifie que le dossier output est correctement vidé
"""

import os
import json

def create_test_files():
    """Crée des fichiers de test dans output pour simuler un ancien état"""
    output_dir = r"C:\Users\JMM\Desktop\convoc generator TCF\output"
    os.makedirs(output_dir, exist_ok=True)
    
    print("CRÉATION DE FICHIERS DE TEST...")
    
    # Créer quelques fichiers PDF de test
    test_files = [
        "convocation_TCF_TEST1.pdf",
        "convocation_TCF_TEST2.pdf", 
        "candidate_pdf_registry.json",
        "rapport_generation.txt",
        "ancien_fichier.log"
    ]
    
    files_created = 0
    for filename in test_files:
        file_path = os.path.join(output_dir, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if filename.endswith('.json'):
                    # Créer un faux registre JSON
                    fake_registry = {
                        "test1": {"nom": "TEST", "prenom": "Test1", "email": "test1@test.com"},
                        "test2": {"nom": "TEST", "prenom": "Test2", "email": "test2@test.com"}
                    }
                    json.dump(fake_registry, f)
                else:
                    f.write(f"Fichier de test créé: {filename}")
            files_created += 1
            print(f"   ✅ Créé: {filename}")
        except Exception as e:
            print(f"   ❌ Erreur création {filename}: {e}")
    
    print(f"📁 {files_created} fichiers de test créés dans output")
    return files_created

def test_output_cleanup():
    """Teste le nettoyage du dossier output"""
    output_dir = r"C:\Users\JMM\Desktop\convoc generator TCF\output"
    
    print("\nTEST NETTOYAGE DOSSIER OUTPUT")
    print("=" * 40)
    
    # Créer des fichiers de test
    files_created = create_test_files()
    
    # Vérifier les fichiers avant nettoyage
    print(f"\nAVANT NETTOYAGE:")
    if os.path.exists(output_dir):
        files_before = os.listdir(output_dir)
        print(f"   Fichiers présents: {len(files_before)}")
        for filename in files_before:
            print(f"   - {filename}")
    else:
        print("   Dossier output n'existe pas")
        return
    
    # Simuler le nettoyage (comme dans la fonction modifiée)
    print(f"\nNETTOYAGE EN COURS...")
    files_deleted = 0
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                files_deleted += 1
                print(f"   🗑️ Supprimé: {filename}")
            elif os.path.isdir(file_path):
                import shutil
                shutil.rmtree(file_path)
                print(f"   🗑️ Dossier supprimé: {filename}")
        except Exception as e:
            print(f"   ⚠️ Erreur suppression {filename}: {e}")
    
    # Vérifier les fichiers après nettoyage
    print(f"\nAPRÈS NETTOYAGE:")
    files_after = os.listdir(output_dir)
    print(f"   Fichiers présents: {len(files_after)}")
    if files_after:
        print("   ⚠️ PROBLÈME: Des fichiers sont encore présents!")
        for filename in files_after:
            print(f"   - {filename}")
    else:
        print("   ✅ Dossier complètement vidé!")
    
    print(f"\nRÉSULTAT:")
    print(f"   Fichiers créés: {files_created}")
    print(f"   Fichiers supprimés: {files_deleted}")
    print(f"   Fichiers restants: {len(files_after)}")
    
    if len(files_after) == 0:
        print("   🎉 SUCCÈS: Nettoyage complet réussi!")
        return True
    else:
        print("   ❌ ÉCHEC: Nettoyage incomplet")
        return False

if __name__ == "__main__":
    test_output_cleanup()