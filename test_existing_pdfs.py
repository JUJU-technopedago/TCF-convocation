#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour vérifier les PDF existants et identifier le problème de correspondance
"""

import os
import glob

def test_existing_pdfs():
    """Teste les PDF existants dans le répertoire output"""
    
    print("🧪 TEST : Analyse des PDF existants")
    print("=" * 60)
    
    output_dir = "output"
    
    if not os.path.exists(output_dir):
        print(f"❌ Répertoire {output_dir} n'existe pas")
        return
    
    # Lister tous les PDF
    all_pdfs = glob.glob(os.path.join(output_dir, "*.pdf"))
    
    print(f"📊 PDF trouvés dans {output_dir}: {len(all_pdfs)}")
    print("-" * 50)
    
    if not all_pdfs:
        print("❌ Aucun PDF trouvé dans le répertoire output")
        print("💡 Suggestion: Générez d'abord les PDF avant d'envoyer les emails")
        return
    
    # Analyser chaque PDF
    for i, pdf_path in enumerate(all_pdfs, 1):
        filename = os.path.basename(pdf_path)
        file_size = os.path.getsize(pdf_path)
        
        print(f"{i}. {filename}")
        print(f"   📊 Taille: {file_size} bytes")
        
        # Analyser le nom du fichier pour identifier le format
        if "convocation_tcf_" in filename.lower():
            print(f"   ✅ Format TCF détecté")
            # Extraire nom et prénom
            parts = filename.lower().replace("convocation_tcf_", "").replace(".pdf", "").split("_")
            if len(parts) >= 2:
                nom, prenom = parts[0], parts[1]
                print(f"   👤 Candidat: {prenom.upper()} {nom.upper()}")
        elif "convocation_" in filename.lower():
            print(f"   ✅ Format DELF/DALF détecté")
        else:
            print(f"   ⚠️ Format inconnu")
        
        print()
    
    # Vérifier si on a des doublons (même PDF envoyé à tous)
    print("🔍 Analyse des doublons potentiels:")
    print("-" * 30)
    
    sizes = {}
    for pdf_path in all_pdfs:
        size = os.path.getsize(pdf_path)
        if size in sizes:
            sizes[size].append(os.path.basename(pdf_path))
        else:
            sizes[size] = [os.path.basename(pdf_path)]
    
    identical_size_count = 0
    for size, files in sizes.items():
        if len(files) > 1:
            print(f"⚠️ Fichiers de taille identique ({size} bytes):")
            for file in files:
                print(f"   - {file}")
            identical_size_count += len(files)
            print()
    
    if identical_size_count == 0:
        print("✅ Aucun fichier de taille identique trouvé - Bon signe!")
    else:
        print(f"⚠️ {identical_size_count} fichiers ont des tailles identiques")
        print("   Cela pourrait indiquer des PDF identiques!")
    
    print("=" * 60)

if __name__ == "__main__":
    test_existing_pdfs()