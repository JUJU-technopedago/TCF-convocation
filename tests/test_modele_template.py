#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du nouveau template modèle avec encadrés gris
"""

from pdf_generator import PDFGenerator
import os

def test_modele_template():
    """Test de génération d'un PDF avec le template modèle"""
    
    print("=== Test du template modèle avec encadrés gris ===")
    
    # Configuration avec le nouveau template
    excel_path = "juries_20250820_192410.xlsx"
    template_path = "templates/convocation_delf_template_modele.html"
    logo_af_path = "assets/logoAF.png"
    logo_delf_path = "assets/logoDELF.png"
    output_dir = "output"
    
    # Vérifier que les fichiers existent
    if not os.path.exists(excel_path):
        print(f"❌ Fichier Excel non trouvé: {excel_path}")
        return
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
        
    if not os.path.exists(logo_af_path):
        print(f"❌ Logo AF non trouvé: {logo_af_path}")
        return
        
    if not os.path.exists(logo_delf_path):
        print(f"❌ Logo DELF non trouvé: {logo_delf_path}")
        return
    
    print("✅ Tous les fichiers requis sont présents")
    
    try:
        # Créer le générateur avec le nouveau template
        generator = PDFGenerator(
            excel_path=excel_path,
            template_path=template_path,
            logo_af_path=logo_af_path,
            logo_delf_path=logo_delf_path,
            output_dir=output_dir
        )
        
        print("✅ Générateur PDF initialisé avec le template modèle")
        
        # Obtenir la liste des candidats
        candidates = generator.get_candidate_list()
        print(f"✅ Trouvé {len(candidates)} candidats")
        
        if candidates:
            # Chercher Sofia COELHO pour le test
            sofia_candidate = None
            for candidate in candidates:
                if (candidate.get('nom', '').upper() == 'COELHO' and 
                    candidate.get('prenom', '').upper() == 'SOFIA'):
                    sofia_candidate = candidate
                    break
            
            if not sofia_candidate:
                # Prendre le premier candidat si Sofia n'est pas trouvée
                sofia_candidate = candidates[0]
            
            print(f"📝 Test avec: {sofia_candidate.get('nom', '')} {sofia_candidate.get('prenom', '')}")
            
            # Générer le PDF avec un nom spécifique pour le test
            output_filename = f"convocation_MODELE_{sofia_candidate.get('nom', '')}_{sofia_candidate.get('prenom', '')}_{sofia_candidate.get('numero_candidat', '')}.pdf"
            pdf_path = generator.generate_pdf(sofia_candidate, output_filename)
            print(f"✅ PDF généré avec le template modèle: {pdf_path}")
            
            # Vérifier que le fichier existe
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"✅ Fichier créé avec succès ({file_size} bytes)")
                print(f"📁 Chemin: {os.path.abspath(pdf_path)}")
                print(f"🎨 Template utilisé: {template_path}")
            else:
                print("❌ Le fichier PDF n'a pas été créé")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_modele_template()
