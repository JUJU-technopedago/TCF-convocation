#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du template HTML TCF avec xhtml2pdf
"""

def test_tcf_html_template():
    """Test du template HTML TCF"""
    print("🧪 TEST TEMPLATE HTML TCF AVEC XHTML2PDF")
    print("=" * 50)
    
    try:
        # Appliquer le correctif cryptography d'abord
        import auto_decrepit_fix
        fixer = auto_decrepit_fix.DefecratedImportFixer()
        fixer.fix_decrepit_imports()
        print("✅ Correctif cryptography appliqué")
        
        # Maintenant importer xhtml2pdf
        from pdf_generator import PDFGenerator
        import os
        from datetime import date
        
        # Données de test TCF
        test_candidate = {
            'nom': 'DUPONT',
            'prenom': 'Marie',
            'date_naissance': '15/05/1990',
            'email': 'marie.dupont@email.com',
            'tcf_type': 'TCF SO',
            'date_examen': date(2024, 12, 15),
            'date_ep_coll': date(2024, 12, 15),
            'date_ep_ind': date(2024, 12, 15),
            'debut_ep_coll': '09:00',
            'heure_preparation': '14:00',
            'duree_collective': '1h30',
            'duree_individuelle': '15 min',
            'salle_collective': '101',
            'salle_individuelle': '102',
            
            # Données formatées pour le template
            'date_collective_format': '15/12/2024',
            'date_individual_format': '15/12/2024',
            'heure_collective': '09:00',
            'heure_individual': '14:00',
            'has_individual_exam': True
        }
        
        print(f"👤 Test candidat: {test_candidate['nom']} {test_candidate['prenom']}")
        
        # Créer le générateur PDF avec template HTML simplifié
        template_path = "templates/convocation_tcf_template_simple.html"
        
        if not os.path.exists(template_path):
            print(f"❌ Template non trouvé: {template_path}")
            return False
            
        print(f"📄 Template: {template_path}")
        
        generator = PDFGenerator(
            excel_path="test_tcf_data.xlsx",
            template_path=template_path,
            logo_af_path="",
            logo_delf_path="",
            output_dir="Test_TCF_HTML",
            access_code="2024",
            qrcode_path="",
            image_a1_path="",
            image_a2_path="",
            image_b1_path="",
            image_b2_path="",
            image_c1_path="",
            image_c2_path=""
        )
        
        # Créer dossier de sortie
        os.makedirs("Test_TCF_HTML", exist_ok=True)
        
        # Définir les salles
        generator.salle_collective = "101"
        generator.salle_individuelle = "102"
        
        # Générer le PDF
        pdf_path = os.path.join("Test_TCF_HTML", "test_tcf_html.pdf")
        
        print(f"🔄 Génération PDF: {pdf_path}")
        
        # Utiliser la méthode pour générer le PDF
        pdf_path = generator.generate_pdf(test_candidate, "test_tcf_html.pdf")
        
        # Vérifier le résultat
        if pdf_path and os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ PDF HTML généré avec succès!")
            print(f"📏 Taille: {file_size} octets")
            print(f"📍 Chemin: {pdf_path}")
            return True
        else:
            print("❌ PDF non généré")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Programme principal"""
    print("🔧 TEST TEMPLATE HTML TCF")
    print("=" * 40)
    
    success = test_tcf_html_template()
    
    if success:
        print("\\n🎉 Template HTML TCF fonctionne!")
        print("✅ Vous pouvez maintenant utiliser le template HTML pour TCF")
        return True
    else:
        print("\\n❌ Problème avec le template HTML TCF")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n✅ Test réussi - Template HTML prêt!")
    else:
        print("\\n❌ Test échoué")