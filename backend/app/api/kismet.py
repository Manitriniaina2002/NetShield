"""Routes API pour intégration Kismet"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.kismet_service import KismetService
from app.models.scan import ScanResult
from app.models.wifi import WiFiNetwork
from datetime import datetime

router = APIRouter(prefix="/api/kismet", tags=["Kismet Integration"])


@router.post("/networks/scan", response_model=ScanResult)
async def scan_with_kismet(
    duration: int = Query(30, ge=10, le=120, description="Durée du scan Kismet en secondes"),
    kismet_url: str = Query("http://localhost:2501", description="URL du serveur Kismet"),
    name: str = Query("Kismet Scan", description="Nom du scan")
):
    """
    Effectue un scan Wi-Fi puissant via Kismet.

    Args:
        duration: Durée du scan (10-120 secondes)
        kismet_url: URL du serveur Kismet
        name: Nom du scan

    Returns:
        Résultat du scan avec liste des réseaux détectés

    Note:
        Nécessite que le serveur Kismet soit en cours d'exécution.
        Installation: https://www.kismetwireless.net/
    """
    try:
        kismet = KismetService(api_url=kismet_url)

        if not await kismet.connect():
            raise HTTPException(
                status_code=503,
                detail=f"Cannot connect to Kismet at {kismet_url}. Ensure Kismet daemon is running."
            )

        try:
            networks = await kismet.scan_networks(duration=duration)

            scan_result = ScanResult(
                id=f"kismet_{datetime.now().timestamp()}",
                scan_name=name,
                scan_timestamp=datetime.now(),
                networks_found=len(networks),
                networks=networks,
                scan_duration=duration,
                interface_used="Kismet",
                mode="kismet",
                message=f"Kismet scan completed. {len(networks)} networks detected."
            )

            return scan_result

        finally:
            await kismet.disconnect()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kismet scan error: {str(e)}")


@router.get("/networks", response_model=dict)
async def get_kismet_networks(
    kismet_url: str = Query("http://localhost:2501", description="URL du serveur Kismet")
):
    """
    Récupère les réseaux actuellement suivi par Kismet sans scan complet.

    Args:
        kismet_url: URL du serveur Kismet

    Returns:
        Liste des réseaux WiFiNetwork détectés
    """
    try:
        kismet = KismetService(api_url=kismet_url)

        if not await kismet.connect():
            raise HTTPException(status_code=503, detail="Cannot connect to Kismet")

        try:
            networks_raw = await kismet.get_networks()
            networks = []

            for net_data in networks_raw:
                try:
                    network = kismet._parse_kismet_network(net_data)
                    if network:
                        networks.append(network)
                except Exception as e:
                    print(f"Error parsing network: {str(e)}")
                    continue

            return {
                "networks": networks,
                "count": len(networks),
                "timestamp": datetime.now().isoformat()
            }

        finally:
            await kismet.disconnect()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/devices", response_model=dict)
async def get_kismet_devices(
    kismet_url: str = Query("http://localhost:2501", description="URL du serveur Kismet")
):
    """
    Récupère tous les appareils détectés par Kismet.

    Args:
        kismet_url: URL du serveur Kismet

    Returns:
        Liste des appareils détectés
    """
    try:
        kismet = KismetService(api_url=kismet_url)

        if not await kismet.connect():
            raise HTTPException(status_code=503, detail="Cannot connect to Kismet")

        try:
            devices = await kismet.get_devices()
            return {
                "devices": devices,
                "count": len(devices),
                "timestamp": datetime.now().isoformat()
            }

        finally:
            await kismet.disconnect()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts", response_model=dict)
async def get_kismet_alerts(
    kismet_url: str = Query("http://localhost:2501", description="URL du serveur Kismet")
):
    """
    Récupère les définitions d'alerte de Kismet (anomalies, attaques détectées).

    Args:
        kismet_url: URL du serveur Kismet

    Returns:
        Liste des alertes configurées
    """
    try:
        kismet = KismetService(api_url=kismet_url)

        if not await kismet.connect():
            raise HTTPException(status_code=503, detail="Cannot connect to Kismet")

        try:
            alerts = await kismet.get_alerts()
            return {
                "alerts": alerts,
                "count": len(alerts),
                "timestamp": datetime.now().isoformat()
            }

        finally:
            await kismet.disconnect()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=dict)
async def get_kismet_status(
    kismet_url: str = Query("http://localhost:2501", description="URL du serveur Kismet")
):
    """
    Récupère l'état du serveur Kismet.

    Args:
        kismet_url: URL du serveur Kismet

    Returns:
        Informations sur le statut et version de Kismet
    """
    try:
        kismet = KismetService(api_url=kismet_url)

        if not await kismet.connect():
            raise HTTPException(
                status_code=503,
                detail=f"Cannot connect to Kismet at {kismet_url}. Is Kismet running?"
            )

        try:
            status = await kismet.get_server_info()
            return {
                "status": "online" if status else "offline",
                "server_info": status,
                "timestamp": datetime.now().isoformat()
            }

        finally:
            await kismet.disconnect()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
