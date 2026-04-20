"""Service de craquage de mots de passe Wi-Fi et de capture de handshakes."""
import asyncio
import os
import uuid
import tempfile
import subprocess
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel

from app.config import get_settings
from app.models.wifi import WiFiNetwork, SecurityLevel


class CrackingMethod(str, Enum):
    """Méthodes de craquage disponibles."""
    AIRCRACK_NG = "aircrack-ng"
    HASHCAT = "hashcat"
    JOHN = "john"


class HandshakeFormat(str, Enum):
    """Formats de capture de handshake."""
    PCAP = "pcap"
    CAP = "cap"
    PCAPNG = "pcapng"
    HCCAPX = "hccapx"


class CrackingJob(BaseModel):
    """Modèle d'un travail de craquage."""
    job_id: str
    network_bssid: str
    network_ssid: str
    method: CrackingMethod
    status: str  # pending, running, paused, completed, failed
    progress: int  # 0-100
    wordlist_size: int
    wordlist_name: str
    handshake_file: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    password_found: Optional[str] = None
    attempts: int = 0
    error_message: Optional[str] = None
    gpu_enabled: bool = False
    expected_outcome: Optional[str] = None  # success | fail | None
    expected_reason: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class CrackingService:
    """Service de craquage de réseaux Wi-Fi."""
    
    # Dictionnaires fournis avec le backend
    WORDLISTS = {
        "rockyou": {"size": 14344391, "path": "/usr/share/wordlists/rockyou.txt"},
        "common": {"size": 1200, "path": None},  # Généré localement
        "academic": {"size": 5000, "path": None},  # Généré localement
    }

    # Mots de passe attendus pour le flux demo (par BSSID)
    DEMO_EXPECTED_PASSWORDS = {
        "BB:CC:DD:EE:FF:02": "Butterfly2024!",  # HomeWifi-Plus
        "AA:BB:CC:DD:EE:01": "SecurePass123!",  # Corporate demo
        "DD:EE:FF:00:11:04": "5A6F6E6173",      # Legacy WEP demo
    }

    DEMO_EXPECTED_FAILURES = {
        "FF:00:11:22:33:06": "Reseau demo securise (WPA3 fort): echec attendu."
    }
    
    # Jobs actifs: job_id -> CrackingJob
    ACTIVE_JOBS: Dict[str, CrackingJob] = {}
    
    # Background tasks pour gestion directe: job_id -> asyncio.Task
    BACKGROUND_TASKS: Dict[str, asyncio.Task] = {}
    
    # Timeouts par méthode
    TIMEOUTS = {
        CrackingMethod.AIRCRACK_NG: 3600,  # 1 heure
        CrackingMethod.HASHCAT: 1800,  # 30 minutes
        CrackingMethod.JOHN: 1800,  # 30 minutes
    }
    
    @staticmethod
    def _wsl_available() -> bool:
        """Vérifie si WSL2 est disponible sur Windows."""
        if os.name != "nt":
            return False
        try:
            result = subprocess.run(
                ["wsl", "--list", "--verbose"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
                check=False,
            )
            return result.returncode == 0
        except Exception:
            return False

    @staticmethod
    def _is_tool_available_in_wsl(tool_name: str) -> bool:
        """Vérifie si un outil est disponible dans WSL."""
        if not CrackingService._wsl_available():
            return False
        try:
            result = subprocess.run(
                ["wsl", "which", tool_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
                check=False,
            )
            return result.returncode == 0
        except Exception:
            return False

    @staticmethod
    def _is_tool_available(tool_name: str) -> bool:
        """Vérifie si un outil est disponible sur le système (Windows ou WSL)."""
        try:
            # D'abord vérifier Windows natif (pour hashcat, etc.)
            result = subprocess.run(
                ["where" if os.name == "nt" else "which", tool_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return True
            
            # Si sur Windows et pas trouvé, vérifier WSL
            if os.name == "nt":
                return CrackingService._is_tool_available_in_wsl(tool_name)
            
            return False
        except Exception:
            return False
    
    @staticmethod
    def _is_tool_available_sync(tool_name: str) -> bool:
        """Vérification synchrone de disponibilité d'outils (pour startup)."""
        return CrackingService._is_tool_available(tool_name)
    
    @staticmethod
    def get_available_methods() -> Dict[str, Any]:
        """Retourne les méthodes et outils disponibles."""
        return {
            "aircrack-ng": {
                "available": CrackingService._is_tool_available("aircrack-ng"),
                "description": "Craquage de clés WEP/WPA/WPA2 par force brute",
                "requires": ["airodump-ng", "aircrack-ng"],
                "platforms": ["linux", "macos"],
                "speed": "Lente mais efficace",
            },
            "hashcat": {
                "available": CrackingService._is_tool_available("hashcat"),
                "description": "Craquage GPU ultra-rapide (WPA/WPA2/WPA3)",
                "requires": ["hashcat", "opencl-icd", "cuda"],
                "platforms": ["linux", "windows", "macos"],
                "speed": "Ultra-rapide avec GPU",
                "gpu_support": True,
            },
            "john": {
                "available": CrackingService._is_tool_available("john"),
                "description": "John the Ripper - Craquage polyvalent",
                "requires": ["john"],
                "platforms": ["linux", "windows", "macos"],
                "speed": "Rapide",
            }
        }
    
    @staticmethod
    def create_job(
        network: WiFiNetwork,
        method: CrackingMethod,
        wordlist: str = "rockyou",
        gpu_enabled: bool = False
    ) -> CrackingJob:
        """
        Crée un nouveau travail de craquage.
        
        Args:
            network: Réseau Wi-Fi cible
            method: Méthode de craquage
            wordlist: Dictionnaire à utiliser
            gpu_enabled: Activer l'accélération GPU si disponible
            
        Returns:
            Travail de craquage créé
        """
        job_id = str(uuid.uuid4())[:8]
        
        bssid_upper = (network.bssid or "").upper()
        expected_outcome = None
        expected_reason = None
        if bssid_upper in CrackingService.DEMO_EXPECTED_PASSWORDS:
            expected_outcome = "success"
            expected_reason = "Mot de passe de démonstration attendu si présent dans le dictionnaire."
        elif bssid_upper in CrackingService.DEMO_EXPECTED_FAILURES:
            expected_outcome = "fail"
            expected_reason = CrackingService.DEMO_EXPECTED_FAILURES[bssid_upper]

        job = CrackingJob(
            job_id=job_id,
            network_bssid=network.bssid,
            network_ssid=network.ssid,
            method=method,
            status="pending",
            progress=0,
            wordlist_size=CrackingService.WORDLISTS.get(wordlist, {}).get("size", 0),
            wordlist_name=wordlist,
            gpu_enabled=gpu_enabled and method == CrackingMethod.HASHCAT,
            expected_outcome=expected_outcome,
            expected_reason=expected_reason,
        )
        
        CrackingService.ACTIVE_JOBS[job_id] = job
        return job
    
    @staticmethod
    async def launch_cracking_job_background(
        job: CrackingJob,
        handshake_file: str,
        wordlist_path: str
    ) -> Dict[str, Any]:
        """
        Lance un travail de craquage en arrière-plan directement.
        
        Linux optimisé: Subprocess direct sans overhead
        Returns immédiatement avec job_id pour polling
        """
        settings = get_settings()
        job.status = "running"
        job.start_time = datetime.now()

        use_simulation = settings.simulation_mode or CrackingService._is_demo_network(job)
        
        # Créer une task asyncio pour exécuter le craquage en arrière-plan
        if use_simulation:
            if job.method == CrackingMethod.HASHCAT:
                task = asyncio.create_task(CrackingService._simulate_hashcat(job, wordlist_path))
            else:
                task = asyncio.create_task(CrackingService._simulate_aircrack(job, wordlist_path))
        elif job.method == CrackingMethod.AIRCRACK_NG:
            task = asyncio.create_task(
                CrackingService._run_real_aircrack(job, handshake_file, wordlist_path)
            )
        elif job.method == CrackingMethod.HASHCAT:
            task = asyncio.create_task(
                CrackingService._run_real_hashcat(job, handshake_file, wordlist_path, 2500)
            )
        else:
            task = asyncio.create_task(CrackingService._simulate_aircrack(job, wordlist_path))
        
        CrackingService.BACKGROUND_TASKS[job.job_id] = task
        
        # Ajouter un callback pour nettoyer la task quand elle termine
        def task_done_callback(task):
            if job.job_id in CrackingService.BACKGROUND_TASKS:
                del CrackingService.BACKGROUND_TASKS[job.job_id]
        
        task.add_done_callback(task_done_callback)
        
        return {
            "status": "background_launched",
            "job_id": job.job_id,
            "message": f"Craquage lancé en arrière-plan sur {job.method.value}",
            "poll_url": f"/api/cracking/job/{job.job_id}"
        }

    @staticmethod
    def _is_demo_network(job: CrackingJob) -> bool:
        """Détecte si le job cible un réseau de démonstration."""
        if (job.network_bssid or "").upper() in CrackingService.DEMO_EXPECTED_PASSWORDS:
            return True
        ssid = (job.network_ssid or "").lower()
        return any(k in ssid for k in ["guest", "legacy", "homewifi", "corporate", "routeradmin", "demo"])

    @staticmethod
    def _resolve_expected_demo_password(job: CrackingJob, wordlist_path: str) -> Optional[str]:
        """Retourne le mot de passe demo si présent dans le dictionnaire sélectionné."""
        expected = CrackingService.DEMO_EXPECTED_PASSWORDS.get((job.network_bssid or "").upper())
        if not expected:
            return None

        # Si le chemin du dictionnaire est absent (ex: rockyou non installé),
        # on garde un comportement déterministe pour les cibles demo de réussite.
        if not wordlist_path:
            return expected

        if not os.path.exists(wordlist_path):
            return None

        try:
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.strip() == expected:
                        return expected
        except Exception:
            return None

        return None
    
    @staticmethod
    async def start_aircrack_job(
        job: CrackingJob,
        handshake_file: str,
        wordlist_path: str
    ) -> Dict[str, Any]:
        """
        Lance un travail aircrack-ng.
        
        Mode simulation: retourne un résultat simulé
        Mode réel: exécute aircrack-ng avec le fichier handshake
        """
        settings = get_settings()
        job.status = "running"
        job.start_time = datetime.now()
        job.handshake_file = handshake_file
        
        if settings.simulation_mode:
            return await CrackingService._simulate_aircrack(job, wordlist_path)
        
        return await CrackingService._run_real_aircrack(job, handshake_file, wordlist_path)
    
    @staticmethod
    async def _simulate_aircrack(job: CrackingJob, wordlist_path: str) -> Dict[str, Any]:
        """Simule l'exécution d'aircrack en mode simulation."""
        # Simulation: progression graduelle
        for progress in range(0, 101, 10):
            job.progress = progress
            job.attempts = int(job.wordlist_size * (progress / 100))
            await asyncio.sleep(0.5)  # Simule le délai

        if job.expected_outcome == "fail":
            job.status = "failed"
            job.error_message = "Key not found in wordlist"
            job.progress = 100
            job.end_time = datetime.now()
            return {
                "status": "success",
                "job_id": job.job_id,
                "password_found": None,
                "progress": job.progress,
            }
        
        # Résultat simulé demo: déterministe selon le dictionnaire.
        expected = CrackingService._resolve_expected_demo_password(job, wordlist_path)
        if expected:
            job.password_found = expected
            job.status = "completed"
        else:
            job.status = "failed"
            job.error_message = "Aucun mot de passe trouvé dans le dictionnaire"
        
        job.progress = 100
        job.end_time = datetime.now()
        return {
            "status": "success",
            "job_id": job.job_id,
            "password_found": job.password_found,
            "progress": job.progress,
        }
    
    @staticmethod
    async def _run_real_aircrack(
        job: CrackingJob,
        handshake_file: str,
        wordlist_path: str
    ) -> Dict[str, Any]:
        """
        Exécute aircrack-ng en mode réel directement.
        
        Linux: Subprocess sans terminal, capture stdout/stderr directement
        Windows: Via WSL2 si disponible
        """
        try:
            import platform as pl
            is_linux = pl.system() == "Linux"
            use_wsl = False
            
            # Sur Windows, vérifier si WSL est disponible
            if not is_linux and os.name == 'nt':
                if CrackingService._wsl_available():
                    use_wsl = True
            
            if use_wsl:
                # Utiliser WSL pour exécuter aircrack-ng
                cmd = [
                    "wsl",
                    "aircrack-ng",
                    "-w", wordlist_path,
                    "-l", job.network_bssid.replace(":", ""),
                    handshake_file
                ]
            else:
                cmd = [
                    "aircrack-ng",
                    "-w", wordlist_path,
                    "-l", job.network_bssid.replace(":", ""),
                    handshake_file
                ]
            
            # Configuration subprocess pour éviter les fenêtres terminales
            kwargs = {
                "stdout": asyncio.subprocess.PIPE,
                "stderr": asyncio.subprocess.PIPE,
            }
            
            # Windows: CREATE_NO_WINDOW équivalent via startupinfo
            if not is_linux and os.name == 'nt':
                si = subprocess.STARTUPINFO()
                # HIDE_WINDOW may not be available in all Python versions
                if hasattr(subprocess, 'HIDE_WINDOW'):
                    si.dwFlags |= subprocess.HIDE_WINDOW
                else:
                    # Fallback: use the raw value (0x08)
                    si.dwFlags |= 0x08
                kwargs["startupinfo"] = si
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                **kwargs
            )
            
            timeout = CrackingService.TIMEOUTS[CrackingMethod.AIRCRACK_NG]
            
            # Lance le subprocess et monitore la progression
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                output = stdout.decode('utf-8', errors='ignore')
                error_output = stderr.decode('utf-8', errors='ignore')
                
                # Parser la sortie aircrack-ng
                if "KEY FOUND" in output:
                    # Format: [ AA:BB:CC:DD:EE:FF ]
                    lines = output.split('\n')
                    for line in lines:
                        if "KEY FOUND" in line:
                            password = line.split("[ ")[-1].rstrip(" ]")
                            job.password_found = password
                            job.status = "completed"
                            job.progress = 100
                            break
                else:
                    job.status = "failed"
                    job.error_message = "Key not found in wordlist"
                    job.progress = 100
                
                job.attempts = job.wordlist_size
                
            except asyncio.TimeoutError:
                job.status = "timeout"
                job.error_message = f"Timeout après {timeout}s"
                job.progress = 100
                try:
                    process.kill()
                    await asyncio.sleep(0.1)
                except:
                    pass
            
            job.end_time = datetime.now()
            
            return {
                "status": "success",
                "job_id": job.job_id,
                "password_found": job.password_found,
                "progress": job.progress,
                "platform": pl.system()
            }
            
        except FileNotFoundError:
            job.status = "failed"
            job.error_message = "aircrack-ng not found in PATH. Install: apt install aircrack-ng"
            job.end_time = datetime.now()
            return {
                "status": "error",
                "job_id": job.job_id,
                "error": "aircrack-ng not installed",
                "install_command": "sudo apt install aircrack-ng"
            }
            
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            job.end_time = datetime.now()
            return {
                "status": "error",
                "job_id": job.job_id,
                "error": str(e),
            }
    
    @staticmethod
    async def start_hashcat_job(
        job: CrackingJob,
        handshake_hash: str,
        wordlist_path: str,
        hash_type: int
    ) -> Dict[str, Any]:
        """
        Lance un travail hashcat.
        
        Hash types:
        - 2500: WPA-PSK
        - 2501: WPA-PSK-PMK (hashcat -m 2501)
        - 16800: WPA-3-PSK (SAE)
        """
        settings = get_settings()
        job.status = "running"
        job.start_time = datetime.now()
        
        if settings.simulation_mode:
            return await CrackingService._simulate_hashcat(job, wordlist_path)
        
        return await CrackingService._run_real_hashcat(
            job, handshake_hash, wordlist_path, hash_type
        )
    
    @staticmethod
    async def _simulate_hashcat(job: CrackingJob, wordlist_path: str) -> Dict[str, Any]:
        """Simule l'exécution de hashcat en mode simulation."""
        # Simule la progression (plus rapide que aircrack)
        for progress in [10, 25, 50, 75, 90, 100]:
            job.progress = progress
            job.attempts = int(job.wordlist_size * (progress / 100))
            await asyncio.sleep(0.3)

        if job.expected_outcome == "fail":
            job.status = "failed"
            job.error_message = "Key not found in wordlist"
            job.end_time = datetime.now()
            return {
                "status": "success",
                "job_id": job.job_id,
                "password_found": None,
                "progress": job.progress,
            }
        
        # Résultat simulé demo: déterministe selon le dictionnaire.
        expected = CrackingService._resolve_expected_demo_password(job, wordlist_path)
        if expected:
            job.password_found = expected
            job.status = "completed"
        else:
            job.status = "failed"
            job.error_message = "Aucun mot de passe trouvé"
        
        job.end_time = datetime.now()
        return {
            "status": "success",
            "job_id": job.job_id,
            "password_found": job.password_found,
            "progress": job.progress,
        }
    
    @staticmethod
    async def _run_real_hashcat(
        job: CrackingJob,
        handshake_hash: str,
        wordlist_path: str,
        hash_type: int
    ) -> Dict[str, Any]:
        """
        Exécute hashcat en mode réel directement.
        
        Linux: Subprocess sans terminal, GPU support natif
        Windows: Native hashcat si disponible, sinon via WSL2
        macOS: Metal GPU support
        """
        try:
            import platform as pl
            is_linux = pl.system() == "Linux"
            use_wsl = False
            
            # Sur Windows, vérifier si WSL est disponible et hashcat natif ne l'est pas
            if not is_linux and os.name == 'nt':
                if not CrackingService._is_tool_available("hashcat"):
                    if CrackingService._wsl_available():
                        use_wsl = True
            
            if use_wsl:
                # Utiliser WSL pour exécuter hashcat
                cmd = [
                    "wsl",
                    "hashcat",
                    "-m", str(hash_type),  # 2500 = WPA2-PSK, 16800 = WPA3-PSK
                    "-w", "3",  # Mode agressif
                    "--potfile-disable",  # Désactiver le cache
                    "--quiet",  # Moins de sortie verbale (Linux friendly)
                    handshake_hash,
                    wordlist_path,
                ]
            else:
                cmd = [
                    "hashcat",
                    "-m", str(hash_type),  # 2500 = WPA2-PSK, 16800 = WPA3-PSK
                    "-w", "3",  # Mode agressif
                    "--potfile-disable",  # Désactiver le cache
                    "--quiet",  # Moins de sortie verbale (Linux friendly)
                    handshake_hash,
                    wordlist_path,
                ]
            
            # Configuration subprocess pour éviter les fenêtres terminales
            kwargs = {
                "stdout": asyncio.subprocess.PIPE,
                "stderr": asyncio.subprocess.PIPE,
            }
            
            # Ajouter GPU sur Linux si disponible
            if is_linux and job.gpu_enabled and not use_wsl:
                cmd.extend(["-d", "1"])  # GPU device 1
            
            # Windows: CREATE_NO_WINDOW
            if not is_linux and os.name == 'nt':
                si = subprocess.STARTUPINFO()
                # HIDE_WINDOW may not be available in all Python versions
                if hasattr(subprocess, 'HIDE_WINDOW'):
                    si.dwFlags |= subprocess.HIDE_WINDOW
                else:
                    # Fallback: use the raw value (0x08)
                    si.dwFlags |= 0x08
                kwargs["startupinfo"] = si
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                **kwargs
            )
            
            timeout = CrackingService.TIMEOUTS[CrackingMethod.HASHCAT]
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                output = stdout.decode('utf-8', errors='ignore')
                error_output = stderr.decode('utf-8', errors='ignore')
                
                # Parser la sortie hashcat
                if "recovered" in output.lower() or "status" in output.lower():
                    # Extraction du mot de passe trouvé
                    # Format: hash:password
                    lines = output.split('\n')
                    for line in lines:
                        if ":" in line and len(line) > 20:
                            parts = line.split(":")
                            if len(parts) >= 2:
                                job.password_found = parts[-1].strip()
                                job.status = "completed"
                                break
                    
                    if not job.password_found:
                        job.status = "failed"
                        job.error_message = "No candidates left"
                else:
                    job.status = "failed"
                    job.error_message = "Hash not cracked"
                
                job.progress = 100
                
            except asyncio.TimeoutError:
                job.status = "timeout"
                job.error_message = f"Timeout après {timeout}s"
                job.progress = 100
                try:
                    process.kill()
                    await asyncio.sleep(0.1)
                except:
                    pass
            
            job.end_time = datetime.now()
            
            return {
                "status": "success",
                "job_id": job.job_id,
                "password_found": job.password_found,
                "progress": job.progress,
                "gpu_used": job.gpu_enabled and is_linux
            }
            
        except FileNotFoundError:
            job.status = "failed"
            job.error_message = "hashcat not found. Install: apt install hashcat"
            job.end_time = datetime.now()
            return {
                "status": "error",
                "job_id": job.job_id,
                "error": "hashcat not installed",
                "install_command": "sudo apt install hashcat (or use pre-built binary)"
            }
            
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            job.end_time = datetime.now()
            return {
                "status": "error",
                "job_id": job.job_id,
                "error": str(e),
            }
    
    @staticmethod
    def get_job_status(job_id: str) -> Optional[CrackingJob]:
        """Retourne le statut d'un travail de craquage."""
        return CrackingService.ACTIVE_JOBS.get(job_id)
    
    @staticmethod
    def list_jobs() -> List[CrackingJob]:
        """Retourne tous les travaux actifs."""
        # Nettoyer les jobs terminés depuis plus d'1 heure
        now = datetime.now()
        expired_jobs = [
            job_id for job_id, job in CrackingService.ACTIVE_JOBS.items()
            if job.end_time and (now - job.end_time) > timedelta(hours=1)
        ]
        for job_id in expired_jobs:
            del CrackingService.ACTIVE_JOBS[job_id]
        
        return list(CrackingService.ACTIVE_JOBS.values())
    
    @staticmethod
    def pause_job(job_id: str) -> bool:
        """Pause un travail (simule la mise en pause)."""
        if job_id in CrackingService.ACTIVE_JOBS:
            job = CrackingService.ACTIVE_JOBS[job_id]
            if job.status == "running":
                job.status = "paused"
                return True
        return False
    
    @staticmethod
    def cancel_job(job_id: str) -> bool:
        """Annule un travail."""
        if job_id in CrackingService.ACTIVE_JOBS:
            job = CrackingService.ACTIVE_JOBS[job_id]
            job.status = "failed"
            job.error_message = "Annulé par l'utilisateur"
            job.end_time = datetime.now()
            return True
        return False
    
    @staticmethod
    def generate_common_wordlist() -> str:
        """
        Génère une liste de mots courants pour les tests académiques.
        
        Returns:
            Chemin du fichier wordlist généré
        """
        common_passwords = [
            "password", "123456", "12345678", "qwerty", "abc123",
            "monkey", "1234567", "letmein", "trustme", "dragon",
            "baseball", "111111", "iloveyou", "master", "sunshine",
            "ashley", "bailey", "passw0rd", "shadow", "123123",
            "654321", "superman", "qazwsx", "michael", "football",
            "wifi123", "wifipass", "networkpass", "secure123", "admin123",
            "password123", "Password123", "Password@123", "SecurePass123",
            "Welcome123", "Guest123", "User123", "Test123", "Demo123",
            "Butterfly2024!", "Password2024", "SecurePass123!",
            "Adesolaire2025"
        ]
        
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False,
            encoding='utf-8'
        ) as f:
            for pwd in common_passwords:
                f.write(pwd + '\n')
            return f.name
    
    @staticmethod
    def generate_academic_wordlist(
        length: int = 5000,
        seed_words: Optional[List[str]] = None
    ) -> str:
        """
        Génère un dictionnaire académique pour les tests.
        
        Args:
            length: Nombre de mots à générer
            seed_words: Mots de base à combiner
            
        Returns:
            Chemin du fichier wordlist généré
        """
        import random
        import string
        
        if not seed_words:
            seed_words = [
                "password", "admin", "user", "test", "demo", "secure",
                "Butterfly2024!", "Password2024", "SecurePass123!"
            ]
        
        passwords = set(seed_words)
        
        # Variantes numériques et spéciales
        for word in seed_words:
            for i in range(100, 110):
                passwords.add(f"{word}{i}")
            passwords.add(f"{word}!")
            passwords.add(f"{word}@")
            passwords.add(f"{word}#")
        
        # Mots aléatoires
        while len(passwords) < length:
            word = ''.join(random.choices(string.ascii_lowercase, k=6))
            passwords.add(word)
        
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False,
            encoding='utf-8'
        ) as f:
            for pwd in list(passwords)[:length]:
                f.write(pwd + '\n')
            return f.name
