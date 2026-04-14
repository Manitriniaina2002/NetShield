"""API routes pour la capture de handshakes WiFi."""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import Optional
from pydantic import BaseModel

from app.models.wifi import WiFiNetwork
from app.services.handshake_capture import (
    HandshakeCaptureService,
    HandshakeCapture,
    CaptureStatus
)
from app.services.wifi_scan import WiFiScanService

router = APIRouter(prefix="/api/handshake", tags=["handshake"])


class StartCaptureRequest(BaseModel):
    """Requête de démarrage de capture."""
    network: WiFiNetwork
    duration: int = 60
    enable_deauth: bool = False
    deauth_count: int = 5


class CaptureStatusResponse(BaseModel):
    """Réponse du statut de capture."""
    capture_id: str
    status: str
    progress: int
    packets_captured: int
    handshake_found: bool
    error_message: Optional[str] = None


@router.post("/capture/start")
async def start_handshake_capture(
    request: StartCaptureRequest,
    background_tasks: BackgroundTasks
) -> dict:
    """Démarre une capture de handshake pour un réseau WiFi."""
    try:
        # Créer une nouvelle capture avec options de déauth
        capture = HandshakeCaptureService.start_capture(
            request.network,
            duration=request.duration,
            enable_deauth=request.enable_deauth,
            deauth_count=request.deauth_count
        )
        
        # Lancer la capture en tâche de fond
        interfaces = HandshakeCaptureService.get_available_interfaces()
        if not interfaces:
            raise HTTPException(
                status_code=500,
                detail="Aucune interface WiFi disponible"
            )
        
        background_tasks.add_task(
            HandshakeCaptureService.launch_capture_job,
            capture,
            interface=interfaces[0],
            duration=request.duration
        )
        
        return {
            "status": "started",
            "capture_id": capture.capture_id,
            "network_ssid": request.network.ssid,
            "network_bssid": request.network.bssid,
            "duration": request.duration,
            "deauth_enabled": request.enable_deauth,
            "deauth_count": request.deauth_count,
            "message": f"Capture démarrée pour {request.network.ssid}" + 
                      (f" (déauth x{request.deauth_count})" if request.enable_deauth else "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capture/status/{capture_id}")
async def get_capture_status(capture_id: str) -> dict:
    """Récupère le statut d'une capture."""
    capture = HandshakeCaptureService.get_capture_status(capture_id)
    
    if not capture:
        raise HTTPException(status_code=404, detail="Capture non trouvée")
    
    response = {
        "capture_id": capture.capture_id,
        "network_bssid": capture.network_bssid,
        "network_ssid": capture.network_ssid,
        "status": capture.status.value,
        "progress": capture.progress,
        "packets_captured": capture.packets_captured,
        "handshake_found": capture.handshake_found,
        "file_size": capture.file_size,
        "duration_seconds": capture.duration_seconds,
        "deauth_enabled": capture.enable_deauth,
        "deauth_sent": capture.deauth_sent,
        "deauth_completed": capture.deauth_completed,
    }
    
    if capture.error_message:
        response["error_message"] = capture.error_message
    
    return response


@router.get("/capture/list")
async def list_active_captures() -> dict:
    """Liste toutes les captures actives."""
    captures = HandshakeCaptureService.list_active_captures()
    
    return {
        "total": len(captures),
        "captures": [
            {
                "capture_id": c.capture_id,
                "network_ssid": c.network_ssid,
                "network_bssid": c.network_bssid,
                "status": c.status.value,
                "progress": c.progress,
                "packets_captured": c.packets_captured,
                "handshake_found": c.handshake_found,
                "deauth_enabled": c.enable_deauth,
                "deauth_sent": c.deauth_sent,
            }
            for c in captures
        ]
    }


@router.post("/capture/cancel/{capture_id}")
async def cancel_capture(capture_id: str) -> dict:
    """Annule une capture en cours."""
    result = HandshakeCaptureService.cancel_capture(capture_id)
    
    if result["status"] == "not_found":
        raise HTTPException(status_code=404, detail="Capture non trouvée")
    
    return result


@router.get("/interfaces")
async def get_wifi_interfaces() -> dict:
    """Récupère les interfaces WiFi disponibles."""
    interfaces = HandshakeCaptureService.get_available_interfaces()
    
    return {
        "interfaces": interfaces,
        "count": len(interfaces)
    }


@router.post("/capture/integrated/{capture_id}")
async def use_capture_for_cracking(
    capture_id: str,
    password_list: Optional[str] = Query(None),
    cracking_method: str = Query("aircrack_ng")
) -> dict:
    """Utilise une capture de handshake pour le cracking de mot de passe."""
    capture = HandshakeCaptureService.get_capture_status(capture_id)
    
    if not capture:
        raise HTTPException(status_code=404, detail="Capture non trouvée")
    
    if not capture.handshake_found:
        raise HTTPException(
            status_code=400,
            detail="Aucun handshake détecté dans cette capture"
        )
    
    if not capture.file_path:
        raise HTTPException(
            status_code=400,
            detail="Le fichier de capture n'est pas disponible"
        )
    
    return {
        "status": "ready_for_cracking",
        "capture_id": capture_id,
        "capture_file": capture.file_path,
        "network_ssid": capture.network_ssid,
        "cracking_method": cracking_method,
        "password_list": password_list,
        "message": f"Capture prête pour le cracking via {cracking_method}"
    }
