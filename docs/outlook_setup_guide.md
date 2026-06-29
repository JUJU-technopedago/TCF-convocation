# 🔐 Guide de Configuration Outlook pour l'Application

## ⚠️ Problème d'Authentification Outlook

L'erreur que vous rencontrez indique qu'Outlook nécessite une **authentification moderne** ou un **mot de passe d'application**.

## 📋 Solutions Recommandées

### Option 1 : Mot de Passe d'Application (Recommandé)

#### Étapes pour créer un mot de passe d'application :

1. **Connectez-vous à votre compte Microsoft** :
   - Allez sur https://account.microsoft.com
   - Connectez-vous avec votre compte Outlook

2. **Activez l'authentification à deux facteurs** (si pas déjà fait) :
   - Sécurité → Authentification à deux facteurs
   - Suivez les instructions pour l'activer

3. **Créez un mot de passe d'application** :
   - Sécurité → Options de sécurité avancées
   - Mots de passe d'application → Créer un nouveau mot de passe d'application
   - Nommez-le "Convocation Generator" ou similaire
   - **Copiez le mot de passe généré** (16 caractères)

4. **Utilisez ce mot de passe dans l'application** :
   - Email : votre adresse Outlook normale
   - Mot de passe : le mot de passe d'application (pas votre mot de passe habituel)

### Option 2 : Configuration Outlook Entreprise

Si vous utilisez un compte Outlook professionnel :

1. **Contactez votre administrateur IT** pour :
   - Activer l'authentification SMTP
   - Configurer les paramètres de sécurité appropriés

2. **Paramètres alternatifs** :
   - Serveur SMTP : smtp.office365.com
   - Port : 587
   - Sécurité : STARTTLS

### Option 3 : Utiliser Gmail ou ProtonMail

Si Outlook pose des problèmes, vous pouvez utiliser :

#### Gmail :
1. Activez l'authentification à 2 facteurs
2. Créez un mot de passe d'application Gmail
3. Utilisez ce mot de passe dans l'application

#### ProtonMail :
1. Activez ProtonMail Bridge (application desktop)
2. Utilisez les paramètres fournis par Bridge

## 🔧 Configuration dans l'Application

### Avec Mot de Passe d'Application :
1. Cliquez sur "🔐 Connexion Sécurisée"
2. Sélectionnez "Microsoft Outlook"
3. Email : `votre.email@outlook.com`
4. Mot de passe : `mot-de-passe-application-16-caracteres`
5. Cochez "Sauvegarder les identifiants"
6. Cliquez "Tester la connexion"

## 📞 Support

Si vous continuez à avoir des problèmes :

1. **Vérifiez les paramètres de sécurité** de votre compte Microsoft
2. **Assurez-vous que SMTP est activé** dans les paramètres Outlook
3. **Essayez avec un autre fournisseur** (Gmail/ProtonMail) temporairement

## 🔍 Diagnostic

Pour diagnostiquer le problème :
- L'erreur "Authentication unsuccessful" indique un problème d'identifiants
- "Contact your administrator" suggère des restrictions de sécurité
- Utilisez un mot de passe d'application plutôt que votre mot de passe principal

---

**Note** : Microsoft a renforcé la sécurité et nécessite maintenant des mots de passe d'application pour les applications tierces.
