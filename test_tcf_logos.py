#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des logos TCF spécifiques selon le type d'examen
"""

def test_tcf_logos_by_type():
    """Test des différents logos TCF selon le type"""
    print("🎯 TEST LOGOS TCF SPÉCIFIQUES")
    print("=" * 50)
    
    try:
        # Appliquer le correctif cryptography
        import auto_decrepit_fix
        fixer = auto_decrepit_fix.DefecratedImportFixer()
        fixer.fix_decrepit_imports()
        
        from pdf_generator import PDFGenerator
        import os
        from datetime import date
        
        # Types de TCF à tester
        tcf_types = [
            'TCF CANADA',
            'TCF TP COMPLET', 
            'TCF TP OBLIGATOIRE',
            'TCF IRN'
        ]
        
        # Template TCF
        template_path = "templates/convocation_tcf_template_simple.html"
        
        if not os.path.exists(template_path):
            print(f"❌ Template non trouvé: {template_path}")
            return False
        
        # Créer dossier de test
        output_dir = "Test_TCF_Logos"
        os.makedirs(output_dir, exist_ok=True)
        
        success_count = 0
        
        for tcf_type in tcf_types:
            try:
                print(f"\\n🧪 Test {tcf_type}")
                
                # Données candidat pour ce type TCF
                test_candidate = {
                    'nom': 'TEST',
                    'prenom': tcf_type.replace(' ', '_'),
                    'date_naissance': '01/01/1990',
                    'email': 'test@email.com',
                    'tcf_type': tcf_type,
                    'date_examen': date(2024, 12, 15),
                    'date_ep_coll': date(2024, 12, 15),
                    'date_ep_ind': date(2024, 12, 15),
                    'debut_ep_coll': '09:00',
                    'heure_preparation': '14:00',
                    'duree_collective': '1h30',
                    'duree_individuelle': '15 min'
                }
                
                # Créer générateur avec logos de test
                generator = PDFGenerator(
                    excel_path="test.xlsx",
                    template_path=template_path,
                    logo_af_path="",  # Pas de logo AF pour le test
                    logo_delf_path=f"assets/logo_{tcf_type.replace(' ', '_').lower()}.png",  # Logo spécifique
                    output_dir=output_dir,
                    access_code="2024",
                    qrcode_path="",
                    image_a1_path="",
                    image_a2_path="",
                    image_b1_path="",
                    image_b2_path="",
                    image_c1_path="",
                    image_c2_path=""
                )
                
                # Nom du fichier
                pdf_filename = f"test_{tcf_type.replace(' ', '_')}.pdf"
                
                print(f"📄 Génération: {pdf_filename}")
                print(f"🖼️ Logo attendu: {generator.logo_delf_path}")
                
                # Générer le PDF
                pdf_path = generator.generate_pdf(test_candidate, pdf_filename)
                
                if pdf_path and os.path.exists(pdf_path):
                    file_size = os.path.getsize(pdf_path)
                    print(f"✅ PDF généré: {file_size} octets")
                    success_count += 1
                else:
                    print(f"❌ Échec génération PDF")
                    
            except Exception as e:
                print(f"❌ Erreur {tcf_type}: {e}")
        
        print(f"\\n📊 RÉSULTATS:")
        print(f"  • Types testés: {len(tcf_types)}")
        print(f"  • Succès: {success_count}")
        print(f"  • Échecs: {len(tcf_types) - success_count}")
        
        if success_count == len(tcf_types):
            print("\\n🎉 Tous les types TCF générés avec succès!")
            return True
        else:
            print(f"\\n⚠️ {len(tcf_types) - success_count} échecs détectés")
            return False
            
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Programme principal"""
    print("🔧 TEST LOGOS TCF PAR TYPE")
    print("=" * 40)
    
    success = test_tcf_logos_by_type()
    
    if success:
        print("\\n✅ Test logos TCF réussi!")
        print("\\n💡 UTILISATION:")
        print("  Pour que les logos s'affichent, assurez-vous d'avoir:")
        print("  • assets/logo_tcf_canada.png")
        print("  • assets/logo_tcf_tp_complet.png") 
        print("  • assets/logo_tcf_tp_obligatoire.png")
        print("  • assets/logo_tcf_irn.png")
        print("  • ou configurer les chemins dans l'interface graphique")
        return True
    else:
        print("\\n❌ Test logos TCF échoué")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n🎯 Test terminé avec succès!")
    else:
        print("\\n💥 Test échoué")