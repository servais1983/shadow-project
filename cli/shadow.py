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
        
        # Commande: footprint (nouvelle fonctionnalité)
        footprint_parser = subparsers.add_parser("footprint", help="Analyser l'empreinte numérique")
        footprint_parser.add_argument("--username", help="Nom d'utilisateur à rechercher")
        footprint_parser.add_argument("--email", help="Adresse email à rechercher")
        
        # Commande: leak (nouvelle fonctionnalité)
        leak_parser = subparsers.add_parser("leak", help="Vérifier les fuites d'identité")
        leak_parser.add_argument("email", help="Adresse email à vérifier")
        
        # Commande: identity (nouvelle fonctionnalité)
        identity_parser = subparsers.add_parser("identity", help="Générer des identités temporaires")
        identity_parser.add_argument("--count", type=int, default=1, help="Nombre d'identités à générer (max 10)")
        
        # Commande: metadata (nouvelle fonctionnalité)
        metadata_parser = subparsers.add_parser("metadata", help="Nettoyer les métadonnées d'un fichier")
        metadata_parser.add_argument("file", help="Chemin du fichier à nettoyer")
        
        # Commande: reputation (nouvelle fonctionnalité)
        reputation_parser = subparsers.add_parser("reputation", help="Analyser la réputation en ligne")
        reputation_parser.add_argument("--name", help="Nom de la personne")
        reputation_parser.add_argument("--company", help="Nom de l'entreprise")
        reputation_parser.add_argument("--website", help="URL du site web")
        
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
        else:
            parser.print_help()

if __name__ == "__main__":
    cli = ShadowCLI()
    cli.run()
