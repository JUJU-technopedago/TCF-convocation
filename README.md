# Générateur de Convocations DELF/DALF

Version courante: 2.0.1

## 🎉 Système entièrement intégré et organisé

Application complète pour générer et envoyer des convocations d'examens DELF/DALF avec détection automatique des fichiers de jurys.

## 📁 Structure du projet

### 📂 Fichiers principaux (racine)
- **`main.py`** - Application principale avec interface graphique
- **`pdf_generator.py`** - Générateur de PDFs de convocations
- **`mailjet_bridge.py`** - Bridge sécurisé pour l'envoi d'emails via Mailjet
- **`jury_file_processor.py`** - Processeur pour fichiers de jurys DELF/DALF

### 📂 `tests/` - Tests et validation
- `test_integrated_jury_system.py` - Test du système intégré
- `test_jury_email_format.py` - Test du format d'email DELF/DALF
- `test_new_email_format.py` - Test du nouveau format d'email
- Et 38 autres fichiers de test pour validation complète

### 📂 `scripts/` - Scripts utilitaires
- `cleanup_final.py` - Script de nettoyage et organisation
- `extract_jury_emails.py` - Extraction d'emails depuis fichiers de jurys
- `convert_jury_to_mailjet_format.py` - Conversion de formats
- `validate_emails_for_mailjet.py` - Validation des emails
- `check_missing_pdfs.py` - Vérification des PDFs manquants
- Et 3 scripts de régénération

### 📂 `docs/` - Documentation
- `GUIDE_UTILISATION_FINALE.md` - **Guide principal d'utilisation**
- `GUIDE_FICHIERS_JURYS.md` - Guide pour fichiers de jurys
- `DELF_DALF_GUIDE.md` - Guide spécifique DELF/DALF
- Et 19 autres guides techniques et de dépannage

### 📂 `archive/` - Fichiers obsolètes
- 39 fichiers archivés (anciennes versions, tests obsolètes, etc.)

### 📂 `templates/` - Templates HTML
- Templates pour génération des emails et PDFs

### 📂 `assets/` - Ressources
- Logos et images pour les convocations

### 📂 `output/` - Fichiers générés
- PDFs de convocations générés
- Logs et fichiers temporaires

## 🚀 Utilisation rapide

### 1. Lancement
```bash
python main.py
```

### 2. Chargement d'un fichier de jurys
- Sélectionnez votre fichier `juries_YYYYMMDD_HHMMSS.xlsx`
- **L'application détecte automatiquement le format et convertit les données**

### 3. Configuration email
- Cliquez sur "📧 MAILJET" pour configurer l'envoi d'emails

### 4. Génération et envoi
- Cliquez sur "Générer et Envoyer"
- L'application traite automatiquement tous les candidats

## ✅ Fonctionnalités principales

### 🔍 Détection automatique
- Reconnaît les fichiers de jurys vs fichiers candidats classiques
- Conversion transparente sans intervention manuelle

### 📧 Format d'email DELF/DALF
- Noms en majuscules automatiques
- Dates françaises avec jour de la semaine
- Sections séparées pour épreuves collectives et individuelles
- Instructions "30 minutes avant" mises en évidence
- Section [IMPORTANT] en rouge (#da002e)

### 🔒 Sécurité
- Credentials Mailjet chiffrés
- Envoi via HTTPS sécurisé
- Gestion d'erreurs robuste

### 📊 Gestion complète
- Support de tous les niveaux (A1, A2, B1, B2, C1, C2)
- Récupération automatique des dates et heures d'épreuves
- Génération de PDFs avec logos et mise en forme

## 📋 Prérequis

- Python 3.11+
- Modules requis: `pip install -r requirements.txt`
- Compte Mailjet pour l'envoi d'emails
- Fichiers de logos dans `assets/`

## 🆘 Support

Consultez la documentation dans le dossier `docs/`:
- **`GUIDE_UTILISATION_FINALE.md`** pour l'utilisation complète
- **`GUIDE_FICHIERS_JURYS.md`** pour les fichiers de jurys
- Autres guides pour dépannage et configuration avancée

## 🎯 Résultats

Le système traite automatiquement:
- **135 candidats** depuis le fichier de jurys de test
- **6 niveaux DELF/DALF** (A1: 7, A2: 18, B1: 26, B2: 49, C1: 28, C2: 7)
- **Format d'email professionnel** conforme aux standards
- **Envoi sécurisé** via Mailjet avec pièces jointes PDF

---

*Système testé et validé - Prêt pour la production* ✨
