"""Configuration de l'application."""
import json
from functools import lru_cache
from typing import Any, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration globale de l'application"""
    
    # Application
    app_name: str = "NetShield - Wi-Fi Security Audit Lab"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, alias="DEBUG")
    
    # CORS
    cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:5173"],
        alias="CORS_ORIGINS",
    )
    
    # Backend
    backend_host: str = Field(default="127.0.0.1", alias="BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")
    
    # Security - Mode simulation
    simulation_mode: bool = Field(default=True, alias="SIMULATION_MODE")
    require_confirmation: bool = Field(default=True, alias="REQUIRE_CONFIRMATION")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # PDF Report
    company_name: str = Field(default="NetShield Labs", alias="COMPANY_NAME")
    pdf_temp_dir: str = Field(default="./temp_reports", alias="PDF_TEMP_DIR")
    
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
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> List[str]:
        """Accepte JSON array ou CSV pour CORS_ORIGINS."""
        if isinstance(value, list):
            return value

        if isinstance(value, str):
            raw = value.strip()
            if not raw:
                return []

            if raw.startswith("["):
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except json.JSONDecodeError:
                    pass

            return [origin.strip() for origin in raw.split(",") if origin.strip()]

        return ["http://localhost:3000", "http://localhost:5173"]


@lru_cache()
def get_settings() -> Settings:
    """Récupère la configuration (cached)"""
    return Settings()
