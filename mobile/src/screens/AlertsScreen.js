import React from 'react';
import { StyleSheet, View, Text, FlatList, TouchableOpacity, Alert } from 'react-native';
import { Card, Title, Paragraph, Chip, Button, ActivityIndicator } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { useEffect, useState } from 'react';
import api from '../utils/api';

const AlertsScreen = () => {
  const navigation = useNavigation();
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        setLoading(true);
        const response = await api.get('/social/alerts');
        setAlerts(response.data);
        setError(null);
      } catch (err) {
        console.error('Erreur lors de la récupération des alertes:', err);
        setError('Impossible de charger les alertes. Veuillez réessayer plus tard.');
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  const handleTakedownRequest = (alertId) => {
    // Navigation vers l'écran de demande de suppression
    navigation.navigate('TakedownRequest', { alertId });
  };

  const getPlatformColor = (platform) => {
    switch(platform) {
      case 'Twitter':
        return '#1DA1F2';
      case 'Instagram':
        return '#C13584';
      case 'Facebook':
        return '#4267B2';
      case 'Forum XYZ':
        return '#FF4500';
      default:
        return '#757575';
    }
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#6200EE" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>{error}</Text>
        <Button 
          mode="contained" 
          onPress={() => navigation.goBack()}
          style={styles.button}
        >
          Retour
        </Button>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Title style={styles.title}>Alertes</Title>
        <Paragraph style={styles.subtitle}>Surveillance de vos données personnelles</Paragraph>
      </View>

      {alerts.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Ionicons name="checkmark-circle-outline" size={64} color="#4CAF50" />
          <Text style={styles.emptyText}>Aucune alerte pour le moment</Text>
        </View>
      ) : (
        <FlatList
          data={alerts}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => (
            <Card style={styles.card}>
              <Card.Content>
                <Title>{item.message}</Title>
                <View style={styles.chipContainer}>
                  <Chip 
                    style={{ backgroundColor: getPlatformColor(item.platform) }}
                    textStyle={{ color: 'white' }}
                  >
                    {item.platform}
                  </Chip>
                </View>
                <Paragraph>URL: {item.url}</Paragraph>
                <Paragraph style={styles.timestamp}>
                  Détecté le: {new Date(item.timestamp).toLocaleString()}
                </Paragraph>
              </Card.Content>
              <Card.Actions style={styles.cardActions}>
                <Button 
                  mode="contained" 
                  onPress={() => handleTakedownRequest(item.id)}
                  style={styles.actionButton}
                >
                  Demander suppression
                </Button>
              </Card.Actions>
            </Card>
          )}
          contentContainerStyle={styles.listContainer}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  header: {
    padding: 16,
    backgroundColor: '#6200EE',
  },
  title: {
    color: 'white',
    fontSize: 24,
  },
  subtitle: {
    color: 'rgba(255, 255, 255, 0.8)',
  },
  listContainer: {
    padding: 16,
  },
  card: {
    marginBottom: 16,
    elevation: 4,
  },
  chipContainer: {
    flexDirection: 'row',
    marginVertical: 8,
  },
  timestamp: {
    fontSize: 12,
    color: '#757575',
    marginTop: 8,
  },
  cardActions: {
    justifyContent: 'flex-end',
    paddingHorizontal: 16,
    paddingBottom: 16,
  },
  actionButton: {
    backgroundColor: '#FF5252',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  emptyText: {
    fontSize: 18,
    marginTop: 16,
    color: '#4CAF50',
  },
  errorText: {
    color: '#B00020',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
  },
  button: {
    marginTop: 16,
  },
});

export default AlertsScreen;