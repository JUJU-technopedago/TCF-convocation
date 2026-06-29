#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test pour régénérer le PDF de YÜZBAŞIOĞLU avec WeasyPrint et Tahoma
"""

import os
from pdf_generator import PDFGenerator

def test_regenerate_yuzbasioglu():
    """Régénère le PDF de YÜZBAŞIOĞLU avec les nouvelles améliorations"""
    
    print("🔄 Régénération du PDF YÜZBAŞIOĞLU avec WeasyPrint + Tahoma")
    print("=" * 70)
    
    # Données de test pour YÜZBAŞIOĞLU
    candidate_data = {
        'nom': 'YÜZBAŞIOĞLU',
        'prenom': 'Nazlı',
        'date_naissance': '17/08/1982',
        'numero_candidat': '032002032197',
        'niveau': 'A2',
        'exam_type': 'DELF',
        'date_examen': '16/09/2025',
        'heure_debut': '09:30',
        'date_ep_coll': '16/09/2025',
        'debut_ep_coll': '09:30',
        'date_ep_ind': '16/09/2025',
        'heure_preparation': '14:00',
        'institution_name': 'Alliance Française Bruxelles Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_postal': '1000',
        'institution_city': 'Bruxelles',
        'access_code': ''
    }
    
    # Tester avec le template modèle (qui utilise maintenant Tahoma)
    template_path = 'templates/convocation_delf_template_modele.html'
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
    
    try:
        # Créer le générateur PDF
        generator = PDFGenerator(
            excel_path="juries_20250820_192410.xlsx",  # Fichier existant pour la structure
            template_path=template_path,
            logo_af_path='assets/logoAF.png',
            logo_delf_path='assets/logoDELF.png',
            output_dir='output',
            access_code=''
        )
        
        print(f"📄 Template utilisé: {template_path}")
        print(f"🔤 Police: Tahoma (avec fallback Arial, Helvetica)")
        print(f"🛠️  Moteur PDF: WeasyPrint (support Unicode complet)")
        
        # Générer le PDF
        pdf_path = generator.generate_pdf(candidate_data)
        
        print(f"✅ PDF généré avec succès: {pdf_path}")
        print(f"📁 Fichier: {os.path.basename(pdf_path)}")
        
        # Vérifier que le fichier existe
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"📊 Taille du fichier: {file_size} bytes")
            
            print("\n" + "=" * 70)
            print("✅ SUCCÈS - Le PDF a été régénéré avec les améliorations suivantes:")
            print("• 🔤 Police Tahoma pour un meilleur support des caractères turcs")
            print("• 🛠️  WeasyPrint pour un rendu Unicode parfait")
            print("• 📝 Caractères turcs: Ğ İ Ş Ç Ü Ö ğ ı ş ç ü ö")
            print("\n💡 Vérifiez maintenant que 'YÜZBAŞIOĞLU Nazlı' s'affiche correctement!")
            
        else:
            print("❌ Erreur: Le fichier PDF n'a pas été créé")
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        print("\n🔧 Solutions possibles:")
        print("1. Vérifiez que WeasyPrint est bien installé")
        print("2. Vérifiez que les logos existent dans assets/")
        print("3. Vérifiez que le template utilise bien Tahoma")

def compare_with_old_pdf():
    """Compare avec l'ancien PDF pour voir les différences"""
    old_pdf = "output/convocation_YÜZBAŞIOĞLU_Nazlı_032002032197.pdf"
    
    if os.path.exists(old_pdf):
        print(f"\n📋 Comparaison avec l'ancien PDF:")
        print(f"• Ancien PDF: {old_pdf}")
        print("• Ancien moteur: xhtml2pdf (problèmes Unicode)")
        print("• Ancienne police: Roboto")
        print("• Problème: Caractères turcs remplacés par des carrés")
        print("• Le nouveau PDF va écraser l'ancien avec les améliorations")

if __name__ == "__main__":
    compare_with_old_pdf()
    test_regenerate_yuzbasioglu()
