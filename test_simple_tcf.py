#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de génération TCF avec ReportLab
"""

def test_simple_tcf_generation():
    """Test simple de génération TCF"""
    print("🧪 TEST SIMPLE GÉNÉRATION TCF")
    print("=" * 40)
    
    try:
        from reportlab_pdf_generator import ReportLabPDFGenerator
        import os
        from datetime import date
        
        # Données de candidat de test
        test_candidate = {
            'nom': 'MARTIN',
            'prenom': 'Jean',
            'date_naissance': '15/03/1990',
            'email': 'jean.martin@email.com',
            'tcf_type': 'TCF SO',
            'date_examen': '15/12/2024',
            'date_ep_coll': date(2024, 12, 15),
            'date_ep_ind': date(2024, 12, 15),
            'debut_ep_coll': '09:00',
            'heure_preparation': '14:00',
            'duree_collective': '1h30',
            'duree_individuelle': '15 min',
            'salle_collective': '101',
            'salle_individuelle': '102',
            'access_code': '2024'
        }
        
        print(f"👤 Candidat: {test_candidate['nom']} {test_candidate['prenom']}")
        print(f"📝 Type TCF: {test_candidate['tcf_type']}")
        
        # Créer le générateur
        generator = ReportLabPDFGenerator()
        
        # Dossier de sortie
        output_dir = "Test_TCF_Simple"
        os.makedirs(output_dir, exist_ok=True)
        
        # Nom du fichier PDF
        pdf_filename = "test_tcf_simple.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        print(f"📄 Génération: {pdf_path}")
        
        # Générer le PDF
        success = generator.generate_convocation(test_candidate, pdf_path)
        
        # Vérifier le résultat
        if success and os.path.exists(pdf_path):
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

def test_check_reportlab_module():
    """Vérifier que le module ReportLab fonctionne"""
    print("\\n🔍 VÉRIFICATION MODULE REPORTLAB")
    print("=" * 40)
    
    try:
        from reportlab_pdf_generator import ReportLabPDFGenerator
        generator = ReportLabPDFGenerator()
        print("✅ Module ReportLabPDFGenerator importé")
        
        # Vérifier les méthodes importantes
        if hasattr(generator, 'generate_convocation'):
            print("✅ Méthode generate_convocation disponible")
        else:
            print("❌ Méthode generate_convocation manquante")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur import ReportLab: {e}")
        return False

def main():
    """Programme principal"""
    print("🔧 TEST REPORTLAB TCF SIMPLIFIÉ")
    print("=" * 50)
    
    # Test 1: Vérifier le module
    success1 = test_check_reportlab_module()
    
    # Test 2: Génération simple
    success2 = False
    if success1:
        success2 = test_simple_tcf_generation()
    
    print("\\n📊 RÉSUMÉ:")
    print(f"  • Module ReportLab: {'✅' if success1 else '❌'}")
    print(f"  • Génération PDF: {'✅' if success2 else '❌'}")
    
    if success2:
        print("\\n🎉 Test réussi!")
        return True
    else:
        print("\\n❌ Test échoué")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n✅ Tous les tests sont passés!")
    else:
        print("\\n❌ Des tests ont échoué")