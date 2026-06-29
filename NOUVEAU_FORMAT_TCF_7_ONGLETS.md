# 📋 NOUVEAU FORMAT EXCEL TCF - 7 ONGLETS

## 🎯 Vue d'ensemble

Le fichier "JURYS FINAL TCF" prend désormais en charge **7 onglets** au lieu de 5.

### ✅ Structure des onglets

1. **TCF CANADA** (inchangé)
2. **TCF TP COMPLET** (inchangé)
3. **TCF TP OBLIGATOIRE** (inchangé)
4. **TCF TP EE** 🆕 (nouveau)
5. **TCF TP EO** 🆕 (nouveau)
6. **TCF IRN** (inchangé)
7. **ADMIN** (inchangé)

---

## 🆕 Nouveaux onglets : TCF TP EE et TCF TP EO

### 📝 TCF TP EE (Expression Écrite)

**Description :**
- Épreuve facultative du TCF TP
- Teste les compétences en expression écrite
- Peut être passée seule ou combinée avec d'autres épreuves TCF TP

**Caractéristiques :**
- ✅ Épreuve collective uniquement
- ⏱️ Durée : 1h00
- 📍 Salle collective requise
- ❌ Pas d'épreuve individuelle

**Structure de l'onglet :**
```
Jury 1 | 13/10/2025 | Début de l'épreuve collective : | 10:00 | Fin de l'épreuve collective : | 11:00
Pass.  | NOM et Prénom              | Date de naissance | Email
10h00  | DUPONT Jean                | 15/03/1990        | jean.dupont@email.com
10h15  | MARTIN Marie               | 22/07/1985        | marie.martin@email.com
```

---

### 🗣️ TCF TP EO (Expression Orale)

**Description :**
- Épreuve facultative du TCF TP
- Teste les compétences en expression orale
- Peut être passée seule ou combinée avec d'autres épreuves TCF TP

**Caractéristiques :**
- ❌ Pas d'épreuve collective
- ✅ Épreuve individuelle uniquement
- ⏱️ Durée : 12 minutes par candidat
- 📍 Salle individuelle requise

**Structure de l'onglet :**
```
Jury 1 | 14/10/2025 | Heure de passage
Pass.  | NOM et Prénom              | Date de naissance | Email
14h00  | DURAND Sophie              | 10/12/1992        | sophie.durand@email.com
14h15  | BERNARD Pierre             | 05/05/1988        | pierre.bernard@email.com
```

---

## ⚙️ Configuration de l'onglet ADMIN

L'onglet ADMIN doit être mis à jour pour inclure les durées des nouvelles épreuves.

### 📅 Durées collectives (lignes 2-5, colonnes A-B)

```
TCF CANADA          | 02:35:00
TCF TP COMPLET      | 02:35:00
TCF TP OBLIGATOIRE  | 01:35:00
TCF TP EE           | 01:00:00  🆕
TCF IRN             | 01:35:00
```

### ⏱️ Durées individuelles (lignes 11-15, colonnes A-B)

```
TCF CANADA          | 12
TCF TP COMPLET      | 12
TCF TP OBLIGATOIRE  | 
TCF TP EO           | 12  🆕
TCF IRN             | 10
```

---

## 🎨 Logos TCF

### Logos par défaut

Les nouvelles épreuves utilisent le logo TCF TP par défaut :

- **TCF TP EE** → `assets/logoTCF_TP.png`
- **TCF TP EO** → `assets/logoTCF_TP.png`

### Logos personnalisés (optionnel)

Vous pouvez créer des logos spécifiques :

- `assets/logoTCF_TP_EE.png` (Expression Écrite)
- `assets/logoTCF_TP_EO.png` (Expression Orale)

Ces logos seront automatiquement utilisés s'ils existent dans le dossier `assets/`.

---

## 📊 Combinaisons possibles

Les épreuves facultatives peuvent être combinées de différentes manières :

