import cv2
import os
import tensorflow as tf
import numpy as np
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def scan_image(image_path):
    """
    Détecte les visages dans une image en utilisant OpenCV
    """
    # Obtenir le chemin du modèle Haar Cascade depuis les variables d'environnement ou utiliser une valeur par défaut
    cascade_path = os.getenv("OPENCV_MODEL_PATH", "haarcascade_frontalface_default.xml")
    
    # Vérifier si le modèle existe
    if not os.path.exists(cascade_path):
        print(f"Attention: Modèle Haar Cascade non trouvé à {cascade_path}")
        return False
    
    try:
        # Charger le classificateur Haar Cascade
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Charger l'image
        img = cv2.imread(image_path)
        
        # Vérifier si l'image a été correctement chargée
        if img is None:
            print(f"Erreur: Impossible de charger l'image à {image_path}")
            return False
        
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Détecter les visages
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Retourner True si au moins un visage est détecté
        return len(faces) > 0
    
    except Exception as e:
        print(f"Erreur lors de la détection faciale: {str(e)}")
        return False

def compare_faces(reference_image_path, target_image_path, similarity_threshold=0.6):
    """
    Compare deux visages pour déterminer s'il s'agit de la même personne
    Utilise TensorFlow et un modèle pré-entraîné pour l'extraction de caractéristiques faciales
    """
    # Note: Cette implémentation est une simulation simplifiée.
    # Une version réelle utiliserait un modèle pré-entraîné comme FaceNet pour encoder les visages.
    
    try:
        # Détecter les visages dans les deux images
        ref_has_face = scan_image(reference_image_path)
        target_has_face = scan_image(target_image_path)
        
        if not ref_has_face or not target_has_face:
            print("Aucun visage détecté dans une des images")
            return False
        
        # Simulation d'une comparaison (dans une impl. réelle, on utiliserait un modèle d'encodage facial)
        # et on calculerait la distance entre les embeddings.
        similarity = np.random.uniform(0, 1)  # Valeur aléatoire pour simuler la similarité
        
        return similarity > similarity_threshold
    
    except Exception as e:
        print(f"Erreur lors de la comparaison faciale: {str(e)}")
        return False
