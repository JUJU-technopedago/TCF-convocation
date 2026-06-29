#!/usr/bin/env python3
"""
Test des objets d'emails avec les vraies données du fichier TCF
"""

import sys
import types

# Patcher le module cryptography avant l'import
class MockFernet:
    def __init__(self, key): pass
    def encrypt(self, data): return b'mock'
    def decrypt(self, data): return b'mock'

mock_fernet = types.ModuleType('cryptography.fernet')
mock_fernet.Fernet = MockFernet
mock_fernet.Fernet.generate_key = lambda: b'key'
sys.modules['cryptography.fernet'] = mock_fernet

from mailjet_bridge import MailjetBridge

def test_real_candidates():
    bridge = MailjetBridge('JURYS FINAL TCF - Copie.xlsx', '.')
    
    # Charger les vrais candidats
    data = bridge._load_excel_data()
    print(f"📋 Candidats chargés: {len(data)}")
    
    if len(data) > 0:
        print("\n📧 TEST AVEC VRAIS CANDIDATS :")
        print("=" * 60)
        
        for i, row in data.iterrows():
            candidat = row.to_dict()
            
            # Informations du candidat
            nom = candidat.get('nom', '')
            prenom = candidat.get('prenom', '')
            type_tcf = candidat.get('type_tcf', '')
            
            print(f"\n{i+1}. {prenom} {nom} ({type_tcf})")
            print(f"   Données disponibles:")
            print(f"   - date_naissance: {candidat.get('date_naissance', 'N/A')}")
            print(f"   - heure_passation: {candidat.get('heure_passation', 'N/A')}")
            print(f"   - date_examen: {candidat.get('date_examen', 'N/A')}")
            
            # Ajouter les champs nécessaires pour la méthode
            candidat['matiere'] = type_tcf  # Utiliser le type TCF comme matière
            candidat['tcf_type'] = type_tcf
            
            # Pour TCF, il faut une date_collective_format
            if type_tcf == 'TCF CANADA':
                candidat['date_collective_format'] = 'le dimanche 13 octobre 2025'
            elif type_tcf == 'TCF TP COMPLET':
                candidat['date_collective_format'] = 'le mercredi 16 octobre 2025'
            elif type_tcf == 'TCF IRN':
                candidat['date_collective_format'] = 'le jeudi 17 octobre 2025'
            else:
                candidat['date_collective_format'] = 'le mercredi 16 octobre 2025'
            
            try:
                subject, _, _ = bridge._create_email_content(candidat)
                print(f"   📧 Objet: {subject}")
                
                # Vérifier que la date est présente
                if 'octobre 2025' in subject:
                    print(f"   ✅ Date présente dans l'objet")
                else:
                    print(f"   ❌ Date manquante dans l'objet!")
                    
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        print("\n" + "=" * 60)
        print("🎯 Vérification: Toutes les dates doivent apparaître dans les objets !")

if __name__ == "__main__":
    test_real_candidates()