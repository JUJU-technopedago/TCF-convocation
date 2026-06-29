#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour les fonctions de formatage de date
"""

from datetime import datetime
import pandas as pd
import os
import sys
import traceback

# Importer directement les fonctions de formatage de date
def test_date_formats():
    """Test les fonctions de formatage de date dans le générateur PDF"""
    
    # Importer les fonctions de formatage de date depuis pdf_generator.py
    from pdf_generator import PDFGenerator
    
    # Créer une classe simplifiée pour tester les fonctions de date
    class DateFormatter:
        def __init__(self):
            pass
        
        def _format_date(self, date_value):
            """Version simplifiée de _format_date du générateur PDF"""
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
        
        def _format_date_french(self, date_value):
            """Version simplifiée de _format_date_french du générateur PDF"""
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
                # Vérifier si c'est une date déjà formatée en français
                if isinstance(date_value, str) and any(jour in date_value.lower() for jour in jours_francais.values()):
                    return date_value  # Déjà au format français
                    
                date_obj = None
                
                if isinstance(date_value, str):
                    # Essayer différents formats de date
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                        try:
                            date_obj = datetime.strptime(date_value, fmt)
                            break
                        except Exception:
                            continue
                            
                    if date_obj is None:
                        return str(date_value)
                        
                elif hasattr(date_value, 'strftime'):
                    date_obj = date_value
                else:
                    return str(date_value)
                
                # Formatter en français
                try:
                    jour_semaine = jours_francais[date_obj.weekday()]
                    jour = date_obj.day
                    mois = mois_francais[date_obj.month]
                    annee = date_obj.year
                    
                    return f"{jour_semaine} {jour:02d} {mois} {annee}"
                except Exception as e:
                    print(f"Erreur lors du formatage de la date (après parsing): {e}")
                    # Fallback: format simple
                    return date_obj.strftime('%d/%m/%Y')
                
            except Exception as e:
                print(f"Erreur lors du formatage de la date française: {e}")
                print(f"Détails: {traceback.format_exc()}")
                return str(date_value)
    
    # Utiliser notre classe simplifiée
    formatter = DateFormatter()
    
    # Liste des dates de test (différents formats)
    test_dates = [
        "2023-01-15",             # Format ISO
        "15/01/2023",             # Format français
        "15-01-2023",             # Format avec tirets
        datetime.now(),           # Objet datetime
        pd.Timestamp.now(),       # Timestamp pandas
        "01/02/2023",             # Format ambigu (jour/mois ou mois/jour?)
        "2023/01/15",             # Format année en premier avec /
        "lundi 15 janvier 2023",  # Déjà formaté en français
        "15 janvier 2023",        # Date française sans jour de semaine
        "",                       # Chaîne vide
        None,                     # None
        "invalid date",           # Date invalide
    ]
    
    # En-tête du tableau de résultats
    print("\n{:<20} | {:<15} | {:<25}".format("Date originale", "Format standard", "Format français"))
    print("-" * 65)
    
    # Tester chaque date
    for date in test_dates:
        try:
            # Formater la date en format standard et français
            date_standard = formatter._format_date(date)
            date_french = formatter._format_date_french(date)
            
            # Afficher les résultats
            orig = str(date)[:20] if date is not None else "None"
            print("{:<20} | {:<15} | {:<25}".format(orig, date_standard, date_french))
        except Exception as e:
            print(f"Erreur avec {date}: {e}")
    
    print("\nTest de formatage des dates terminé!")

if __name__ == "__main__":
    test_date_formats()