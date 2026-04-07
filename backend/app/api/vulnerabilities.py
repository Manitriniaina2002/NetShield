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