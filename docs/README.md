# Générateur de Convocations d'Examens

Application complète pour générer des convocations d'examens au format PDF avec logos SVG et envoi automatique par email via Outlook.

## 🚀 Fonctionnalités

- **Génération de PDF** : Création automatique de convocations personnalisées au format PDF
- **Support SVG** : Intégration de logos SVG dans les convocations
- **Lecture Excel** : Import des données candidats depuis un fichier Excel
- **Envoi automatique** : Envoi des convocations par email via Microsoft Outlook
- **Interface graphique** : Interface utilisateur intuitive avec Tkinter
- **Journalisation** : Suivi détaillé des opérations avec logs

## 📋 Prérequis

### Logiciels requis
- Python 3.8 ou supérieur
- Microsoft Outlook installé et configuré
- Microsoft Excel (pour créer/modifier les fichiers de données)

### Dépendances Python
```bash
pip install -r requirements.txt
```

Les dépendances incluent :
- `pandas` : Lecture des fichiers Excel
- `openpyxl` : Support des fichiers Excel modernes
- `weasyprint` : Génération de PDF à partir de HTML
- `jinja2` : Moteur de templates HTML
- `pywin32` : Intégration avec Microsoft Outlook
- `pillow` : Traitement d'images

## 📁 Structure du projet

```
convoc-generator/
├── main.py                          # Application principale
├── pdf_generator.py                 # Module de génération PDF
├── email_sender.py                  # Module d'envoi d'emails
├── requirements.txt                 # Dépendances Python
├── templates/
│   └── convocation_template.html    # Template HTML des convocations
├── assets/
│   └── logo.svg                     # Logo de l'établissement
├── output/                          # Répertoire des PDF générés
├── exemple_candidats.xlsx           # Fichier d'exemple
└── README.md                        # Documentation
```

## 🔧 Installation

1. **Cloner ou télécharger** le projet dans un répertoire
2. **Installer Python** si ce n'est pas déjà fait
3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurer Outlook** : Assurez-vous qu'Outlook est installé et configuré avec votre compte email

## 📊 Format du fichier Excel

Le fichier Excel doit contenir les colonnes suivantes :

### Colonnes obligatoires
- `nom` : Nom du candidat
- `prenom` : Prénom du candidat
- `numero_candidat` : Numéro unique du candidat
- `email` : Adresse email du candidat
- `date_naissance` : Date de naissance (format DD/MM/YYYY)
- `matiere` : Matière de l'examen
- `date_examen` : Date de l'examen (format DD/MM/YYYY)
- `heure_debut` : Heure de début (format HH:MM)
- `heure_fin` : Heure de fin (format HH:MM)
- `duree` : Durée de l'examen (ex: "3 heures")
- `salle` : Salle d'examen

### Colonnes optionnelles
- `telephone` : Numéro de téléphone
- `batiment` : Bâtiment de l'examen
- `surveillant` : Nom du surveillant
- `materiel_autorise` : Matériel autorisé pour l'examen
- `instructions_supplementaires` : Instructions spéciales
- `institution_name` : Nom de l'établissement
- `institution_address` : Adresse de l'établissement
- `institution_city` : Ville de l'établissement
- `institution_postal` : Code postal
- `institution_phone` : Téléphone de l'établissement

## 🎯 Utilisation

### Lancement de l'application
```bash
python main.py
```

### Étapes d'utilisation

1. **Sélectionner le fichier Excel** contenant les données des candidats
2. **Vérifier le template HTML** (par défaut : `templates/convocation_template.html`)
3. **Sélectionner le logo SVG** (par défaut : `assets/logo.svg`)
4. **Choisir le répertoire de sortie** (par défaut : `output/`)
5. **Générer les PDF** en cliquant sur "Générer PDF"
6. **Envoyer les emails** en cliquant sur "Envoyer Emails"
7. **Ou faire les deux** en cliquant sur "Générer et Envoyer"

### Options disponibles

- **Générer PDF** : Crée uniquement les fichiers PDF
- **Envoyer Emails** : Envoie les emails avec les PDF existants
- **Générer et Envoyer** : Fait les deux opérations en séquence

## 🎨 Personnalisation

### Template HTML
Le template `templates/convocation_template.html` peut être modifié pour :
- Changer l'apparence des convocations
- Ajouter des éléments graphiques
- Modifier la mise en page
- Personnaliser les couleurs et polices

### Logo SVG
Remplacez le fichier `assets/logo.svg` par votre propre logo :
- Format SVG recommandé pour la qualité
- Dimensions optimales : 200x80 pixels
- Couleurs adaptées à l'impression

## 📧 Configuration Email

L'application utilise Microsoft Outlook pour l'envoi d'emails. Assurez-vous que :
- Outlook est installé et configuré
- Votre compte email est actif
- Les paramètres de sécurité permettent l'envoi automatique

### Contenu des emails
Les emails envoyés contiennent :
- Un message personnalisé avec les détails de l'examen
- La convocation en pièce jointe (PDF)
- Les instructions importantes
- Les coordonnées de contact

## 🔍 Dépannage

### Erreurs courantes

**"Python est introuvable"**
- Installez Python depuis python.org
- Ajoutez Python au PATH système

**"Impossible de se connecter à Outlook"**
- Vérifiez qu'Outlook est installé
- Lancez Outlook au moins une fois manuellement
- Vérifiez les paramètres de sécurité

**"Erreur lors de la lecture du fichier Excel"**
- Vérifiez le format du fichier (.xlsx)
- Assurez-vous que les colonnes obligatoires sont présentes
- Fermez le fichier Excel s'il est ouvert

**"Fichier PDF de convocation non trouvé"**
- Générez d'abord les PDF avant d'envoyer les emails
- Vérifiez que le répertoire de sortie contient les fichiers

### Logs et débogage
- Les logs sont affichés dans l'interface et sauvegardés dans `convocation_generator.log`
- Consultez les messages d'erreur pour identifier les problèmes
- Vérifiez les chemins des fichiers et répertoires

## 📝 Exemple d'utilisation

1. Préparez votre fichier Excel avec les données des candidats
2. Personnalisez le logo SVG si nécessaire
3. Lancez l'application : `python main.py`
4. Sélectionnez vos fichiers dans l'interface
5. Cliquez sur "Générer et Envoyer"
6. Surveillez les logs pour suivre le processus

## 🤝 Support

Pour toute question ou problème :
1. Consultez les logs d'erreur
2. Vérifiez la configuration des prérequis
3. Testez avec le fichier d'exemple fourni

## 📄 Licence

Ce projet est fourni tel quel pour usage éducatif et professionnel.

---

**Note** : Cette application nécessite un environnement Windows avec Microsoft Outlook pour fonctionner correctement.
