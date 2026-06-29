#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction URGENTE du problème de PDF identiques
"""

import os

def fix_pdf_generation_now():
    """Fix immédiat du problème de génération PDF identique"""
    
    print("🚨 CORRECTION URGENTE : Fix du problème PDF identiques")
    print("=" * 60)
    
    # Lire le contenu actuel de main.py
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Identifier le problème : vérifier si la boucle passe bien des données différentes
    old_loop = '''        for candidate in candidates:
            try:
                # DEBUG: Afficher les données du candidat
                print(f"🔍 DEBUG: Candidat {candidate.get('nom', 'INCONNU')} {candidate.get('prenom', '')}:")
                print(f"  - tcf_type: {candidate.get('tcf_type', 'NON_DEFINI')}")
                print(f"  - niveau: {candidate.get('niveau', 'NON_DEFINI')}")
                print(f"  - Toutes les clés: {list(candidate.keys())}")
                
                # Sélectionner le logo TCF approprié pour ce candidat
                tcf_logo_path = self.get_tcf_logo_path(candidate['tcf_type'])
                
                # Mettre à jour le logo TCF pour ce candidat spécifique
                generator.logo_delf_path = tcf_logo_path
                
                # Ajouter les données formatées pour le template
                if 'date_ep_coll' in candidate and candidate['date_ep_coll']:
                    candidate['date_collective_format'] = candidate['date_ep_coll'].strftime("%d/%m/%Y")
                else:
                    candidate['date_collective_format'] = ""
                    
                if 'date_ep_ind' in candidate and candidate['date_ep_ind']:
                    candidate['date_individual_format'] = candidate['date_ep_ind'].strftime("%d/%m/%Y")
                else:
                    candidate['date_individual_format'] = ""
                
                # Ajouter les variables pour le template
                candidate['heure_collective'] = candidate.get('debut_ep_coll', '')
                candidate['heure_individual'] = candidate.get('heure_preparation', '')
                candidate['salle'] = self.salle_collective.get().split()[0] if self.salle_collective.get() else "1"
                candidate['has_individual_exam'] = True  # TCF a toujours une épreuve individuelle
                
                # Les durées sont maintenant définies dans le processeur, pas besoin de les redéfinir ici
                
                # Nom du fichier PDF
                nom = candidate.get('nom', 'INCONNU')
                prenom = candidate.get('prenom', '')
                pdf_filename = f"convocation_tcf_{nom}_{prenom}.pdf".replace(" ", "_")
                pdf_path = os.path.join(output_dir, pdf_filename)
                
                # Générer le PDF avec le template HTML
                pdf_path = generator.generate_pdf(candidate, pdf_filename)'''
    
    new_loop = '''        for candidate in candidates:
            try:
                # DEBUG FORCÉ: Vérifier que chaque candidat est bien différent
                nom = candidate.get('nom', 'INCONNU')
                prenom = candidate.get('prenom', '')
                email = candidate.get('email', 'N/A')
                print(f"\\n🔍 GÉNÉRATION PDF POUR: {prenom} {nom}")
                print(f"   Email: {email}")
                print(f"   TCF Type: {candidate.get('tcf_type', 'N/A')}")
                print(f"   Numéro: {candidate.get('numero_candidat', 'N/A')}")
                
                # CRÉER UNE COPIE PROPRE DES DONNÉES POUR ÉVITER LA CONTAMINATION
                candidate_copy = dict(candidate)
                
                # Sélectionner le logo TCF approprié pour ce candidat
                tcf_logo_path = self.get_tcf_logo_path(candidate_copy['tcf_type'])
                
                # Mettre à jour le logo TCF pour ce candidat spécifique
                generator.logo_delf_path = tcf_logo_path
                
                # Ajouter les données formatées pour le template
                if 'date_ep_coll' in candidate_copy and candidate_copy['date_ep_coll']:
                    candidate_copy['date_collective_format'] = candidate_copy['date_ep_coll'].strftime("%d/%m/%Y")
                else:
                    candidate_copy['date_collective_format'] = ""
                    
                if 'date_ep_ind' in candidate_copy and candidate_copy['date_ep_ind']:
                    candidate_copy['date_individual_format'] = candidate_copy['date_ep_ind'].strftime("%d/%m/%Y")
                else:
                    candidate_copy['date_individual_format'] = ""
                
                # Ajouter les variables pour le template
                candidate_copy['heure_collective'] = candidate_copy.get('debut_ep_coll', '')
                candidate_copy['heure_individual'] = candidate_copy.get('heure_preparation', '')
                candidate_copy['salle'] = self.salle_collective.get().split()[0] if self.salle_collective.get() else "1"
                candidate_copy['has_individual_exam'] = True  # TCF a toujours une épreuve individuelle
                
                # Les durées sont maintenant définies dans le processeur, pas besoin de les redéfinir ici
                
                # Nom du fichier PDF - UTILISER UN NOM UNIQUE AVEC TIMESTAMP
                import time
                timestamp = str(int(time.time() * 1000))[-6:]  # 6 derniers chiffres du timestamp
                pdf_filename = f"convocation_tcf_{nom}_{prenom}_{timestamp}.pdf".replace(" ", "_")
                pdf_path = os.path.join(output_dir, pdf_filename)
                
                print(f"   📄 Nom fichier: {pdf_filename}")
                
                # DEBUG: Vérifier que les données correctes sont passées
                print(f"   🔍 Données passées au générateur:")
                print(f"      nom: {candidate_copy.get('nom', 'N/A')}")
                print(f"      prenom: {candidate_copy.get('prenom', 'N/A')}")
                print(f"      tcf_type: {candidate_copy.get('tcf_type', 'N/A')}")
                
                # Générer le PDF avec le template HTML - UTILISER candidate_copy
                pdf_path = generator.generate_pdf(candidate_copy, pdf_filename)'''
    
    if old_loop in content:
        # Appliquer la correction
        new_content = content.replace(old_loop, new_loop)
        
        # Sauvegarder
        with open('main.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ CORRECTION APPLIQUÉE:")
        print("   - Ajout de debug forcé pour chaque candidat")
        print("   - Utilisation d'une copie propre des données (candidate_copy)")
        print("   - Noms de fichiers avec timestamp pour éviter les écrasements")
        print("   - Debug des données passées au générateur PDF")
        
        print("\n🎯 MAINTENANT:")
        print("1. Testez la génération de PDF avec l'application")
        print("2. Vérifiez les logs pour voir si chaque candidat a bien des données différentes")
        print("3. Vérifiez que les PDF générés ont des contenus différents")
        
        return True
    else:
        print("❌ Pattern de code non trouvé - la structure a peut-être changé")
        return False

if __name__ == "__main__":
    fix_pdf_generation_now()