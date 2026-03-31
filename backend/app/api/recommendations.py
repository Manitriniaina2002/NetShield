"""Routes API pour les recommandations"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.recommendation import Recommendation
from app.models.vulnerability import Vulnerability
from app.models.wifi import WiFiNetwork
from app.services.recommendation import RecommendationService

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.post("/generate", response_model=List[Recommendation])
async def generate_recommendations(
    vulnerabilities: List[Vulnerability],
    networks: List[WiFiNetwork]
):
    """
    Génère automatiquement des recommandations de sécurité
    
    Args:
        vulnerabilities: Liste des vulnérabilités identifiées
        networks: Liste des réseaux analysés
        
    Returns:
        Liste des recommandations générées automatiquement
    """
    try:
        recommendations = await RecommendationService.generate_recommendations(
            vulnerabilities,
            networks
        )
        return recommendations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-priority/{priority}")
async def get_recommendations_by_priority(
    priority: str,
    recommendations: List[Recommendation]
):
    """
    Filtre les recommandations par niveau de priorité
    
    Args:
        priority: Niveau de priorité
        recommendations: Liste des recommandations
        
    Returns:
        Recommandations filtrées
    """
    try:
        filtered = [r for r in recommendations if priority.lower() in r.priority.value.lower()]
        return {"recommendations": filtered}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-category/{category}")
async def get_recommendations_by_category(
    category: str,
    recommendations: List[Recommendation]
):
    """
    Filtre les recommandations par catégorie
    
    Args:
        category: Catégorie
        recommendations: Liste des recommandations
        
    Returns:
        Recommandations filtrées
    """
    try:
        filtered = [r for r in recommendations if category.lower() in r.category.lower()]
        return {"recommendations": filtered}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
