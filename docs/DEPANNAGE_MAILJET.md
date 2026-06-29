# 🔧 Dépannage - Erreur "Credentials Mailjet invalides"

## ❌ Erreur rencontrée
```
Erreur lors de la configuration: Credentials Mailjet invalides
```

## 🔍 Causes possibles et solutions

### 1. **Vérification des clés API Mailjet**

#### ✅ **Étapes à suivre :**
1. Connectez-vous à [mailjet.com](https://www.mailjet.com)
2. Allez dans **Account Settings** → **Master API Key & Sub API key management**
3. Vérifiez que vous copiez bien :
   - **API Key** (Public Key) - commence généralement par des chiffres/lettres
   - **Secret Key** (Private Key) - plus longue, mélange de caractères

#### ⚠️ **Points d'attention :**
- Ne copiez pas d'espaces avant/après les clés
- Vérifiez qu'il n'y a pas de caractères cachés
- Les clés sont sensibles à la casse

### 2. **État du compte Mailjet**

#### ✅ **Vérifications :**
- Votre compte Mailjet est-il **activé** ?
- Avez-vous **validé votre email** lors de l'inscription ?
- Votre compte est-il **suspendu** ou en attente ?

### 3. **Permissions de l'API Key**

#### ✅ **Dans Mailjet :**
1. Vérifiez que votre API Key a les permissions :
   - **Send emails** (Envoyer des emails)
   - **Campaign management** (optionnel)
2. Si vous utilisez une Sub API Key, vérifiez ses permissions

### 4. **Test de connexion manuelle**

#### 🧪 **Test rapide :**
Exécutez ce test pour vérifier vos credentials :

```bash
python test_mailjet_bridge.py
```

Ou testez manuellement en Python :
```python
from mailjet_rest import Client

# Remplacez par vos vraies clés
api_key = "VOTRE_API_KEY"
secret_key = "VOTRE_SECRET_KEY"

mailjet = Client(auth=(api_key, secret_key), version='v3.1')
result = mailjet.contact.get()

if result.status_code == 200:
    print("✅ Connexion réussie!")
else:
    print(f"❌ Erreur: {result.status_code}")
    print(result.json())
```

### 5. **Problèmes de réseau/firewall**

#### ✅ **Vérifications :**
- Votre connexion Internet fonctionne-t-elle ?
- Y a-t-il un firewall qui bloque les connexions HTTPS ?
- Pouvez-vous accéder à api.mailjet.com dans votre navigateur ?

---

## 🔄 **Solution étape par étape**

### **Étape 1 : Récupération des bonnes clés**
1. Allez sur https://app.mailjet.com/account/apikeys
2. Copiez **exactement** :
   - **API Key** (clé publique)
   - **Secret Key** (clé privée)

### **Étape 2 : Test avant configuration**
Avant de configurer dans l'application, testez vos clés :
```bash
python -c "from mailjet_rest import Client; print('Test:', Client(auth=('VOTRE_API_KEY', 'VOTRE_SECRET_KEY')).contact.get().status_code)"
```

### **Étape 3 : Reconfiguration propre**
1. Supprimez les anciens fichiers de configuration :
   - `mailjet_config.json` (si il existe)
   - `mailjet.key` (si il existe)
2. Relancez l'application
3. Cliquez sur **📧 MAILJET**
4. Saisissez vos nouvelles clés validées

---

## 🆘 **Si le problème persiste**

### **Option 1 : Recréer les clés API**
1. Dans Mailjet, **supprimez** votre ancienne API Key
2. **Créez** une nouvelle API Key
3. **Testez** la nouvelle clé avant configuration

### **Option 2 : Vérifier le plan Mailjet**
- Les comptes gratuits Mailjet ont-ils des limitations ?
- Votre compte est-il en règle côté paiement ?

### **Option 3 : Support Mailjet**
Si rien ne fonctionne, contactez le support Mailjet :
- https://www.mailjet.com/support/

---

## 📞 **Messages d'erreur courants**

| Erreur | Cause probable | Solution |
|--------|----------------|----------|
| `401 Unauthorized` | Clés API incorrectes | Vérifier les clés |
| `403 Forbidden` | Permissions insuffisantes | Vérifier les permissions de l'API Key |
| `Connection Error` | Problème réseau | Vérifier la connexion Internet |
| `SSL Error` | Certificats SSL | Mettre à jour les certificats |

---

## ✅ **Une fois résolu**

Après avoir configuré avec succès :
1. Vous verrez : **✅ Mailjet: votre-email@domaine.com (HTTPS sécurisé)**
2. Vous pourrez envoyer des emails de manière sécurisée
3. Consultez `GUIDE_MAILJET.md` pour l'utilisation complète

---

**💡 Conseil :** Gardez vos clés API Mailjet dans un endroit sûr pour éviter de refaire cette configuration !
