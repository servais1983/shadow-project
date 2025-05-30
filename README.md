![image](shadow.jpg)

# 🛡️ Shadow – Gardien Numérique

Interface en ligne de commande pour Kali Linux permettant la surveillance, notification et suppression de données personnelles en ligne.

## 🔐 Fonctions principales

* **Surveillance multi-plateforme** : Détection de vos données personnelles sur Twitter, Instagram, forums, etc.
* **Reconnaissance faciale** : Identification automatique de vos photos via OpenCV et TensorFlow
* **Génération DMCA automatique** : Création de demandes légales pour suppression de contenu
* **Interface CLI pour Kali Linux** : Contrôle complet via ligne de commande pour les analystes en cybersécurité
* **Analyse d'empreinte numérique** : Détection de votre présence en ligne sur différentes plateformes
* **Alerte de fuite d'identité** : Vérification si vos données ont été compromises
* **Générateur d'identités temporaires** : Création de profils temporaires pour protéger votre identité
* **Nettoyage de métadonnées** : Suppression des informations sensibles dans vos fichiers
* **Analyse de réputation** : Évaluation de votre image en ligne avec recommandations
* **Moniteur de Dark Web** : Surveillance des forums et marketplaces du dark web pour détecter vos informations
* **Générateur de mots de passe sécurisés** : Création de mots de passe forts avec évaluation de sécurité
* **Analyse de vulnérabilité personnelle** : Évaluation de votre exposition aux risques de sécurité

## 🚀 Installation et utilisation

```bash
# Installation des dépendances requises
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-pil

# Configuration de l'environnement Python
python3 -m venv venv
source venv/bin/activate
pip install requests pillow

# Lancement de l'interface CLI
./cli/shadow.py deploy    # Déployer l'application
./cli/shadow.py status    # Vérifier l'état des services
./cli/shadow.py stop      # Arrêter les services
./cli/shadow.py facial    # Tester la reconnaissance faciale
```

## 📁 Structure du projet

```
shadow-project/
├── cli/                   # Interface en ligne de commande pour Kali Linux
│   └── shadow.py          # Script principal CLI
├── data/                  # Dossier pour les rapports générés
└── autres fichiers...     # Fichiers de support
```

## 🛠️ Fonctionnalités CLI pour Kali Linux

L'interface CLI de Shadow pour Kali Linux offre plusieurs fonctionnalités spécialisées :

### 1. Gestion des services

```bash
./cli/shadow.py deploy    # Déploie l'application
./cli/shadow.py status    # Affiche l'état des services
./cli/shadow.py stop      # Arrête les services
```

### 2. Reconnaissance faciale optimisée

```bash
./cli/shadow.py facial    # Teste les capacités de reconnaissance faciale
```

### 3. Analyse d'empreinte numérique

Détecte votre présence en ligne sur différentes plateformes sociales et sites web.

```bash
./cli/shadow.py footprint --username johndoe    # Recherche par nom d'utilisateur
./cli/shadow.py footprint --email john@example.com    # Recherche par email
```

### 4. Alerte de fuite d'identité

Vérifie si votre adresse email a été compromise dans des fuites de données connues.

```bash
./cli/shadow.py leak john@example.com    # Vérifie les fuites pour cette adresse email
```

### 5. Générateur d'identités temporaires

Crée des profils temporaires pour protéger votre identité lors de l'inscription à des services.

```bash
./cli/shadow.py identity --count 3    # Génère 3 identités temporaires
```

### 6. Nettoyage de métadonnées

Supprime les informations sensibles (géolocalisation, appareil, etc.) de vos fichiers.

```bash
./cli/shadow.py metadata /chemin/vers/image.jpg    # Nettoie les métadonnées d'une image
```

### 7. Analyse de réputation

Évalue votre réputation en ligne et fournit des recommandations pour l'améliorer.

```bash
./cli/shadow.py reputation --name "John Doe"    # Analyse pour une personne
./cli/shadow.py reputation --company "Acme Inc"    # Analyse pour une entreprise
./cli/shadow.py reputation --website "example.com"    # Analyse pour un site web
```

### 8. Moniteur de Dark Web

Surveille le dark web pour détecter si vos informations personnelles sont exposées ou vendues.

```bash
./cli/shadow.py darkweb --email john@example.com    # Surveille une adresse email
./cli/shadow.py darkweb --username johndoe    # Surveille un nom d'utilisateur
./cli/shadow.py darkweb --phone "+33612345678"    # Surveille un numéro de téléphone
```

### 9. Générateur de mots de passe sécurisés

Crée des mots de passe forts avec évaluation de leur niveau de sécurité.

```bash
./cli/shadow.py password --length 16    # Génère un mot de passe de 16 caractères
./cli/shadow.py password --count 5    # Génère 5 mots de passe
./cli/shadow.py password --no-special    # Sans caractères spéciaux
./cli/shadow.py password --no-uppercase --no-numbers    # Personnalisation avancée
```

### 10. Analyse de vulnérabilité personnelle

Évalue votre exposition aux risques de sécurité et fournit des recommandations personnalisées.

```bash
./cli/shadow.py vulnerability --email john@example.com    # Analyse par email
./cli/shadow.py vulnerability --username johndoe    # Analyse par nom d'utilisateur
./cli/shadow.py vulnerability --profile profile.json    # Analyse à partir d'un profil complet
```

## 📋 Prérequis

* Python 3.10+ avec venv
* Pillow (pour le nettoyage de métadonnées)
* Kali Linux

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
