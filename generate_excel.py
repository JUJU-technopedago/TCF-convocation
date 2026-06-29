import os
import datetime
from jury_excel_processor import JuryExcelProcessor

def generate_all_pdf_simple():
    """
    Version simplifiée du générateur de PDF qui utilise directement JuryExcelProcessor
    """
    print("=" * 60)
    print("GÉNÉRATEUR DE CONVOCATIONS - VERSION SIMPLIFIÉE")
    print("=" * 60)
    
    # Définir les chemins
    excel_path = "JURYS.xlsx"
    template_path = "templates/convocation_delf_template_modele.html"
    
    # Vérifier les chemins des logos
    logo_af_path = "logoAF.svg"
    logo_delf_path = "logoDELF.svg"
    
    # Créer un dossier de sortie avec horodatage
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output_convocations_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Dossier de sortie: {output_dir}")
    print("-" * 60)
    
    # Initialiser le processeur Excel
    print("Chargement des données Excel...")
    processor = JuryExcelProcessor(excel_path)
    
    try:
        # Charger les données
        processor.load_jury_data()
        
        # Obtenir tous les candidats
        candidates = processor.get_all_candidates()
        print(f"Trouvé {len(candidates)} candidats")
        
        # Compter par niveau
        levels = {}
        for candidate in candidates:
            level = candidate.get('niveau', 'Inconnu')
            levels[level] = levels.get(level, 0) + 1
        
        # Afficher le récapitulatif par niveau
        for level, count in sorted(levels.items()):
            print(f"  - Niveau {level}: {count} candidats")
        
        # Vérifier les candidats à besoins spéciaux
        special_needs = [c for c in candidates if c.get('besoins_speciaux', False)]
        print(f"\nCandidats avec besoins spéciaux: {len(special_needs)}")
        
        for candidate in special_needs:
            print(f"  - {candidate.get('nom', '')} {candidate.get('prenom', '')}: Niveau {candidate.get('niveau', '')}")
            print(f"    → Fin épreuve: {candidate.get('fin_ep_coll_affichage', candidate.get('fin_ep_coll', 'Non définie'))}")
        
        # Générer un Excel avec tous les candidats
        output_excel = os.path.join(output_dir, "tous_candidats.xlsx")
        count = processor.export_to_standard_excel(output_excel)
        print(f"\nExcel généré avec {count} candidats: {output_excel}")
        
        print("\nPour générer les PDF, utilisez:")
        print(f"  > python -c \"from pdf_generator import PDFGenerator; g = PDFGenerator('{excel_path}', '{template_path}', '{logo_af_path}', '{logo_delf_path}', '{output_dir}'); g.generate_all_pdfs()\"")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    generate_all_pdf_simple()