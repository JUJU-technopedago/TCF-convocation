#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test pour vérifier l'affichage des caractères turcs avec la police Tahoma
"""

import os
from jinja2 import Template

def test_turkish_characters():
    """Test l'affichage des caractères turcs dans les templates"""
    
    # Données de test avec des caractères turcs
    test_data = {
        'nom': 'YÜZBAŞIOĞLU',
        'prenom': 'Nazlı',
        'date_naissance': '15/03/1995',
        'numero_candidat': '032002032197',
        'date_examen': '25/08/2025',
        'heure_debut': '09:00',
        'niveau': 'B2',
        'exam_type': 'DELF',
        'institution_name': 'Alliance Française de Bruxelles-Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_postal': '1000',
        'institution_city': 'Bruxelles',
        'date_ep_coll': '25/08/2025',
        'debut_ep_coll': '09:00',
        'date_ep_ind': '25/08/2025',
        'heure_preparation': '14:30',
        'access_code': 'AF2025',
        'logo_af_path': 'assets/logoAF.png',
        'logo_delf_path': 'assets/logoDELF.png'
    }
    
    # Liste des templates à tester
    templates = [
        'templates/convocation_delf_template_modele.html',
        'templates/convocation_delf_template.html',
        'templates/convocation_delf_template_simple.html',
        'templates/convocation_delf_template_word_style.html'
    ]
    
    print("🔤 Test des caractères turcs avec la police Tahoma")
    print("=" * 60)
    
    for template_path in templates:
        if os.path.exists(template_path):
            print(f"\n📄 Template: {template_path}")
            
            # Lire le template
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Vérifier que Tahoma est bien définie
            if "'Tahoma'" in template_content:
                print("✅ Police Tahoma détectée")
            else:
                print("❌ Police Tahoma non trouvée")
                continue
            
            # Générer le HTML avec les données turques
            template = Template(template_content)
            rendered_html = template.render(**test_data)
            
            # Créer le fichier de test
            test_filename = f"test_turkish_{os.path.basename(template_path)}"
            with open(test_filename, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            
            print(f"✅ Fichier de test créé: {test_filename}")
            
            # Vérifier la présence des caractères turcs
            turkish_chars = ['Ğ', 'İ', 'Ş', 'Ç', 'Ü', 'Ö', 'ğ', 'ı', 'ş', 'ç', 'ü', 'ö']
            found_chars = []
            for char in turkish_chars:
                if char in rendered_html:
                    found_chars.append(char)
            
            if found_chars:
                print(f"🔤 Caractères turcs trouvés: {', '.join(found_chars)}")
            else:
                print("⚠️  Aucun caractère turc spécifique trouvé")
        else:
            print(f"❌ Template non trouvé: {template_path}")
    
    print("\n" + "=" * 60)
    print("📋 Résumé du test:")
    print("• Nom testé: YÜZBAŞIOĞLU Nazlı")
    print("• Police utilisée: Tahoma (avec fallback Arial, Helvetica)")
    print("• Caractères turcs: Ğ İ Ş Ç Ü Ö ğ ı ş ç ü ö")
    print("• Avantages de Tahoma:")
    print("  - Support complet des caractères turcs")
    print("  - Police système universelle")
    print("  - Très lisible pour l'impression")
    print("  - Plus professionnelle qu'Arial pour les caractères étendus")
    
    print("\n💡 Pour tester visuellement:")
    print("1. Ouvrez les fichiers test_turkish_*.html dans un navigateur")
    print("2. Vérifiez que 'YÜZBAŞIOĞLU' s'affiche correctement")
    print("3. Comparez avec l'ancienne police Roboto si nécessaire")

if __name__ == "__main__":
    test_turkish_characters()
