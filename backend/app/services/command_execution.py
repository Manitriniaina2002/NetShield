"""Services d'exécution de commandes sécurisée"""
import subprocess
import asyncio
import json
import os
import getpass
from typing import Dict, Any, List, Optional
from app.config import get_settings


class CommandExecutionService:
    """Service sécurisé d'exécution de commandes système"""
    
    # Commandes autorisées (whitelist)
    ALLOWED_COMMANDS = {
        "ifconfig": "Affiche les interfaces réseau",
        "ip": "Commandes réseau avancées",
        "airmon-ng": "Activer/désactiver le mode monitor",
        "airodump-ng": "Scanner les réseaux Wi-Fi",
        "ps": "Lister les processus",
        "kill": "Terminer un processus"
    }
    
    # Stockage des sessions authentifiées (session_id -> timestamp)
    AUTHENTICATED_SESSIONS: Dict[str, float] = {}
    
    # Durée de vie d'une session auth (en secondes)
    SESSION_LIFETIME = 3600  # 1 heure
    
    @staticmethod
    async def verify_admin_auth(password: str, session_id: str = None) -> Dict[str, Any]:
        """
        Vérifie l'authentification administrateur
        
        Mode Simulation: Accepte tout mot de passe (min. 4 caractères)
        Mode Réel Linux: Vérifie que le processus tourne en root (uid == 0)
        Mode Réel Windows: Vérifie que l'utilisateur est admin
        
        Args:
            password: Mot de passe administrateur
            session_id: ID de session à créer
            
        Returns:
            Succès de l'authentification et session ID
        """
        import time
        import uuid
        import logging
        
        logger = logging.getLogger(__name__)
        settings = get_settings()
        
        # En mode simulation, accepter tout mot de passe non vide
        if settings.simulation_mode:
            logger.info("Mode SIMULATION - Authentification par mot de passe")
            if password and len(password) >= 4:
                session_id = str(uuid.uuid4())
                CommandExecutionService.AUTHENTICATED_SESSIONS[session_id] = time.time()
                logger.info(f"✅ Authentification simulation réussie - Session: {session_id[:8]}...")
                return {
                    "success": True,
                    "session_id": session_id,
                    "message": "Authentification admin réussie (Mode Simulation)",
                    "expires_in": CommandExecutionService.SESSION_LIFETIME,
                    "mode": "simulation"
                }
            else:
                logger.warning("❌ Mot de passe trop court pour authentification simulation")
                return {
                    "success": False,
                    "error": "Mot de passe invalide (min. 4 caractères)",
                    "mode": "simulation"
                }
        
        # Mode réel: Vérifier les permissions root/admin
        logger.info("Mode RÉEL - Vérification des permissions root/admin")
        
        # Vérifie si on est Linux/Unix
        try:
            current_uid = os.geteuid()
            logger.info(f"Système Linux détecté - UID actuel: {current_uid}")
            
            if current_uid == 0:  # Nous sommes root
                session_id = str(uuid.uuid4())
                CommandExecutionService.AUTHENTICATED_SESSIONS[session_id] = time.time()
                logger.info(f"✅ Authentification ROOT Linux réussie - Session: {session_id[:8]}...")
                return {
                    "success": True,
                    "session_id": session_id,
                    "is_root": True,
                    "message": "Authentification ROOT réussie",
                    "expires_in": CommandExecutionService.SESSION_LIFETIME,
                    "mode": "real_linux"
                }
            else:
                logger.error(f"❌ Processus ne tourne pas en root (uid={current_uid})")
                return {
                    "success": False,
                    "error": f"Authentification échouée - Le processus doit tourner en root (uid=0). UID courant: {current_uid}",
                    "mode": "real_linux",
                    "current_uid": current_uid
                }
        
        except AttributeError:
            # Windows - utiliser la méthode Windows
            logger.info("Système Windows détecté")
            try:
                import ctypes
                is_admin = ctypes.windll.shell.IsUserAnAdmin()
                logger.info(f"Statut admin: {is_admin}")
                
                if is_admin:
                    session_id = str(uuid.uuid4())
                    CommandExecutionService.AUTHENTICATED_SESSIONS[session_id] = time.time()
                    logger.info(f"✅ Authentification ADMIN Windows réussie - Session: {session_id[:8]}...")
                    return {
                        "success": True,
                        "session_id": session_id,
                        "is_admin": True,
                        "message": "Authentification ADMIN réussie",
                        "expires_in": CommandExecutionService.SESSION_LIFETIME,
                        "mode": "real_windows"
                    }
                else:
                    logger.error("❌ L'utilisateur n'a pas les droits administrateur")
                    return {
                        "success": False,
                        "error": "Authentification échouée - Requiert les droits administrateur Windows",
                        "mode": "real_windows"
                    }
            except Exception as e:
                logger.error(f"❌ Erreur lors de la vérification Windows: {str(e)}")
                return {
                    "success": False,
                    "error": f"Erreur lors de la vérification admin: {str(e)}",
                    "mode": "real_windows"
                }
        
        except Exception as e:
            logger.error(f"❌ Erreur inattendue: {str(e)}")
            return {
                "success": False,
                "error": f"Erreur d'authentification: {str(e)}"
            }
    
    @staticmethod
    def verify_session(session_id: str) -> bool:
        """
        Vérifie si une session est valide et active
        
        Args:
            session_id: ID de session à vérifier
            
        Returns:
            True si la session est valide
        """
        import time
        
        if session_id not in CommandExecutionService.AUTHENTICATED_SESSIONS:
            return False
        
        # Vérifier que la session n'a pas expiré
        session_time = CommandExecutionService.AUTHENTICATED_SESSIONS[session_id]
        if time.time() - session_time > CommandExecutionService.SESSION_LIFETIME:
            del CommandExecutionService.AUTHENTICATED_SESSIONS[session_id]
            return False
        
        return True
    
    @staticmethod
    async def execute_command(
        command: str,
        args: List[str] = None,
        timeout: int = 30,
        session_id: str = None
    ) -> Dict[str, Any]:
        """
        Exécute une commande de manière sécurisée (simulation en mode laboratoire)
        
        Args:
            command: Commande à exécuter
            args: Arguments additionnels
            timeout: Timeout en secondes
            session_id: ID de session authentifiée
            
        Returns:
            Résultat de l'exécution
        """
        settings = get_settings()
        
        # Vérifier l'authentification
        if not session_id or not CommandExecutionService.verify_session(session_id):
            return {
                "success": False,
                "error": "Authentification requise - Utilisez /api/commands/auth d'abord",
                "code": 401,
                "require_auth": True
            }
        
        # Vérifier si la commande est autorisée
        if command not in CommandExecutionService.ALLOWED_COMMANDS:
            return {
                "success": False,
                "error": f"Commande non autorisée: {command}",
                "code": 403
            }
        
        # Si on est en mode simulation, retourner des données simulées
        if settings.simulation_mode:
            return await CommandExecutionService._simulate_command(command, args)
        
        # Sinon, exécuter la commande réelle (avec restrictions)
        try:
            cmd_list = [command] + (args or [])
            
            process = await asyncio.create_subprocess_exec(
                *cmd_list,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                return {
                    "success": False,
                    "error": "Commande timeout"
                }
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode('utf-8', errors='ignore'),
                "error": stderr.decode('utf-8', errors='ignore'),
                "code": process.returncode
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    async def _simulate_command(command: str, args: List[str]) -> Dict[str, Any]:
        """Simule l'exécution d'une commande"""
        
        if command == "ifconfig":
            return {
                "success": True,
                "output": """wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a00:27ff:fe26:30c7  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:26:30:c7  txqueuelen 1000  (Ethernet)
        RX packets 1024  bytes 512000 (512.0 MB)
        TX packets 512  bytes 256000 (256.0 MB)

wlan0mon: flags=4098<BROADCAST,SIMPLEX,MULTICAST>  mtu 1500"""
            }
        
        elif command == "airmon-ng":
            if args and args[0] == "start":
                return {
                    "success": True,
                    "output": f"Found 1 (0x)process: wlan0 and turn it into monitoring mode",
                    "info": {"interface": "wlan0mon", "mode": "monitor"}
                }
            elif args and args[0] == "stop":
                return {
                    "success": True,
                    "output": "Stopped monitor mode",
                    "info": { "interface": "wlan0", "mode": "managed"}
                }
        
        elif command == "airodump-ng":
            # Retourner des données de scan simulées
            return {
                "success": True,
                "output": "Scan terminé avec 6 réseaux détectés",
                "networks": 6
            }
        
        elif command == "ps":
            return {
                "success": True,
                "output": """PID   USER     COMMAND
1234  root     /sbin/wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf
5678  user     python wifi_scanner.py
9012  root     /usr/sbin/hostapd -B /etc/hostapd.conf"""
            }
        
        elif command == "kill":
            if args:
                return {
                    "success": True,
                    "output": f"Processus {args[0]} terminé"
                }
        
        return {
            "success": False,
            "error": "Commande non reconnue en mode simulation"
        }
