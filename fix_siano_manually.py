import pandas as pd
import os
import sys
from pdf_generator import PDFGenerator
from jury_excel_processor import JuryExcelProcessor

def manual_fix_for_siano():
    """Applique une correction manuelle pour générer la convocation de SIANO Marco"""
    try:
        # Charger le fichier Excel
        excel_path = "JURYS.xlsx"
        df = pd.read_excel(excel_path, sheet_name="Niveau B2", header=None)
        
        # Trouver SIANO Marco
        siano_row = None
        for i in range(df.shape[0]):
            if not pd.isna(df.iloc[i, 3]) and "SIANO" in str(df.iloc[i, 3]):
                siano_row = i
                break
        
        if siano_row is None:
            print("SIANO Marco non trouvé")
            return
            
        # Créer un dictionnaire avec les données de SIANO Marco
        siano_data = {
            'nom': "SIANO",
            'prenom': "Marco",
            'numero_candidat': str(df.iloc[siano_row, 2]),
            'date_naissance': "31 août 2008",
            'email': str(df.iloc[siano_row, 5]),
            'niveau': "B2",
            'date_examen': "09/10/2025",
            'matiere': "DELF B2",
            'institution_name': "Alliance Française Bruxelles Europe",
            'institution_address': "Avenue des Arts 46",
            'institution_city': "Bruxelles",
            'institution_postal': "1000",
            'institution_phone': "+32 2 788 21 60",
            'contact_urgence': "info@alliancefrancaise.be",
            'heure_preparation': str(df.iloc[siano_row, 0]),
            'heure_passage': str(df.iloc[siano_row, 1]),
            'date_ep_coll': "09/10/2025",
            'debut_ep_coll': "14:00",
            'heure_debut': str(df.iloc[siano_row, 0]),
            'duree': "2h30 (collective) + 20min (individuelle)",
            'salle': "Salle d'examen",
            # Spécifique aux besoins spéciaux
            'besoins_speciaux': True,
            'tiers_temps': True,
            'fin_ep_coll': "17:20",
            'fin_ep_coll_affichage': "17:20 (tiers-temps)"
        }
        
        print("Données préparées pour SIANO Marco:")
        for key, value in siano_data.items():
            print(f"  {key}: {value}")
            
        # Créer le générateur de PDF avec les bons chemins
        template_path = "templates/convocation_delf_template_modele.html"
        if not os.path.exists(template_path):
            print(f"Template non trouvé: {template_path}")
            template_path = "convocation_delf_template_modele.html"
        
        generator = PDFGenerator(
            excel_path=excel_path,
            template_path=template_path,
            logo_af_path="logoAF.svg",
            logo_delf_path="logoDELF.svg",
            output_dir="output_siano_fix"
        )
        
        # Générer le PDF avec les données manuelles
        os.makedirs("output_siano_fix", exist_ok=True)
        output_path = generator.generate_pdf(
            siano_data,
            output_filename="convocation_SIANO_Marco_fixed.pdf"
        )
        
        print(f"\nConvocation générée: {output_path}")
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    manual_fix_for_siano()