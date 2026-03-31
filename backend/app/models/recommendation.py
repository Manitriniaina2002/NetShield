"""Modèles pour les recommandations"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class PriorityLevel(str, Enum):
    """Niveau de priorité des recommandations"""
    CRITICAL = "Critique - Appliquer immédiatement"
    HIGH = "Élevée - Appliquer dans les 48h"
    MEDIUM = "Moyen - Appliquer dans la semaine"
    LOW = "Faible - À considérer"


class Recommendation(BaseModel):
    """Modèle d'une recommandation de sécurité"""
    
    id: Optional[str] = Field(default_factory=lambda: None)
    title: str = Field(..., description="Titre de la recommandation")
    description: str = Field(..., description="Description détaillée")
    action_steps: list[str] = Field(..., description="Étapes actionables")
    priority: PriorityLevel = Field(..., description="Priorité")
    category: str = Field(..., description="Catégorie (Authentification/Chiffrement/Configuration/etc)")
    affected_vulnerability: Optional[str] = Field(None, description="Type de vulnérabilité corrigée")
    estimated_effort: str = Field(..., description="Effort estimé (Faible/Moyen/Élevé)")
    tools_required: list[str] = Field(default_factory=list, description="Outils nécessaires")
    impact: str = Field(..., description="Impact sur la sécurité")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Activer WPA2/WPA3",
                "description": "Remplacer le chiffrement WEP par WPA2 ou WPA3",
                "action_steps": [
                    "Accéder à l'interface du routeur (192.168.1.1)",
                    "Accéder à Paramètres > Sécurité Wi-Fi",
                    "Sélectionner WPA2 ou WPA3",
                    "Définir un mot de passe fort (>12 caractères)"
                ],
                "priority": "Critique - Appliquer immédiatement",
                "category": "Chiffrement",
                "estimated_effort": "Faible",
                "impact": "Prévient ~99% des attaques Wi-Fi communes"
            }
        }
