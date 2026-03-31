"""Routes API pour les scans Wi-Fi"""
from fastapi import APIRouter, Query, HTTPException
from typing import List
from app.models.wifi import WiFiNetwork
from app.models.scan import ScanResult
from app.services.wifi_scan import WiFiScanService
from datetime import datetime

router = APIRouter(prefix="/api/scan", tags=["WiFi Scan"])


@router.post("/networks", response_model=ScanResult)
async def scan_networks(
    duration: int = Query(10, ge=5, le=60, description="Durée du scan en secondes"),
    name: str = Query("Audit Scan", description="Nom du scan")
):
    """
    Lance un scan Wi-Fi et retourne les réseaux détectés
    
    Args:
        duration: Durée du scan (5-60 secondes)
        name: Nom du scan
        
    Returns:
        Résultat du scan avec liste des réseaux
    """
    try:
        # Exécuter le scan
        networks = await WiFiScanService.scan_networks(duration_seconds=duration)
        
        # Créer le résultat du scan
        scan_result = ScanResult(
            id=f"scan_{datetime.now().timestamp()}",
            scan_name=name,
            scan_timestamp=datetime.now(),
            networks_found=len(networks),
            networks=networks,
            scan_duration=duration,
            interface_used="wlan0",
            mode="simulation"
        )
        
        return scan_result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/networks/{bssid}", response_model=dict)
async def get_network_details(
    bssid: str,
    channel: int = Query(1, ge=1, le=14)
):
    """
    Récupère les détails d'un réseau spécifique
    
    Args:
        bssid: MAC address du routeur
        channel: Canal Wi-Fi
        
    Returns:
        Détails du réseau
    """
    try:
        details = await WiFiScanService.scan_specific_network(bssid, channel)
        
        if not details:
            raise HTTPException(status_code=404, detail="Réseau non trouvé")
        
        return details
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/networks/sort")
async def sort_networks(
    networks: List[WiFiNetwork],
    sort_by: str = Query("signal", regex="^(signal|security|clients|channel)$")
):
    """
    Trie les réseaux selon un critère
    
    Args:
        networks: Liste des réseaux
        sort_by: Critère de tri (signal/security/clients/channel)
        
    Returns:
        Réseaux triés
    """
    try:
        if sort_by == "signal":
            sorted_networks = sorted(networks, key=lambda x: x.signal_strength, reverse=True)
        elif sort_by == "security":
            security_order = {"WPA3": 0, "WPA2": 1, "WPA": 2, "WEP": 3, "Open": 4}
            sorted_networks = sorted(
                networks,
                key=lambda x: security_order.get(x.security.value, 999)
            )
        elif sort_by == "clients":
            sorted_networks = sorted(networks, key=lambda x: x.clients, reverse=True)
        elif sort_by == "channel":
            sorted_networks = sorted(networks, key=lambda x: x.channel)
        else:
            sorted_networks = networks
        
        return {"sorted_networks": sorted_networks}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
