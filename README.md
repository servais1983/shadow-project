![image](https://github.com/user-attachments/assets/75084d53-618f-42a5-8d07-2e43f0be4e0c)

# 🛡️ Shadow – Gardien Numérique

Interface en ligne de commande pour Kali Linux permettant la surveillance, notification et suppression de données personnelles en ligne.

## 🔐 Fonctions principales

* **Surveillance multi-plateforme** : Détection de vos données personnelles sur Twitter, Instagram, forums, etc.
* **Reconnaissance faciale** : Identification automatique de vos photos via OpenCV et TensorFlow
* **Génération DMCA automatique** : Création de demandes légales pour suppression de contenu
* **Interface CLI pour Kali Linux** : Contrôle complet via ligne de commande pour les analystes en cybersécurité

## 🚀 Installation et utilisation

```bash
# Installation des dépendances requises
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

# Configuration de l'environnement Python
python3 -m venv venv
source venv/bin/activate
pip install requests

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

Version optimisée pour Kali Linux de l'algorithme de reconnaissance faciale :

```bash
./cli/shadow.py facial    # Teste les capacités de reconnaissance faciale
```

Améliorations spécifiques :
- Optimisation pour les systèmes avec ressources limitées
- Traitement plus rapide des images
- Meilleure précision dans les environnements à faible luminosité

## 📋 Prérequis

* Python 3.10+ avec venv
* Kali Linux

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
