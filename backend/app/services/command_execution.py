"""Services d'execution de commandes securisee."""
import asyncio
import os
import platform
import shutil
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

from app.config import get_settings


class CommandExecutionService:
    """Service securise d'execution de commandes systeme."""

    # Commandes logiques exposees a l'UI/API.
    ALLOWED_COMMANDS = {
        # Commandes réseau (cross-platform)
        "ifconfig": "Afficher les interfaces reseau",
        "ip": "Commandes reseau avancees",
        "ipconfig": "Afficher configuration IP (Windows)",
        "netsh": "Commandes reseau avancees (Windows)",
        
        # Commandes Wi-Fi scanning (Linux)
        "airmon-ng": "Activer/desactiver le mode monitor (Linux)",
        "airodump-ng": "Scanner les reseaux Wi-Fi (Linux)",
        
        # Commandes Wi-Fi (Windows)
        "netsh_wlan_show": "Afficher reseaux Wi-Fi (Windows)",
        "netsh_wlan_interfaces": "Afficher interfaces Wi-Fi (Windows)",
        
        # Commandes de craquage (requires powerful hardware)
        "aircrack-ng": "Craquage WEP/WPA/WPA2 (Linux/macOS)",
        "hashcat": "GPU-accelerated password cracking",
        "john": "John the Ripper - craquage de mots de passe",
        
        # Commandes système
        "ps": "Lister les processus",
        "kill": "Terminer un processus",
        "tasklist": "Lister les processus (Windows)",
        "taskkill": "Terminer un processus (Windows)",
    }

    # Sessions authentifiees: session_id -> metadata
    AUTHENTICATED_SESSIONS: Dict[str, Dict[str, Any]] = {}
    SESSION_LIFETIME = 3600  # 1 heure

    @staticmethod
    def _platform_name() -> str:
        return platform.system().lower()

    @staticmethod
    def _is_admin_context() -> bool:
        """Retourne True si le processus a des privileges admin/root."""
        if os.name == "nt":
            try:
                import ctypes

                return bool(ctypes.windll.shell32.IsUserAnAdmin())
            except Exception:
                return False

        try:
            return os.geteuid() == 0
        except AttributeError:
            return False

    @staticmethod
    def _session_expired(created_at: float) -> bool:
        return (time.time() - created_at) > CommandExecutionService.SESSION_LIFETIME

    @staticmethod
    async def _verify_linux_sudo_password(password: str) -> Tuple[bool, str]:
        """Valide un mot de passe sudo via une vraie demande d'elevation."""
        if not password:
            return False, "Mot de passe root/admin requis en mode reel"

        try:
            process = await asyncio.create_subprocess_exec(
                "sudo",
                "-S",
                "-k",
                "-p",
                "",
                "-v",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _, stderr = await process.communicate(input=f"{password}\n".encode("utf-8"))

            if process.returncode != 0:
                error_text = stderr.decode("utf-8", errors="ignore").strip()
                if not error_text:
                    error_text = "Authentification root/admin invalide"
                return False, error_text

            return True, ""
        except FileNotFoundError:
            return False, "Commande 'sudo' introuvable sur ce systeme"
        except Exception as exc:
            return False, f"Erreur verification sudo: {str(exc)}"

    @staticmethod
    def get_runtime_info() -> Dict[str, Any]:
        """Expose les infos de compatibilite de la plateforme courante."""
        current_platform = CommandExecutionService._platform_name()
        linux_only = ["airmon-ng", "airodump-ng", "aircrack-ng", "john"]
        gpu_accelerated = ["hashcat"]

        return {
            "platform": current_platform,
            "is_admin_context": CommandExecutionService._is_admin_context(),
            "simulation_mode": get_settings().simulation_mode,
            "linux_only_commands": linux_only if current_platform == "windows" else [],
            "gpu_accelerated_commands": gpu_accelerated,
            "recommended_tools": {
                "cracking": "hashcat (GPU)" if current_platform != "windows" else "aircrack-ng (CPU via WSL2)",
                "handshake_capture": "airodump-ng (Linux/WSL2) / Wireshark (all platforms)"
            }
        }

    @staticmethod
    async def verify_admin_auth(password: str) -> Dict[str, Any]:
        """
        Verifie l'authentification administrateur.

        Mode simulation: tout mot de passe >= 4 caracteres.
        Mode reel: le backend doit deja tourner avec privileges admin/root.
        """
        settings = get_settings()

        if settings.simulation_mode:
            if not password or len(password) < 4:
                return {
                    "success": False,
                    "error": "Mot de passe invalide (minimum 4 caracteres)",
                    "mode": "simulation",
                }

            session_id = str(uuid.uuid4())
            CommandExecutionService.AUTHENTICATED_SESSIONS[session_id] = {
                "created_at": time.time(),
                "platform": CommandExecutionService._platform_name(),
                "mode": "simulation",
            }

            return {
                "success": True,
                "session_id": session_id,
                "message": "Authentification admin reussie (mode simulation)",
                "expires_in": CommandExecutionService.SESSION_LIFETIME,
                "mode": "simulation",
            }

        current_platform = CommandExecutionService._platform_name()

        if not CommandExecutionService._is_admin_context():
            if current_platform == "linux":
                valid, error = await CommandExecutionService._verify_linux_sudo_password(password)
                if not valid:
                    return {
                        "success": False,
                        "error": error,
                        "mode": "real",
                        "platform": current_platform,
                    }

                session_id = str(uuid.uuid4())
                CommandExecutionService.AUTHENTICATED_SESSIONS[session_id] = {
                    "created_at": time.time(),
                    "platform": current_platform,
                    "mode": "real",
                    "sudo_authenticated": True,
                    # Conservé en memoire uniquement pour re-soumettre sudo -S a chaque commande.
                    "sudo_password": password,
                }

                return {
                    "success": True,
                    "session_id": session_id,
                    "message": "Authentification root reussie via sudo",
                    "expires_in": CommandExecutionService.SESSION_LIFETIME,
                    "mode": "real",
                }

            if current_platform == "windows":
                reason = "Demarrez le backend avec 'Executer en tant qu'administrateur'."
            else:
                reason = "Demarrez le backend avec sudo/root (uid=0)."

            return {
                "success": False,
                "error": f"Privileges insuffisants. {reason}",
                "mode": "real",
                "platform": current_platform,
            }

        session_id = str(uuid.uuid4())
        CommandExecutionService.AUTHENTICATED_SESSIONS[session_id] = {
            "created_at": time.time(),
            "platform": current_platform,
            "mode": "real",
        }

        return {
            "success": True,
            "session_id": session_id,
            "message": "Authentification admin/root reussie",
            "expires_in": CommandExecutionService.SESSION_LIFETIME,
            "mode": "real",
        }

    @staticmethod
    def verify_session(session_id: str) -> bool:
        """Verifie si une session est valide et active."""
        session = CommandExecutionService.AUTHENTICATED_SESSIONS.get(session_id)
        if not session:
            return False

        if CommandExecutionService._session_expired(session["created_at"]):
            del CommandExecutionService.AUTHENTICATED_SESSIONS[session_id]
            return False

        return True

    @staticmethod
    def _resolve_command(command: str, args: Optional[List[str]]) -> Tuple[str, List[str]]:
        """Traduit les commandes logiques selon l'OS courant."""
        current_platform = CommandExecutionService._platform_name()
        normalized_args = list(args or [])

        if current_platform == "windows":
            windows_map = {
                "ifconfig": "ipconfig",
                "ip": "netsh",
                "ps": "tasklist",
                "kill": "taskkill",
                "netsh_wlan_show": "netsh",
                "netsh_wlan_interfaces": "netsh",
            }

            if command in {"airmon-ng", "airodump-ng"}:
                raise ValueError(
                    f"La commande '{command}' est disponible uniquement sous Linux avec aircrack-ng."
                )

            # Handle Windows WiFi-specific commands
            if command == "netsh_wlan_show":
                return "netsh", ["wlan", "show", "networks", "mode=Bssid"]
            
            if command == "netsh_wlan_interfaces":
                return "netsh", ["wlan", "show", "interfaces"]

            executable = windows_map.get(command, command)

            if executable == "taskkill" and normalized_args:
                upper_args = [a.upper() for a in normalized_args]
                if "/PID" not in upper_args and "/IM" not in upper_args:
                    if normalized_args[0].isdigit():
                        normalized_args = ["/PID", normalized_args[0], "/F"]

            return executable, normalized_args

        if command == "ifconfig":
            if shutil.which("ifconfig"):
                return "ifconfig", normalized_args

            if shutil.which("ip"):
                return "ip", ["addr"] + normalized_args

            raise ValueError("Aucune commande reseau disponible: ni 'ifconfig' ni 'ip'.")

        if command in {"ip", "ps", "kill", "airmon-ng", "airodump-ng"}:
            if not shutil.which(command):
                if command in {"airmon-ng", "airodump-ng"}:
                    raise ValueError(
                        f"La commande '{command}' est introuvable. Installez la suite aircrack-ng."
                    )
                raise ValueError(f"Commande introuvable sur ce systeme: {command}")

        # Linux/Mac specific WiFi commands - not on Windows
        if command in {"netsh_wlan_show", "netsh_wlan_interfaces"}:
            raise ValueError(
                f"La commande '{command}' est disponible uniquement sous Windows."
            )

        return command, normalized_args

    @staticmethod
    async def execute_command(
        command: str,
        args: Optional[List[str]] = None,
        timeout: int = 30,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute une commande de maniere securisee."""
        settings = get_settings()

        if not session_id or not CommandExecutionService.verify_session(session_id):
            return {
                "success": False,
                "error": "Authentification requise - utilisez /api/commands/auth.",
                "code": 401,
                "require_auth": True,
            }

        if command not in CommandExecutionService.ALLOWED_COMMANDS:
            return {
                "success": False,
                "error": f"Commande non autorisee: {command}",
                "code": 403,
            }

        if settings.simulation_mode:
            return await CommandExecutionService._simulate_command(command, args)

        try:
            executable, normalized_args = CommandExecutionService._resolve_command(command, args)
            cmd_list = [executable] + normalized_args

            session = CommandExecutionService.AUTHENTICATED_SESSIONS.get(session_id or "", {})
            needs_sudo = (
                not CommandExecutionService._is_admin_context()
                and CommandExecutionService._platform_name() == "linux"
                and bool(session.get("sudo_authenticated"))
            )

            process_stdin = None
            process_input = None

            if needs_sudo:
                cmd_list = ["sudo", "-S", "-p", ""] + cmd_list
                process_stdin = asyncio.subprocess.PIPE
                process_input = f"{session.get('sudo_password', '')}\n".encode("utf-8")

            process = await asyncio.create_subprocess_exec(
                *cmd_list,
                stdin=process_stdin,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input=process_input), timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()
                return {
                    "success": False,
                    "error": f"Timeout: commande non terminee apres {timeout}s",
                    "code": 408,
                }

            return {
                "success": process.returncode == 0,
                "output": stdout.decode("utf-8", errors="ignore"),
                "error": stderr.decode("utf-8", errors="ignore"),
                "code": process.returncode,
                "command": " ".join(cmd_list),
                "platform": CommandExecutionService._platform_name(),
            }

        except ValueError as e:
            return {
                "success": False,
                "error": str(e),
                "code": 400,
                "platform": CommandExecutionService._platform_name(),
            }
        except FileNotFoundError as e:
            return {
                "success": False,
                "error": f"Executable introuvable: {str(e)}",
                "code": 404,
                "platform": CommandExecutionService._platform_name(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur d'execution: {str(e)}",
                "code": 500,
                "platform": CommandExecutionService._platform_name(),
            }

    @staticmethod
    async def _simulate_command(command: str, args: Optional[List[str]]) -> Dict[str, Any]:
        """Simule l'execution d'une commande."""
        current_platform = CommandExecutionService._platform_name()

        if command == "ifconfig":
            if current_platform == "windows":
                return {
                    "success": True,
                    "output": (
                        "Windows IP Configuration\n\n"
                        "Wireless LAN adapter Wi-Fi:\n"
                        "   IPv4 Address. . . . . . . . . . . : 192.168.1.42\n"
                        "   Subnet Mask . . . . . . . . . . . : 255.255.255.0\n"
                        "   Default Gateway . . . . . . . . . : 192.168.1.1"
                    ),
                }

            return {
                "success": True,
                "output": (
                    "wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n"
                    "        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255\n"
                    "        ether 08:00:27:26:30:c7  txqueuelen 1000"
                ),
            }

        if command == "airmon-ng":
            if args and args[0] == "start":
                return {
                    "success": True,
                    "output": "Interface wlan0 basculee en mode monitor (simulation)",
                    "info": {"interface": "wlan0mon", "mode": "monitor"},
                }
            if args and args[0] == "stop":
                return {
                    "success": True,
                    "output": "Mode monitor desactive (simulation)",
                    "info": {"interface": "wlan0", "mode": "managed"},
                }

        if command == "airodump-ng":
            return {
                "success": True,
                "output": "Scan termine avec 6 reseaux detectes (simulation)",
                "networks": 6,
            }

        if command == "ps":
            if current_platform == "windows":
                return {
                    "success": True,
                    "output": (
                        "Image Name                     PID Session Name        Session#    Mem Usage\n"
                        "System Idle Process              0 Services                   0          8 K\n"
                        "explorer.exe                  4024 Console                    1     85,420 K"
                    ),
                }

            return {
                "success": True,
                "output": (
                    "PID   USER     COMMAND\n"
                    "1234  root     /sbin/wpa_supplicant -B -i wlan0\n"
                    "5678  user     python wifi_scanner.py"
                ),
            }

        if command == "kill":
            if args:
                return {
                    "success": True,
                    "output": f"Processus {args[0]} termine (simulation)",
                }

        if command == "ip":
            return {
                "success": True,
                "output": "Commande reseau executee (simulation)",
            }

        return {
            "success": False,
            "error": "Commande non reconnue en mode simulation",
            "code": 400,
        }