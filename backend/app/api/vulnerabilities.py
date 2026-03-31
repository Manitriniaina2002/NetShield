"""Routes API pour l'analyse des vulnérabilités"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.wifi import WiFiNetwork
from app.models.vulnerability import Vulnerability
from app.services.vulnerability_analysis import VulnerabilityAnalysisService

router = APIRouter(prefix="/api/vulnerabilities", tags=["Vulnerabilities"])


@router.post("/analyze/{bssid}", response_model=List[Vulnerability])
async def analyze_network(bssid: str, network: WiFiNetwork):
    """
    Analyse un réseau Wi-Fi pour les vulnérabilités
    
    Args:
        bssid: MAC address du routeur (pour validation)
        network: Données du réseau à analyser
        
    Returns:
        Liste des vulnérabilités identifiées
    """
    try:
        vulnerabilities = await VulnerabilityAnalysisService.analyze_network(network)
        return vulnerabilities
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-batch", response_model=dict)
async def analyze_networks_batch(networks: List[WiFiNetwork]):
    """
    Analyse un lot de réseaux Wi-Fi
    
    Args:
        networks: Liste des réseaux à analyser
        
    Returns:
        Synthèse des vulnérabilités pour tous les réseaux
    """
    try:
        result = await VulnerabilityAnalysisService.analyze_all_networks(networks)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_vulnerability_statistics(networks: List[WiFiNetwork]):
    """
    Génère des statistiques sur les vulnérabilités
    
    Args:
        networks: Liste des réseaux analysés
        
    Returns:
        Statistiques des vulnérabilités
    """
    try:
        result = await VulnerabilityAnalysisService.analyze_all_networks(networks)
        return result["statistics"]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

















































































        raise HTTPException(status_code=500, detail=str(e))    except Exception as e:            return {"recommendations": filtered}        filtered = [r for r in recommendations if category.lower() in r.category.lower()]    try:    """        Recommandations filtrées    Returns:                recommendations: Liste des recommandations        category: Catégorie    Args:        Filtre les recommandations par catégorie    """):    recommendations: List[Recommendation]    category: str,async def get_recommendations_by_category(@router.get("/by-category/{category}")        raise HTTPException(status_code=500, detail=str(e))    except Exception as e:            return {"recommendations": filtered}        filtered = [r for r in recommendations if priority.lower() in r.priority.value.lower()]    try:    """        Recommandations filtrées    Returns:                recommendations: Liste des recommandations        priority: Niveau de priorité    Args:        Filtre les recommandations par niveau de priorité    """):    recommendations: List[Recommendation]    priority: str,async def get_recommendations_by_priority(@router.get("/by-priority/{priority}")        raise HTTPException(status_code=500, detail=str(e))    except Exception as e:            return recommendations        )            networks            vulnerabilities,        recommendations = await RecommendationService.generate_recommendations(    try:    """        Liste des recommandations générées automatiquement    Returns:                networks: Liste des réseaux analysés        vulnerabilities: Liste des vulnérabilités identifiées    Args:        Génère automatiquement des recommandations de sécurité    """):    networks: List[WiFiNetwork]    vulnerabilities: List[Vulnerability],async def generate_recommendations(@router.post("/generate", response_model=List[Recommendation])router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])from app.services.recommendation import RecommendationServicefrom app.models.wifi import WiFiNetworkfrom app.models.vulnerability import Vulnerabilityfrom app.models.recommendation import Recommendationfrom typing import Listfrom fastapi import APIRouter, HTTPExceptionfrom fastapi import APIRouter, HTTPException
from typing import List
from app.models.wifi import WiFiNetwork
from app.models.vulnerability import Vulnerability
from app.services.vulnerability_analysis import VulnerabilityAnalysisService

router = APIRouter(prefix="/api/vulnerabilities", tags=["Vulnerabilities"])


@router.post("/analyze/{bssid}", response_model=List[Vulnerability])
async def analyze_network(bssid: str, network: WiFiNetwork):
    """
    Analyse un réseau Wi-Fi pour les vulnérabilités
    
    Args:
        bssid: MAC address du routeur (pour validation)
        network: Données du réseau à analyser
        
    Returns:
        Liste des vulnérabilités identifiées
    """
    try:
        if network.bssid != bssid:
            raise HTTPException(
                status_code=400,
                detail="BSSID dans le chemin ne correspond pas aux données"
            )
        
        vulnerabilities = await VulnerabilityAnalysisService.analyze_network(network)
        return vulnerabilities
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-batch", response_model=dict)
async def analyze_networks_batch(networks: List[WiFiNetwork]):
    """
    Analyse un lot de réseaux Wi-Fi
    
    Args:
        networks: Liste des réseaux à analyser
        
    Returns:
        Synthèse des vulnérabilités pour tous les réseaux
    """
    try:
        result = await VulnerabilityAnalysisService.analyze_all_networks(networks)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_vulnerability_statistics(networks: List[WiFiNetwork]):
    """
    Génère des statistiques sur les vulnérabilités
    
    Args:
        networks: Liste des réseaux analysés
        
    Returns:
        Statistiques des vulnérabilités
    """
    try:
        result = await VulnerabilityAnalysisService.analyze_all_networks(networks)
        return result["statistics"]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
