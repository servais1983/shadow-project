import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Constants from 'expo-constants';

// Récupérer l'URL de l'API depuis les variables d'environnement d'Expo
const { API_URL } = Constants.manifest.extra || {};
const BASE_URL = API_URL || 'http://localhost:8000';

// Créer une instance axios avec des paramètres par défaut
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // Timeout de 10 secondes
});

// Intercepteur pour ajouter le token d'authentification à chaque requête
api.interceptors.request.use(
  async (config) => {
    try {
      // Récupérer le token depuis AsyncStorage
      const token = await AsyncStorage.getItem('auth_token');
      
      // Si un token existe, l'ajouter aux headers
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      
      return config;
    } catch (error) {
      console.error('Erreur lors de la récupération du token:', error);
      return config;
    }
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
  async (error) => {
    // Si l'erreur est 401 (non autorisé), déconnecter l'utilisateur
    if (error.response && error.response.status === 401) {
      try {
        // Supprimer le token
        await AsyncStorage.removeItem('auth_token');
        
        // Vous pourriez également rediriger l'utilisateur vers la page de connexion
        // en utilisant un mécanisme de navigation accessible ici
      } catch (storageError) {
        console.error('Erreur lors de la suppression du token:', storageError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;