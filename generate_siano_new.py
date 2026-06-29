from pdf_generator import PDFGenerator
import os
import datetime
from jury_excel_processor import JuryExcelProcessor

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
    
    # Créer un dossier de sortie avec horodatage
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output_siano_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Dossier de sortie: {output_dir}")
    
    # Initialiser le processeur Excel
    processor = JuryExcelProcessor(excel_path)
    
    try:
        # Charger les données
        processor.load_jury_data()
        
        # Obtenir tous les candidats
        candidates = processor.get_all_candidates()
        
        # Rechercher SIANO Marco
        siano = None
        for candidate in candidates:
            if candidate.get('nom') == 'SIANO' and candidate.get('prenom') == 'Marco':
                siano = candidate
                break
        
        if not siano:
            print("SIANO Marco non trouvé dans les données, création manuelle...")
            
            # Créer un candidat minimal
            siano = {
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
                'fin_ep_coll': '16:30',
                'heure_debut': '10:40',
                'heure_fin': '13:30',
                'heure_preparation': '10:40',
                'heure_passage': '11:15',
                'salle': 'Salle d\'examen',
                'duree': '2h30 (collective) + 20min (individuelle)',
                'institution_name': 'Alliance Française Bruxelles Europe',
                'institution_address': 'Avenue des Arts 46',
                'institution_city': 'Bruxelles',
                'institution_postal': '1000',
                'institution_phone': '+32 2 788 21 60',
                'contact_urgence': 'info@alliancefrancaise.be',
                'besoins_speciaux': False,
                'tiers_temps': False
            }
            
            # Appliquer le cas spécial
            siano = processor._apply_special_case_fixes(siano)
        
        print("\nDonnées de SIANO Marco:")
        for key, value in sorted(siano.items()):
            if key in ['nom', 'prenom', 'besoins_speciaux', 'tiers_temps', 'fin_ep_coll', 'fin_ep_coll_affichage', 'niveau']:
                print(f"  - {key}: {value}")
        
        # Créer le générateur de PDF
        print("\nInitialisation du générateur de PDF...")
        generator = PDFGenerator(
            excel_path=excel_path,
            template_path=template_path,
            logo_af_path=logo_af_path,
            logo_delf_path=logo_delf_path,
            output_dir=output_dir
        )
        
        # Générer la convocation
        print("Génération du PDF...")
        output_path = generator.generate_pdf(
            siano, 
            output_filename=f"convocation_SIANO_Marco_B2.pdf"
        )
        
        print(f"\nConvocation générée avec succès: {output_path}")
        
    except Exception as e:
        print(f"Erreur lors de la génération de la convocation: {e}")

if __name__ == "__main__":
    generate_siano_convocation()