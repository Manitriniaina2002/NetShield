"""Routes API pour les scans Wi-Fi"""
from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
import platform
from app.models.wifi import WiFiNetwork
from app.models.wifi import SecurityLevel
from app.models.scan import ScanResult
from app.services.wifi_scan import WiFiScanService
from app.config import get_settings
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import get_db_engine, get_session_maker
from app.services.database_service import DatabaseService

router = APIRouter(prefix="/api/scan", tags=["WiFi Scan"])


def get_db():
    """Dependency pour obtenir une session de base de donnees."""
    engine = get_db_engine()
    SessionLocal = get_session_maker(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _map_demo_security_to_level(security_level: str) -> SecurityLevel:
    """Mappe les tags de demo vers le modele SecurityLevel."""
    value = (security_level or "").strip().upper()

    if "OPEN" in value:
        return SecurityLevel.OPEN
    if "WEP" in value:
        return SecurityLevel.WEP
    if "WPA3" in value:
        return SecurityLevel.WPA3
    if "WPA2" in value:
        return SecurityLevel.WPA2
    if "WPA" in value:
        return SecurityLevel.WPA

    return SecurityLevel.UNKNOWN


def _build_network_from_handshake(handshake) -> WiFiNetwork:
    """Convertit un handshake stocke en objet WiFiNetwork reutilisable."""
    security_tag = (handshake.tags or "Unknown").split(",")[0]
    security = _map_demo_security_to_level(security_tag)

    signal_strength = -55
    signal_percentage = 70
    clients = max(1, min(20, handshake.deauth_count if handshake.deauth_count > 0 else 3))

    return WiFiNetwork(
        id=f"demo_{handshake.capture_id}",
        ssid=handshake.network_ssid,
        bssid=handshake.network_bssid,
        channel=6,
        frequency="2.4GHz",
        security=security,
        signal_strength=signal_strength,
        signal_percentage=signal_percentage,
        clients=clients,
        last_seen=handshake.created_at or datetime.now(),
    )


def _merge_unique_by_bssid(primary: List[WiFiNetwork], extra: List[WiFiNetwork]) -> List[WiFiNetwork]:
    """Fusionne deux listes en dedoublonnant par BSSID."""
    seen = {n.bssid.upper() for n in primary}
    merged = list(primary)

    for network in extra:
        if network.bssid.upper() in seen:
            continue
        merged.append(network)
        seen.add(network.bssid.upper())

    return merged


@router.post("/networks", response_model=ScanResult)
async def scan_networks(
    duration: int = Query(10, ge=5, le=60, description="Durée du scan en secondes"),
    name: str = Query("Audit Scan", description="Nom du scan"),
    include_demo_data: bool = Query(True, description="Inclure les reseaux demo stockes"),
    include_demo_failed: bool = Query(False, description="Inclure aussi les captures demo echouees"),
    db: Session = Depends(get_db)
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
        
        if include_demo_data:
            handshakes = DatabaseService.get_all_handshakes(db, limit=500)
            demo_handshakes = [h for h in handshakes if "demo" in (h.tags or "").lower()]
            if not include_demo_failed:
                demo_handshakes = [h for h in demo_handshakes if h.success]

            demo_networks = [_build_network_from_handshake(h) for h in demo_handshakes]
            networks = _merge_unique_by_bssid(networks, demo_networks)

            if scan_mode == "real":
                scan_mode = "real_plus_demo"
            elif scan_mode == "simulation":
                scan_mode = "simulation_plus_demo"
            elif scan_mode == "simulation_fallback":
                scan_mode = "fallback_plus_demo"

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
