import pandas as pd
import os
import sys

# Trouver le dossier de sortie le plus récent
output_dirs = [d for d in os.listdir('.') if d.startswith('output_convocations_')]
if not output_dirs:
    print("Aucun dossier de sortie trouvé")
    sys.exit(1)

# Trier par date (le plus récent en premier)
output_dirs.sort(reverse=True)
latest_dir = output_dirs[0]
print(f"Utilisation du dossier: {latest_dir}")

# Chemin vers le fichier Excel
excel_path = os.path.join(latest_dir, 'candidats_export.xlsx')
if not os.path.exists(excel_path):
    print(f"Fichier Excel non trouvé: {excel_path}")
    sys.exit(1)

# Lire le fichier Excel
df = pd.read_excel(excel_path)
print(f"Nombre total de candidats: {len(df)}")

# Afficher les informations sur les candidats
print("\nListe des candidats:")
for i, row in df.iterrows():
    nom = row.get('nom', '')
    prenom = row.get('prenom', '')
    niveau = row.get('niveau', '')
    numero = row.get('numero_candidat', '')
    besoins_speciaux = row.get('besoins_speciaux', False)
    
    bs_text = " (besoins spéciaux)" if besoins_speciaux else ""
    print(f"{i+1}. {nom} {prenom} - Niveau {niveau} - N°{numero}{bs_text}")

# Vérifier si SIANO Marco est présent
siano_rows = df[df['nom'].str.contains('SIANO', case=False, na=False)]
if len(siano_rows) > 0:
    print("\nInformations sur SIANO Marco:")
    for i, row in siano_rows.iterrows():
        print(f"  Nom: {row.get('nom', '')} {row.get('prenom', '')}")
        print(f"  Niveau: {row.get('niveau', '')}")
        print(f"  Numéro: {row.get('numero_candidat', '')}")
        print(f"  Besoins spéciaux: {row.get('besoins_speciaux', False)}")
        print(f"  Tiers-temps: {row.get('tiers_temps', False)}")
        print(f"  Fin épreuve collective: {row.get('fin_ep_coll_affichage', row.get('fin_ep_coll', 'Non définie'))}")
else:
    print("\nSIANO Marco n'a pas été trouvé dans la liste des candidats.")

# Compter les candidats par niveau
niveau_counts = df['niveau'].value_counts().to_dict()
print("\nRépartition par niveau:")
for niveau, count in sorted(niveau_counts.items()):
    print(f"  - Niveau {niveau}: {count} candidats")

# Compter les candidats avec besoins spéciaux
special_needs_count = df['besoins_speciaux'].sum()
print(f"\nCandidats avec besoins spéciaux: {special_needs_count}")
if special_needs_count > 0:
    special_needs = df[df['besoins_speciaux'] == True]
    print("Liste des candidats avec besoins spéciaux:")
    for i, row in special_needs.iterrows():
        print(f"  - {row.get('nom', '')} {row.get('prenom', '')} - Niveau {row.get('niveau', '')}")