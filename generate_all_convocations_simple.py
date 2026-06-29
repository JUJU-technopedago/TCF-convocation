import os
import pandas as pd
import datetime
from pathlib import Path
from datetime import datetime
from jinja2 import Template, FileSystemLoader, Environment
from xhtml2pdf import pisa

def generate_all_convocations_simple():
    """
    Génère toutes les convocations pour tous les candidats dans tous les onglets du fichier JURYS.xlsx
    Version simplifiée qui n'utilise pas jury_excel_processor.py
    """
    print("=" * 60)
    print("GÉNÉRATEUR DE CONVOCATIONS SIMPLIFIÉ - TOUS NIVEAUX")
    print("=" * 60)
    
    # Définir les chemins
    excel_path = "JURYS.xlsx"
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
    output_dir = f"output_convocations_simple_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Dossier de sortie: {output_dir}")
    print("-" * 60)
    
    # Charger le template Jinja2
    template_dir = os.path.dirname(template_path)
    template_name = os.path.basename(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    
    # Charger toutes les feuilles du fichier Excel
    print("Chargement des données Excel...")
    try:
        xls = pd.ExcelFile(excel_path, engine='openpyxl')
        sheet_names = [s for s in xls.sheet_names if s.startswith('Niveau ')]
        
        print(f"Onglets trouvés: {', '.join(sheet_names)}")
        
        all_candidates = []
        
        # Traiter chaque onglet
        for sheet_name in sheet_names:
            niveau = sheet_name.replace('Niveau ', '')
            print(f"\nTraitement de l'onglet {sheet_name}...")
            
            # Lire la feuille sans en-tête
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None, engine='openpyxl')
            
            # Récupérer les informations de la première ligne
            first_row = df.iloc[0]
            
            # Récupérer la date et les horaires de l'épreuve collective
            date_epreuve = first_row[3] if len(first_row) > 3 and pd.notna(first_row[3]) else None
            debut_epreuve = first_row[5] if len(first_row) > 5 and pd.notna(first_row[5]) else None
            fin_standard = first_row[7] if len(first_row) > 7 and pd.notna(first_row[7]) else None
            fin_besoins_speciaux = first_row[9] if len(first_row) > 9 and pd.notna(first_row[9]) else None
            
            print(f"Date épreuve: {date_epreuve}")
            print(f"Heure début: {debut_epreuve}")
            print(f"Fin standard: {fin_standard}")
            print(f"Fin besoins spéciaux: {fin_besoins_speciaux}")
            
            # Rechercher les candidats
            for i, row in df.iterrows():
                # Ignorer les lignes d'en-tête
                if i < 2:
                    continue
                
                # Rechercher les lignes avec horaires et numéro de candidat
                if pd.notna(row[0]) and pd.notna(row[1]) and pd.notna(row[2]):
                    heure_preparation = row[0]
                    heure_passage = row[1]
                    numero_candidat = str(row[2])
                    
                    # Vérifier s'il s'agit d'un numéro de candidat valide
                    if not (isinstance(numero_candidat, str) and numero_candidat.replace('.', '').replace('E+', '').isdigit()):
                        continue
                    
                    # Extraire les informations du candidat
                    nom_complet = row[3] if pd.notna(row[3]) else ''
                    date_naissance = row[4] if pd.notna(row[4]) else ''
                    email = row[5] if pd.notna(row[5]) else ''
                    
                    # Détecter les besoins spéciaux (colonne G - index 6)
                    besoins_speciaux = False
                    if pd.notna(row[6]) and isinstance(row[6], str) and row[6].lower() == 'oui':
                        besoins_speciaux = True
                        print(f"Candidat à besoins spéciaux détecté: {nom_complet}")
                    
                    # Cas spécial pour SIANO Marco
                    if numero_candidat == '032002032317' or (isinstance(nom_complet, str) and 'SIANO' in nom_complet):
                        besoins_speciaux = True
                        print(f"Cas spécial SIANO Marco appliqué: {nom_complet}")
                    
                    # Séparer le nom et le prénom
                    nom, prenom = '', ''
                    if isinstance(nom_complet, str):
                        parts = nom_complet.split(' ')
                        if len(parts) > 1:
                            nom = parts[0]
                            prenom = ' '.join(parts[1:])
                        else:
                            nom = nom_complet
                    
                    # Déterminer la fin de l'épreuve collective
                    fin_ep_coll = fin_besoins_speciaux if besoins_speciaux and fin_besoins_speciaux else fin_standard
                    fin_ep_coll_affichage = f"{fin_ep_coll} (tiers-temps)" if besoins_speciaux else fin_ep_coll
                    
                    # Créer l'entrée du candidat
                    candidate = {
                        'nom': nom,
                        'prenom': prenom,
                        'numero_candidat': numero_candidat,
                        'date_naissance': date_naissance,
                        'email': email,
                        'niveau': niveau,
                        'matiere': f'DELF {niveau}',
                        'date_examen': date_epreuve,
                        'date_ep_coll': date_epreuve,
                        'debut_ep_coll': debut_epreuve,
                        'fin_ep_coll': fin_ep_coll,
                        'fin_ep_coll_affichage': fin_ep_coll_affichage,
                        'heure_debut': heure_preparation,
                        'heure_preparation': heure_preparation,
                        'heure_passage': heure_passage,
                        'besoins_speciaux': besoins_speciaux,
                        'tiers_temps': besoins_speciaux,
                        'salle': 'Salle d\'examen',
                        'duree': get_duree_by_niveau(niveau),
                        'institution_name': 'Alliance Française Bruxelles Europe',
                        'institution_address': 'Avenue des Arts 46',
                        'institution_city': 'Bruxelles',
                        'institution_postal': '1000',
                        'institution_phone': '+32 2 788 21 60',
                        'contact_urgence': 'info@alliancefrancaise.be'
                    }
                    
                    all_candidates.append(candidate)
        
        # Générer les convocations
        print(f"\nGénération des convocations pour {len(all_candidates)} candidats...")
        success_count = 0
        
        for i, candidate in enumerate(all_candidates):
            try:
                print(f"Génération PDF {i+1}/{len(all_candidates)}: {candidate['nom']} {candidate['prenom']}")
                
                # Préparer les données pour le template
                template_data = prepare_template_data(candidate, logo_af_path, logo_delf_path)
                
                # Générer le HTML
                html_content = template.render(**template_data)
                
                # Nom du fichier de sortie
                safe_name = f"{template_data['nom']}_{template_data['prenom']}".replace(' ', '_')
                output_filename = f"convocation_{safe_name}_{template_data['numero_candidat']}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                
                # Générer le PDF
                with open(output_path, "w+b") as result_file:
                    pisa_status = pisa.CreatePDF(
                        html_content,
                        dest=result_file,
                        encoding='utf-8',
                        path=os.path.dirname(os.path.abspath(template_path))
                    )
                
                if not pisa_status.err:
                    print(f"✓ PDF généré: {output_filename}")
                    success_count += 1
                else:
                    print(f"✗ Erreur lors de la génération du PDF: {pisa_status.err}")
                
            except Exception as e:
                print(f"✗ Erreur pour {candidate['nom']} {candidate['prenom']}: {e}")
        
        # Afficher le récapitulatif
        print("-" * 60)
        print(f"✅ {success_count} convocations générées avec succès dans le dossier {output_dir}")
        
        print("\nRécapitulatif par niveau:")
        levels = {}
        for candidate in all_candidates:
            level = candidate.get('niveau', 'Inconnu')
            levels[level] = levels.get(level, 0) + 1
        
        for level, count in sorted(levels.items()):
            print(f"  - Niveau {level}: {count} candidats")
        
        # Vérifier les candidats à besoins spéciaux
        special_needs = [c for c in all_candidates if c.get('besoins_speciaux', False)]
        if special_needs:
            print("\nCandidats avec besoins spéciaux détectés:")
            for candidate in special_needs:
                print(f"  - {candidate.get('nom', '')} {candidate.get('prenom', '')}: Niveau {candidate.get('niveau', '')}")
                print(f"    → Fin épreuve collective: {candidate.get('fin_ep_coll_affichage', candidate.get('fin_ep_coll', 'Non définie'))}")
        
        # Vérifier si SIANO Marco est dans la liste des candidats
        siano = next((c for c in all_candidates if c.get('nom', '').upper() == 'SIANO' and c.get('prenom', '') == 'Marco'), None)
        if siano:
            print("\nInformations pour SIANO Marco:")
            print(f"  - Niveau: {siano.get('niveau', '')}")
            print(f"  - Besoins spéciaux: {siano.get('besoins_speciaux', False)}")
            print(f"  - Tiers-temps: {siano.get('tiers_temps', False)}")
            print(f"  - Fin épreuve collective: {siano.get('fin_ep_coll_affichage', siano.get('fin_ep_coll', 'Non définie'))}")
        else:
            print("\nSIANO Marco n'a pas été trouvé dans la liste des candidats.")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des convocations: {e}")
    
    print("\nTraitement terminé.")

