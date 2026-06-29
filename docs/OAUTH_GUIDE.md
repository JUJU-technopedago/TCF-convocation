# Guide d'Authentification OAuth2 - Générateur de Convocations DELF

## 🌐 Authentification Web Sécurisée

Ce guide explique comment utiliser la nouvelle fonctionnalité d'authentification OAuth2 qui résout les problèmes de connexion Outlook en utilisant une authentification web sécurisée.

## ✨ Avantages de l'OAuth2

- **🔒 Plus sécurisé** : Aucun mot de passe stocké dans l'application
- **🌐 Authentification web** : Interface familière du navigateur
- **🔄 Tokens automatiques** : Gestion automatique des tokens d'accès
- **✅ Compatible Microsoft** : Fonctionne avec tous les comptes Microsoft/Outlook
- **🚫 Pas d'app password** : Plus besoin de configurer des mots de passe d'application

## 🚀 Comment utiliser l'OAuth2

### 1. Lancer l'application
```bash
python main.py
```

### 2. Cliquer sur "🌐 Authentification OAuth"
Dans l'interface principale, cliquez sur le bouton "🌐 Authentification OAuth" au lieu de "🔐 Connexion Sécurisée".

### 3. Authentification web
1. Une fenêtre de dialogue s'ouvre
2. Cliquez sur "🌐 Authentifier via Navigateur"
3. Votre navigateur web s'ouvre automatiquement
4. Connectez-vous avec votre compte Microsoft/Outlook
5. Autorisez l'application à accéder à votre email
6. La fenêtre du navigateur se ferme automatiquement

### 4. Vérification
- Le statut passe à "✅ OAuth: votre-email@outlook.com (microsoft)"
- Vous pouvez tester la connexion avec le bouton "🔍 Tester la Connexion"

### 5. Utilisation normale
Une fois authentifié, utilisez l'application normalement :
- Générer PDF
- Envoyer Emails
- Générer et Envoyer

## 🔧 Fonctionnalités OAuth

### Authentification Automatique
- **Cache des tokens** : Les tokens sont sauvegardés de manière sécurisée
- **Renouvellement automatique** : Les tokens expirés sont renouvelés automatiquement
- **Connexion rapide** : Reconnexion automatique si un token valide existe

### Sécurité Renforcée
- **Stockage sécurisé** : Utilise le trousseau Windows pour stocker les tokens
- **Chiffrement** : Tous les tokens sont chiffrés
- **Pas de mots de passe** : Aucun mot de passe stocké dans l'application

### Interface Moderne
- **Dialogue intuitif** : Interface claire et moderne
- **Feedback visuel** : Indicateurs de progression et de statut
- **Messages d'erreur** : Messages d'erreur clairs et utiles

## 🧪 Test du Système OAuth

### Script de test automatique
```bash
python test_oauth_system.py
```

Ce script teste :
1. **Authentification OAuth** : Ouverture du navigateur et authentification
2. **Connexion email** : Test de la connexion à Microsoft Graph
3. **Envoi d'email** : Envoi d'un email de test
4. **Application principale** : Test de l'intégration complète

### Test manuel
1. Lancez l'application : `python main.py`
2. Cliquez sur "🌐 Authentification OAuth"
3. Suivez le processus d'authentification web
4. Testez la connexion
5. Générez et envoyez des convocations

## 🔍 Résolution de Problèmes

### Erreur "Port 8080 déjà utilisé"
Si le port 8080 est occupé :
1. Fermez les autres applications utilisant ce port
2. Ou redémarrez l'application

### Navigateur ne s'ouvre pas
1. Vérifiez que votre navigateur par défaut est configuré
2. Copiez l'URL affichée dans la console et ouvrez-la manuellement

### Token expiré
1. Cliquez sur "Déconnecter"
2. Reconnectez-vous avec "🌐 Authentification OAuth"

### Erreurs de permissions
Assurez-vous que votre compte Microsoft a les permissions pour :
- Envoyer des emails
- Accéder à Microsoft Graph

## 📋 Comparaison des Méthodes

| Fonctionnalité | OAuth2 🌐 | Connexion Sécurisée 🔐 |
|----------------|-----------|------------------------|
| Sécurité | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Facilité d'usage | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Compatibilité Outlook | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Configuration requise | Aucune | App Password |
| Interface | Navigateur web | Dialogue application |

## 🔄 Migration depuis l'ancienne méthode

Si vous utilisiez l'ancienne méthode de connexion :

1. **Déconnectez-vous** de l'ancienne méthode
2. **Utilisez OAuth2** : Cliquez sur "🌐 Authentification OAuth"
3. **Supprimez les app passwords** : Plus besoin dans votre compte Microsoft
4. **Profitez** de la nouvelle sécurité et simplicité !

## 🆘 Support

### Logs et Débogage
Les logs détaillés sont disponibles dans :
- `convocation_generator.log` : Logs de l'application
- Console Python : Messages en temps réel

### Problèmes Courants

**"Erreur OAuth Microsoft: ..."**
- Vérifiez votre connexion internet
- Assurez-vous que votre compte Microsoft est actif
- Réessayez l'authentification

**"Erreur envoi email: ..."**
- Vérifiez que le token n'est pas expiré
- Reconnectez-vous si nécessaire
- Vérifiez les adresses email des destinataires

## 🎯 Recommandations

### Pour une utilisation optimale :
1. **Utilisez OAuth2** pour tous les nouveaux projets
2. **Testez régulièrement** la connexion
3. **Gardez l'application à jour** pour les dernières améliorations de sécurité
4. **Sauvegardez vos données** Excel avant l'envoi en masse

### Sécurité :
- Ne partagez jamais vos tokens d'accès
- Déconnectez-vous après utilisation sur des ordinateurs partagés
- Utilisez des comptes avec les permissions minimales nécessaires

---

## 📞 Contact

Pour toute question ou problème avec l'authentification OAuth2, consultez les logs ou contactez le support technique.

**Version OAuth2 : 1.0**  
**Dernière mise à jour : Janvier 2025**
