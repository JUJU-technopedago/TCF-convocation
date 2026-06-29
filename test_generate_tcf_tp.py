#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour générer les convocations des 3 onglets TCF TP
"""

import sys
import os
from tcf_excel_processor import TCFExcelProcessor
from pdf_generator import PDFGenerator
from candidate_pdf_registry import CandidatePDFRegistry

def test_generate_tcf_tp_convocations():
    """Teste la génération des convocations pour les 3 onglets TCF TP"""
    
    print('🧪 TEST GÉNÉRATION CONVOCATIONS TCF TP')
    print('=' * 70)
    
    # Configuration
    excel_path = 'JURYS FINAL TCF.xlsx'
    template_path = 'templates/convocation_tcf_template_modele.html'
    output_dir = 'output_test_tcf_tp'
    
    # Vérifier les fichiers
    if not os.path.exists(excel_path):
        print(f"❌ Fichier Excel non trouvé: {excel_path}")
        return
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé: {template_path}")
        return
    
    # Créer le dossier de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    print(f'\n📁 Configuration:')
    print(f'   Excel: {excel_path}')
    print(f'   Template: {template_path}')
    print(f'   Output: {output_dir}')
    
    # Charger les données TCF
    print(f'\n📊 Chargement des données TCF...')
    processor = TCFExcelProcessor(excel_path)
    processor.load_tcf_data()
    
    # Récupérer tous les candidats
    candidates = processor.get_all_candidates()
    
    print(f'\n✅ {len(candidates)} candidat(s) chargé(s)')
    
    # Filtrer les candidats des 3 onglets TCF TP
    tcf_tp_sheets = ['TCF TP OBLIGATOIRE', 'TCF TP EE', 'TCF TP EO']
    tcf_tp_candidates = [c for c in candidates if c.get('tcf_type') in tcf_tp_sheets]
    
    print(f'🎯 {len(tcf_tp_candidates)} candidat(s) TCF TP à traiter')
    
    # Afficher le détail
    print(f'\n📋 Répartition par type:')
    for sheet in tcf_tp_sheets:
        count = len([c for c in tcf_tp_candidates if c.get('tcf_type') == sheet])
        print(f'   • {sheet}: {count} candidat(s)')
    
    if not tcf_tp_candidates:
        print('\n⚠️ Aucun candidat TCF TP trouvé')
        return
    
    # Initialiser le registre
    registry = CandidatePDFRegistry(output_dir)
    
    # Créer le générateur PDF
    generator = PDFGenerator(
        excel_path=excel_path,
        template_path=template_path,
        logo_af_path='logos/logo_af.png',
        logo_delf_path='logos/logo_tcf.png',
        output_dir=output_dir,
        access_code='1234',
        qrcode_path='qrcode.png',
        image_a1_path='',
        image_a2_path='',
        image_b1_path='',
        image_b2_path='',
        image_c1_path='',
        image_c2_path=''
    )
    
    # Générer les PDFs
    print(f'\n🔄 Génération des PDFs...')
    print('=' * 70)
    
    success_count = 0
    failed_count = 0
    
    for i, candidate in enumerate(tcf_tp_candidates, 1):
        try:
            nom = candidate.get('nom', 'INCONNU')
            prenom = candidate.get('prenom', '')
            tcf_type = candidate.get('tcf_type', 'N/A')
            
            print(f'\n[{i}/{len(tcf_tp_candidates)}] 📄 {prenom} {nom} ({tcf_type})')
            
            # Générer nom de fichier
            secure_filename = registry.generate_secure_filename(candidate, "TCF")
            
            # Préparer les données du candidat
            candidate_copy = dict(candidate)
            
            # Formater les dates
            if 'date_ep_coll' in candidate_copy and candidate_copy['date_ep_coll']:
                if hasattr(candidate_copy['date_ep_coll'], 'strftime'):
                    candidate_copy['date_collective_format'] = candidate_copy['date_ep_coll'].strftime("%d/%m/%Y")
            
            if 'date_ep_ind' in candidate_copy and candidate_copy['date_ep_ind']:
                if hasattr(candidate_copy['date_ep_ind'], 'strftime'):
                    candidate_copy['date_individual_format'] = candidate_copy['date_ep_ind'].strftime("%d/%m/%Y")
            
            # Ajouter les variables pour le template
            candidate_copy['heure_collective'] = candidate_copy.get('debut_ep_coll', '')
            candidate_copy['heure_individual'] = candidate_copy.get('heure_preparation', '')
            candidate_copy['salle'] = '1'
            
            # Déterminer si ce type a une épreuve individuelle
            has_individual = tcf_type != 'TCF TP EE'
            candidate_copy['has_individual_exam'] = has_individual
            
            print(f'   📌 Type: {tcf_type}')
            print(f'   🕒 Heure collective: {candidate_copy.get("heure_collective", "N/A")}')
            print(f'   🕒 Heure individuelle: {candidate_copy.get("heure_individual", "N/A")}')
            print(f'   👤 Épreuve individuelle: {"Oui" if has_individual else "Non"}')
            
            # Générer le PDF
            pdf_path = generator.generate_pdf(candidate_copy, secure_filename)
            
            if pdf_path and os.path.exists(pdf_path):
                # Enregistrer dans le registre
                registry.register_candidate_pdf(candidate_copy, secure_filename, pdf_path)
                print(f'   ✅ PDF généré: {secure_filename}')
                success_count += 1
            else:
                print(f'   ❌ Échec de génération')
                failed_count += 1
                
        except Exception as e:
            print(f'   ❌ Erreur: {e}')
            import traceback
            traceback.print_exc()
            failed_count += 1
    
    # Résumé
    print(f'\n\n' + '=' * 70)
    print(f'📊 RÉSUMÉ:')
    print('=' * 70)
    print(f'✅ Succès: {success_count} PDF(s)')
    print(f'❌ Échecs: {failed_count} PDF(s)')
    print(f'📁 Dossier: {output_dir}')
    print('=' * 70)
    
    # Lister les fichiers générés
    if success_count > 0:
        print(f'\n📄 Fichiers générés:')
        for filename in sorted(os.listdir(output_dir)):
            if filename.endswith('.pdf'):
                filepath = os.path.join(output_dir, filename)
                size = os.path.getsize(filepath)
                print(f'   • {filename} ({size:,} octets)')

if __name__ == "__main__":
    test_generate_tcf_tp_convocations()
