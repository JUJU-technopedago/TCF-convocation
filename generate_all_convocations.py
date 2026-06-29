import os
import sys
from datetime import datetime
from jury_excel_processor import JuryExcelProcessor
from pdf_generator import PDFGenerator

def generate_all_convocations():
    """
    Génère toutes les convocations pour tous les candidats dans tous les onglets du fichier JURYS.xlsx
    """
    print("=" * 60)
    print("GÉNÉRATEUR DE CONVOCATIONS - TOUS NIVEAUX")
    print("=" * 60)
    
    # Trouver le fichier Excel le plus récent
    excel_files = [f for f in os.listdir('.') if f.startswith('juries_') and f.endswith('.xlsx')]
    
    if not excel_files:
        print("Aucun fichier Excel trouvé avec le format juries_*.xlsx")
        sys.exit(1)
    
    # Trier par date de modification (le plus récent en premier)
    excel_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    excel_path = excel_files[0]
    print(f"Utilisation du fichier: {excel_path}")
    
    # Définir les chemins
    template_path = "convocation_delf_template_modele.html"
    if not os.path.exists(template_path):
        template_path = "templates/convocation_delf_template_modele.html"
    
    # Vérifier les chemins des logos
    logo_af_path = "logoAF.svg"
    logo_delf_path = "logoDELF.svg"
    
    if not os.path.exists(logo_af_path):
        print(f"⚠️ Logo AF non trouvé à {logo_af_path}, utilisation du chemin par défaut")
        logo_af_path = "assets/logoAF.svg"
    
    if not os.path.exists(logo_delf_path):
        print(f"⚠️ Logo DELF non trouvé à {logo_delf_path}, utilisation du chemin par défaut")
        logo_delf_path = "assets/logoDELF.svg"
    
    # Créer un dossier de sortie avec horodatage
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output_convocations_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Dossier de sortie: {output_dir}")
    print("-" * 60)
    
    # Initialiser le processeur Excel et le générateur PDF
    print("Initialisation du processeur Excel et du générateur PDF...")
    processor = JuryExcelProcessor(excel_path)
    pdf_generator = PDFGenerator(
        excel_path=excel_path,
        template_path=template_path,
        logo_af_path=logo_af_path,
        logo_delf_path=logo_delf_path,
        output_dir=output_dir
    )
    
    # Charger les données des jurys
    print("Chargement des données du fichier Excel...")
    processor.load_jury_data()
    
    # Obtenir tous les candidats
    all_candidates = processor.get_all_candidates()
    
    if not all_candidates:
        print("Aucun candidat trouvé dans le fichier Excel.")
        return
    
    print(f"Nombre total de candidats trouvés: {len(all_candidates)}")
    
    # Compter les candidats par niveau
    niveau_counts = {}
    for candidat in all_candidates:
        niveau = candidat.get('niveau', 'Inconnu')
        niveau_counts[niveau] = niveau_counts.get(niveau, 0) + 1
    
    print("\nCandidats par niveau:")
    for niveau, count in sorted(niveau_counts.items()):
        print(f"  - Niveau {niveau}: {count} candidats")
    
    # Compter les candidats avec besoins spéciaux
    special_needs = [c for c in all_candidates if c.get('besoins_speciaux', False)]
    special_needs_count = len(special_needs)
    print(f"Candidats avec besoins spéciaux: {special_needs_count}")
    
    # Générer les PDF pour chaque candidat
    generated_files = []
    success_count = 0
    print("\nGénération des convocations PDF:")
    
    for i, candidat in enumerate(all_candidates):
        try:
            # Format du nom de fichier: convocation_NOM_Prenom_Niveau.pdf
            nom_fichier = f"convocation_{candidat['nom']}_{candidat['prenom']}_{candidat['niveau']}.pdf"
            
            # Générer le PDF directement avec le processeur PDF
            try:
                pdf_path = pdf_generator.generate_pdf(candidat)
                success_count += 1
                
                # Afficher la progression
                print(f"[{i+1}/{len(all_candidates)}] Généré: {os.path.basename(pdf_path)}")
                
                # Afficher des détails supplémentaires pour les candidats à besoins spéciaux
                if candidat.get('besoins_speciaux', False):
                    print(f"  - Besoins spéciaux: Oui")
                    print(f"  - Fin épreuve collective: {candidat.get('fin_ep_coll_affichage', '')}")
                
            except Exception as e:
                print(f"ERREUR pour le candidat {candidat.get('nom', '')} {candidat.get('prenom', '')}: {str(e)}")
            
        except Exception as e:
            print(f"ERREUR pour le candidat {candidat.get('nom', '')} {candidat.get('prenom', '')}: {str(e)}")
    
    print("-" * 60)
    print(f"✅ {success_count} convocations générées avec succès dans le dossier {output_dir}")
    
    # Récapitulatif des besoins spéciaux
    if special_needs:
        print("\nCandidats avec besoins spéciaux détectés:")
        for candidate in special_needs:
            print(f"  - {candidate.get('nom', '')} {candidate.get('prenom', '')}: Niveau {candidate.get('niveau', '')}")
            print(f"    → Fin épreuve collective: {candidate.get('fin_ep_coll_affichage', candidate.get('fin_ep_coll', 'Non définie'))}")
            
    # Vérifier si SIANO Marco est dans la liste des candidats à besoins spéciaux
    siano = next((c for c in all_candidates if 'SIANO' in c.get('nom', '').upper() and 'Marco' in c.get('prenom', '')), None)
    if siano:
        print("\nInformations pour SIANO Marco:")
        print(f"  - Niveau: {siano.get('niveau', '')}")
        print(f"  - Besoins spéciaux: {siano.get('besoins_speciaux', False)}")
        print(f"  - Tiers-temps: {siano.get('tiers_temps', False)}")
        print(f"  - Fin épreuve collective: {siano.get('fin_ep_coll_affichage', siano.get('fin_ep_coll', 'Non définie'))}")
    else:
        print("\nSIANO Marco n'a pas été trouvé dans la liste des candidats.")
    
    # Exporter également vers Excel pour validation
    excel_output = os.path.join(output_dir, "candidats_export.xlsx")
    processor.export_to_standard_excel(excel_output)
    print(f"\nExport Excel créé: {excel_output}")
    
    print("\nTraitement terminé.")

if __name__ == "__main__":
    generate_all_convocations()