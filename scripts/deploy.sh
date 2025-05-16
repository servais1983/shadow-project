#!/bin/bash
echo "Déploiement local avec Docker..."

# S'assurer que Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
  echo "Erreur: Docker n'est pas en cours d'exécution ou vous n'avez pas les autorisations nécessaires."
  exit 1
fi

# Vérifier si docker-compose est installé
if ! command -v docker-compose &> /dev/null; then
  echo "Erreur: docker-compose n'est pas installé."
  exit 1
fi

# Copier les fichiers .env.example vers .env s'ils n'existent pas déjà
if [ ! -f ./backend/.env ]; then
  echo "Copie de backend/.env.example vers backend/.env"
  cp ./backend/.env.example ./backend/.env
fi

if [ ! -f ./frontend/.env ]; then
  echo "Copie de frontend/.env.example vers frontend/.env"
  cp ./frontend/.env.example ./frontend/.env
fi

# Lancer les conteneurs Docker en mode détaché
echo "Lancement des conteneurs Docker..."
docker-compose up --build -d

# Vérifier que les conteneurs sont en cours d'exécution
if [ $? -eq 0 ]; then
  echo "✅ Déploiement réussi!"
  echo "📋 Services:"
  echo "  - API: http://localhost:8000"
  echo "  - Dashboard: http://localhost:3000"
  echo "  - Base de données: postgresql://user:pass@localhost:5432/shadow"
  echo "📝 Logs: docker-compose logs -f"
  echo "🛑 Arrêter: docker-compose down"
else
  echo "❌ Le déploiement a échoué. Vérifiez les logs pour plus d'informations."
  echo "docker-compose logs"
fi
