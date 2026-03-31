"""Configuration de l'application"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Configuration globale de l'application"""
    
    # Application
    app_name: str = "NetShield - Wi-Fi Security Audit Lab"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False") == "True"
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Backend
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000
    
    # Security - Mode simulation
    simulation_mode: bool = True  # Toujours en mode simulation pour la sécurité
    require_confirmation: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    # PDF Report
    company_name: str = "NetShield Labs"
    pdf_temp_dir: str = "./temp_reports"
    
    # Legal Notice
    legal_notice: str = """
    ⚠️ AVERTISSEMENT LÉGAL ET ÉTHIQUE
    
    Cet outil est destiné UNIQUEMENT à :
    - Des fins éducatives
    - Des tests de sécurité autorisés (pentest avec consentement écrit)
    - Un environnement contrôlé (laboratoire, sandboxe)
    
    Utilisation INTERDITE :
    - Tout accès non autorisé à des réseaux Wi-Fi
    - Tout test sur des réseaux tiers sans consentement explicite
    - Toute activité violant les lois locales/nationales
    
    L'utilisateur assume l'entière responsabilité légale de l'utilisation de cet outil.
    NetShield Labs décline toute responsabilité pour les usages malveillants.
    """
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Récupère la configuration (cached)"""
    return Settings()
