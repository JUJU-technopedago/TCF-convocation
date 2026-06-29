# 📋 ADAPTATION DU TEMPLATE TCF TP - RÉSUMÉ DES MODIFICATIONS

**Date:** 17 novembre 2025  
**Fichier modifié:** `templates/convocation_tcf_template_modele.html`

---

## 🎯 Objectif

Adapter l'affichage des convocations selon le type de TCF TP :

1. **TCF TP OBLIGATOIRE** : Remplacer "Épreuves collectives" par "**Épreuves obligatoires**"
2. **TCF TP EE** (Expression Écrite) : Remplacer "Épreuves collectives" par "**Épreuves obligatoires**"
3. **TCF TP EO** (Expression Orale) : **Supprimer complètement** le bloc "Épreuves collectives"

---

## ✅ Modifications effectuées

### 1. Section des épreuves - Premier cas (épreuves collectives en premier)

**Avant :**
```html
<div class="exam-section">
    <div class="exam-section-title"><u>Épreuves collectives</u> :</div>
    ...
</div>
```

**Après :**
```html
{% if tcf_type != 'TCF TP EO' %}
<div class="exam-section">
    {% if tcf_type in ['TCF TP OBLIGATOIRE', 'TCF TP EE'] %}
    <div class="exam-section-title"><u>Épreuves obligatoires</u> :</div>
    {% else %}
    <div class="exam-section-title"><u>Épreuves collectives</u> :</div>
    {% endif %}
    ...
</div>
{% endif %}
```

### 2. Section des épreuves - Deuxième cas (épreuves collectives en second)

Même logique appliquée pour la deuxième occurrence (quand les épreuves collectives sont après l'épreuve individuelle).

### 3. Adaptation du texte des consignes

**Avant :**
```html
Afin d'assurer la bonne tenue des épreuves collectives et individuelles, vous êtes prié.e de
```

**Après :**
```html
{% if tcf_type == 'TCF TP EO' %}
Afin d'assurer la bonne tenue de l'épreuve individuelle, vous êtes prié.e de
{% elif tcf_type in ['TCF TP OBLIGATOIRE', 'TCF TP EE'] %}
Afin d'assurer la bonne tenue des épreuves obligatoires et individuelles, vous êtes prié.e de
{% else %}
Afin d'assurer la bonne tenue des épreuves collectives et individuelles, vous êtes prié.e de
{% endif %}
```

### 4. Adaptation de la note tiers-temps

**Avant :**
```html
En tant que bénéficiaire d'un aménagement spécifique, un tiers-temps vous est alloué lors des épreuves collectives.
```

**Après :**
```html
{% if tcf_type in ['TCF TP OBLIGATOIRE', 'TCF TP EE'] %}
En tant que bénéficiaire d'un aménagement spécifique, un tiers-temps vous est alloué lors des épreuves obligatoires.
{% else %}
En tant que bénéficiaire d'un aménagement spécifique, un tiers-temps vous est alloué lors des épreuves collectives.
{% endif %}
```

---

## 🧪 Tests de validation

Le script `test_template_tcf_tp_adaptation.py` valide que :

✅ **TCF TP OBLIGATOIRE :**
- Affiche "Épreuves obligatoires" au lieu de "Épreuves collectives"
- Affiche aussi l'épreuve individuelle
- Texte des consignes adapté : "épreuves obligatoires et individuelles"
- Note tiers-temps adaptée : "lors des épreuves obligatoires"

✅ **TCF TP EE :**
- Affiche "Épreuves obligatoires" au lieu de "Épreuves collectives"
- Affiche aussi l'épreuve individuelle
- Texte des consignes adapté : "épreuves obligatoires et individuelles"
- Note tiers-temps adaptée : "lors des épreuves obligatoires"

✅ **TCF TP EO :**
- **Aucun** bloc "Épreuves collectives" ou "Épreuves obligatoires"
- Affiche **uniquement** l'épreuve individuelle
- Texte des consignes adapté : "de l'épreuve individuelle" (singulier)

✅ **TCF CANADA / TCF TP COMPLET / TCF IRN :**
- Comportement **standard conservé**
- Affiche "Épreuves collectives" normalement
- Texte des consignes standard : "épreuves collectives et individuelles"

---

## 📊 Résultats des tests

```
🧪 TEST DES ADAPTATIONS DU TEMPLATE TCF TP
======================================================================

✅ TCF TP OBLIGATOIRE: "Épreuves collectives" → "Épreuves obligatoires"
✅ TCF TP EE: "Épreuves collectives" → "Épreuves obligatoires"
✅ TCF TP EO: Bloc "Épreuves collectives" complètement supprimé
✅ TCF CANADA/COMPLET/IRN: Comportement standard conservé
✅ Consignes adaptées selon le type d'épreuve
✅ Note tiers-temps adaptée selon le type d'épreuve
```

---

## 🔑 Variables Jinja2 utilisées

Le template utilise la variable `tcf_type` qui peut contenir :
- `"TCF CANADA"`
- `"TCF TP COMPLET"`
- `"TCF TP OBLIGATOIRE"` → Affichage spécial
- `"TCF TP EE"` → Affichage spécial
- `"TCF TP EO"` → Affichage spécial (sans bloc collectif)
- `"TCF IRN"`

Cette variable est automatiquement fournie par le système de génération de PDF depuis les données Excel.

---

## 🚀 Utilisation

Les modifications sont **automatiques** et **transparentes**. Le système détecte le type de TCF depuis l'Excel et adapte automatiquement le rendu du PDF.

**Aucune action supplémentaire requise** lors de la génération des convocations.

---

## 📝 Notes techniques

- Les modifications utilisent les **conditions Jinja2** (`{% if %}`, `{% elif %}`, `{% else %}`)
- Compatibilité **100% garantie** avec les types TCF existants
- Pas d'impact sur les autres types de convocations (DELF/DALF)
- Le système reste **rétrocompatible** avec les anciennes structures Excel

---

**Statut :** ✅ **Implémenté et testé avec succès**
