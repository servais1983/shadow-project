from fastapi import APIRouter, HTTPException
from typing import Dict

router = APIRouter()

@router.post("/dmca", response_model=Dict[str, str])
def create_dmca_notice(domain: str, reason: str, contact: str):
    """
    Génère une lettre DMCA pour demander la suppression de contenu
    """
    from src.legal.dmca import generate_dmca
    
    dmca_text = generate_dmca(domain, reason, contact)
    
    return {
        "status": "created",
        "dmca_text": dmca_text
    }

@router.post("/takedown/{platform}")
def request_takedown(platform: str, url: str, reason: str):
    """
    Envoie automatiquement une demande de suppression à une plateforme
    """
    platforms = {
        "twitter": "Twitter API",
        "facebook": "Facebook API",
        "instagram": "Instagram API",
        "youtube": "YouTube API"
    }
    
    if platform not in platforms:
        raise HTTPException(status_code=400, detail="Plateforme non supportée")
    
    # Logique pour envoyer la demande via l'API appropriée
    
    return {
        "status": "requested",
        "platform": platform,
        "url": url,
        "message": f"Demande envoyée via {platforms[platform]}"
    }

@router.get("/status/{request_id}")
def check_takedown_status(request_id: str):
    """
    Vérifie le statut d'une demande de suppression
    """
    # Simulation de réponse
    return {
        "request_id": request_id,
        "status": "pending",
        "updated_at": "2025-05-16T10:30:00Z"
    }
