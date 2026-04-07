"""Routes API pour l'analyse des vulnerabilites."""
from typing import List

from fastapi import APIRouter, HTTPException

from app.models.vulnerability import Vulnerability
from app.models.wifi import WiFiNetwork
from app.services.vulnerability_analysis import VulnerabilityAnalysisService

router = APIRouter(prefix="/api/vulnerabilities", tags=["Vulnerabilities"])


@router.post("/analyze/{bssid}", response_model=List[Vulnerability])
async def analyze_network(bssid: str, network: WiFiNetwork):
    """Analyse un reseau Wi-Fi pour detecter ses vulnerabilites."""
    try:
        if network.bssid.upper() != bssid.upper():
            raise HTTPException(
                status_code=400,
                detail="Le BSSID fourni dans l'URL ne correspond pas au reseau envoye.",
            )

        vulnerabilities = await VulnerabilityAnalysisService.analyze_network(network)
        return vulnerabilities

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-batch", response_model=dict)
async def analyze_networks_batch(networks: List[WiFiNetwork]):
    """Analyse un lot de reseaux Wi-Fi."""
    try:
        result = await VulnerabilityAnalysisService.analyze_all_networks(networks)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/statistics", response_model=dict)
async def get_vulnerability_statistics(networks: List[WiFiNetwork]):
    """Retourne les statistiques de vulnerabilites pour une liste de reseaux."""
    try:
        result = await VulnerabilityAnalysisService.analyze_all_networks(networks)
        return result.get("statistics", {})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cracking-strategy/{bssid}")
async def get_cracking_strategy(bssid: str, network: WiFiNetwork):
    """
    Retourne une stratégie de craquage recommandée pour un réseau.
    
    Basée sur le protocole de sécurité (WEP/WPA/WPA2/WPA3).
    
    Args:
        bssid: BSSID du réseau
        network: Modèle WiFiNetwork avec détails du réseau
        
    Returns:
        Dict avec stratégie de craquage, outils recommandés et paramètres
    """
    try:
        if network.bssid.upper() != bssid.upper():
            raise HTTPException(
                status_code=400,
                detail="Le BSSID fourni dans l'URL ne correspond pas au réseau envoyé.",
            )
        
        strategy = VulnerabilityAnalysisService.get_cracking_strategy(network)
        
        return {
            "network_bssid": bssid,
            "network_ssid": network.ssid,
            "security_level": network.security.value,
            "cracking_strategy": strategy,
            "endpoint": f"/api/cracking/start"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cracking-strategies-batch")
async def get_cracking_strategies_batch(networks: List[WiFiNetwork]):
    """
    Retourne les stratégies de craquage pour un lot de réseaux.
    
    Args:
        networks: Liste des réseaux à analyser
        
    Returns:
        Dict avec stratégies groupées par viabilité
    """
    try:
        viable = []
        not_viable = []
        
        for network in networks:
            strategy = VulnerabilityAnalysisService.get_cracking_strategy(network)
            
            network_info = {
                "network_bssid": network.bssid,
                "network_ssid": network.ssid,
                "security_level": network.security.value,
                "strategy": strategy
            }
            
            if strategy.get("viable", False):
                viable.append(network_info)
            else:
                not_viable.append(network_info)
        
        return {
            "total_networks": len(networks),
            "viable_for_cracking": {
                "count": len(viable),
                "networks": viable
            },
            "not_viable_for_cracking": {
                "count": len(not_viable),
                "networks": not_viable,
                "reasons": [n["strategy"].get("reason", "") for n in not_viable]
            },
            "academic_note": "Mode simulation active - craquage simulé pour tests académiques"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))