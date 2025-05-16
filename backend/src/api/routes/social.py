from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from datetime import datetime

router = APIRouter()

# Données simulées pour les alertes
sample_alerts = [
    {
        "id": 1, 
        "message": "Votre photo a été détectée sur Twitter", 
        "platform": "Twitter", 
        "url": "https://twitter.com/example/status/123456", 
        "timestamp": datetime.now().isoformat()
    },
    {
        "id": 2, 
        "message": "Mention de votre nom sur un forum", 
        "platform": "Forum XYZ", 
        "url": "https://forum.xyz/thread/789", 
        "timestamp": datetime.now().isoformat()
    }
]

@router.get("/alerts", response_model=List[Dict[str, Any]])
def get_alerts():
    """
    Récupère toutes les alertes de sécurité détectées pour l'utilisateur
    """
    return sample_alerts

@router.get("/scan/{platform}")
def scan_platform(platform: str):
    """
    Lance une analyse sur une plateforme spécifique
    """
    if platform not in ["twitter", "instagram", "facebook", "forums"]:
        raise HTTPException(status_code=400, detail="Plateforme non supportée")
    
    return {"status": "scanning", "platform": platform}

@router.post("/upload")
def upload_protected_content():
    """
    Upload de contenu à protéger (photos, textes, etc.)
    """
    return {"status": "uploaded", "message": "Contenu ajouté à la surveillance"}
