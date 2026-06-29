# Guide d'utilisation finale - Système intégré avec fichiers de jurys

## 🎉 Système entièrement intégré et fonctionnel!

Le système d'emails est maintenant **entièrement automatisé** et compatible avec les fichiers de jurys DELF/DALF. Plus besoin de conversion manuelle!

## ✅ Fonctionnalités intégrées

### 🔍 Détection automatique
- L'application détecte automatiquement si le fichier Excel est un fichier de jurys
- Aucune intervention manuelle requise

### 🔄 Conversion automatique
- Conversion transparente des fichiers de jurys en format candidats
- Extraction automatique de tous les niveaux (A1, A2, B1, B2, C1, C2)
- Récupération des bonnes dates et heures pour chaque type d'épreuve

### 📧 Format d'email DELF/DALF
- Noms en majuscules automatiques
- Dates françaises avec jour de la semaine
- Sections séparées pour épreuves collectives et individuelles
- Instruction "30 minutes avant" mise en évidence
- Section [IMPORTANT] en rouge (#da002e)

## 🚀 Utilisation simple

### 1. Dans l'application principale (main.py)

1. **Lancez l'application:**
   ```bash
   python main.py
   ```

2. **Sélectionnez votre fichier de jurys:**
   - Cliquez sur "Parcourir" à côté de "Fichier Excel des candidats"
   - Sélectionnez votre fichier `juries_YYYYMMDD_HHMMSS.xlsx`
   - **L'application détectera automatiquement que c'est un fichier de jurys**

3. **Configurez Mailjet (si pas déjà fait):**
   - Cliquez sur "📧 MAILJET"
   - Suivez les instructions pour configurer vos credentials

4. **Générez les PDFs et envoyez les emails:**
   - Cliquez sur "Générer et Envoyer"
   - L'application va automatiquement:
     - Détecter le fichier de jurys
     - Convertir en interne les 135 candidats
     - Générer les PDFs avec les bonnes informations
     - Envoyer les emails au format DELF/DALF

### 2. Vérification du processus

L'application affichera dans le journal d'activité:
```
📋 Fichier de jurys détecté - Conversion automatique activée
🔄 Détection d'un fichier de jurys - Conversion automatique en cours...
Traitement du niveau A1...
Traitement du niveau A2...
...
✅ Conversion réussie: 135 candidats extraits du fichier de jurys
```

## 📊 Résultats attendus

### Extraction automatique:
- **A1**: 7 candidats
- **A2**: 18 candidats  
- **B1**: 26 candidats
- **B2**: 49 candidats
- **C1**: 28 candidats
- **C2**: 7 candidats
- **Total**: 135 candidats

### Format d'email généré:
```
Sujet: Convocation d'examen - DELF A1 - Erik ANDERSSON

Bonjour Erik ANDERSSON,

Vous êtes convoqué pour passer les épreuves du DELF A1

ÉPREUVES COLLECTIVES
Date : jeudi 14 août 2025
Heure : 09:20

ÉPREUVE INDIVIDUELLE  
Date : jeudi 14 août 2025
Heure : 07:00

[IMPORTANT] (en rouge)
- Présentez-vous 30 minutes avant le début de l'épreuve
- Munissez-vous d'une pièce d'identité officielle
- ...
```

## 🔧 Récupération des dates et heures

Le système récupère automatiquement:

### Pour les épreuves collectives:
- **Date**: Extraite de la ligne "Date épreuve collective" (ex: 14/08/2025)
- **Heure**: Extraite de "Début de l'épreuve collective" (ex: 09:20)

### Pour les épreuves individuelles:
- **Date**: Date du jury individuel ou date collective si non spécifiée
- **Heure**: Heure de "Pass." (passation) pour chaque candidat

### Conversion automatique:
- Dates converties au format français: "jeudi 14 août 2025"
- Heures conservées au format original: "09:20"
- Type d'examen détecté automatiquement: DELF (A1,A2,B1,B2) ou DALF (C1,C2)

## ⚠️ Points importants

### Fichiers supportés:
- ✅ Fichiers de jurys avec feuilles "Niveau A1", "Niveau A2", etc.
- ✅ Feuille "ADMIN" pour la configuration
- ✅ Fichiers candidats classiques (détection automatique)

### PDFs requis:
- Les PDFs doivent être générés avant l'envoi des emails
- Nommage attendu: `convocation_NOM_Prenom_NumeroCandidat.pdf`
- Répertoire: `output/`

### Emails:
- Format DELF/DALF automatique selon le niveau
- Pièces jointes PDF automatiquement attachées
- Envoi via Mailjet sécurisé (HTTPS)

## 🎯 Avantages du système intégré

1. **Zéro manipulation manuelle** - Chargez directement vos fichiers de jurys
2. **Détection intelligente** - Reconnaît automatiquement le type de fichier
3. **Conversion transparente** - Traite tous les niveaux en une fois
4. **Format professionnel** - Emails conformes aux standards DELF/DALF
5. **Dates précises** - Récupère les bonnes heures pour chaque type d'épreuve
6. **Sécurité** - Envoi via Mailjet avec chiffrement HTTPS

## 🚀 Prêt à utiliser!

Le système est maintenant **entièrement opérationnel** et **prêt pour la production**. 

Chargez simplement votre fichier `juries_20250825_181821.xlsx` dans l'application principale et laissez la magie opérer! ✨

---

*Système testé et validé le 26/08/2025 - 135 candidats traités avec succès*
