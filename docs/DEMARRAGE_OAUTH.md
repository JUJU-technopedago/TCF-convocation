# 🚀 Démarrage Rapide - Authentification OAuth2

## ✨ Nouvelle Fonctionnalité : Authentification Web Sécurisée

Votre générateur de convocations DELF dispose maintenant d'une authentification OAuth2 moderne qui résout tous les problèmes de connexion Outlook !

## 🎯 Avantages Immédiats

- ✅ **Fini les erreurs 535** : Plus de problèmes d'authentification Outlook
- ✅ **Sécurité maximale** : Authentification via navigateur web officiel Microsoft
- ✅ **Simplicité** : Plus besoin de configurer des mots de passe d'application
- ✅ **Fiabilité** : Utilise les API officielles Microsoft Graph

## 🚀 Comment Utiliser (3 étapes simples)

### 1. Lancer l'application
```bash
python main.py
```

### 2. Cliquer sur "🌐 Authentification OAuth"
Dans l'interface, cliquez sur le nouveau bouton **"🌐 Authentification OAuth"** au lieu de l'ancien "🔐 Connexion Sécurisée".

### 3. Suivre l'authentification web
1. Une fenêtre s'ouvre avec un code (ex: `A1B2C3D4`)
2. Votre navigateur s'ouvre automatiquement sur Microsoft
3. Entrez le code affiché
4. Connectez-vous avec votre compte Microsoft/Outlook
5. Autorisez l'application
6. C'est terminé ! ✅

## 🧪 Test Rapide

Pour tester le système avant utilisation :
```bash
python oauth_device_auth.py
```

## 📋 Utilisation Normale

Une fois authentifié :
1. **Sélectionnez votre fichier Excel** avec les candidats
2. **Générez les PDF** des convocations
3. **Envoyez les emails** - maintenant via OAuth2 sécurisé !

## 🔄 Migration depuis l'ancienne méthode

Si vous utilisiez l'ancienne méthode :
1. **Déconnectez-vous** (bouton "Déconnecter")
2. **Utilisez le nouveau bouton** "🌐 Authentification OAuth"
3. **Supprimez vos app passwords** Microsoft (plus nécessaires)

## 🆘 Résolution de Problèmes

### "Erreur lors de l'initialisation du flux"
- Vérifiez votre connexion internet
- Réessayez dans quelques minutes

### "Le navigateur ne s'ouvre pas"
- Copiez l'URL affichée et ouvrez-la manuellement
- Ou utilisez un autre navigateur

### "Token expiré"
- Cliquez sur "Déconnecter" puis reconnectez-vous
- Les tokens sont automatiquement renouvelés

## 🎉 C'est Tout !

Votre système est maintenant équipé de l'authentification OAuth2 la plus moderne et sécurisée. Profitez de l'envoi d'emails sans problème !

---

**💡 Conseil** : Gardez cette fenêtre ouverte lors de votre première utilisation pour référence rapide.

**🔒 Sécurité** : Vos identifiants ne sont jamais stockés dans l'application - tout passe par Microsoft de manière sécurisée.
