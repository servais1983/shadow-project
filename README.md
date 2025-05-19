![image](https://github.com/user-attachments/assets/75084d53-618f-42a5-8d07-2e43f0be4e0c)

# 🛡️ Shadow – Gardien Numérique

Plateforme complète de surveillance, notification et suppression de données personnelles en ligne.

## 🔐 Fonctions principales

* **Surveillance multi-plateforme** : Détection de vos données personnelles sur Twitter, Instagram, forums, etc.
* **Reconnaissance faciale** : Identification automatique de vos photos via OpenCV et TensorFlow
* **Génération DMCA automatique** : Création de demandes légales pour suppression de contenu
* **Dashboard interactif** : Interface utilisateur intuitive pour suivre vos alertes
* **Application mobile** : Alertes et notifications en temps réel
* **Interface CLI pour Kali Linux** : Contrôle complet via ligne de commande pour les analystes en cybersécurité
* **Scanner de vulnérabilités intégré** : Analyse des cibles avec intégration native aux outils Kali Linux

## 🚀 Lancer Localement

### Interface graphique (Docker)

```bash
./scripts/deploy.sh
```

Accès :
* API : [http://localhost:8000](http://localhost:8000)
* Dashboard : [http://localhost:3000](http://localhost:3000)

### Interface CLI pour Kali Linux

```bash
# Installation des dépendances requises
sudo apt-get update
sudo apt-get install -y docker.io build-essential python3-dev python3-pip python3-venv nmap

# Installation de Docker Compose V2
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Démarrage du service Docker
sudo systemctl start docker
sudo usermod -aG docker $USER
sudo chmod 666 /var/run/docker.sock

# Configuration de l'environnement Python
python3 -m venv venv
source venv/bin/activate
pip install requests docker

# Lancement de l'interface CLI
./cli/shadow.py deploy    # Déployer l'application
./cli/shadow.py status    # Vérifier l'état des services
./cli/shadow.py stop      # Arrêter les services
./cli/shadow.py scan      # Scanner les vulnérabilités d'une cible
./cli/shadow.py facial    # Tester la reconnaissance faciale
```

## 📁 Structure du projet

Shadow est conçu comme un monorepo comprenant les composants suivants :

```
shadow-project/
├── backend/               # API FastAPI + Scraping + IA
│   ├── src/
│   │   ├── api/           # Endpoints FastAPI
│   │   ├── scraping/      # Scrapy/requests pour Twitter, Instagram, etc.
│   │   ├── ai/            # Reconnaissance faciale (OpenCV/TensorFlow)
│   │   ├── legal/         # Génération DMCA, API de suppression
│   │   └── models/        # SQLAlchemy + PostgreSQL
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/              # Dashboard utilisateur (React)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── Dockerfile
│   ├── package.json
│   └── .env.example
├── mobile/                # App mobile (React Native + Expo)
│   ├── src/
│   │   ├── screens/
│   │   ├── navigation/
│   │   └── utils/
│   └── package.json
├── cli/                   # Interface en ligne de commande pour Kali Linux
│   └── shadow.py          # Script principal CLI
├── infrastructure/        # Terraform + Helm charts
│   ├── aws/
│   ├── gcp/
│   └── helm/
├── scripts/
│   ├── deploy.sh
│   └── db-migrations/
├── docker-compose.yml
└── .github/
    └── workflows/
        └── deploy.yml
```

## 🛠️ Fonctionnalités CLI pour Kali Linux

L'interface CLI de Shadow pour Kali Linux offre plusieurs fonctionnalités spécialisées :

### 1. Déploiement et gestion des services

```bash
./cli/shadow.py deploy    # Déploie tous les services via Docker
./cli/shadow.py status    # Affiche l'état des services en cours d'exécution
./cli/shadow.py stop      # Arrête tous les services
```

### 2. Scanner de vulnérabilités

Fonctionnalité innovante qui utilise les outils natifs de Kali Linux pour analyser les vulnérabilités d'une cible :

```bash
./cli/shadow.py scan example.com    # Lance un scan de vulnérabilités sur example.com
```

Le scanner effectue :
- Détection de ports ouverts
- Identification de services vulnérables
- Analyse des failles de sécurité connues
- Génération d'un rapport détaillé

### 3. Reconnaissance faciale optimisée

Version optimisée pour Kali Linux de l'algorithme de reconnaissance faciale :

```bash
./cli/shadow.py facial    # Teste les capacités de reconnaissance faciale
```

Améliorations spécifiques :
- Optimisation pour les systèmes avec ressources limitées
- Traitement plus rapide des images
- Meilleure précision dans les environnements à faible luminosité

## 📋 Prérequis

* Docker et Docker Compose V2
* Python 3.10+ avec venv
* Nmap (pour la fonctionnalité de scan)
* Kali Linux (pour l'interface CLI optimisée)

## 🧪 Tests

Pour exécuter les tests :

```bash
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
npm test

# Mobile
cd mobile
npm test

# CLI
./cli/shadow.py status    # Vérifie que l'interface CLI fonctionne correctement
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez consulter nos directives de contribution dans `CONTRIBUTING.md`.

## 🔧 Dépannage pour Kali Linux

Si vous rencontrez des problèmes avec Docker ou Docker Compose :

1. Vérifiez que le service Docker est en cours d'exécution :
   ```bash
   sudo systemctl status docker
   ```

2. Si le service est inactif, démarrez-le :
   ```bash
   sudo systemctl start docker
   ```

3. Assurez-vous que votre utilisateur appartient au groupe docker :
   ```bash
   sudo usermod -aG docker $USER
   ```

4. Vérifiez les permissions du socket Docker :
   ```bash
   sudo chmod 666 /var/run/docker.sock
   ```

5. Si Docker Compose rencontre des erreurs, réinstallez-le manuellement :
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
   ```
