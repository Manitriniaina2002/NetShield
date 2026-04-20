"""Routes API pour les opérations de craquage de mots de passe."""
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import logging
from sqlalchemy.orm import Session

from app.services.cracking import (
    CrackingService,
    CrackingMethod,
    CrackingJob,
)
from app.services.wifi_scan import WiFiScanService
from app.services.database_service import DatabaseService
from app.config import get_settings
from app.models.database import get_db_engine, get_session_maker

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/cracking", tags=["Cracking"])


def get_db():
    """Dependency pour obtenir une session de base de donnees."""
    engine = get_db_engine()
    SessionLocal = get_session_maker(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class StartCrackingRequest(BaseModel):
    """Demande de démarrage du craquage."""
    network_bssid: str
    method: CrackingMethod = CrackingMethod.AIRCRACK_NG
    wordlist: str = "rockyou"  # rockyou, common, academic
    gpu_enabled: bool = False
    handshake_id: Optional[int] = None  # ID de la capture stockée


class CrackingStatusResponse(BaseModel):
    """Réponse du statut de craquage."""
    job_id: str
    network_bssid: str
    network_ssid: str
    status: str
    progress: int
    password_found: Optional[str] = None
    error_message: Optional[str] = None


@router.get("/status")
async def get_cracking_status():
    """
    Récupère les informations d'état des outils de craquage disponibles.
    
    Returns:
        Dict contenant les outils disponibles et leur status
    """
    return {
        "available_tools": CrackingService.get_available_methods(),
        "platform": "windows" if __import__("platform").system() == "Windows" else "linux",
        "note": "Mode simulation activé" if get_settings().simulation_mode else "Mode réel - Outils système utilisés",
    }


@router.get("/wordlists")
async def get_available_wordlists():
    """
    Récupère les dictionnaires de mots disponibles.
    
    Returns:
        Dict des dictionnaires disponibles avec tailles
    """
    return {
        "common": {
            "description": "1200 mots de passe courants",
            "size": 1200,
            "suitable_for": "Tests rapides, académique"
        },
        "rockyou": {
            "description": "14+ millions de mots de passe (le plus populaire)",
            "size": 14344391,
            "suitable_for": "Craquage complet, Pentest réel"
        },
        "academic": {
            "description": "5000 mots générés pour exercices académiques",
            "size": 5000,
            "suitable_for": "Laboratoire, démonstration"
        }
    }


@router.post("/start")
async def start_cracking_job(request: StartCrackingRequest, db: Session = Depends(get_db)):
    """
    Démarre un travail de craquage de mot de passe pour un réseau.
    
    SÉCURITÉ: Authentification admin requise en mode réel
    
    Args:
        request: Configuration du travail
        
    Returns:
        Job details avec ID
        
    Notes:
        - Mode simulation: résultat simulé après délai
        - Mode réel: requiert aircrack-ng/hashcat installé
        - Pas de limite de job actifs, mais surveillance mémoire
    """
    logger.debug(f"Start cracking request: network_bssid={request.network_bssid}, method={request.method}, wordlist={request.wordlist}")
    
    settings = get_settings()
    
    # En mode réel, vérifier l'authentification (TODO: intégrer avec CommandExecutionService)
    if not settings.simulation_mode:
        # À implémenter: vérifier les privilèges admin
        pass
    
    # Récupérerlutionlechemin du fichier handshake
    handshake_file = "/tmp/capture.cap"
    handshake_db_id = None
    network_ssid = f"Network_{request.network_bssid.replace(':', '')[-6:]}"
    if request.handshake_id:
        # Récupérer le handshake stocké depuis la base de données
        try:
            handshake = DatabaseService.get_handshake_by_db_id(db, request.handshake_id)
            if not handshake:
                raise HTTPException(status_code=404, detail=f"Handshake {request.handshake_id} non trouvé")
            handshake_file = handshake.capture_file_path or handshake_file
            handshake_db_id = handshake.id
            network_ssid = handshake.network_ssid or network_ssid
        except Exception as e:
            logger.error(f"Error retrieving handshake: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du handshake: {str(e)}")
    
    # Chercher le réseau et lancer le craquage
    try:
        # Pour l'API, on crée simplement le job
        # La vraie implémentation cherche le réseau scannés
        job = CrackingService.create_job(
            network=type('obj', (object,), {
                'bssid': request.network_bssid,
                'ssid': network_ssid,
                'channel': 1,
                'signal_strength': -50,
                'security': 'WPA2'
            })(),
            method=request.method,
            wordlist=request.wordlist,
            gpu_enabled=request.gpu_enabled
        )
        
        # Récupérer le chemin du wordlist
        wordlist_path = "/usr/share/wordlists/rockyou.txt"  # Défaut
        if request.wordlist == "common":
            wordlist_path = CrackingService.generate_common_wordlist()
        elif request.wordlist == "academic":
            wordlist_path = CrackingService.generate_academic_wordlist()

        # Enregistrer la tentative de craquage en base
        try:
            DatabaseService.save_cracking_attempt(
                db=db,
                attempt_id=job.job_id,
                network_ssid=job.network_ssid,
                network_bssid=job.network_bssid,
                cracking_method=job.method.value,
                wordlist_path=wordlist_path,
                wordlist_name=request.wordlist,
                handshake_id=handshake_db_id,
                wordlist_size=job.wordlist_size,
                gpu_enabled=request.gpu_enabled,
                notes="Attempt started from /api/cracking/start"
            )
        except Exception:
            # Ne bloque pas le workflow si la persistance échoue.
            pass
        
        # Lancer le job directement en arrière-plan (sans await bloking)
        await CrackingService.launch_cracking_job_background(
            job=job,
            handshake_file=handshake_file,
            wordlist_path=wordlist_path
        )
        
        return {
            "job_id": job.job_id,
            "network_bssid": job.network_bssid,
            "network_ssid": job.network_ssid,
            "method": job.method.value,
            "status": "background_running",
            "progress": 0,
            "message": "Craquage lancé directement en arrière-plan sans terminal. Utilisez /api/cracking/job/{job_id} pour monitorer",
            "poll_url": f"/api/cracking/job/{job.job_id}"
        }
    except ValueError as ve:
        logger.error(f"Validation error in cracking start: {str(ve)}")
        raise HTTPException(status_code=422, detail=f"Validation error: {str(ve)}")
    except Exception as e:
        logger.error(f"Error in cracking start: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/job/{job_id}")
async def get_job_status(job_id: str):
    """
    Récupère le statut d'un travail de craquage.
    
    Args:
        job_id: ID du travail
        
    Returns:
        Statut détaillé du travail
    """
    job = CrackingService.get_job_status(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} non trouvé")
    
    response = {
        "job_id": job.job_id,
        "network_bssid": job.network_bssid,
        "network_ssid": job.network_ssid,
        "status": job.status,
        "progress": job.progress,
        "wordlist_size": job.wordlist_size,
        "wordlist_name": job.wordlist_name,
        "method": job.method,
        "attempts": job.attempts,
        "gpu_enabled": job.gpu_enabled,
    }
    
    if job.start_time:
        response["start_time"] = job.start_time.isoformat()
    if job.end_time:
        response["end_time"] = job.end_time.isoformat()
    if job.password_found:
        response["password_found"] = job.password_found
    if job.error_message:
        response["error_message"] = job.error_message
    
    return response


@router.get("/jobs")
async def list_all_jobs():
    """
    Liste tous les travaux actifs.
    
    Returns:
        Liste des travaux actifs et leurs statuts
    """
    jobs = CrackingService.list_jobs()
    
    return {
        "total": len(jobs),
        "jobs": [
            {
                "job_id": job.job_id,
                "network_bssid": job.network_bssid,
                "network_ssid": job.network_ssid,
                "status": job.status,
                "progress": job.progress,
                "method": job.method,
                "password_found": job.password_found,
            }
            for job in jobs
        ]
    }


@router.post("/job/{job_id}/pause")
async def pause_job(job_id: str):
    """
    Met en pause un travail de craquage.
    
    Args:
        job_id: ID du travail
        
    Returns:
        Statut de l'opération
    """
    success = CrackingService.pause_job(job_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Job {job_id} non trouvé ou non pausable")
    
    return {
        "success": True,
        "job_id": job_id,
        "message": "Travail mis en pause"
    }


@router.post("/job/{job_id}/cancel")
async def cancel_job(job_id: str):
    """
    Annule un travail de craquage.
    
    Args:
        job_id: ID du travail
        
    Returns:
        Statut de l'opération
    """
    success = CrackingService.cancel_job(job_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Job {job_id} non trouvé")
    
    return {
        "success": True,
        "job_id": job_id,
        "message": "Travail annulé"
    }


@router.get("/methods")
async def get_cracking_methods():
    """
    Récupère les méthodes de craquage disponibles.
    
    Returns:
        Dict des méthodes avec détails
    """
    return {
        "aircrack-ng": {
            "name": "Aircrack-ng",
            "description": "Craquage WEP/WPA/WPA2 par dictionnaire et force brute",
            "speed": "Lent mais fiable",
            "is_available": CrackingService._is_tool_available("aircrack-ng"),
            "requires_handshake": True,
            "supported_protocols": ["WEP", "WPA", "WPA2"],
            "best_for": "Tests académiques, Linx/MacOS",
            "tutorial": "https://www.aircrack-ng.org/doku.php"
        },
        "hashcat": {
            "name": "Hashcat",
            "description": "GPU-acceleré craquage ultra-rapide",
            "speed": "Puissant avec GPU",
            "is_available": CrackingService._is_tool_available("hashcat"),
            "requires_handshake": True,
            "gpu_support": True,
            "supported_protocols": ["WPA", "WPA2", "WPA3"],
            "best_for": "Productions, tests de performance",
            "tutorial": "https://hashcat.net/wiki/"
        },
        "john": {
            "name": "John the Ripper",
            "description": "Craquage polyvalent WPA/WPA2",
            "speed": "Modéré",
            "is_available": CrackingService._is_tool_available("john"),
            "requires_handshake": True,
            "supported_protocols": ["WPA", "WPA2"],
            "best_for": "Tests croisés, validations",
            "tutorial": "https://www.openwall.com/john/"
        }
    }


@router.get("/handshake-capture-guide")
async def get_handshake_capture_guide():
    """
    Retourne un guide pour capturer les handshakes WPA/WPA2.
    
    Returns:
        Instructions de capture pour différentes plateformes
    """
    return {
        "overview": "Pour cracker un réseau WPA/WPA2, un handshake 4-way doit d'abord être capturé",
        "linux_guide": {
            "step1": "airmon-ng start wlan0",
            "step2": "airodump-ng wlan0mon",
            "step3": "airodump-ng -c [channel] -w capture -b [BSSID] wlan0mon",
            "step4": "aireplay-ng -0 1 -a [BSSID] wlan0mon  (déconnecte un client)",
            "step5": "Un client se reconnecte, handshake capturé",
            "result": "capture-01.cap (contient le handshake)"
        },
        "windows_guide": {
            "note": "Requiere une carte Wi-Fi compatible monitor mode",
            "tools": ["NetAdapter", "Wireshark Npcap", "Aircrack-ng pour Windows"],
            "step1": "Installer CommView ou kismet-agent",
            "step2": "Capturer le handshake lors de la reconnexion d'un client",
            "challenge": "Mode monitor limité sur Windows - WSL2 avec USB adaptateur recommandé"
        },
        "wpa3_note": {
            "protocol": "WPA3 (SAE)",
            "challenge": "SAE (Simultaneous Authentication of Equals) résiste bien aux attaques hors ligne",
            "feasibility": "Attaques en-ligne (PMKID) plus viables pour WPA3",
            "tool": "hashcat -m 16800 (WPA3-PSK supporte le PMKID)"
        }
    }
