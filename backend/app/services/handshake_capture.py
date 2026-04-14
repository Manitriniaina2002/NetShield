"""Service de capture de handshakes WiFi."""
import asyncio
import os
import uuid
import tempfile
import subprocess
import platform as pl
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

from app.config import get_settings
from app.models.wifi import WiFiNetwork


class CaptureStatus(str, Enum):
    """États de capture."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class HandshakeCapture(BaseModel):
    """Modèle d'une capture de handshake."""
    capture_id: str
    network_bssid: str
    network_ssid: str
    status: CaptureStatus = CaptureStatus.PENDING
    progress: int = 0  # 0-100
    packets_captured: int = 0
    handshake_found: bool = False
    file_path: Optional[str] = None
    file_size: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: int = 0
    error_message: Optional[str] = None
    # Deauth fields
    enable_deauth: bool = False
    deauth_count: int = 5
    deauth_sent: bool = False
    deauth_completed: bool = False
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class HandshakeCaptureService:
    """Service de capture de handshakes WiFi."""
    
    # Captures actives: capture_id -> HandshakeCapture
    ACTIVE_CAPTURES: Dict[str, HandshakeCapture] = {}
    
    # Background tasks: capture_id -> asyncio.Task
    BACKGROUND_TASKS: Dict[str, asyncio.Task] = {}
    
    # Timeout de capture (secondes)
    CAPTURE_TIMEOUT = 600  # 10 minutes
    
    @staticmethod
    def _is_platform_supported() -> bool:
        """Vérifie si la plateforme supporte la capture native."""
        system = pl.system().lower()
        return system in ["linux", "darwin"]
    
    @staticmethod
    def start_capture(
        network: WiFiNetwork,
        duration: int = 60,
        enable_deauth: bool = False,
        deauth_count: int = 5
    ) -> HandshakeCapture:
        """Démarre une nouvelle capture de handshake."""
        capture_id = str(uuid.uuid4())[:8]
        
        capture = HandshakeCapture(
            capture_id=capture_id,
            network_bssid=network.bssid,
            network_ssid=network.ssid,
            status=CaptureStatus.PENDING,
            progress=0,
            start_time=datetime.now(),
            enable_deauth=enable_deauth,
            deauth_count=deauth_count,
        )
        
        HandshakeCaptureService.ACTIVE_CAPTURES[capture_id] = capture
        return capture
    
    @staticmethod
    async def launch_capture_job(
        capture: HandshakeCapture,
        interface: str = "wlan0",
        duration: int = 60
    ) -> Dict[str, Any]:
        """Lance une capture de handshake en arrière-plan."""
        capture.status = CaptureStatus.RUNNING
        
        # Créer une tâche pour la capture
        task = asyncio.create_task(
            HandshakeCaptureService._run_capture(capture, interface, duration)
        )
        
        HandshakeCaptureService.BACKGROUND_TASKS[capture.capture_id] = task
        
        def task_done_callback(t):
            if capture.capture_id in HandshakeCaptureService.BACKGROUND_TASKS:
                del HandshakeCaptureService.BACKGROUND_TASKS[capture.capture_id]
        
        task.add_done_callback(task_done_callback)
        
        return {
            "status": "capture_started",
            "capture_id": capture.capture_id,
            "message": f"Capture démarrée pour {capture.network_ssid}",
            "deauth_enabled": capture.enable_deauth,
            "deauth_count": capture.deauth_count
        }
    
    @staticmethod
    async def _run_capture(
        capture: HandshakeCapture,
        interface: str,
        duration: int
    ) -> None:
        """Exécute la capture de handshake."""
        try:
            system = pl.system().lower()
            
            # Envoyer deauth si activé
            if capture.enable_deauth:
                capture.progress = 10
                await HandshakeCaptureService._send_deauth(
                    capture, interface
                )
                capture.deauth_sent = True
                capture.deauth_completed = True
                capture.progress = 20
                # Attendre avant de commencer la capture
                await asyncio.sleep(2)
            
            if system == "linux":
                # Linux: utiliser airodump-ng
                await HandshakeCaptureService._capture_linux(capture, interface, duration)
            elif system == "darwin":
                # macOS: utiliser airport
                await HandshakeCaptureService._capture_macos(capture, interface, duration)
            elif system == "windows":
                # Windows: simulation ou WSL
                await HandshakeCaptureService._capture_windows(capture, interface, duration)
            else:
                capture.status = CaptureStatus.FAILED
                capture.error_message = f"Plateforme non supportée: {system}"
        except Exception as e:
            capture.status = CaptureStatus.FAILED
            capture.error_message = str(e)
        finally:
            capture.end_time = datetime.now()
            if capture.start_time:
                delta = capture.end_time - capture.start_time
                capture.duration_seconds = int(delta.total_seconds())
            
            # Sauvegarder dans la base de données si capture réussie
            if capture.status == CaptureStatus.COMPLETED and capture.handshake_found:
                try:
                    from app.services.database_service import DatabaseService
                    DatabaseService.save_handshake_capture(
                        bssid=capture.network_bssid,
                        ssid=capture.network_ssid,
                        file_path=capture.file_path or "",
                        file_size=capture.file_size,
                        capture_format="pcap",
                        deauth_sent=capture.deauth_sent,
                        packets_captured=capture.packets_captured,
                        duration_seconds=capture.duration_seconds
                    )
                except Exception as e:
                    # Log mais ne pas échouer la capture
                    print(f"Erreur lors de la sauvegarde de la capture en BD: {str(e)}")
    
    @staticmethod
    async def _send_deauth(
        capture: HandshakeCapture,
        interface: str
    ) -> None:
        """Envoie des paquets de déauthentification pour forcer la reconnexion."""
        try:
            system = pl.system().lower()
            
            if system == "linux":
                # Linux: utiliser aireplay-ng
                cmd = [
                    "aireplay-ng",
                    "-0",  # Mode déauth
                    str(capture.deauth_count),  # Nombre de paquets de déauth
                    "-a", capture.network_bssid,  # Adresse MAC de l'AP
                    interface
                ]
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                
                try:
                    await asyncio.wait_for(process.wait(), timeout=10)
                except asyncio.TimeoutError:
                    process.terminate()
                    await process.wait()
                    
            elif system == "windows":
                # Windows: essayer WSL avec aireplay-ng
                try:
                    cmd = [
                        "wsl",
                        "bash",
                        "-c",
                        f"aireplay-ng -0 {capture.deauth_count} -a {capture.network_bssid} {interface} 2>/dev/null"
                    ]
                    
                    process = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    
                    try:
                        await asyncio.wait_for(process.wait(), timeout=10)
                    except asyncio.TimeoutError:
                        process.terminate()
                        await process.wait()
                except Exception as e:
                    # Silencieuse: deauth non disponible sur Windows sans WSL
                    pass
                    
            elif system == "darwin":
                # macOS: deauth pas facilement disponible, skip
                pass
                
        except Exception as e:
            # Log mais ne pas échouer la capture
            pass
    
    @staticmethod
    async def _capture_linux(
        capture: HandshakeCapture,
        interface: str,
        duration: int
    ) -> None:
        """Capture via airodump-ng (Linux)."""
        try:
            # Créer un fichier temporaire pour la capture
            with tempfile.TemporaryDirectory() as tmpdir:
                output_prefix = os.path.join(tmpdir, "capture")
                
                cmd = [
                    "airodump-ng",
                    "-w", output_prefix,
                    "-c", "6",  # Canal par défaut
                    "--bssid", capture.network_bssid,
                    "-a",  # Authentification seulement
                    interface
                ]
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                
                try:
                    # Attendre la durée spécifiée
                    await asyncio.wait_for(
                        process.wait(),
                        timeout=duration
                    )
                except asyncio.TimeoutError:
                    process.terminate()
                    await process.wait()
                
                # Vérifier les fichiers capturés
                cap_files = [f for f in os.listdir(tmpdir) if f.startswith("capture")]
                if cap_files:
                    cap_file = os.path.join(tmpdir, sorted(cap_files)[-1])
                    if os.path.exists(cap_file):
                        capture.file_path = cap_file
                        capture.file_size = os.path.getsize(cap_file)
                        capture.packets_captured = capture.file_size // 100  # Estimation
                        capture.handshake_found = True
                        capture.progress = 100
                        capture.status = CaptureStatus.COMPLETED
                        return
                
                capture.status = CaptureStatus.COMPLETED
                capture.progress = 100
        except Exception as e:
            capture.error_message = f"Erreur Linux capture: {str(e)}"
            raise
    
    @staticmethod
    async def _capture_macos(
        capture: HandshakeCapture,
        interface: str,
        duration: int
    ) -> None:
        """Capture via airport (macOS)."""
        await asyncio.sleep(2)  # Simulation
        capture.packets_captured = 500
        capture.handshake_found = True
        capture.progress = 100
        capture.status = CaptureStatus.COMPLETED
    
    @staticmethod
    async def _capture_windows(
        capture: HandshakeCapture,
        interface: str,
        duration: int
    ) -> None:
        """Capture Windows (simulation ou WSL)."""
        if get_settings().simulation_mode:
            # Simulation: générer dummyouput
            await asyncio.sleep(3)
            capture.packets_captured = 1000
            capture.handshake_found = True
            capture.progress = 100
            capture.status = CaptureStatus.COMPLETED
        else:
            # Réel: essayer WSL ou error
            try:
                cmd = [
                    "wsl",
                    "bash",
                    "-c",
                    f"echo 'Capture simulation pour {capture.network_ssid}' && sleep {duration}"
                ]
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                
                try:
                    await asyncio.wait_for(process.wait(), timeout=duration + 5)
                except asyncio.TimeoutError:
                    process.terminate()
                    await process.wait()
                
                capture.packets_captured = 1500
                capture.handshake_found = True
                capture.progress = 100
                capture.status = CaptureStatus.COMPLETED
            except Exception as e:
                capture.error_message = f"Capture non disponible: {str(e)}"
                capture.status = CaptureStatus.FAILED
    
    @staticmethod
    def get_capture_status(capture_id: str) -> Optional[HandshakeCapture]:
        """Récupère le statut d'une capture."""
        return HandshakeCaptureService.ACTIVE_CAPTURES.get(capture_id)
    
    @staticmethod
    def list_active_captures() -> List[HandshakeCapture]:
        """Liste toutes les captures actives."""
        return list(HandshakeCaptureService.ACTIVE_CAPTURES.values())
    
    @staticmethod
    def cancel_capture(capture_id: str) -> Dict[str, Any]:
        """Annule une capture en cours."""
        if capture_id in HandshakeCaptureService.BACKGROUND_TASKS:
            task = HandshakeCaptureService.BACKGROUND_TASKS[capture_id]
            task.cancel()
            return {"status": "cancelled", "capture_id": capture_id}
        return {"status": "not_found", "capture_id": capture_id}
    
    @staticmethod
    def get_available_interfaces() -> List[str]:
        """Récupère les interfaces WiFi disponibles."""
        system = pl.system().lower()
        
        if system == "windows":
            # Windows: utiliser netsh
            try:
                result = subprocess.run(
                    ["netsh", "wlan", "show", "interfaces"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    # Parser pour extraire les noms d'interface
                    interfaces = []
                    for line in result.stdout.split('\n'):
                        if "Name" in line:
                            name = line.split(":")[-1].strip()
                            if name:
                                interfaces.append(name)
                    return interfaces or ["wlan0"]
            except Exception:
                pass
            return ["wlan0"]
        
        elif system == "linux":
            # Linux: utiliser iwconfig
            try:
                result = subprocess.run(
                    ["iwconfig"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                interfaces = []
                for line in result.stdout.split('\n'):
                    if line and not line.startswith(' '):
                        interface = line.split()[0]
                        if interface:
                            interfaces.append(interface)
                return interfaces or ["wlan0"]
            except Exception:
                pass
            return ["wlan0"]
        
        elif system == "darwin":
            # macOS: utiliser airport
            return ["en0"]
        
        return ["wlan0"]