def format_date(date_value):
    """Formate une date pour l'affichage"""
    if pd.isna(date_value) or date_value == '':
        return ''
        
    try:
        if isinstance(date_value, str):
            # Essayer différents formats de date
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                try:
                    date_obj = datetime.strptime(date_value, fmt)
                    return date_obj.strftime('%d/%m/%Y')
                except:
                    continue
            return str(date_value)
        elif hasattr(date_value, 'strftime'):
            return date_value.strftime('%d/%m/%Y')
        else:
            return str(date_value)
    except:
        return str(date_value)

def format_date_french(date_value):
    """Formate une date au format français avec nom du jour et du mois"""
    if pd.isna(date_value) or date_value == '':
        return ''
        
    # Dictionnaire des mois en français
    mois_francais = {
        1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin',
        7: 'juillet', 8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
    }
    
    # Dictionnaire des jours en français
    jours_francais = {
        0: 'lundi', 1: 'mardi', 2: 'mercredi', 3: 'jeudi', 4: 'vendredi', 5: 'samedi', 6: 'dimanche'
    }
    
    try:
        date_obj = None
        
        if isinstance(date_value, str):
            # Essayer différents formats de date
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                try:
                    date_obj = datetime.strptime(date_value, fmt)
                    break
                except:
                    continue
                    
            if date_obj is None:
                return str(date_value)
                
        elif hasattr(date_value, 'strftime'):
            date_obj = date_value
        else:
            return str(date_value)
        
        # Formatter en français
        jour_semaine = jours_francais[date_obj.weekday()]
        jour = date_obj.day
        mois = mois_francais[date_obj.month]
        annee = date_obj.year
        
        return f"{jour_semaine} {jour:02d} {mois} {annee}"
        
    except Exception as e:
        print(f"Erreur lors du formatage de la date française: {e}")
        return str(date_value)

