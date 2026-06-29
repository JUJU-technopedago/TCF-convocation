# Solution pour le problème de génération de PDF

## Résumé du problème

Lors de la génération des PDF de convocation, certains candidats provoquaient une erreur:
```
TypeError: unsupported operand type(s) for -: 'str' and 'int'
```

Cette erreur survenait dans le module xhtml2pdf lors du traitement de tables HTML contenant des pourcentages pour les largeurs.

## Cause racine

Le problème vient de deux facteurs combinés:

1. Dans certains enregistrements, les valeurs de temps (heure_debut, heure_fin) étaient stockées comme des chaînes de caractères et non comme des nombres.
2. Le template HTML utilisait des pourcentages pour les largeurs de colonnes, ce qui provoquait une opération arithmétique dans xhtml2pdf (via reportlab) qui tentait de soustraire un entier d'une chaîne.

## Solution

Nous avons implémenté deux correctifs complémentaires:

### 1. Modification du code

Dans `pdf_generator.py` et `jury_excel_processor.py`, nous avons ajouté une méthode `_ensure_string` qui garantit qu'une valeur est bien convertie en chaîne de caractères:

```python
def _ensure_string(self, value):
    """
    S'assure qu'une valeur est bien une chaîne de caractères.
    Convertit les nombres en chaînes si nécessaire.
    """
    if value is None:
        return ""
    return str(value)
```

Et nous l'utilisons pour garantir que les temps sont bien traités comme des chaînes.

### 2. Modification du template HTML

Nous avons créé un script `generate_with_fixed_template.py` qui:
1. Crée une version modifiée du template HTML en remplaçant les valeurs en pourcentage par des valeurs en pixels
2. Utilise ce template modifié pour générer les PDF

Exemple de modifications dans le template:
- `width: 50%;` → `width: 300px;`
- `width: 40%;` → `width: 250px;`
- `width: 60%;` → `width: 350px;`
- `width: 100%;` → `width: 600px;`
- `height: 100%;` → `height: 100px;`

## Comment utiliser la solution

### Option 1: Utiliser le script avec le template fixé

1. Exécutez le fichier batch `generer_avec_template_fixe.bat` pour utiliser le template fixé avec votre fichier Excel
2. Ou exécutez la commande: `python generate_with_fixed_template.py chemin_du_fichier_excel`

### Option 2: Tester avec les candidats problématiques

1. Exécutez le fichier batch `generer_problematiques.bat` pour générer les PDF pour tous les candidats problématiques mentionnés dans les logs
2. Ou exécutez la commande: `python generate_with_fixed_template.py problematic`

Les PDF générés se trouveront dans le dossier `output_fixed_template` ou `output_problematic`.

## Recommandations à long terme

1. Vérifier et standardiser les types de données dans les fichiers Excel (convertir les temps en format chaîne)
2. Éviter d'utiliser des pourcentages dans les templates HTML destinés à xhtml2pdf
3. Mettre à jour tous les templates existants pour utiliser des dimensions en pixels plutôt qu'en pourcentages

## Notes techniques

Le problème spécifique se produisait dans le module reportlab, qui est utilisé par xhtml2pdf:
- Lors du calcul de la hauteur des cellules dans une table
- Lorsqu'une opération arithmétique tentait de soustraire un entier (c) d'une chaîne (H[i])
- L'erreur exacte était: `TypeError: unsupported operand type(s) for -: 'str' and 'int'`