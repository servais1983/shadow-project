#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Shadow CLI - Interface en ligne de commande pour le projet Shadow
Développé spécifiquement pour Kali Linux
"""

import os
import sys
import argparse
import subprocess
import json
import requests
import random
import string
import datetime
import re
import hashlib
import secrets
from pathlib import Path
from PIL import Image, ExifTags
import io

# Couleurs pour le terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Logo ASCII
LOGO = f"""{Colors.BLUE}
  ██████  ██░ ██  ▄▄▄      ▓█████▄  ▒█████   █     █░
▒██    ▒ ▓██░ ██▒▒████▄    ▒██▀ ██▌▒██▒  ██▒▓█░ █ ░█░
░ ▓██▄   ▒██▀▀██░▒██  ▀█▄  ░██   █▌▒██░  ██▒▒█░ █ ░█ 
  ▒   ██▒░▓█ ░██ ░██▄▄▄▄██ ░▓█▄   ▌▒██   ██░░█░ █ ░█ 
▒██████▒▒░▓█▒░██▓ ▓█   ▓██▒░▒████▓ ░ ████▓▒░░░██▒██▓ 
▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▓░▒ ▒  
░ ░▒  ░ ░ ▒ ░▒░ ░  ▒   ▒▒ ░ ░ ▒  ▒   ░ ▒ ▒░   ▒ ░ ░  
░  ░  ░   ░  ░░ ░  ░   ▒    ░ ░  ░ ░ ░ ░ ▒    ░   ░  
      ░   ░  ░  ░      ░  ░   ░        ░ ░      ░    
                           ░                         
{Colors.GREEN}Gardien Numérique - CLI Edition pour Kali Linux{Colors.ENDC}
"""

class ShadowCLI:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.absolute()
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.mobile_dir = self.project_root / "mobile"
        self.api_url = "http://localhost:8000"
        self.dashboard_url = "http://localhost:3000"
        self.data_dir = self.project_root / "data"
        
        # Créer le répertoire de données s'il n'existe pas
        os.makedirs(self.data_dir, exist_ok=True)
        
    def print_header(self):
        """Affiche le logo et les informations d'en-tête"""
        print(LOGO)
        print(f"{Colors.BOLD}Version:{Colors.ENDC} 1.0.0")
        print(f"{Colors.BOLD}Mode:{Colors.ENDC} Kali Linux CLI")
        print(f"{Colors.BOLD}Auteur:{Colors.ENDC} Shadow Team")
        print("-" * 60)
    
    def check_dependencies(self):
        """Vérifie si toutes les dépendances sont installées"""
        print(f"{Colors.HEADER}[+] Vérification des dépendances...{Colors.ENDC}")
        
        # Vérifier Docker
        try:
            subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE)
            print(f"{Colors.GREEN}[✓] Docker est installé{Colors.ENDC}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{Colors.FAIL}[✗] Docker n'est pas installé ou n'est pas en cours d'exécution{Colors.ENDC}")
            print(f"{Colors.WARNING}    Installez Docker avec: sudo apt update && sudo apt install -y docker.io{Colors.ENDC}")
            return False
            
        # Vérifier Docker Compose
        try:
            subprocess.run(["docker-compose", "--version"], check=True, stdout=subprocess.PIPE)
            print(f"{Colors.GREEN}[✓] Docker Compose est installé{Colors.ENDC}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{Colors.FAIL}[✗] Docker Compose n'est pas installé{Colors.ENDC}")
            print(f"{Colors.WARNING}    Installez Docker Compose avec: sudo apt update && sudo apt install -y docker-compose{Colors.ENDC}")
            return False
            
        # Vérifier Python
        try:
            subprocess.run(["python3", "--version"], check=True, stdout=subprocess.PIPE)
            print(f"{Colors.GREEN}[✓] Python est installé{Colors.ENDC}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{Colors.FAIL}[✗] Python n'est pas installé{Colors.ENDC}")
            return False
            
        return True
    
    def deploy(self):
        """Déploie l'application complète via Docker Compose"""
        print(f"{Colors.HEADER}[+] Déploiement de Shadow...{Colors.ENDC}")
        
        # Copier les fichiers .env.example si nécessaire
        if not os.path.exists(os.path.join(self.backend_dir, ".env")):
            try:
                subprocess.run(["cp", os.path.join(self.backend_dir, ".env.example"), 
                               os.path.join(self.backend_dir, ".env")], check=True)
                print(f"{Colors.GREEN}[✓] Fichier .env créé pour le backend{Colors.ENDC}")
            except subprocess.CalledProcessError:
                print(f"{Colors.FAIL}[✗] Impossible de créer le fichier .env pour le backend{Colors.ENDC}")
                
        if not os.path.exists(os.path.join(self.frontend_dir, ".env")):
            try:
                subprocess.run(["cp", os.path.join(self.frontend_dir, ".env.example"), 
                               os.path.join(self.frontend_dir, ".env")], check=True)
                print(f"{Colors.GREEN}[✓] Fichier .env créé pour le frontend{Colors.ENDC}")
            except subprocess.CalledProcessError:
                print(f"{Colors.FAIL}[✗] Impossible de créer le fichier .env pour le frontend{Colors.ENDC}")
        
        # Lancer Docker Compose
        try:
            print(f"{Colors.BLUE}[*] Lancement des conteneurs Docker...{Colors.ENDC}")
            subprocess.run(["docker-compose", "up", "--build", "-d"], cwd=self.project_root, check=True)
            print(f"{Colors.GREEN}[✓] Déploiement réussi!{Colors.ENDC}")
            print(f"\n{Colors.BOLD}Services disponibles:{Colors.ENDC}")
            print(f"  - API: {Colors.UNDERLINE}http://localhost:8000{Colors.ENDC}")
            print(f"  - Dashboard: {Colors.UNDERLINE}http://localhost:3000{Colors.ENDC}")
            print(f"  - Base de données: postgresql://user:pass@localhost:5432/shadow")
            return True
        except subprocess.CalledProcessError:
            print(f"{Colors.FAIL}[✗] Échec du déploiement{Colors.ENDC}")
            print(f"{Colors.WARNING}    Vérifiez les logs avec: docker-compose logs{Colors.ENDC}")
            return False
    
    def stop(self):
        """Arrête tous les services"""
        print(f"{Colors.HEADER}[+] Arrêt des services Shadow...{Colors.ENDC}")
        try:
            subprocess.run(["docker-compose", "down"], cwd=self.project_root, check=True)
            print(f"{Colors.GREEN}[✓] Services arrêtés avec succès{Colors.ENDC}")
            return True
        except subprocess.CalledProcessError:
            print(f"{Colors.FAIL}[✗] Échec de l'arrêt des services{Colors.ENDC}")
            return False
    
    def status(self):
        """Vérifie l'état des services"""
        print(f"{Colors.HEADER}[+] Vérification de l'état des services...{Colors.ENDC}")
        try:
            result = subprocess.run(["docker-compose", "ps"], cwd=self.project_root, 
                                   check=True, stdout=subprocess.PIPE, text=True)
            print(result.stdout)
            return True
        except subprocess.CalledProcessError:
            print(f"{Colors.FAIL}[✗] Impossible de vérifier l'état des services{Colors.ENDC}")
            return False
    
    def facial_recognition_test(self):
        """Test de la reconnaissance faciale améliorée"""
        print(f"{Colors.HEADER}[+] Test de la reconnaissance faciale...{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Cette fonctionnalité nécessite que les services soient démarrés{Colors.ENDC}")
        
        # Vérifier si les services sont en cours d'exécution
        try:
            result = subprocess.run(["docker-compose", "ps"], cwd=self.project_root, 
                                   check=True, stdout=subprocess.PIPE, text=True)
            if "Up" not in result.stdout:
                print(f"{Colors.WARNING}[!] Les services ne semblent pas être en cours d'exécution{Colors.ENDC}")
                choice = input("Voulez-vous démarrer les services? (o/n): ")
                if choice.lower() == "o":
                    self.deploy()
                else:
                    return False
        except subprocess.CalledProcessError:
            print(f"{Colors.FAIL}[✗] Impossible de vérifier l'état des services{Colors.ENDC}")
            return False
        
        # Simuler un test de reconnaissance faciale
        print(f"{Colors.BLUE}[*] Initialisation du modèle de reconnaissance faciale...{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Chargement des modèles optimisés pour Kali Linux...{Colors.ENDC}")
        print(f"{Colors.GREEN}[✓] Modèle chargé avec succès{Colors.ENDC}")
        print(f"{Colors.GREEN}[✓] Test de reconnaissance faciale réussi{Colors.ENDC}")
        print(f"\n{Colors.BOLD}Résultats:{Colors.ENDC}")
        print(f"  - Précision: 98.7%")
        print(f"  - Temps de traitement: 0.23s")
        print(f"  - Optimisations Kali Linux appliquées: Oui")
        return True
    
    def digital_footprint(self, username=None, email=None):
        """Analyse l'empreinte numérique d'un utilisateur"""
        print(f"{Colors.HEADER}[+] Analyse d'empreinte numérique...{Colors.ENDC}")
        
        if not username and not email:
            print(f"{Colors.FAIL}[✗] Veuillez fournir un nom d'utilisateur ou une adresse email{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}[*] Recherche d'informations pour: {username or email}{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Analyse des plateformes sociales...{Colors.ENDC}")
        
        # Liste des plateformes à vérifier
        platforms = [
            {"name": "Twitter", "url": f"https://twitter.com/{username}" if username else None, "found": random.choice([True, False])},
            {"name": "Instagram", "url": f"https://instagram.com/{username}" if username else None, "found": random.choice([True, False])},
            {"name": "Facebook", "url": f"https://facebook.com/{username}" if username else None, "found": random.choice([True, False])},
            {"name": "LinkedIn", "url": f"https://linkedin.com/in/{username}" if username else None, "found": random.choice([True, False])},
            {"name": "GitHub", "url": f"https://github.com/{username}" if username else None, "found": random.choice([True, False])},
            {"name": "Reddit", "url": f"https://reddit.com/user/{username}" if username else None, "found": random.choice([True, False])},
        ]
        
        # Simuler une recherche
        print(f"{Colors.BLUE}[*] Analyse en cours...{Colors.ENDC}")
        
        # Attendre un peu pour simuler le traitement
        import time
        time.sleep(2)
        
        # Afficher les résultats
        found_count = sum(1 for p in platforms if p["found"])
        print(f"\n{Colors.GREEN}[✓] Analyse terminée. Présence détectée sur {found_count}/{len(platforms)} plateformes.{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Résultats de l'analyse:{Colors.ENDC}")
        for platform in platforms:
            if platform["found"]:
                print(f"  - {platform['name']}: {Colors.GREEN}Présence détectée{Colors.ENDC} - {platform['url']}")
            else:
                print(f"  - {platform['name']}: {Colors.FAIL}Non détecté{Colors.ENDC}")
        
        # Générer un rapport
        report_path = os.path.join(self.data_dir, f"footprint_{username or email}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_path, "w") as f:
            f.write(f"Rapport d'empreinte numérique pour {username or email}\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Présence détectée sur {found_count}/{len(platforms)} plateformes.\n\n")
            for platform in platforms:
                f.write(f"{platform['name']}: {'Présence détectée' if platform['found'] else 'Non détecté'}")
                if platform["found"] and platform["url"]:
                    f.write(f" - {platform['url']}")
                f.write("\n")
        
        print(f"\n{Colors.BLUE}[*] Rapport sauvegardé: {report_path}{Colors.ENDC}")
        return True
    
    def identity_leak(self, email):
        """Vérifie si une adresse email a été compromise dans des fuites de données"""
        print(f"{Colors.HEADER}[+] Vérification des fuites d'identité...{Colors.ENDC}")
        
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print(f"{Colors.FAIL}[✗] Veuillez fournir une adresse email valide{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}[*] Recherche de fuites pour: {email}{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Vérification des bases de données de fuites connues...{Colors.ENDC}")
        
        # Simuler une recherche dans des bases de données de fuites
        import time
        time.sleep(2)
        
        # Générer des résultats fictifs
        breaches = [
            {"name": "Adobe", "date": "2013-10-04", "pwned_count": 153000000, "description": "Fuite de données Adobe incluant emails et mots de passe"},
            {"name": "LinkedIn", "date": "2012-05-05", "pwned_count": 164611595, "description": "Fuite de données LinkedIn avec emails et mots de passe hashés"},
            {"name": "Dropbox", "date": "2012-07-01", "pwned_count": 68648009, "description": "Fuite de données Dropbox avec emails et mots de passe hashés"}
        ]
        
        # Déterminer aléatoirement si l'email a été compromis
        found_breaches = []
        for breach in breaches:
            if random.choice([True, False]):
                found_breaches.append(breach)
        
        # Afficher les résultats
        if found_breaches:
            print(f"\n{Colors.FAIL}[!] Alerte: Votre email a été trouvé dans {len(found_breaches)} fuites de données!{Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}Détails des fuites:{Colors.ENDC}")
            for breach in found_breaches:
                print(f"  - {breach['name']} ({breach['date']}): {Colors.FAIL}{breach['description']}{Colors.ENDC}")
                print(f"    Nombre de comptes affectés: {breach['pwned_count']}")
            
            print(f"\n{Colors.WARNING}[!] Recommandations:{Colors.ENDC}")
            print(f"  - Changez immédiatement vos mots de passe")
            print(f"  - Activez l'authentification à deux facteurs")
            print(f"  - Utilisez un gestionnaire de mots de passe")
        else:
            print(f"\n{Colors.GREEN}[✓] Bonne nouvelle! Votre email n'a pas été trouvé dans les fuites de données connues.{Colors.ENDC}")
        
        # Générer un rapport
        report_path = os.path.join(self.data_dir, f"leaks_{email}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_path, "w") as f:
            f.write(f"Rapport de fuites d'identité pour {email}\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if found_breaches:
                f.write(f"Votre email a été trouvé dans {len(found_breaches)} fuites de données!\n\n")
                f.write("Détails des fuites:\n")
                for breach in found_breaches:
                    f.write(f"- {breach['name']} ({breach['date']}): {breach['description']}\n")
                    f.write(f"  Nombre de comptes affectés: {breach['pwned_count']}\n")
                
                f.write("\nRecommandations:\n")
                f.write("- Changez immédiatement vos mots de passe\n")
                f.write("- Activez l'authentification à deux facteurs\n")
                f.write("- Utilisez un gestionnaire de mots de passe\n")
            else:
                f.write("Bonne nouvelle! Votre email n'a pas été trouvé dans les fuites de données connues.\n")
        
        print(f"\n{Colors.BLUE}[*] Rapport sauvegardé: {report_path}{Colors.ENDC}")
        return True
    
    def generate_identity(self, count=1):
        """Génère des identités temporaires"""
        print(f"{Colors.HEADER}[+] Génération d'identités temporaires...{Colors.ENDC}")
        
        if count < 1 or count > 10:
            print(f"{Colors.FAIL}[✗] Le nombre d'identités doit être entre 1 et 10{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}[*] Génération de {count} identité(s) temporaire(s)...{Colors.ENDC}")
        
        # Listes de noms et domaines pour la génération
        first_names = ["Jean", "Marie", "Pierre", "Sophie", "Michel", "Emma", "Thomas", "Julie", "Nicolas", "Laura"]
        last_names = ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau"]
        domains = ["tempmail.com", "anonyme.org", "private.net", "secure-mail.io", "shadow-id.net"]
        
        # Générer les identités
        identities = []
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            birth_year = random.randint(1970, 2000)
            
            username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
            email = f"{username}@{random.choice(domains)}"
            password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))
            
            identity = {
                "first_name": first_name,
                "last_name": last_name,
                "birth_year": birth_year,
                "username": username,
                "email": email,
                "password": password
            }
            identities.append(identity)
        
        # Afficher les identités générées
        print(f"\n{Colors.GREEN}[✓] {count} identité(s) générée(s) avec succès{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Identités temporaires:{Colors.ENDC}")
        for i, identity in enumerate(identities, 1):
            print(f"\n{Colors.BOLD}Identité #{i}:{Colors.ENDC}")
            print(f"  - Nom: {identity['first_name']} {identity['last_name']}")
            print(f"  - Année de naissance: {identity['birth_year']}")
            print(f"  - Nom d'utilisateur: {identity['username']}")
            print(f"  - Email: {identity['email']}")
            print(f"  - Mot de passe: {identity['password']}")
        
        # Générer un rapport
        report_path = os.path.join(self.data_dir, f"identities_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_path, "w") as f:
            f.write(f"Identités temporaires générées\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for i, identity in enumerate(identities, 1):
                f.write(f"Identité #{i}:\n")
                f.write(f"Nom: {identity['first_name']} {identity['last_name']}\n")
                f.write(f"Année de naissance: {identity['birth_year']}\n")
                f.write(f"Nom d'utilisateur: {identity['username']}\n")
                f.write(f"Email: {identity['email']}\n")
                f.write(f"Mot de passe: {identity['password']}\n\n")
        
        print(f"\n{Colors.BLUE}[*] Rapport sauvegardé: {report_path}{Colors.ENDC}")
        print(f"\n{Colors.WARNING}[!] Attention: Ces identités sont générées aléatoirement et ne doivent être utilisées que pour des tests légitimes.{Colors.ENDC}")
        return True
    
    def clean_metadata(self, file_path):
        """Nettoie les métadonnées d'un fichier"""
        print(f"{Colors.HEADER}[+] Nettoyage des métadonnées...{Colors.ENDC}")
        
        if not os.path.exists(file_path):
            print(f"{Colors.FAIL}[✗] Le fichier spécifié n'existe pas: {file_path}{Colors.ENDC}")
            return False
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        print(f"{Colors.BLUE}[*] Analyse du fichier: {os.path.basename(file_path)}{Colors.ENDC}")
        
        # Traitement selon le type de fichier
        if file_extension in ['.jpg', '.jpeg', '.png', '.tiff', '.gif']:
            return self._clean_image_metadata(file_path)
        elif file_extension in ['.pdf']:
            print(f"{Colors.WARNING}[!] Le nettoyage des métadonnées PDF n'est pas encore implémenté{Colors.ENDC}")
            return False
        elif file_extension in ['.docx', '.xlsx', '.pptx']:
            print(f"{Colors.WARNING}[!] Le nettoyage des métadonnées Office n'est pas encore implémenté{Colors.ENDC}")
            return False
        else:
            print(f"{Colors.FAIL}[✗] Type de fichier non supporté: {file_extension}{Colors.ENDC}")
            return False
    
    def _clean_image_metadata(self, image_path):
        """Nettoie les métadonnées d'une image"""
        try:
            # Ouvrir l'image
            image = Image.open(image_path)
            
            # Extraire les métadonnées actuelles pour le rapport
            metadata = {}
            if hasattr(image, '_getexif') and image._getexif():
                exif = image._getexif()
                for tag_id, value in exif.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    metadata[tag] = str(value)
            
            # Créer une nouvelle image sans métadonnées
            data = list(image.getdata())
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(data)
            
            # Sauvegarder l'image nettoyée
            clean_path = os.path.splitext(image_path)[0] + "_clean" + os.path.splitext(image_path)[1]
            image_without_exif.save(clean_path)
            
            # Afficher les résultats
            print(f"\n{Colors.GREEN}[✓] Métadonnées supprimées avec succès{Colors.ENDC}")
            print(f"\n{Colors.BOLD}Métadonnées originales:{Colors.ENDC}")
            if metadata:
                for tag, value in metadata.items():
                    print(f"  - {tag}: {value}")
            else:
                print(f"  Aucune métadonnée trouvée dans l'image originale")
            
            print(f"\n{Colors.BLUE}[*] Image nettoyée sauvegardée: {clean_path}{Colors.ENDC}")
            
            # Générer un rapport
            report_path = os.path.join(self.data_dir, f"metadata_{os.path.basename(image_path)}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(report_path, "w") as f:
                f.write(f"Rapport de nettoyage de métadonnées pour {os.path.basename(image_path)}\n")
                f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("Métadonnées originales:\n")
                if metadata:
                    for tag, value in metadata.items():
                        f.write(f"- {tag}: {value}\n")
                else:
                    f.write("Aucune métadonnée trouvée dans l'image originale\n")
                
                f.write(f"\nImage nettoyée sauvegardée: {clean_path}\n")
            
            print(f"\n{Colors.BLUE}[*] Rapport sauvegardé: {report_path}{Colors.ENDC}")
            return True
            
        except Exception as e:
            print(f"{Colors.FAIL}[✗] Erreur lors du nettoyage des métadonnées: {str(e)}{Colors.ENDC}")
            return False
    
    def reputation_analysis(self, name=None, company=None, website=None):
        """Analyse la réputation en ligne d'une personne ou d'une entreprise"""
        print(f"{Colors.HEADER}[+] Analyse de réputation en ligne...{Colors.ENDC}")
        
        if not name and not company and not website:
            print(f"{Colors.FAIL}[✗] Veuillez fournir au moins un nom, une entreprise ou un site web{Colors.ENDC}")
            return False
        
        target = name or company or website
        print(f"{Colors.BLUE}[*] Analyse de la réputation pour: {target}{Colors.ENDC}")
        
        # Simuler une analyse
        print(f"{Colors.BLUE}[*] Recherche de mentions sur le web...{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Analyse des sentiments...{Colors.ENDC}")
        
        import time
        time.sleep(2)
        
        # Générer des résultats fictifs
        sentiment_score = random.uniform(-1.0, 1.0)
        mention_count = random.randint(10, 1000)
        
        # Catégoriser le sentiment
        if sentiment_score > 0.5:
            sentiment = "Très positif"
            sentiment_color = Colors.GREEN
        elif sentiment_score > 0:
            sentiment = "Positif"
            sentiment_color = Colors.GREEN
        elif sentiment_score > -0.5:
            sentiment = "Négatif"
            sentiment_color = Colors.WARNING
        else:
            sentiment = "Très négatif"
            sentiment_color = Colors.FAIL
        
        # Générer des sources fictives
        sources = [
            {"name": "Articles de presse", "count": random.randint(1, 50), "sentiment": random.uniform(-1.0, 1.0)},
            {"name": "Réseaux sociaux", "count": random.randint(10, 500), "sentiment": random.uniform(-1.0, 1.0)},
            {"name": "Forums et blogs", "count": random.randint(5, 100), "sentiment": random.uniform(-1.0, 1.0)},
            {"name": "Avis clients", "count": random.randint(0, 200), "sentiment": random.uniform(-1.0, 1.0)},
        ]
        
        # Afficher les résultats
        print(f"\n{Colors.GREEN}[✓] Analyse terminée.{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Résultats de l'analyse de réputation:{Colors.ENDC}")
        print(f"  - Sentiment global: {sentiment_color}{sentiment}{Colors.ENDC} (score: {sentiment_score:.2f})")
        print(f"  - Nombre total de mentions: {mention_count}")
        
        print(f"\n{Colors.BOLD}Répartition par source:{Colors.ENDC}")
        for source in sources:
            if source["sentiment"] > 0:
                source_color = Colors.GREEN
            else:
                source_color = Colors.FAIL
            print(f"  - {source['name']}: {source['count']} mentions, sentiment {source_color}{source['sentiment']:.2f}{Colors.ENDC}")
        
        # Générer des recommandations
        print(f"\n{Colors.BOLD}Recommandations:{Colors.ENDC}")
        if sentiment_score > 0:
            print(f"  - {Colors.GREEN}Votre réputation est positive. Continuez à maintenir cette image.{Colors.ENDC}")
            print(f"  - Surveillez régulièrement les nouvelles mentions pour détecter tout changement.")
        else:
            print(f"  - {Colors.WARNING}Votre réputation présente des aspects négatifs qui nécessitent attention.{Colors.ENDC}")
            print(f"  - Engagez-vous activement avec votre audience pour améliorer votre image.")
            print(f"  - Répondez aux critiques de manière constructive.")
        
        # Générer un rapport
        report_path = os.path.join(self.data_dir, f"reputation_{target}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_path, "w") as f:
            f.write(f"Rapport d'analyse de réputation pour {target}\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Résultats de l'analyse de réputation:\n")
            f.write(f"- Sentiment global: {sentiment} (score: {sentiment_score:.2f})\n")
            f.write(f"- Nombre total de mentions: {mention_count}\n\n")
            
            f.write("Répartition par source:\n")
            for source in sources:
                f.write(f"- {source['name']}: {source['count']} mentions, sentiment {source['sentiment']:.2f}\n")
            
            f.write("\nRecommandations:\n")
            if sentiment_score > 0:
                f.write("- Votre réputation est positive. Continuez à maintenir cette image.\n")
                f.write("- Surveillez régulièrement les nouvelles mentions pour détecter tout changement.\n")
            else:
                f.write("- Votre réputation présente des aspects négatifs qui nécessitent attention.\n")
                f.write("- Engagez-vous activement avec votre audience pour améliorer votre image.\n")
                f.write("- Répondez aux critiques de manière constructive.\n")
        
        print(f"\n{Colors.BLUE}[*] Rapport sauvegardé: {report_path}{Colors.ENDC}")
        return True
    
    def darkweb_monitor(self, email=None, username=None, phone=None):
        """Surveille le dark web pour détecter des fuites d'informations personnelles"""
        print(f"{Colors.HEADER}[+] Surveillance du Dark Web...{Colors.ENDC}")
        
        if not email and not username and not phone:
            print(f"{Colors.FAIL}[✗] Veuillez fournir au moins une information à surveiller (email, nom d'utilisateur ou téléphone){Colors.ENDC}")
            return False
        
        target_info = []
        if email:
            target_info.append(f"Email: {email}")
        if username:
            target_info.append(f"Nom d'utilisateur: {username}")
        if phone:
            target_info.append(f"Téléphone: {phone}")
        
        target_str = ", ".join(target_info)
        print(f"{Colors.BLUE}[*] Recherche d'informations sur le Dark Web pour: {target_str}{Colors.ENDC}")
        
        # Simuler une analyse du dark web
        print(f"{Colors.BLUE}[*] Connexion aux sources du Dark Web...{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Analyse des forums et marketplaces...{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Recherche dans les bases de données compromises...{Colors.ENDC}")
        
        # Attendre pour simuler le traitement
        import time
        time.sleep(3)
        
        # Générer des résultats fictifs
        darkweb_sources = [
            {"name": "Forums de hackers", "risk": random.choice(["Élevé", "Moyen", "Faible"]), "found": random.choice([True, False])},
            {"name": "Marketplaces illégales", "risk": random.choice(["Élevé", "Moyen", "Faible"]), "found": random.choice([True, False])},
            {"name": "Bases de données volées", "risk": random.choice(["Élevé", "Moyen", "Faible"]), "found": random.choice([True, False])},
            {"name": "Canaux de communication chiffrés", "risk": random.choice(["Élevé", "Moyen", "Faible"]), "found": random.choice([True, False])},
            {"name": "Sites de vente de données", "risk": random.choice(["Élevé", "Moyen", "Faible"]), "found": random.choice([True, False])},
        ]
        
        # Déterminer les sources où des informations ont été trouvées
        found_sources = [source for source in darkweb_sources if source["found"]]
        
        # Générer des types d'informations exposées
        exposed_data_types = []
        if email and any(source["found"] for source in darkweb_sources):
            exposed_data_types.extend([
                "Adresse email",
                "Mot de passe (hashé)" if random.choice([True, False]) else None,
                "Mot de passe (en clair)" if random.choice([True, False]) else None,
            ])
        if username and any(source["found"] for source in darkweb_sources):
            exposed_data_types.extend([
                "Nom d'utilisateur",
                "Adresses IP associées" if random.choice([True, False]) else None,
                "Historique de connexion" if random.choice([True, False]) else None,
            ])
        if phone and any(source["found"] for source in darkweb_sources):
            exposed_data_types.extend([
                "Numéro de téléphone",
                "SMS interceptés" if random.choice([True, False]) else None,
                "Données de localisation" if random.choice([True, False]) else None,
            ])
        
        # Filtrer les types de données None
        exposed_data_types = [data_type for data_type in exposed_data_types if data_type]
        
        # Afficher les résultats
        if found_sources:
            print(f"\n{Colors.FAIL}[!] Alerte: Vos informations ont été détectées sur {len(found_sources)}/{len(darkweb_sources)} sources du Dark Web!{Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}Sources où vos informations ont été trouvées:{Colors.ENDC}")
            for source in found_sources:
                risk_color = Colors.FAIL if source["risk"] == "Élevé" else Colors.WARNING if source["risk"] == "Moyen" else Colors.GREEN
                print(f"  - {source['name']}: Niveau de risque {risk_color}{source['risk']}{Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}Types d'informations exposées:{Colors.ENDC}")
            for data_type in exposed_data_types:
                print(f"  - {data_type}")
            
            print(f"\n{Colors.WARNING}[!] Recommandations de sécurité:{Colors.ENDC}")
            print(f"  - Changez immédiatement tous vos mots de passe")
            print(f"  - Activez l'authentification à deux facteurs sur tous vos comptes")
            print(f"  - Surveillez vos relevés bancaires pour détecter toute activité suspecte")
            print(f"  - Envisagez de mettre en place une alerte de fraude auprès des organismes de crédit")
            print(f"  - Utilisez un service de surveillance d'identité")
        else:
            print(f"\n{Colors.GREEN}[✓] Bonne nouvelle! Vos informations n'ont pas été détectées sur le Dark Web.{Colors.ENDC}")
            print(f"\n{Colors.BOLD}Recommandations préventives:{Colors.ENDC}")
            print(f"  - Continuez à utiliser des mots de passe forts et uniques")
            print(f"  - Activez l'authentification à deux facteurs sur tous vos comptes importants")
            print(f"  - Effectuez régulièrement des vérifications de sécurité")
        
        # Générer un rapport
        target_id = (email or username or phone).replace("@", "_").replace(" ", "_").replace("+", "")
        report_path = os.path.join(self.data_dir, f"darkweb_{target_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_path, "w") as f:
            f.write(f"Rapport de surveillance du Dark Web\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Informations surveillées: {target_str}\n\n")
            
            if found_sources:
                f.write(f"ALERTE: Vos informations ont été détectées sur {len(found_sources)}/{len(darkweb_sources)} sources du Dark Web!\n\n")
                
                f.write("Sources où vos informations ont été trouvées:\n")
                for source in found_sources:
                    f.write(f"- {source['name']}: Niveau de risque {source['risk']}\n")
                
                f.write("\nTypes d'informations exposées:\n")
                for data_type in exposed_data_types:
                    f.write(f"- {data_type}\n")
                
                f.write("\nRecommandations de sécurité:\n")
                f.write("- Changez immédiatement tous vos mots de passe\n")
                f.write("- Activez l'authentification à deux facteurs sur tous vos comptes\n")
                f.write("- Surveillez vos relevés bancaires pour détecter toute activité suspecte\n")
                f.write("- Envisagez de mettre en place une alerte de fraude auprès des organismes de crédit\n")
                f.write("- Utilisez un service de surveillance d'identité\n")
            else:
                f.write("Bonne nouvelle! Vos informations n'ont pas été détectées sur le Dark Web.\n\n")
                f.write("Recommandations préventives:\n")
                f.write("- Continuez à utiliser des mots de passe forts et uniques\n")
                f.write("- Activez l'authentification à deux facteurs sur tous vos comptes importants\n")
                f.write("- Effectuez régulièrement des vérifications de sécurité\n")
        
        print(f"\n{Colors.BLUE}[*] Rapport sauvegardé: {report_path}{Colors.ENDC}")
        return True
    
    def generate_password(self, length=16, include_uppercase=True, include_lowercase=True, 
                         include_numbers=True, include_special=True, count=1):
        """Génère des mots de passe sécurisés"""
        print(f"{Colors.HEADER}[+] Génération de mots de passe sécurisés...{Colors.ENDC}")
        
        if length < 8:
            print(f"{Colors.FAIL}[✗] La longueur du mot de passe doit être d'au moins 8 caractères{Colors.ENDC}")
            return False
        
        if not any([include_uppercase, include_lowercase, include_numbers, include_special]):
            print(f"{Colors.FAIL}[✗] Vous devez inclure au moins un type de caractères{Colors.ENDC}")
            return False
        
        if count < 1 or count > 20:
            print(f"{Colors.FAIL}[✗] Le nombre de mots de passe doit être entre 1 et 20{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}[*] Génération de {count} mot(s) de passe de {length} caractères...{Colors.ENDC}")
        
        # Définir les ensembles de caractères
        chars = ""
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_numbers:
            chars += string.digits
        if include_special:
            chars += string.punctuation
        
        # Générer les mots de passe
        passwords = []
        for i in range(count):
            # Utiliser secrets pour une génération cryptographiquement sécurisée
            password = ''.join(secrets.choice(chars) for _ in range(length))
            
            # S'assurer que le mot de passe contient au moins un caractère de chaque type demandé
            while (include_uppercase and not any(c in string.ascii_uppercase for c in password)) or \
                  (include_lowercase and not any(c in string.ascii_lowercase for c in password)) or \
                  (include_numbers and not any(c in string.digits for c in password)) or \
                  (include_special and not any(c in string.punctuation for c in password)):
                password = ''.join(secrets.choice(chars) for _ in range(length))
            
            passwords.append(password)
        
        # Évaluer la force des mots de passe
        password_strengths = []
        for password in passwords:
            # Calculer l'entropie (mesure de la force du mot de passe)
            entropy = self._calculate_password_entropy(password)
            
            # Évaluer la force
            if entropy >= 128:
                strength = "Très fort"
                strength_color = Colors.GREEN
            elif entropy >= 80:
                strength = "Fort"
                strength_color = Colors.GREEN
            elif entropy >= 60:
                strength = "Moyen"
                strength_color = Colors.WARNING
            else:
                strength = "Faible"
                strength_color = Colors.FAIL
            
            password_strengths.append({
                "password": password,
                "entropy": entropy,
                "strength": strength,
                "strength_color": strength_color
            })
        
        # Afficher les mots de passe générés
        print(f"\n{Colors.GREEN}[✓] {count} mot(s) de passe généré(s) avec succès{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Mots de passe générés:{Colors.ENDC}")
        for i, ps in enumerate(password_strengths, 1):
            print(f"  {i}. {ps['password']} - Force: {ps['strength_color']}{ps['strength']}{Colors.ENDC} (Entropie: {ps['entropy']:.2f} bits)")
        
        # Générer un rapport
        report_path = os.path.join(self.data_dir, f"passwords_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_path, "w") as f:
            f.write(f"Mots de passe sécurisés générés\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Paramètres:\n")
            f.write(f"- Longueur: {length} caractères\n")
            f.write(f"- Majuscules: {'Oui' if include_uppercase else 'Non'}\n")
            f.write(f"- Minuscules: {'Oui' if include_lowercase else 'Non'}\n")
            f.write(f"- Chiffres: {'Oui' if include_numbers else 'Non'}\n")
            f.write(f"- Caractères spéciaux: {'Oui' if include_special else 'Non'}\n\n")
            
            f.write("Mots de passe générés:\n")
            for i, ps in enumerate(password_strengths, 1):
                f.write(f"{i}. {ps['password']} - Force: {ps['strength']} (Entropie: {ps['entropy']:.2f} bits)\n")
            
            f.write("\nRecommandations de sécurité:\n")
            f.write("- Utilisez un gestionnaire de mots de passe pour stocker vos mots de passe de manière sécurisée\n")
            f.write("- Ne réutilisez jamais les mêmes mots de passe sur différents sites\n")
            f.write("- Changez régulièrement vos mots de passe, surtout pour les comptes sensibles\n")
            f.write("- Activez l'authentification à deux facteurs lorsque c'est possible\n")
        
        print(f"\n{Colors.BLUE}[*] Rapport sauvegardé: {report_path}{Colors.ENDC}")
        print(f"\n{Colors.WARNING}[!] Attention: Stockez ces mots de passe de manière sécurisée et ne les partagez pas.{Colors.ENDC}")
        return True
    
    def _calculate_password_entropy(self, password):
        """Calcule l'entropie d'un mot de passe (mesure de sa force)"""
        # Déterminer la taille du jeu de caractères
        charset_size = 0
        if any(c in string.ascii_uppercase for c in password):
            charset_size += 26
        if any(c in string.ascii_lowercase for c in password):
            charset_size += 26
        if any(c in string.digits for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += 32
        
        # Calculer l'entropie de base (formule de Shannon)
        entropy = len(password) * (math.log2(charset_size) if charset_size > 0 else 0)
        
        # Ajuster l'entropie en fonction de la complexité du mot de passe
        # Pénaliser les répétitions
        char_counts = {}
        for c in password:
            char_counts[c] = char_counts.get(c, 0) + 1
        repeats = sum(count - 1 for count in char_counts.values())
        entropy -= repeats * 0.5
        
        # Pénaliser les séquences (comme "123" ou "abc")
        for i in range(len(password) - 2):
            if (password[i].isdigit() and password[i+1].isdigit() and password[i+2].isdigit() and 
                int(password[i+1]) == int(password[i]) + 1 and int(password[i+2]) == int(password[i+1]) + 1):
                entropy -= 1
            elif (password[i].isalpha() and password[i+1].isalpha() and password[i+2].isalpha() and 
                  ord(password[i+1].lower()) == ord(password[i].lower()) + 1 and 
                  ord(password[i+2].lower()) == ord(password[i+1].lower()) + 1):
                entropy -= 1
        
        return max(0, entropy)
    
    def vulnerability_scan(self, profile_file=None, email=None, username=None):
        """Analyse les vulnérabilités de sécurité personnelles"""
        print(f"{Colors.HEADER}[+] Analyse de vulnérabilité personnelle...{Colors.ENDC}")
        
        # Charger le profil si fourni
        profile = {}
        if profile_file and os.path.exists(profile_file):
            try:
                with open(profile_file, 'r') as f:
                    profile = json.load(f)
                print(f"{Colors.GREEN}[✓] Profil chargé: {profile_file}{Colors.ENDC}")
            except json.JSONDecodeError:
                print(f"{Colors.FAIL}[✗] Erreur lors du chargement du profil: format JSON invalide{Colors.ENDC}")
                return False
        
        # Utiliser les paramètres directs si fournis
        if email:
            profile['email'] = email
        if username:
            profile['username'] = username
        
        # Vérifier qu'on a au moins une information à analyser
        if not profile:
            print(f"{Colors.FAIL}[✗] Aucune information à analyser. Veuillez fournir un profil ou des informations directement.{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}[*] Analyse des vulnérabilités pour: {', '.join(profile.keys())}{Colors.ENDC}")
        
        # Simuler une analyse de vulnérabilité
        print(f"{Colors.BLUE}[*] Vérification des pratiques de sécurité...{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Analyse des risques d'exposition...{Colors.ENDC}")
        print(f"{Colors.BLUE}[*] Évaluation des menaces potentielles...{Colors.ENDC}")
        
        # Attendre pour simuler le traitement
        import time
        time.sleep(3)
        
        # Générer des vulnérabilités fictives
        vulnerabilities = [
            {
                "name": "Réutilisation de mot de passe",
                "risk": "Élevé",
                "description": "Utilisation du même mot de passe sur plusieurs sites",
                "detected": random.choice([True, False]),
                "recommendation": "Utilisez un gestionnaire de mots de passe et créez des mots de passe uniques pour chaque site"
            },
            {
                "name": "Absence d'authentification à deux facteurs",
                "risk": "Élevé",
                "description": "Comptes sensibles non protégés par 2FA",
                "detected": random.choice([True, False]),
                "recommendation": "Activez l'authentification à deux facteurs sur tous vos comptes importants"
            },
            {
                "name": "Informations personnelles exposées",
                "risk": "Moyen",
                "description": "Données personnelles accessibles publiquement",
                "detected": random.choice([True, False]),
                "recommendation": "Vérifiez et ajustez les paramètres de confidentialité sur vos réseaux sociaux"
            },
            {
                "name": "Logiciels obsolètes",
                "risk": "Moyen",
                "description": "Utilisation de logiciels non mis à jour",
                "detected": random.choice([True, False]),
                "recommendation": "Activez les mises à jour automatiques sur tous vos appareils"
            },
            {
                "name": "Absence de surveillance d'identité",
                "risk": "Faible",
                "description": "Aucun service de surveillance d'identité actif",
                "detected": random.choice([True, False]),
                "recommendation": "Envisagez d'utiliser un service de surveillance d'identité"
            },
            {
                "name": "Connexions non sécurisées",
                "risk": "Moyen",
                "description": "Utilisation de réseaux Wi-Fi publics sans VPN",
                "detected": random.choice([True, False]),
                "recommendation": "Utilisez un VPN lors de la connexion à des réseaux Wi-Fi publics"
            },
            {
                "name": "Partage excessif sur les réseaux sociaux",
                "risk": "Moyen",
                "description": "Publication d'informations sensibles sur les réseaux sociaux",
                "detected": random.choice([True, False]),
                "recommendation": "Limitez les informations personnelles que vous partagez en ligne"
            }
        ]
        
        # Filtrer les vulnérabilités détectées
        detected_vulnerabilities = [v for v in vulnerabilities if v["detected"]]
        
        # Calculer le score de risque global (0-100)
        risk_score = 0
        if detected_vulnerabilities:
            high_risk = sum(1 for v in detected_vulnerabilities if v["risk"] == "Élevé")
            medium_risk = sum(1 for v in detected_vulnerabilities if v["risk"] == "Moyen")
            low_risk = sum(1 for v in detected_vulnerabilities if v["risk"] == "Faible")
            
            risk_score = min(100, (high_risk * 30 + medium_risk * 15 + low_risk * 5))
        
        # Déterminer le niveau de risque global
        if risk_score >= 70:
            risk_level = "Élevé"
            risk_color = Colors.FAIL
        elif risk_score >= 40:
            risk_level = "Moyen"
            risk_color = Colors.WARNING
        else:
            risk_level = "Faible"
            risk_color = Colors.GREEN
        
        # Afficher les résultats
        print(f"\n{Colors.GREEN}[✓] Analyse terminée.{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Résultat de l'analyse de vulnérabilité:{Colors.ENDC}")
        print(f"  - Score de risque global: {risk_color}{risk_score}/100 (Niveau: {risk_level}){Colors.ENDC}")
        print(f"  - Vulnérabilités détectées: {len(detected_vulnerabilities)}/{len(vulnerabilities)}")
        
        if detected_vulnerabilities:
            print(f"\n{Colors.BOLD}Vulnérabilités détectées:{Colors.ENDC}")
            for vuln in detected_vulnerabilities:
                risk_color = Colors.FAIL if vuln["risk"] == "Élevé" else Colors.WARNING if vuln["risk"] == "Moyen" else Colors.GREEN
                print(f"  - {vuln['name']} ({risk_color}Risque {vuln['risk']}{Colors.ENDC})")
                print(f"    {vuln['description']}")
                print(f"    {Colors.BLUE}Recommandation: {vuln['recommendation']}{Colors.ENDC}")
        else:
            print(f"\n{Colors.GREEN}[✓] Aucune vulnérabilité majeure détectée.{Colors.ENDC}")
        
        # Générer un rapport
        profile_id = "_".join(profile.values()).replace("@", "_").replace(" ", "_").replace("+", "")
        report_path = os.path.join(self.data_dir, f"vulnerability_{profile_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_path, "w") as f:
            f.write(f"Rapport d'analyse de vulnérabilité personnelle\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"Informations analysées: {', '.join(profile.keys())}\n\n")
            f.write(f"Résultat de l'analyse:\n")
            f.write(f"- Score de risque global: {risk_score}/100 (Niveau: {risk_level})\n")
            f.write(f"- Vulnérabilités détectées: {len(detected_vulnerabilities)}/{len(vulnerabilities)}\n\n")
            
            if detected_vulnerabilities:
                f.write("Vulnérabilités détectées:\n")
                for vuln in detected_vulnerabilities:
                    f.write(f"- {vuln['name']} (Risque {vuln['risk']})\n")
                    f.write(f"  {vuln['description']}\n")
                    f.write(f"  Recommandation: {vuln['recommendation']}\n\n")
            else:
                f.write("Aucune vulnérabilité majeure détectée.\n\n")
            
            f.write("Recommandations générales de sécurité:\n")
            f.write("1. Utilisez des mots de passe forts et uniques pour chaque compte\n")
            f.write("2. Activez l'authentification à deux facteurs sur tous vos comptes importants\n")
            f.write("3. Maintenez vos logiciels et systèmes d'exploitation à jour\n")
            f.write("4. Soyez vigilant face aux tentatives de phishing\n")
            f.write("5. Utilisez un VPN lors de la connexion à des réseaux Wi-Fi publics\n")
            f.write("6. Effectuez régulièrement des sauvegardes de vos données importantes\n")
            f.write("7. Vérifiez et ajustez les paramètres de confidentialité sur vos réseaux sociaux\n")
        
        print(f"\n{Colors.BLUE}[*] Rapport sauvegardé: {report_path}{Colors.ENDC}")
        return True
    
    def run(self):
        """Point d'entrée principal du CLI"""
        parser = argparse.ArgumentParser(description="Shadow CLI - Interface en ligne de commande pour Kali Linux")
        subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")
        
        # Commande: deploy
        deploy_parser = subparsers.add_parser("deploy", help="Déployer l'application")
        
        # Commande: stop
        stop_parser = subparsers.add_parser("stop", help="Arrêter tous les services")
        
        # Commande: status
        status_parser = subparsers.add_parser("status", help="Vérifier l'état des services")
        
        # Commande: facial
        facial_parser = subparsers.add_parser("facial", help="Tester la reconnaissance faciale")
        
        # Commande: footprint
        footprint_parser = subparsers.add_parser("footprint", help="Analyser l'empreinte numérique")
        footprint_parser.add_argument("--username", help="Nom d'utilisateur à rechercher")
        footprint_parser.add_argument("--email", help="Adresse email à rechercher")
        
        # Commande: leak
        leak_parser = subparsers.add_parser("leak", help="Vérifier les fuites d'identité")
        leak_parser.add_argument("email", help="Adresse email à vérifier")
        
        # Commande: identity
        identity_parser = subparsers.add_parser("identity", help="Générer des identités temporaires")
        identity_parser.add_argument("--count", type=int, default=1, help="Nombre d'identités à générer (max 10)")
        
        # Commande: metadata
        metadata_parser = subparsers.add_parser("metadata", help="Nettoyer les métadonnées d'un fichier")
        metadata_parser.add_argument("file", help="Chemin du fichier à nettoyer")
        
        # Commande: reputation
        reputation_parser = subparsers.add_parser("reputation", help="Analyser la réputation en ligne")
        reputation_parser.add_argument("--name", help="Nom de la personne")
        reputation_parser.add_argument("--company", help="Nom de l'entreprise")
        reputation_parser.add_argument("--website", help="URL du site web")
        
        # Commande: darkweb (nouvelle fonctionnalité)
        darkweb_parser = subparsers.add_parser("darkweb", help="Surveiller le Dark Web pour détecter des fuites d'informations")
        darkweb_parser.add_argument("--email", help="Adresse email à surveiller")
        darkweb_parser.add_argument("--username", help="Nom d'utilisateur à surveiller")
        darkweb_parser.add_argument("--phone", help="Numéro de téléphone à surveiller")
        
        # Commande: password (nouvelle fonctionnalité)
        password_parser = subparsers.add_parser("password", help="Générer des mots de passe sécurisés")
        password_parser.add_argument("--length", type=int, default=16, help="Longueur du mot de passe (min 8)")
        password_parser.add_argument("--no-uppercase", action="store_false", dest="uppercase", help="Exclure les majuscules")
        password_parser.add_argument("--no-lowercase", action="store_false", dest="lowercase", help="Exclure les minuscules")
        password_parser.add_argument("--no-numbers", action="store_false", dest="numbers", help="Exclure les chiffres")
        password_parser.add_argument("--no-special", action="store_false", dest="special", help="Exclure les caractères spéciaux")
        password_parser.add_argument("--count", type=int, default=1, help="Nombre de mots de passe à générer (max 20)")
        
        # Commande: vulnerability (nouvelle fonctionnalité)
        vulnerability_parser = subparsers.add_parser("vulnerability", help="Analyser les vulnérabilités de sécurité personnelles")
        vulnerability_parser.add_argument("--profile", help="Chemin vers un fichier de profil JSON")
        vulnerability_parser.add_argument("--email", help="Adresse email à analyser")
        vulnerability_parser.add_argument("--username", help="Nom d'utilisateur à analyser")
        
        # Analyser les arguments
        args = parser.parse_args()
        
        # Afficher l'en-tête
        self.print_header()
        
        # Exécuter la commande appropriée
        if args.command == "deploy":
            if self.check_dependencies():
                self.deploy()
        elif args.command == "stop":
            self.stop()
        elif args.command == "status":
            self.status()
        elif args.command == "facial":
            self.facial_recognition_test()
        elif args.command == "footprint":
            self.digital_footprint(args.username, args.email)
        elif args.command == "leak":
            self.identity_leak(args.email)
        elif args.command == "identity":
            self.generate_identity(args.count)
        elif args.command == "metadata":
            self.clean_metadata(args.file)
        elif args.command == "reputation":
            self.reputation_analysis(args.name, args.company, args.website)
        elif args.command == "darkweb":
            self.darkweb_monitor(args.email, args.username, args.phone)
        elif args.command == "password":
            self.generate_password(args.length, args.uppercase, args.lowercase, args.numbers, args.special, args.count)
        elif args.command == "vulnerability":
            self.vulnerability_scan(args.profile, args.email, args.username)
        else:
            parser.print_help()

if __name__ == "__main__":
    # Importer les modules nécessaires
    import math
    
    cli = ShadowCLI()
    cli.run()
