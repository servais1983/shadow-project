import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def search_twitter(keyword, max_results=10):
    """
    Recherche des tweets contenant le keyword spécifié
    """
    twitter_bearer = os.getenv("TWITTER_BEARER", "YOUR_TWITTER_BEARER")
    
    headers = {"Authorization": f"Bearer {twitter_bearer}"}
    params = {
        "q": keyword, 
        "result_type": "recent", 
        "count": max_results
    }
    
    try:
        r = requests.get(
            "https://api.twitter.com/1.1/search/tweets.json", 
            headers=headers, 
            params=params
        )
        r.raise_for_status()  # Vérifie si la requête a réussi
        
        return r.json().get("statuses", [])
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la recherche Twitter: {str(e)}")
        return []

def check_for_personal_content(username, keywords=None, image_urls=None):
    """
    Surveille le compte Twitter d'un utilisateur pour du contenu personnel
    """
    # Si aucun mot-clé n'est fourni, utiliser une liste par défaut
    if keywords is None:
        keywords = []
    
    # Si aucune URL d'image n'est fournie, utiliser une liste vide
    if image_urls is None:
        image_urls = []
    
    # Récupérer les tweets récents de l'utilisateur
    user_tweets = search_twitter(f"from:{username}")
    
    findings = []
    
    # Vérifier si les tweets contiennent des mots-clés sensibles
    for tweet in user_tweets:
        tweet_text = tweet.get("text", "").lower()
        
        for keyword in keywords:
            if keyword.lower() in tweet_text:
                findings.append({
                    "type": "keyword_match",
                    "platform": "Twitter",
                    "content": tweet_text,
                    "url": f"https://twitter.com/{username}/status/{tweet['id_str']}",
                    "keyword": keyword
                })
    
    # Note: La vérification des images nécessiterait un traitement supplémentaire
    # avec l'API Twitter et l'analyse d'images
    
    return findings
