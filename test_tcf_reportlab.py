#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test TCF avec ReportLab - éviter les problèmes xhtml2pdf/cryptography
"""

def test_tcf_reportlab_simple():
    """Test de génération TCF avec ReportLab simple"""
    print("🧪 TEST TCF AVEC REPORTLAB SIMPLE")
    print("=" * 50)
    
    try:
        # Importer les modules nécessaires
        from tcf_excel_processor import TCFExcelProcessor
        from reportlab_pdf_generator import ReportLabPDFGenerator
        import os
        
        # Chemin du fichier de test
        excel_path = "test_tcf_data.xlsx"
        if not os.path.exists(excel_path):
            print("❌ Fichier de test non trouvé:", excel_path)
            return False
        
        print(f"📁 Fichier Excel: {excel_path}")
        
        # Charger les données TCF
        processor = TCFExcelProcessor(excel_path)
        processor.load_tcf_data()
        candidates = processor.get_all_candidates()
        
        if not candidates:
            print("❌ Aucun candidat trouvé")
            return False
        
        print(f"👥 Candidats trouvés: {len(candidates)}")
        
        # Prendre le premier candidat pour le test
        candidate = candidates[0]
        print(f"🧑 Test avec: {candidate.get('nom', 'INCONNU')} {candidate.get('prenom', '')}")
        
        # Créer le générateur ReportLab
        generator = ReportLabPDFGenerator()
        
        # Dossier de sortie
        output_dir = "Test_TCF_ReportLab"
        os.makedirs(output_dir, exist_ok=True)
        
        # Nom du fichier PDF
        pdf_filename = f"test_tcf_{candidate.get('nom', 'test')}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        print(f"📄 Génération PDF: {pdf_path}")
        
        # Générer le PDF avec les données du candidat
        generator.generate_tcf_pdf(candidate, pdf_path)
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ PDF généré avec succès!")
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

def test_main_tcf_generation():
    """Test avec la méthode principale de main.py"""
    print("\\n🧪 TEST AVEC MÉTHODE PRINCIPALE")
    print("=" * 50)
    
    try:
        # Simuler les paramètres comme dans main.py
        import tkinter as tk
        from main import ConvocationGenerator
        import os
        
        # Créer une instance de l'app (sans interface)
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        
        app = ConvocationGenerator(root)
        
        # Configurer les chemins nécessaires
        app.excel_file_path.set("test_tcf_data.xlsx")
        app.output_dir.set("Test_TCF_Main")
        app.access_code.set("2024")
        app.salle_collective.set("Salle 101")
        app.salle_individuelle.set("Salle 102")
        
        # Créer le dossier de sortie
        os.makedirs(app.output_dir.get(), exist_ok=True)
        
        print(f"📁 Excel: {app.excel_file_path.get()}")
        print(f"📂 Sortie: {app.output_dir.get()}")
        
        # Générer les PDFs TCF
        result = app._generate_tcf_pdfs()
        
        root.destroy()
        
        if result and result > 0:
            print(f"✅ {result} PDFs générés avec succès!")
            return True
        else:
            print("❌ Aucun PDF généré")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Programme principal de test"""
    print("🔧 TEST GÉNÉRATION TCF SANS XHTML2PDF")
    print("=" * 60)
    
    # Test 1: ReportLab simple
    success1 = test_tcf_reportlab_simple()
    
    # Test 2: Méthode principale
    success2 = test_main_tcf_generation()
    
    print("\\n📊 RÉSUMÉ DES TESTS:")
    print(f"  • ReportLab simple: {'✅' if success1 else '❌'}")
    print(f"  • Méthode principale: {'✅' if success2 else '❌'}")
    
    if success1 or success2:
        print("\\n🎉 Au moins un test a réussi!")
        return True
    else:
        print("\\n❌ Tous les tests ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n✅ Test global réussi!")
    else:
        print("\\n❌ Test global échoué")