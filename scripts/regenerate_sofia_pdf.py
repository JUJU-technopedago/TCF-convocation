#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Régénération du PDF pour Sofia COELHO avec le template corrigé
"""

from pdf_generator import PDFGenerator
import os

def regenerate_sofia_pdf():
    """Régénère le PDF pour Sofia COELHO"""
    
    print("=== Régénération PDF pour Sofia COELHO ===")
    
    # Configuration
    excel_path = "juries_20250820_192410.xlsx"
    template_path = "templates/convocation_delf_template_word_style.html"
    logo_af_path = "assets/logoAF.png"
    logo_delf_path = "assets/logoDELF.png"
    output_dir = "output"
    
    try:
        # Créer le générateur
        generator = PDFGenerator(
            excel_path=excel_path,
            template_path=template_path,
            logo_af_path=logo_af_path,
            logo_delf_path=logo_delf_path,
            output_dir=output_dir
        )
        
        print("✅ Générateur PDF initialisé")
        
        # Obtenir la liste des candidats
        candidates = generator.get_candidate_list()
        print(f"✅ Trouvé {len(candidates)} candidats")
        
        # Chercher Sofia COELHO
        sofia_candidate = None
        for candidate in candidates:
            if (candidate.get('nom', '').upper() == 'COELHO' and 
                candidate.get('prenom', '').upper() == 'SOFIA'):
                sofia_candidate = candidate
                break
        
        if sofia_candidate:
            print(f"📝 Candidat trouvé: {sofia_candidate.get('nom', '')} {sofia_candidate.get('prenom', '')}")
            print(f"   Numéro: {sofia_candidate.get('numero_candidat', '')}")
            
            # Générer le PDF
            pdf_path = generator.generate_pdf(sofia_candidate)
            print(f"✅ PDF régénéré: {pdf_path}")
            
            # Vérifier que le fichier existe
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"✅ Fichier créé avec succès ({file_size} bytes)")
                print(f"📁 Chemin: {os.path.abspath(pdf_path)}")
                
                # Comparer avec l'ancien fichier
                old_pdf = "output/convocation_COELHO_Sofia_032002032202.pdf"
                if os.path.exists(old_pdf):
                    old_size = os.path.getsize(old_pdf)
                    print(f"📊 Ancien fichier: {old_size} bytes")
                    print(f"📊 Nouveau fichier: {file_size} bytes")
                    if file_size > old_size:
                        print("✅ Le nouveau fichier est plus volumineux (probablement mieux)")
            else:
                print("❌ Le fichier PDF n'a pas été créé")
        else:
            print("❌ Sofia COELHO non trouvée dans la liste des candidats")
            print("Candidats disponibles:")
            for i, candidate in enumerate(candidates[:5]):  # Afficher les 5 premiers
                print(f"  {i+1}. {candidate.get('nom', '')} {candidate.get('prenom', '')}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    regenerate_sofia_pdf()
