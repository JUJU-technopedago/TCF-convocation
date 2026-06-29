# Guide DELF/DALF - Système de Convocations

## Vue d'ensemble

Le système de génération de convocations supporte maintenant automatiquement les examens DELF et DALF selon le niveau du candidat :

- **DELF** : Niveaux A1, A2, B1, B2
- **DALF** : Niveaux C1, C2

## Fonctionnalités

### 1. Détection automatique du type d'examen

Le système analyse automatiquement la colonne `niveau` dans votre fichier Excel et détermine le type d'examen :

```python
# Logique de détermination
if niveau in ['C1', 'C2']:
    exam_type = 'DALF'
else:
    exam_type = 'DELF'
```

### 2. Templates mis à jour

Tous les templates HTML ont été mis à jour pour afficher dynamiquement le bon type d'examen :

- `templates/convocation_delf_template_modele.html`
- `templates/convocation_delf_template.html`
- `templates/convocation_delf_template_simple.html`
- `templates/convocation_delf_template_word_style.html`

**Avant :**
```html
Examen DELF, Niveau {{ niveau }} du CECRL
```

**Après :**
```html
Examen {{ exam_type }}, Niveau {{ niveau }} du CECRL
```

### 3. Emails personnalisés

Les emails envoyés aux candidats utilisent également le bon type d'examen :

**Sujet :** `Convocation {exam_type} - {prenom} {nom}`
**Corps :** `Convocation à l'examen {exam_type}`

## Structure des données Excel

Votre fichier Excel doit contenir au minimum une colonne `niveau` avec les valeurs :

| Niveau | Type d'examen |
|--------|---------------|
| A1     | DELF          |
| A2     | DELF          |
| B1     | DELF          |
| B2     | DELF          |
| C1     | DALF          |
| C2     | DALF          |

## Exemple de fichier Excel

```
nom     | prenom | niveau | numero_candidat | email
--------|--------|--------|-----------------|------------------
MARTIN  | Sophie | A1     | 032002032001    | sophie@example.com
DUBOIS  | Pierre | B2     | 032002032002    | pierre@example.com
SCHMIDT | Anna   | C1     | 032002032003    | anna@example.com
TANAKA  | Hiroshi| C2     | 032002032004    | hiroshi@example.com
```

## Test du système

Un script de test `test_delf_dalf_logic.py` est disponible pour vérifier le bon fonctionnement :

```bash
python test_delf_dalf_logic.py
```

Ce script :
1. Crée des données de test avec tous les niveaux
2. Vérifie la logique de détermination DELF/DALF
3. Génère des PDF de test pour validation visuelle

## Résultats attendus

### PDF générés
- **A1, A2, B1, B2** : Affichent "Examen DELF, Niveau XX du CECRL"
- **C1, C2** : Affichent "Examen DALF, Niveau XX du CECRL"

### Emails envoyés
- **A1, A2, B1, B2** : Sujet "Convocation DELF - Prénom Nom"
- **C1, C2** : Sujet "Convocation DALF - Prénom Nom"

## Compatibilité

Cette mise à jour est **rétrocompatible** :
- Les anciens fichiers Excel continuent de fonctionner
- Si la colonne `niveau` est absente, le système utilise "DELF" par défaut
- Tous les templates existants fonctionnent avec la nouvelle logique

## Fichiers modifiés

1. **pdf_generator.py** : Ajout de la logique de détermination du type d'examen
2. **main.py** : Mise à jour des templates d'email
3. **Templates HTML** : Utilisation de la variable `exam_type`
4. **test_delf_dalf_logic.py** : Script de test complet

## Utilisation

1. **Préparez votre fichier Excel** avec la colonne `niveau`
2. **Lancez l'application** : `python main.py`
3. **Sélectionnez votre fichier Excel** dans l'interface
4. **Générez les PDF** - le système détectera automatiquement DELF/DALF
5. **Envoyez les emails** - les sujets et contenus seront personnalisés

## Vérification

Pour vérifier que tout fonctionne correctement :

1. Exécutez le test : `python test_delf_dalf_logic.py`
2. Vérifiez les PDF générés dans le dossier `output/`
3. Confirmez que les niveaux C1/C2 affichent "DALF" et les autres "DELF"

## Support

En cas de problème :
1. Vérifiez que la colonne `niveau` existe dans votre Excel
2. Assurez-vous que les valeurs sont bien A1, A2, B1, B2, C1, ou C2
3. Exécutez le script de test pour diagnostiquer les problèmes
