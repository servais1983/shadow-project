import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

// Importer les écrans
import HomeScreen from '../screens/HomeScreen';
import AlertsScreen from '../screens/AlertsScreen';
import ProfileScreen from '../screens/ProfileScreen';
import ScanScreen from '../screens/ScanScreen';
import TakedownRequestScreen from '../screens/TakedownRequestScreen';
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';

// Créer les navigateurs
const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

// Navigateur principal pour les utilisateurs authentifiés
const MainTabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Home') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Alerts') {
            iconName = focused ? 'notifications' : 'notifications-outline';
          } else if (route.name === 'Scan') {
            iconName = focused ? 'scan' : 'scan-outline';
          } else if (route.name === 'Profile') {
            iconName = focused ? 'person' : 'person-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
      })}
      tabBarOptions={{
        activeTintColor: '#6200EE',
        inactiveTintColor: 'gray',
      }}
    >
      <Tab.Screen 
        name="Home" 
        component={HomeScreen} 
        options={{ title: 'Accueil' }}
      />
      <Tab.Screen 
        name="Alerts" 
        component={AlertsScreen} 
        options={{ title: 'Alertes' }}
      />
      <Tab.Screen 
        name="Scan" 
        component={ScanScreen} 
        options={{ title: 'Scanner' }}
      />
      <Tab.Screen 
        name="Profile" 
        component={ProfileScreen} 
        options={{ title: 'Profil' }}
      />
    </Tab.Navigator>
  );
};

// Navigateur d'authentification
const AuthNavigator = () => {
  return (
    <Stack.Navigator 
      initialRouteName="Login"
      screenOptions={{
        headerStyle: {
          backgroundColor: '#6200EE',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}
    >
      <Stack.Screen 
        name="Login" 
        component={LoginScreen} 
        options={{ title: 'Connexion' }}
      />
      <Stack.Screen 
        name="Register" 
        component={RegisterScreen} 
        options={{ title: 'Inscription' }}
      />
    </Stack.Navigator>
  );
};

// Navigateur principal de l'application
const AppNavigator = () => {
  // Ici, nous devrions vérifier si l'utilisateur est authentifié
  // En utilisant un contexte d'authentification ou un état global
  const isAuthenticated = false; // Remplacer par la logique d'authentification réelle

  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
        }}
      >
        {isAuthenticated ? (
          <>
            <Stack.Screen name="Main" component={MainTabNavigator} />
            <Stack.Screen 
              name="TakedownRequest" 
              component={TakedownRequestScreen}
              options={{
                headerShown: true,
                title: 'Demande de suppression',
                headerStyle: {
                  backgroundColor: '#6200EE',
                },
                headerTintColor: '#fff',
              }}
            />
          </>
        ) : (
          <Stack.Screen name="Auth" component={AuthNavigator} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;