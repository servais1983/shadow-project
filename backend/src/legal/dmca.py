def generate_dmca(domain, reason, contact):
    """
    Génère une lettre DMCA pour demander la suppression de contenu
    
    Args:
        domain (str): Nom de domaine ou plateforme concernée
        reason (str): Motif de la demande DMCA
        contact (str): Informations de contact du demandeur
        
    Returns:
        str: Texte formaté de la demande DMCA
    """
    
    current_date = "16 mai 2025"  # À remplacer par la date actuelle du système dans une version réelle
    
    dmca_template = f"""
    À l'attention de : Hébergeur/Propriétaire de {domain}
    Objet : Notification de retrait DMCA
    Date : {current_date}
    
    Bonjour,
    
    Je vous contacte conformément au Digital Millennium Copyright Act (DMCA).
    
    J'ai constaté que du contenu protégé par des droits d'auteur/droits à l'image est publié sur votre site sans mon autorisation.
    
    Motif de la demande : {reason}
    
    Je déclare sous peine de parjure que :
    
    1. Je suis le propriétaire exclusif des droits, ou autorisé à agir au nom du propriétaire des droits.
    2. Le contenu mentionné ci-dessus n'est pas autorisé par le titulaire des droits, son agent ou la loi.
    
    Je vous demande donc de retirer immédiatement ce contenu de votre site, conformément à la section 512(c) du DMCA.
    
    Mes coordonnées :
    {contact}
    
    Je vous remercie de votre coopération.
    
    Cordialement,
    Shadow (pour le compte de l'utilisateur)
    """
    
    return dmca_template.strip()

def generate_gdpr_request(platform, personal_data_types, user_details):
    """
    Génère une demande de suppression basée sur le RGPD (Europe)
    
    Args:
        platform (str): Nom de la plateforme
        personal_data_types (list): Types de données personnelles concernées
        user_details (dict): Détails de l'utilisateur faisant la demande
        
    Returns:
        str: Texte formaté de la demande RGPD
    """
    data_types_text = ", ".join(personal_data_types)
    
    gdpr_template = f"""
    À l'attention du Délégué à la Protection des Données de {platform}
    Objet : Demande de suppression de données personnelles (RGPD)
    
    Bonjour,
    
    Conformément à l'article 17 du Règlement Général sur la Protection des Données (RGPD), je souhaite exercer mon droit à l'effacement.
    
    Je demande la suppression complète des données personnelles suivantes me concernant :
    {data_types_text}
    
    Informations me concernant :
    Nom : {user_details.get('name', 'Non fourni')}
    Email : {user_details.get('email', 'Non fourni')}
    Identifiant utilisateur : {user_details.get('user_id', 'Non fourni')}
    
    Conformément au RGPD, vous disposez d'un délai d'un mois pour répondre à cette demande.
    
    Je vous remercie de votre attention.
    
    Cordialement,
    {user_details.get('name', 'L\'utilisateur')}
    """
    
    return gdpr_template.strip()
