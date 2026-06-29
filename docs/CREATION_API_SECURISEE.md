# 🔐 Création d'une API Sécurisée - Application Azure AD

## 🎯 Solution Définitive

Pour résoudre définitivement les problèmes d'authentification OAuth, nous allons créer **votre propre application Azure AD** avec une API sécurisée personnalisée.

## 📋 Étapes de Création

### 1. Créer une Application Azure AD

1. **Connectez-vous au portail Azure** : https://portal.azure.com
2. **Allez dans "Azure Active Directory"**
3. **Cliquez sur "App registrations"**
4. **Cliquez sur "New registration"**

### 2. Configuration de l'Application

**Nom de l'application** : `Générateur Convocations DELF`

**Types de comptes pris en charge** :
- ✅ Comptes dans cet annuaire organisationnel uniquement
- OU ✅ Comptes dans n'importe quel annuaire organisationnel (Azure AD multitenant)

**URI de redirection** :
- Type : `Public client/native (mobile & desktop)`
- URI : `http://localhost:8080/auth/callback`

### 3. Permissions API

Après création, allez dans **"API permissions"** :

1. **Cliquez sur "Add a permission"**
2. **Sélectionnez "Microsoft Graph"**
3. **Choisissez "Delegated permissions"**
4. **Ajoutez ces permissions** :
   - `Mail.Send` - Envoyer des emails
   - `User.Read` - Lire le profil utilisateur
5. **Cliquez sur "Grant admin consent"** (si vous êtes admin)

### 4. Configuration de l'Authentification

Dans **"Authentication"** :
- ✅ Cochez "Allow public client flows"
- ✅ Ajoutez `http://localhost:8080/auth/callback` comme URI de redirection

### 5. Récupérer les Informations

Dans **"Overview"**, notez :
- **Application (client) ID** : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **Directory (tenant) ID** : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

## 🔧 Configuration du Code

Une fois votre application créée, je vais créer un module personnalisé qui utilise VOS identifiants.
