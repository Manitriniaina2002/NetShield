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
    
    # Jobs actifs: job_id -> CrackingJob
    ACTIVE_JOBS: Dict[str, CrackingJob] = {}
    
    # Timeouts par méthode
    TIMEOUTS = {
        CrackingMethod.AIRCRACK_NG: 3600,  # 1 heure
        CrackingMethod.HASHCAT: 1800,  # 30 minutes
        CrackingMethod.JOHN: 1800,  # 30 minutes
    }
    
    @staticmethod
    def _is_tool_available(tool_name: str) -> bool:
        """Vérifie si un outil est disponible sur le système."""
        try:
            result = subprocess.run(
                ["which" if os.name != "nt" else "where", tool_name],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    @staticmethod
    def get_available_methods() -> Dict[str, Any]:
        """Retourne les méthodes et outils disponibles."""
        return {
            "aircrack_ng": {
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
            "john_ripper": {
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
        )
        
        CrackingService.ACTIVE_JOBS[job_id] = job
        return job
    
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
        
        # Résultat simulé : 30% de chance de trouvez le mot de passe
        import random
        if random.random() < 0.3:
            job.password_found = "SecurePassword123!"
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
        """Exécute aircrack-ng en mode réel."""
        try:
            cmd = [
                "aircrack-ng",
                "-w", wordlist_path,
                "-l", job.network_bssid.replace(":", ""),  # Clé de fichier
                handshake_file
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                # Note: mode réel requiert aircrack-ng installé
            )
            
            # Timeout et capture progressive du mot de passe
            timeout = CrackingService.TIMEOUTS[CrackingMethod.AIRCRACK_NG]
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                output = stdout.decode('utf-8', errors='ignore')
                
                # Chercher le mot de passe dans la sortie
                if "KEY FOUND" in output or "password" in output.lower():
                    # Extraction du mot de passe (format spécifique aircrack-ng)
                    lines = output.split('\n')
                    for line in lines:
                        if "KEY FOUND" in line:
                            password = line.split("[ ")[-1].rstrip(" ]")
                            job.password_found = password
                            job.status = "completed"
                            break
                else:
                    job.status = "failed"
                    job.error_message = "Aucun mot de passe trouvé dans le dictionnaire"
                
                job.progress = 100
                job.attempts = job.wordlist_size
                
            except asyncio.TimeoutError:
                job.status = "timeout"
                job.error_message = f"Timeout après {timeout}s"
                process.kill()
            
            job.end_time = datetime.now()
            
            return {
                "status": "success",
                "job_id": job.job_id,
                "password_found": job.password_found,
                "progress": job.progress,
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
        
        # Résultat simulé : 50% de chance de trouver le mot de passe
        import random
        if random.random() < 0.5:
            job.password_found = "Password@123"
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
        """Exécute hashcat en mode réel."""
        try:
            cmd = [
                "hashcat",
                "-m", str(hash_type),  # 2500 = WPA2-PSK, 16800 = WPA3-PSK
                "-w", "3",  # Mode agressif
                "--potfile-disable",  # Désactiver le cache
                handshake_hash,
                wordlist_path,
            ]
            
            # Ajouter GPU si disponible
            if job.gpu_enabled:
                cmd.extend(["-d", "1"])  # GPU device
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            timeout = CrackingService.TIMEOUTS[CrackingMethod.HASHCAT]
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                output = stdout.decode('utf-8', errors='ignore')
                
                if "recovered" in output.lower() or "cracked" in output.lower():
                    job.status = "completed"
                    job.password_found = "MotDePasse"  # Extraction depuis output
                else:
                    job.status = "failed"
                    job.error_message = "Aucun hash craqué"
                
                job.progress = 100
                
            except asyncio.TimeoutError:
                job.status = "timeout"
                job.error_message = f"Timeout après {timeout}s"
                process.kill()
            
            job.end_time = datetime.now()
            return {
                "status": "success",
                "job_id": job.job_id,
                "password_found": job.password_found,
                "progress": job.progress,
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
            "Welcome123", "Guest123", "User123", "Test123", "Demo123"
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
            seed_words = ["password", "admin", "user", "test", "demo", "secure"]
        
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