### ✅ Combinaisons valides

1. **TCF TP OBLIGATOIRE** seul
2. **TCF TP EE** seul
3. **TCF TP EO** seul
4. **TCF TP OBLIGATOIRE + EE**
5. **TCF TP OBLIGATOIRE + EO**
6. **TCF TP OBLIGATOIRE + EE + EO** (= TCF TP COMPLET)
7. **TCF TP EE + EO**

### 📝 Notes importantes

- Un candidat peut passer plusieurs épreuves TCF TP le même jour
- Chaque épreuve génère une convocation séparée
- Les horaires doivent être coordonnés entre les épreuves

---

## 🚀 Utilisation dans l'application

### Génération des convocations

1. **Ouvrir l'application**
   ```bash
   python main.py
   ```

2. **Sélectionner le fichier Excel**
   - Le fichier doit contenir les 7 onglets
   - Format : `JURYS FINAL TCF.xlsx`

3. **Vérifier la configuration**
   - Type d'examen : TCF
   - Salles configurées (collective et individuelle)
   - Logos disponibles

4. **Générer les PDFs**
   - Cliquez sur "Générer PDF"
   - Les candidats des 7 onglets seront traités
   - Les convocations TCF TP EE et EO seront générées automatiquement

### Envoi des emails

Les emails pour TCF TP EE et TCF TP EO sont envoyés de la même manière que les autres épreuves TCF.

---

## 🔍 Vérification

### Test de configuration

Pour vérifier que le système reconnaît les nouveaux onglets :

```bash
python test_new_tcf_types.py
```

### Résultat attendu

```
🎉 TOUS LES TESTS RÉUSSIS!
   ✅ Les nouveaux types TCF TP EE et EO sont configurés
   ✅ Les logos sont mappés correctement
   ✅ Le système est prêt à traiter les 7 onglets
```

---

## ❓ FAQ

### Q: Puis-je utiliser l'ancien format à 5 onglets ?
**R:** Oui, l'application reste compatible avec les anciens fichiers. Les onglets TCF TP EE et EO sont optionnels.

### Q: Comment savoir si mes onglets sont bien formatés ?
**R:** L'application affiche des messages de log détaillés lors du chargement. Vérifiez le journal d'activité.

### Q: Les durées dans l'onglet ADMIN sont-elles obligatoires ?
**R:** Oui, l'onglet ADMIN doit contenir les durées pour tous les types d'épreuves, y compris TCF TP EE et EO.

### Q: Puis-je utiliser les mêmes salles pour toutes les épreuves ?
**R:** Oui, mais assurez-vous que les horaires ne se chevauchent pas.

### Q: Comment créer des logos personnalisés ?
**R:** Placez vos logos PNG dans le dossier `assets/` avec les noms :
- `logoTCF_TP_EE.png`
- `logoTCF_TP_EO.png`

---

## 📞 Support

Pour toute question ou problème :

1. Vérifiez d'abord le journal d'activité de l'application
2. Exécutez le script de test : `python test_new_tcf_types.py`
3. Vérifiez que votre fichier Excel contient bien les 7 onglets
4. Assurez-vous que l'onglet ADMIN est correctement configuré

---

## ✨ Résumé des changements

| Élément | Avant | Après |
|---------|-------|-------|
| Nombre d'onglets | 5 | **7** 🆕 |
| Types TCF TP | 2 (COMPLET, OBLIGATOIRE) | **4** (COMPLET, OBLIGATOIRE, EE, EO) 🆕 |
| Épreuves facultatives | 0 | **2** (EE, EO) 🆕 |
| Logos TCF TP | 1 | **3** (TP, TP EE, TP EO) 🆕 |
| Configuration ADMIN | 5 types | **7 types** 🆕 |

---

**Date de mise à jour :** 29 juin 2026  
**Version :** 2.0.1 - Correctif du format de date de naissance au chargement