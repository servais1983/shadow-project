import axios from 'axios';

// Récupérer l'URL de l'API depuis les variables d'environnement
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Créer une instance axios avec des paramètres par défaut
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification à chaque requête
api.interceptors.request.use(
  (config) => {
    // Récupérer le token depuis le localStorage
    const token = localStorage.getItem('auth_token');
    
    // Si un token existe, l'ajouter aux headers
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs de réponse (ex: token expiré)
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Si l'erreur est 401 (non autorisé), déconnecter l'utilisateur
    if (error.response && error.response.status === 401) {
      // Supprimer le token
      localStorage.removeItem('auth_token');
      
      // Rediriger vers la page de connexion
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

export default api;
