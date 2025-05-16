import React, { useEffect, useState } from "react";
import axios from "../services/api";
import { 
  Typography, 
  Paper, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  Chip, 
  Button,
  CircularProgress
} from "@material-ui/core";
import { Alert, AlertTitle } from "@material-ui/lab";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        setLoading(true);
        const response = await axios.get("/social/alerts");
        setAlerts(response.data);
        setError(null);
      } catch (err) {
        console.error("Erreur lors de la récupération des alertes:", err);
        setError("Impossible de charger les alertes. Veuillez réessayer plus tard.");
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
    
    // Rafraîchir les alertes toutes les 5 minutes
    const intervalId = setInterval(fetchAlerts, 5 * 60 * 1000);
    
    // Nettoyer l'intervalle lors du démontage du composant
    return () => clearInterval(intervalId);
  }, []);

  const getSeverityColor = (platform) => {
    switch(platform) {
      case 'Twitter':
        return '#1DA1F2'; // Bleu Twitter
      case 'Instagram':
        return '#C13584'; // Violet Instagram
      case 'Facebook':
        return '#4267B2'; // Bleu Facebook
      case 'Forum XYZ':
        return '#FF4500'; // Orange
      default:
        return '#757575'; // Gris par défaut
    }
  };

  const handleTakedownRequest = (alertId) => {
    // Logique pour initier une demande de suppression
    console.log(`Demande de suppression pour l'alerte: ${alertId}`);
    // Rediriger vers la page de formulaire de suppression ou ouvrir un modal
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" m={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box m={2}>
        <Alert severity="error">
          <AlertTitle>Erreur</AlertTitle>
          {error}
        </Alert>
      </Box>
    );
  }

  return (
    <div>
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Alertes
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
          Surveillance des mentions de vos données personnelles en ligne
        </Typography>
      </Box>

      {alerts.length === 0 ? (
        <Paper elevation={2} style={{ padding: 16 }}>
          <Typography>Aucune alerte pour le moment. Tout semble sécurisé!</Typography>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {alerts.map((alert, index) => (
            <Grid item xs={12} key={index}>
              <Card>
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h6" component="h2">
                      {alert.message}
                    </Typography>
                    <Chip 
                      label={alert.platform} 
                      style={{ 
                        backgroundColor: getSeverityColor(alert.platform),
                        color: 'white'
                      }} 
                    />
                  </Box>
                  
                  <Typography variant="body2" color="textSecondary" component="p" gutterBottom>
                    URL: <a href={alert.url} target="_blank" rel="noopener noreferrer">{alert.url}</a>
                  </Typography>
                  
                  <Typography variant="caption" color="textSecondary">
                    Détecté le: {new Date(alert.timestamp).toLocaleString()}
                  </Typography>
                  
                  <Box mt={2} display="flex" justifyContent="flex-end">
                    <Button 
                      variant="outlined" 
                      color="secondary" 
                      onClick={() => handleTakedownRequest(index)}
                    >
                      Demander suppression
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </div>
  );
}
