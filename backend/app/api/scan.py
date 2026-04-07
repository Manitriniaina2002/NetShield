"""Routes API pour les scans Wi-Fi"""
from fastapi import APIRouter, Query, HTTPException
from typing import List
import platform
from app.models.wifi import WiFiNetwork
from app.models.scan import ScanResult
from app.services.wifi_scan import WiFiScanService
from app.config import get_settings
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
        settings = get_settings()
        system_name = platform.system().lower()
        interface_name = "Wi-Fi" if system_name == "windows" else "wlan0"
        
        # Essayer un scan réel en premier
        scan_mode = "simulation"
        networks = []
        error_msg = None
        
        if not settings.simulation_mode:
            try:
                networks = await WiFiScanService.scan_networks(duration_seconds=duration)
                scan_mode = "real"
            except Exception as real_error:
                # Fallback à la simulation avec message d'erreur
                error_msg = f"Real mode error: {str(real_error)}"
                print(f"[SCAN ERROR] {error_msg}")
                networks = await WiFiScanService._scan_networks_simulated(duration_seconds=duration)
                scan_mode = "simulation_fallback"
        else:
            networks = await WiFiScanService._scan_networks_simulated(duration_seconds=duration)
        
        # Créer le résultat du scan
        scan_result = ScanResult(
            id=f"scan_{datetime.now().timestamp()}",
            scan_name=name,
            scan_timestamp=datetime.now(),
            networks_found=len(networks),
            networks=networks,
            scan_duration=duration,
            interface_used=interface_name,
            mode=scan_mode,
            message=f"Scan {scan_mode} completed. {error_msg if error_msg else 'Success'}"
        )
        
        return scan_result
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Scan error: {str(e)}")


@router.get("/networks/{bssid}", response_model=dict)
async def get_network_details(
    bssid: str,
    channel: int = Query(1, ge=1, le=196)
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
    sort_by: str = Query("signal", pattern="^(signal|security|clients|channel)$")
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
