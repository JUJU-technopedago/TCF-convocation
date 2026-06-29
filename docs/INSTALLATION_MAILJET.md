# 🚀 Installation Rapide - Bridge Mailjet

## ⚡ Installation Express

### Option 1 : Script automatique (Recommandé)
Double-cliquez sur le fichier `install_mailjet.bat` pour installer automatiquement toutes les dépendances nécessaires.

### Option 2 : Installation manuelle
Ouvrez un terminal et exécutez :
```bash
pip install mailjet-rest==1.3.4
pip install requests==2.31.0 
pip install cryptography==41.0.7
```

### Option 3 : Via requirements.txt
```bash
pip install -r requirements.txt
```

---

## 🎯 Après Installation

1. **Lancez l'application** : `python main.py` ou double-cliquez sur `lancer_application.bat`
2. **Cliquez sur le bouton "📧 MAILJET"**
3. **Configurez vos clés API Mailjet** (première fois seulement)
4. **Connectez-vous** avec votre mot de passe
5. **Envoyez des emails sécurisés via HTTPS !**

---

## 📋 Prérequis Mailjet

Pour utiliser Mailjet, vous devez avoir :

### 1. Compte Mailjet
- Rendez-vous sur [mailjet.com](https://www.mailjet.com)
- Créez un compte gratuit ou payant

### 2. Clés API
- Connectez-vous à Mailjet
- Allez dans **Account Settings** → **Master API Key & Sub API key management**
- Notez votre **API Key** et **Secret Key**

### 3. Email Expéditeur
- Utilisez une adresse email que vous contrôlez
- De préférence du même domaine que votre compte Mailjet

---

## ✅ Test d'Installation

Après installation, testez le système :
```bash
python test_mailjet_bridge.py
```

---

## 🆘 Dépannage

### "Module Mailjet non disponible"
- Exécutez `install_mailjet.bat` ou installez manuellement
- Vérifiez que Python trouve les modules : `pip list | grep mailjet`

### "Credentials Mailjet invalides"
- Vérifiez vos clés API dans l'interface Mailjet
- Assurez-vous que le compte est actif

### "Mot de passe incorrect"
- Reconfigurez vos credentials si nécessaire
- Utilisez un nouveau mot de passe de 6+ caractères

---

## 🔒 Sécurité

- ✅ Communications HTTPS chiffrées
- ✅ Credentials stockés de manière sécurisée 
- ✅ Vérification SSL/TLS automatique
- ✅ Chiffrement AES-256 des clés API

---

**🎉 Profitez de Mailjet avec une sécurisation HTTPS complète !**

Pour plus de détails, consultez `GUIDE_MAILJET.md`.
