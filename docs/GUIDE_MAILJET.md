# Guide d'utilisation du Bridge Mailjet Sécurisé

## 🚀 Introduction

Ce guide vous explique comment utiliser le **Bridge Mailjet Sécurisé** pour l'envoi automatisé d'emails de convocation avec une sécurisation HTTPS complète.

## 📋 Table des matières

1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Configuration Mailjet](#configuration-mailjet)
4. [Configuration des credentials](#configuration-des-credentials)
5. [Utilisation du bridge](#utilisation-du-bridge)
6. [Sécurité](#sécurité)
7. [Dépannage](#dépannage)
8. [API Reference](#api-reference)

---

## 🛠️ Prérequis

### Compte Mailjet
- Un compte Mailjet actif (gratuit ou payant)
- Clés API Mailjet (API Key et Secret Key)
- Domaine vérifié dans Mailjet (recommandé)

### Système
- Python 3.7+
- Connexion Internet stable
- Certificats SSL/TLS à jour

### Fichiers requis
- Fichier Excel des candidats
- Fichiers PDF des convocations
- Structure de projet compatible

---

## 📦 Installation

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les nouvelles dépendances incluent :
- `mailjet-rest==1.3.4` : API Mailjet
- `requests==2.31.0` : Requêtes HTTPS sécurisées
- `cryptography==41.0.7` : Chiffrement des credentials

### 2. Vérifier l'installation

```bash
python test_mailjet_bridge.py
```

---

## ⚙️ Configuration Mailjet

### 1. Créer un compte Mailjet

1. Rendez-vous sur [mailjet.com](https://www.mailjet.com)
2. Créez un compte gratuit ou payant
3. Vérifiez votre email

### 2. Obtenir les clés API

1. Connectez-vous à votre compte Mailjet
2. Allez dans **Account Settings** → **Master API Key & Sub API key management**
3. Créez une nouvelle API Key ou utilisez la clé master
4. Notez votre **API Key** et **Secret Key**

### 3. Vérifier votre domaine (recommandé)

1. Dans Mailjet, allez dans **Account Settings** → **Sender domains & addresses**
2. Ajoutez votre domaine email
3. Suivez les instructions de vérification DNS
4. Attendez la validation (peut prendre 24h)

---

## 🔐 Configuration des credentials

### Configuration initiale (une seule fois)

```python
from mailjet_bridge import MailjetBridge

# Créer une instance du bridge
bridge = MailjetBridge(
    excel_path="candidats.xlsx",
    pdf_dir="output",
    sender_email="votre-email@domaine.com", 
    sender_name="Service des Examens"
)

# Configurer les credentials (première fois uniquement)
bridge.setup_credentials(
    api_key="votre_api_key_mailjet",
    secret_key="votre_secret_key_mailjet", 
    password="mot_de_passe_securise"
)
```

### Sécurité des credentials

- ⚠️ **NE JAMAIS** mettre les clés API en dur dans le code
- ✅ Les credentials sont chiffrés avec un mot de passe
- ✅ Utilisation de PBKDF2 avec 100 000 itérations
- ✅ Fichiers de configuration chiffrés localement

---

## 🚀 Utilisation du bridge

### Script basique

```python
#!/usr/bin/env python3
from mailjet_bridge import MailjetBridge
import getpass

def main():
    # Initialiser le bridge
    bridge = MailjetBridge(
        excel_path="candidats.xlsx",
        pdf_dir="output",
        sender_email="examens@votredomaine.com",
        sender_name="Service des Examens"
    )
    
    # Authentification
    password = getpass.getpass("Mot de passe de configuration: ")
    bridge._authenticate(password)
    
    # Test de connexion
    if bridge.test_connection():
        print("✓ Connexion Mailjet OK")
        
        # Fonction de callback pour le suivi
        def print_progress(message):
            print(message)
        
        # Envoyer tous les emails
        count = bridge.send_all_emails(print_progress)
        print(f"Terminé! {count} emails envoyés.")
    else:
        print("✗ Échec de la connexion Mailjet")

if __name__ == "__main__":
    main()
```

### Envoi d'un email individuel

```python
# Données d'un candidat
candidate_data = {
    'nom': 'DUPONT',
    'prenom': 'Jean',
    'email': 'jean.dupont@example.com',
    'numero_candidat': 'DELF2024001',
    'matiere': 'DELF B2',
    'date_examen': '2024-03-15',
    'heure_debut': '09:00',
    'salle': 'Salle A1'
}

# Envoyer l'email
bridge.send_email(candidate_data)
```

### Envoi en lot avec gestion d'erreurs

```python
def envoi_securise():
    try:
        bridge = MailjetBridge(...)
        
        # Authentification
        password = getpass.getpass("Mot de passe: ")
        bridge._authenticate(password)
        
        # Vérifications préalables
        if not bridge.test_connection():
            raise Exception("Connexion Mailjet échouée")
        
        # Fonction de suivi personnalisée
        def progress_callback(message):
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")
            
            # Optionnel : logging dans un fichier
            with open("envoi_emails.log", "a") as f:
                f.write(f"[{timestamp}] {message}\n")
        
        # Envoi des emails
        count = bridge.send_all_emails(progress_callback)
        
        print(f"\n🎉 Envoi terminé avec succès!")
        print(f"📧 {count} emails envoyés via Mailjet")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
        
    return True
```

---

## 🔒 Sécurité

### Fonctionnalités de sécurité

#### 1. **HTTPS Obligatoire**
- Toutes les communications avec Mailjet utilisent HTTPS
- Vérification SSL/TLS automatique
- Certificats vérifiés

#### 2. **Chiffrement des credentials**
- Clés API chiffrées avec AES-256 (Fernet)
- Dérivation de clé PBKDF2 avec SHA-256
- 100 000 itérations pour résister aux attaques par force brute

#### 3. **Gestion des mots de passe**
- Hash sécurisé des mots de passe (SHA-256)
- Pas de stockage en clair
- Authentification requise à chaque utilisation

#### 4. **Protection des fichiers**
- Fichiers de configuration chiffrés
- Permissions restrictives
- Auto-nettoyage des fichiers temporaires

### Bonnes pratiques

#### ✅ À faire
- Utiliser des mots de passe forts (12+ caractères)
- Changer régulièrement les mots de passe
- Sauvegarder les credentials de manière sécurisée
- Vérifier les logs d'envoi
- Tester avec un petit échantillon d'abord

#### ❌ À éviter
- Partager les mots de passe
- Stocker les clés API en dur dans le code
- Utiliser des connexions non sécurisées
- Ignorer les erreurs SSL/TLS

---

## 🔧 Dépannage

### Erreurs courantes

#### **Erreur : "Client Mailjet non initialisé"**
```python
# Solution : Authentifiez-vous d'abord
bridge._authenticate("votre_mot_de_passe")
```

#### **Erreur : "Fichiers de configuration non trouvés"**
```python
# Solution : Configurez d'abord les credentials
bridge.setup_credentials(api_key, secret_key, password)
```

#### **Erreur : "Mot de passe incorrect"**
- Vérifiez la saisie du mot de passe
- Reconfigurez si nécessaire

#### **Erreur : "Credentials Mailjet invalides"**
- Vérifiez vos clés API dans Mailjet
- Assurez-vous que le compte est actif
- Vérifiez les permissions de l'API Key

#### **Erreur : "Fichier PDF de convocation non trouvé"**
- Vérifiez que les PDF existent dans le répertoire
- Contrôlez les noms de fichiers (format attendu)
- Vérifiez les colonnes Excel (nom, prenom, numero_candidat)

### Debug et logs

```python
import logging

# Activer les logs détaillés
logging.basicConfig(level=logging.DEBUG)

# Vérifier les infos du compte
try:
    account_info = bridge.get_account_info()
    print(f"Compte Mailjet: {account_info}")
except Exception as e:
    print(f"Erreur compte: {e}")
```

### Test de connectivité

```python
# Test complet
python test_mailjet_bridge.py

# Test de connexion uniquement
if bridge.test_connection():
    print("Connexion OK")
else:
    print("Problème de connexion")
```

---

## 📚 API Reference

### Classe `MailjetBridge`

#### Constructeur
```python
MailjetBridge(
    excel_path: str,     # Chemin vers le fichier Excel
    pdf_dir: str,        # Répertoire des PDF
    sender_email: str,   # Email expéditeur
    sender_name: str,    # Nom expéditeur
    config_password: str = ""  # Mot de passe optionnel
)
```

#### Méthodes principales

##### `setup_credentials(api_key, secret_key, password)`
Configure et chiffre les credentials Mailjet.

**Paramètres:**
- `api_key` (str) : Clé API Mailjet
- `secret_key` (str) : Clé secrète Mailjet
- `password` (str) : Mot de passe de chiffrement

**Exemple:**
```python
bridge.setup_credentials("abc123", "def456", "mon_mot_de_passe")
```

##### `send_email(candidate_data, progress_callback=None)`
Envoie un email à un candidat.

**Paramètres:**
- `candidate_data` (dict) : Données du candidat
- `progress_callback` (function) : Fonction de callback optionnelle

**Retour:** `bool` - True si succès

**Exemple:**
```python
success = bridge.send_email({
    'nom': 'MARTIN',
    'prenom': 'Sophie',
    'email': 'sophie.martin@test.com',
    # ... autres champs
})
```

##### `send_all_emails(progress_callback=None)`
Envoie des emails à tous les candidats du fichier Excel.

**Paramètres:**
- `progress_callback` (function) : Fonction de callback optionnelle

**Retour:** `int` - Nombre d'emails envoyés avec succès

##### `test_connection()`
Test la connexion à l'API Mailjet.

**Retour:** `bool` - True si la connexion fonctionne

##### `get_account_info()`
Récupère les informations du compte Mailjet.

**Retour:** `dict` - Informations du compte

### Classe `MailjetSecurityManager`

#### `encrypt_credentials(api_key, secret_key, password)`
Chiffre et sauvegarde les credentials.

#### `decrypt_credentials(password)`
Déchiffre et récupère les credentials.

**Retour:** `dict` avec 'api_key' et 'secret_key'

---

## 📄 Format des données

### Fichier Excel requis

Colonnes obligatoires :
- `nom` : Nom du candidat
- `prenom` : Prénom du candidat  
- `email` : Adresse email
- `numero_candidat` : Numéro d'inscription
- `matiere` : Matière/examen
- `date_examen` : Date de l'examen
- `heure_debut` : Heure de début
- `salle` : Salle d'examen

### Fichiers PDF

Format de nom attendu :
- `convocation_{NOM}_{PRENOM}_{NUMERO}.pdf`
- `convocation_{NOM}_{PRENOM}.pdf`
- `{NOM}_{PRENOM}_{NUMERO}.pdf`

---

## 🌐 Intégration avec l'application principale

### Modification du main.py

```python
# Ajouter l'import
from mailjet_bridge import MailjetBridge

# Ajouter une option Mailjet dans l'interface
def setup_mailjet_option():
    """Configure l'option Mailjet dans l'interface"""
    # Code d'intégration avec tkinter
    pass

# Dans la fonction d'envoi d'emails
def send_emails_mailjet():
    """Fonction d'envoi via Mailjet"""
    try:
        bridge = MailjetBridge(
            excel_path=excel_path,
            pdf_dir="output",
            sender_email=sender_email,
            sender_name="Service des Examens"
        )
        
        password = simpledialog.askstring("Mailjet", "Mot de passe:", show='*')
        bridge._authenticate(password)
        
        if bridge.test_connection():
            count = bridge.send_all_emails(update_progress)
            messagebox.showinfo("Succès", f"{count} emails envoyés via Mailjet!")
        else:
            messagebox.showerror("Erreur", "Connexion Mailjet échouée")
            
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur Mailjet: {e}")
```

---

## 🆘 Support

### En cas de problème

1. **Vérifiez les logs** : Regardez les messages d'erreur détaillés
2. **Testez la connectivité** : Utilisez `test_mailjet_bridge.py`
3. **Vérifiez les credentials** : Testez dans l'interface Mailjet
4. **Consultez la documentation Mailjet** : [dev.mailjet.com](https://dev.mailjet.com)

### Limites de l'API Mailjet

- **Gratuit** : 6 000 emails/mois, 200 emails/jour
- **Payant** : Selon votre plan
- **Débit** : Respect automatique des limites API
- **Taille** : 15MB par email (pièces jointes incluses)

---

## 🔄 Migration depuis Outlook

### Avantages du passage à Mailjet

| Critère | Outlook | Mailjet |
|---------|---------|---------|
| **Sécurité** | Dépend du client | HTTPS natif |
| **Fiabilité** | Variable | API professionnelle |
| **Suivi** | Limité | Statistiques complètes |
| **Délivrabilité** | Moyenne | Optimisée |
| **Configuration** | Complexe | Simple |

### Script de migration

```python
def migrate_from_outlook():
    """Migre la configuration d'Outlook vers Mailjet"""
    
    # 1. Sauvegarder les données existantes
    # 2. Configurer Mailjet
    # 3. Tester l'envoi
    # 4. Valider la migration
    
    print("Migration vers Mailjet terminée!")
```

---

## 📈 Monitoring et statistiques

### Suivi des envois

Mailjet fournit automatiquement :
- Emails envoyés
- Emails délivrés  
- Emails ouverts
- Clics sur les liens
- Bounces et erreurs

### Dashboard Mailjet

Connectez-vous à votre compte Mailjet pour accéder aux statistiques détaillées.

---

**🎯 Le bridge Mailjet sécurisé est maintenant prêt à l'emploi ! Envoyez vos convocations en toute sécurité avec HTTPS.**
