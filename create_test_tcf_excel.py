#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Créer un fichier Excel de test pour les examens TCF
"""

import pandas as pd
from datetime import datetime, date

def create_test_tcf_excel():
    """Créer un fichier Excel TCF de test"""
    print("📊 CRÉATION FICHIER EXCEL TCF DE TEST")
    print("=" * 50)
    
    # Données de test pour TCF
    test_data = [
        {
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
            'salle_collective': 'Salle 101',
            'salle_individuelle': 'Salle 102'
        },
        {
            'nom': 'DURAND',
            'prenom': 'Marie',
            'date_naissance': '22/08/1985',
            'email': 'marie.durand@email.com',
            'tcf_type': 'TCF TP',
            'date_examen': '15/12/2024',
            'date_ep_coll': date(2024, 12, 15),
            'date_ep_ind': date(2024, 12, 15),
            'debut_ep_coll': '09:00',
            'heure_preparation': '14:30',
            'duree_collective': '1h30',
            'duree_individuelle': '15 min',
            'salle_collective': 'Salle 101',
            'salle_individuelle': 'Salle 102'
        },
        {
            'nom': 'GARCIA',
            'prenom': 'Carlos',
            'date_naissance': '10/11/1992',
            'email': 'carlos.garcia@email.com',
            'tcf_type': 'TCF SO',
            'date_examen': '15/12/2024',
            'date_ep_coll': date(2024, 12, 15),
            'date_ep_ind': date(2024, 12, 15),
            'debut_ep_coll': '09:00',
            'heure_preparation': '15:00',
            'duree_collective': '1h30',
            'duree_individuelle': '15 min',
            'salle_collective': 'Salle 101',
            'salle_individuelle': 'Salle 102'
        }
    ]
    
    try:
        # Créer le DataFrame
        df = pd.DataFrame(test_data)
        
        # Nom du fichier
        excel_filename = 'test_tcf_data.xlsx'
        
        # Sauvegarder avec le nom de feuille attendu par le processeur
        df.to_excel(excel_filename, index=False, sheet_name='TCF SO')
        
        print(f"✅ Fichier Excel créé: {excel_filename}")
        print(f"👥 Candidats: {len(test_data)}")
        print(f"📋 Colonnes: {list(df.columns)}")
        
        # Vérifier le fichier
        df_check = pd.read_excel(excel_filename)
        print(f"✓ Vérification: {len(df_check)} lignes lues")
        
        return excel_filename
        
    except Exception as e:
        print(f"❌ Erreur création Excel: {e}")
        return None

def main():
    """Programme principal"""
    filename = create_test_tcf_excel()
    if filename:
        print(f"\\n🎉 Fichier de test prêt: {filename}")
        return True
    else:
        print("\\n❌ Échec création fichier de test")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n✅ Test Excel créé avec succès!")
    else:
        print("\\n❌ Échec création test Excel")