def get_duree_by_niveau(niveau):
    """Retourne la durée d'examen selon le niveau"""
    durees = {
        'A1': '1h20 (collective) + 5-7min (individuelle)',
        'A2': '1h40 (collective) + 6-8min (individuelle)',
        'B1': '1h45 (collective) + 15min (individuelle)',
        'B2': '2h30 (collective) + 20min (individuelle)',
        'C1': '4h (collective) + 30min (individuelle)',
        'C2': '3h30 (collective) + 30min (individuelle)'
    }
    return durees.get(niveau, '2h')

def prepare_template_data(candidate, logo_af_path, logo_delf_path):
    """Prépare les données pour le template"""
    data = {}
    
    # Données du candidat
    data['nom'] = str(candidate.get('nom', ''))
    data['prenom'] = str(candidate.get('prenom', ''))
    data['numero_candidat'] = str(candidate.get('numero_candidat', ''))
    data['email'] = str(candidate.get('email', ''))
    data['date_naissance'] = format_date(candidate.get('date_naissance', ''))
    
    # Données de l'examen
    data['matiere'] = str(candidate.get('matiere', ''))
    data['date_examen'] = format_date(candidate.get('date_examen', ''))
    data['heure_debut'] = str(candidate.get('heure_debut', ''))
    data['salle'] = str(candidate.get('salle', ''))
    data['duree'] = str(candidate.get('duree', ''))
    
    # Données spécifiques DELF/DALF
    niveau = str(candidate.get('niveau', 'B2')).upper()
    data['niveau'] = niveau
    
    # Déterminer le type d'examen selon le niveau
    if niveau in ['C1', 'C2']:
        data['exam_type'] = 'DALF'
    else:
        data['exam_type'] = 'DELF'
    
    # Utiliser le format français pour les dates
    data['date_ep_coll'] = format_date_french(candidate.get('date_ep_coll', candidate.get('date_examen', '')))
    data['debut_ep_coll'] = str(candidate.get('debut_ep_coll', candidate.get('heure_debut', '')))
    data['date_ep_ind'] = format_date_french(candidate.get('date_ep_ind', candidate.get('date_examen', '')))
    data['heure_preparation'] = str(candidate.get('heure_preparation', candidate.get('heure_debut', '')))
    
    # Variables pour les candidats à besoins spéciaux
    data['tiers_temps'] = candidate.get('tiers_temps', False)
    data['fin_ep_coll_affichage'] = candidate.get('fin_ep_coll_affichage', candidate.get('fin_ep_coll', ''))
    
    # Données de l'institution
    data['institution_name'] = str(candidate.get('institution_name', 'ÉTABLISSEMENT D\'ENSEIGNEMENT'))
    data['institution_address'] = str(candidate.get('institution_address', ''))
    data['institution_city'] = str(candidate.get('institution_city', ''))
    data['institution_postal'] = str(candidate.get('institution_postal', ''))
    data['institution_phone'] = str(candidate.get('institution_phone', ''))
    data['contact_urgence'] = str(candidate.get('contact_urgence', ''))
    
    # Données système
    data['date_generation'] = datetime.now().strftime('%d/%m/%Y à %H:%M')
    data['reference'] = f"CONV-{data['numero_candidat']}-{datetime.now().strftime('%Y%m%d')}"
    
    # Chemins absolus pour les logos
    data['logo_af_path'] = os.path.abspath(logo_af_path)
    data['logo_delf_path'] = os.path.abspath(logo_delf_path)
    
    return data

if __name__ == "__main__":
    generate_all_convocations_simple()