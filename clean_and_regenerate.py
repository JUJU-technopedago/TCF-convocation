#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour nettoyer et régénérer les convocations avec les emails corrigés
"""

import os
import shutil

print("="*80)
print("NETTOYAGE ET RÉGÉNÉRATION DES CONVOCATIONS")
print("="*80)

# Chemin du dossier output
output_dir = "output"

if os.path.exists(output_dir):
    print(f"\n📂 Dossier trouvé: {output_dir}")
    
    # Compter les fichiers
    files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    print(f"   Nombre de fichiers: {len(files)}")
    
    # Demander confirmation
    response = input("\n⚠️  Voulez-vous SUPPRIMER tous les fichiers dans output/ ? (oui/non): ")
    
    if response.lower() in ['oui', 'o', 'yes', 'y']:
        print("\n🧹 Nettoyage en cours...")
        
        deleted_count = 0
        for filename in files:
            filepath = os.path.join(output_dir, filename)
            try:
                os.remove(filepath)
                deleted_count += 1
                if deleted_count <= 5:  # Afficher les 5 premiers
                    print(f"   ✓ Supprimé: {filename}")
                elif deleted_count == 6:
                    print(f"   ... ({len(files) - 5} autres fichiers)")
            except Exception as e:
                print(f"   ✗ Erreur: {filename} - {e}")
        
        print(f"\n✅ Nettoyage terminé: {deleted_count} fichiers supprimés")
        print("\n" + "="*80)
        print("PROCHAINES ÉTAPES:")
        print("="*80)
        print("1. Lancez l'application: python main.py")
        print("2. Cliquez sur 'Générer PDF'")
        print("3. Attendez la fin de la génération")
        print("4. Cliquez sur 'Envoyer Emails'")
        print("\n✨ Tous les emails seront maintenant envoyés correctement!")
        
    else:
        print("\n❌ Opération annulée")
else:
    print(f"\n❌ Dossier {output_dir} non trouvé")
