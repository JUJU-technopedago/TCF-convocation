# Guide d'utilisation - Fichiers de Jurys DELF/DALF

## Vue d'ensemble

Le système d'emails est maintenant compatible avec les fichiers de jurys structurés par niveaux DELF/DALF. Ce guide explique comment convertir et utiliser ces fichiers.

## Structure des fichiers de jurys

Les fichiers de jurys sont organisés avec:
- **Feuilles par niveau**: `Niveau A1`, `Niveau A2`, `Niveau B1`, `Niveau B2`, `Niveau C1`, `Niveau C2`
- **Feuille ADMIN**: Configuration des durées d'épreuves
- **Candidats groupés par jurys** avec horaires de préparation et passation

### Exemple de structure:
```
Niveau A1:
  - Date épreuve collective: 14/08/2025
  - Début épreuve collective: 09:20
  - Jury 1, Jury 2, etc.
  - Candidats avec: Prép, Pass, Numéro, NOM Prénom, Email, etc.
```

## Étapes d'utilisation

### 1. Conversion du fichier de jurys

Utilisez le processeur pour convertir votre fichier de jurys:

```bash
python jury_file_processor.py
```

**Ce script va:**
- Lire le fichier `juries_20250825_181821.xlsx`
- Extraire tous les candidats de tous les niveaux
- Créer un fichier `candidats_from_jury.xlsx` compatible avec le système d'emails

### 2. Vérification de la conversion

Le script affiche un résumé:
```
✅ 135 candidats extraits du fichier de jurys
📊 Résumé:
   - Total candidats: 135
   - A1: 7 candidats
   - A2: 18 candidats
   - B1: 26 candidats
   - B2: 49 candidats
   - C1: 28 candidats
   - C2: 7 candidats
```

### 3. Test du format d'email

Testez le nouveau format avec:

```bash
python test_jury_email_format.py
```

**Vérifications automatiques:**
- ✅ Sujet décodé (caractères spéciaux)
- ✅ Nom en majuscules
- ✅ Type DELF/DALF correct
- ✅ Date française avec jour de la semaine
- ✅ "30 minutes avant" présent
- ✅ Couleur rouge (#da002e) pour [IMPORTANT]
- ✅ Sections séparées (ÉPREUVES COLLECTIVES / ÉPREUVE INDIVIDUELLE)

### 4. Envoi des emails

Utilisez le fichier converti avec le système d'emails:

```bash
python send_emails_final.py
```

Ou intégrez-le dans l'application principale en modifiant le chemin du fichier Excel.

## Format d'email DELF/DALF

Le nouveau format inclut:

### Sujet
```
Convocation d'examen - DELF A1 - Erik ANDERSSON
```

### Contenu
```html
<p>Bonjour <strong>Erik ANDERSSON</strong>,</p>
<p>Vous êtes convoqué pour passer les épreuves du <strong>DELF A1</strong></p>

<h3><u><strong>ÉPREUVES COLLECTIVES</strong></u></h3>
<p><strong>Date:</strong> jeudi 14 août 2025</p>
<p><strong>Heure:</strong> 09:20</p>

<h3><u><strong>ÉPREUVE INDIVIDUELLE</strong></u></h3>
<p><strong>Date:</strong> jeudi 14 août 2025</p>
<p><strong>Heure:</strong> 07:00</p>

<h4 style="color: #da002e; font-weight: bold;">[IMPORTANT]</h4>
<p style="color: #da002e;">
<strong>Présentez-vous 30 minutes avant l'heure de votre convocation.</strong>
</p>
```

## Personnalisation

### Modifier le fichier source

Pour utiliser un autre fichier de jurys, modifiez dans `jury_file_processor.py`:

```python
processor = JuryFileProcessor("votre_fichier_jurys.xlsx")
```

### Modifier le fichier de sortie

Pour changer le nom du fichier converti:

```python
output_file = "votre_nom_candidats.xlsx"
processor.save_to_mailjet_format(output_file)
```

## Dépannage

### Erreur "Fichier non trouvé"
- Vérifiez que le fichier de jurys existe
- Vérifiez le nom du fichier dans le script

### Candidats manquants
- Vérifiez la structure des feuilles Excel
- Les numéros de candidats doivent être numériques
- Les emails doivent être présents

### Format d'email incorrect
- Vérifiez que `mailjet_bridge.py` contient les dernières modifications
- Testez avec `test_jury_email_format.py`

## Avantages du système

1. **Compatibilité totale** avec les fichiers de jurys existants
2. **Conversion automatique** de la structure complexe
3. **Format d'email conforme** aux spécifications DELF/DALF
4. **Gestion des niveaux** A1, A2, B1, B2, C1, C2
5. **Extraction des horaires** de jurys individuels
6. **Préservation des informations** (besoins spéciaux, etc.)

## Fichiers créés

- `jury_file_processor.py` - Convertisseur principal
- `candidats_from_jury.xlsx` - Fichier converti pour emails
- `test_jury_email_format.py` - Tests du format d'email
- `GUIDE_FICHIERS_JURYS.md` - Ce guide

Le système est maintenant entièrement compatible avec vos fichiers de jurys DELF/DALF!
