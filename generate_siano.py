from pdf_generator import PDFGenerator
import os
import datetime

def generate_siano_convocation():
    """Génère une convocation spécifiquement pour SIANO Marco pour tester les besoins spéciaux"""
    print("Génération d'une convocation pour SIANO Marco...")
    
    # Chemin vers le fichier Excel JURYS.xlsx
    excel_path = "JURYS.xlsx"
    
    # Chemin vers le template HTML
    template_path = "templates/convocation_delf_template_modele.html"
    
    # Logos
    logo_af_path = "logoAF.svg"
    logo_delf_path = "logoDELF.svg"
    
    # QR code path (optionnel)
    qrcode_path = None  # Aucune génération automatique, l'utilisateur doit fournir un fichier PNG
    
    # Vérifier si les fichiers existent
    if not os.path.exists(excel_path):
        print(f"Fichier Excel non trouvé: {excel_path}")
        return
    
    if not os.path.exists(template_path):
        print(f"Template HTML non trouvé: {template_path}")
        return
    
    # Créer un dossier de sortie avec horodatage
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output_siano_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Créer le générateur de PDF
    generator = PDFGenerator(
        excel_path=excel_path,
        template_path=template_path,
        logo_af_path=logo_af_path,
        logo_delf_path=logo_delf_path,
        output_dir=output_dir,
        qrcode_path=qrcode_path
    )
    
    # Définir les salles spécifiques (elles seront formatées automatiquement avec l'étage)
    generator.salle_collective = "11"  # Rez-de-chaussée
    generator.salle_individuelle = "17"  # 1er étage
    
    # Créer manuellement les données pour SIANO Marco
    from jury_excel_processor import JuryExcelProcessor
    processor = JuryExcelProcessor(excel_path)
    
    # Créer un candidat minimal
    siano_manual = {
        'nom': 'SIANO',
        'prenom': 'Marco',
        'numero_candidat': '032002032317',
        'date_naissance': '31 août 2008',
        'email': 'lia.mazzella@gmail.com',
        'niveau': 'B2',
        'matiere': 'DELF B2',
        'date_examen': '09/10/2025',
        'date_ep_coll': '09/10/2025',
        'debut_ep_coll': '14:00',
        'fin_ep_coll': '16:30',  # Sera modifié par _apply_special_case_fixes
        'heure_debut': '10:40',
        'heure_fin': '13:30',
        'heure_preparation': '10:40',
        'heure_passage': '11:15',
        'salle': 'Salle d\'examen',
        'salle_collective': '11',  # Salle d'examen collective (sera formatée avec l'étage)
        'salle_individuelle': '17', # Salle de préparation individuelle (sera formatée avec l'étage)
        'duree': '2h30 (collective) + 20min (individuelle)',
        'institution_name': 'Alliance Française Bruxelles Europe',
        'institution_address': 'Avenue des Arts 46',
        'institution_city': 'Bruxelles',
        'institution_postal': '1000',
        'institution_phone': '+32 2 788 21 60',
        'contact_urgence': 'info@alliancefrancaise.be',
        'besoins_speciaux': False,  # Sera modifié par _apply_special_case_fixes
        'tiers_temps': False  # Sera modifié par _apply_special_case_fixes
    }
    
    # Appliquer le cas spécial
    siano_manual = processor._apply_special_case_fixes(siano_manual)
    
    print("\nCandidat créé manuellement avec les données suivantes:")
    for key, value in sorted(siano_manual.items()):
        if key in ['nom', 'prenom', 'besoins_speciaux', 'tiers_temps', 'fin_ep_coll', 'fin_ep_coll_affichage']:
            print(f"  - {key}: {value}")
    
    # Générer la convocation
    try:
        output_path = generator.generate_pdf(
            siano_manual, 
            output_filename=f"convocation_SIANO_Marco_B2.pdf"
        )
        
        print(f"\nConvocation générée: {output_path}")
        
    except Exception as e:
        print(f"Erreur lors de la génération de la convocation: {e}")

if __name__ == "__main__":
    generate_siano_convocation()