# Solution au problème de génération PDF dans main.py

## Problème détecté

Lors de la génération des PDF via l'interface principale (`main.py`), les utilisateurs rencontraient une erreur:

```
TypeError: unsupported operand type(s) for -: 'str' and 'int'
```

Cette erreur se produisait car le template HTML (`convocation_delf_template_modele.html`) utilisait des valeurs en pourcentage dans les tableaux, ce qui causait des problèmes de types dans xhtml2pdf.

## Solution implémentée

Nous avons implémenté deux correctifs pour résoudre ce problème:

1. **Création d'un module de correction de template** (`fix_template.py`):
   - Ce module crée une version modifiée du template HTML
   - Il remplace les valeurs en pourcentage par des valeurs en pixels
   - Exemple: `width: 50%;` → `width: 300px;`

2. **Modification de la méthode `generate_pdfs` dans `main.py`**:
   - Détection automatique du template problématique
   - Utilisation du template corrigé lorsque le template original est détecté
   - Gestion des exceptions pour assurer la rétrocompatibilité

## Comment utiliser la solution

### Option 1: Utiliser le nouveau fichier batch

Pour lancer l'application avec la correction intégrée:
1. Double-cliquez sur `lancer_application_fixee.bat`
2. L'application se lancera normalement et utilisera automatiquement le template corrigé

### Option 2: Utiliser l'application normalement

La correction a été intégrée dans le flux de travail normal de l'application:
1. Lancez l'application avec `lancer_application.bat` ou `python main.py`
2. Quand vous générerez des PDFs, l'application détectera le template problématique
3. Le système utilisera automatiquement la version corrigée du template

## Points techniques

1. Les conversions de type sont maintenant appliquées à toutes les valeurs d'heure
2. Les pourcentages dans les tableaux ont été remplacés par des valeurs en pixels:
   - `width: 50%;` → `width: 300px;`
   - `width: 40%;` → `width: 250px;`
   - `width: 60%;` → `width: 350px;`
   - `width: 100%;` → `width: 600px;`
   - `height: 100%;` → `height: 100px;`

3. Le système crée le template corrigé si nécessaire, sans modifier le template original

## Fichiers créés ou modifiés

- `fix_template.py` (nouveau): Module qui corrige le template HTML
- `main.py` (modifié): Utilise maintenant le template corrigé
- `lancer_application_fixee.bat` (nouveau): Fichier batch pour lancer l'application

## Recommandations

Pour éviter ce problème à l'avenir:
1. Éviter d'utiliser des pourcentages dans les templates HTML destinés à xhtml2pdf
2. Utiliser des valeurs en pixels pour les dimensions des tableaux
3. S'assurer que toutes les valeurs utilisées dans les calculs sont du même type