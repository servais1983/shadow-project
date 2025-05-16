# 🛡️ Shadow – Gardien Numérique

Plateforme complète de surveillance, notification et suppression de données personnelles en ligne.

## 🔐 Fonctions principales

* **Surveillance multi-plateforme** : Détection de vos données personnelles sur Twitter, Instagram, forums, etc.
* **Reconnaissance faciale** : Identification automatique de vos photos via OpenCV et TensorFlow
* **Génération DMCA automatique** : Création de demandes légales pour suppression de contenu
* **Dashboard interactif** : Interface utilisateur intuitive pour suivre vos alertes
* **Application mobile** : Alertes et notifications en temps réel

## 🚀 Lancer Localement

```bash
./scripts/deploy.sh
```

Accès :
* API : [http://localhost:8000](http://localhost:8000)
* Dashboard : [http://localhost:3000](http://localhost:3000)

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

## 📋 Prérequis

* Docker et Docker Compose
* Node.js 18+ et npm
* Python 3.10+
* PostgreSQL (pour développement local sans Docker)

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
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez consulter nos directives de contribution dans `CONTRIBUTING.md`.
