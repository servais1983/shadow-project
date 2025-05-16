from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de connexion à la base de données depuis les variables d'environnement
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/shadow")

# Créer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer la classe de base pour les modèles
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modèle pour les utilisateurs
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    protected_content = relationship("ProtectedContent", back_populates="owner")
    alerts = relationship("Alert", back_populates="user")

# Modèle pour le contenu protégé
class ProtectedContent(Base):
    __tablename__ = "protected_content"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_type = Column(String)  # 'image', 'text', etc.
    content_path = Column(String)  # Chemin vers le contenu stocké
    description = Column(String, nullable=True)
    hash_value = Column(String)  # Hash du contenu pour l'identification rapide
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    owner = relationship("User", back_populates="protected_content")
    alerts = relationship("Alert", back_populates="content")

# Modèle pour les alertes
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("protected_content.id"), nullable=True)
    platform = Column(String)  # 'twitter', 'instagram', etc.
    url = Column(String)  # URL où le contenu a été trouvé
    message = Column(String)
    severity = Column(Integer)  # 1: faible, 2: moyen, 3: élevé
    status = Column(String)  # 'new', 'processing', 'resolved'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="alerts")
    content = relationship("ProtectedContent", back_populates="alerts")

# Modèle pour les demandes DMCA
class DMCARequest(Base):
    __tablename__ = "dmca_requests"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=True)
    platform = Column(String)
    status = Column(String)  # 'sent', 'pending', 'accepted', 'rejected'
    dmca_text = Column(Text)
    response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Fonction pour créer toutes les tables dans la base de données
def init_db():
    Base.metadata.create_all(bind=engine)
