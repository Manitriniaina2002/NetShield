"""Services pour les scans Wi-Fi."""
import asyncio
import platform
import random
import re
import shutil
from datetime import datetime
from typing import Dict, List, Optional

from app.config import get_settings
from app.models.wifi import SecurityLevel, WiFiNetwork


class WiFiScanService:
    """Service de scan Wi-Fi (simulation et reel)."""

    # Donnees de test pour simulation
    SIMULATED_NETWORKS = [
        {
            "ssid": "FreeFi_Public",
            "bssid": "AA:11:22:33:44:55",
            "channel": 6,
            "frequency": "2.4GHz",
            "security": SecurityLevel.OPEN,
            "signal_strength": -45,
            "clients": 12,
        },
        {
            "ssid": "CoffeShop_WiFi",
            "bssid": "BB:22:33:44:55:66",
            "channel": 11,
            "frequency": "2.4GHz",
            "security": SecurityLevel.WEP,
            "signal_strength": -55,
            "clients": 8,
        },
        {
            "ssid": "HomeNetwork",
            "bssid": "CC:33:44:55:66:77",
            "channel": 1,
            "frequency": "2.4GHz",
            "security": SecurityLevel.WPA,
            "signal_strength": -35,
            "clients": 5,
        },
        {
            "ssid": "SecureOffice",
            "bssid": "DD:44:55:66:77:88",
            "channel": 48,
            "frequency": "5GHz",
            "security": SecurityLevel.WPA2,
            "signal_strength": -50,
            "clients": 15,
        },
        {
            "ssid": "ModernHome",
            "bssid": "EE:55:66:77:88:99",
            "channel": 36,
            "frequency": "5GHz",
            "security": SecurityLevel.WPA3,
            "signal_strength": -40,
            "clients": 3,
        },
        {
            "ssid": "HiddenNetwork",
            "bssid": "FF:66:77:88:99:AA",
            "channel": 6,
            "frequency": "2.4GHz",
            "security": SecurityLevel.WPA2,
            "signal_strength": -70,
            "clients": 2,
        },
    ]

    @staticmethod
    async def scan_networks(duration_seconds: int = 10) -> List[WiFiNetwork]:
        """
        Lance un scan Wi-Fi en simulation ou en mode reel selon la configuration.

        Args:
            duration_seconds: Duree du scan

        Returns:
            Liste des reseaux detectes
        """
        settings = get_settings()

        if settings.simulation_mode:
            return await WiFiScanService._scan_networks_simulated(duration_seconds)

        return await WiFiScanService._scan_networks_real(duration_seconds)

    @staticmethod
    async def _scan_networks_simulated(duration_seconds: int) -> List[WiFiNetwork]:
        """Scan simule pour laboratoire et demos."""
        await asyncio.sleep(min(duration_seconds / 10, 2))

        networks: List[WiFiNetwork] = []
        for i, net_data in enumerate(WiFiScanService.SIMULATED_NETWORKS):
            signal_variation = random.randint(-5, 5)
            signal_strength = net_data["signal_strength"] + signal_variation

            networks.append(
                WiFiNetwork(
                    id=f"network_{i}_{datetime.now().timestamp()}",
                    ssid=net_data["ssid"],
                    bssid=net_data["bssid"],
                    channel=net_data["channel"],
                    frequency=net_data["frequency"],
                    security=net_data["security"],
                    signal_strength=signal_strength,
                    signal_percentage=WiFiScanService._dbm_to_percentage(signal_strength),
                    clients=net_data["clients"],
                    last_seen=datetime.now(),
                )
            )

        return networks

    @staticmethod
    async def _scan_networks_real(duration_seconds: int) -> List[WiFiNetwork]:
        """Scan reel en fonction du systeme d'exploitation."""
        system_name = platform.system().lower()

        if system_name == "windows":
            return await WiFiScanService._scan_windows_networks(duration_seconds)

        if system_name == "linux":
            return await WiFiScanService._scan_linux_networks(duration_seconds)

        raise RuntimeError(
            f"Mode reel non supporte sur ce systeme: {platform.system()}. "
            "Utilisez Linux ou Windows."
        )

    @staticmethod
    async def _scan_windows_networks(duration_seconds: int) -> List[WiFiNetwork]:
        """Scan des reseaux Wi-Fi reels sous Windows via netsh."""
        await asyncio.sleep(min(duration_seconds / 10, 1))

        try:
            output = await WiFiScanService._run_command(
                ["netsh", "wlan", "show", "networks", "mode=Bssid"],
                timeout=max(15, duration_seconds + 5),
            )
        except Exception as e:
            raise RuntimeError(
                f"Windows Wi-Fi scan failed: {str(e)}. "
                "Ensure: 1) Administrator privileges, "
                "2) Wi-Fi adapter is enabled, "
                "3) netsh is available. Falling back to simulation mode."
            )

        networks: List[WiFiNetwork] = []
        current_ssid = ""
        current_auth = ""
        current_encryption = ""
        current_entry: Optional[Dict[str, object]] = None

        for line in output.splitlines():
            stripped = line.strip()
            if not stripped:
                continue

            ssid_match = re.match(r"^SSID\s+\d+\s*:\s*(.*)$", stripped, re.IGNORECASE)
            if ssid_match:
                if current_entry:
                    networks.append(WiFiScanService._build_network_from_raw(current_entry))
                    current_entry = None

                current_ssid = ssid_match.group(1).strip() or "HiddenNetwork"
                current_auth = ""
                current_encryption = ""
                continue

            auth_match = re.match(
                r"^(Authentication|Authentification)\s*:\s*(.*)$",
                stripped,
                re.IGNORECASE,
            )
            if auth_match:
                current_auth = auth_match.group(2).strip()
                continue

            enc_match = re.match(
                r"^(Encryption|Chiffrement)\s*:\s*(.*)$",
                stripped,
                re.IGNORECASE,
            )
            if enc_match:
                current_encryption = enc_match.group(2).strip()
                continue

            bssid_match = re.match(
                r"^BSSID\s+\d+\s*:\s*([0-9A-Fa-f:]{17})$", stripped, re.IGNORECASE
            )
            if bssid_match:
                if current_entry:
                    networks.append(WiFiScanService._build_network_from_raw(current_entry))

                current_entry = {
                    "ssid": current_ssid or "HiddenNetwork",
                    "bssid": bssid_match.group(1).upper(),
                    "channel": 1,
                    "frequency": "2.4GHz",
                    "security": WiFiScanService._detect_security(
                        current_auth,
                        current_encryption,
                        empty_means_unknown=True,
                    ),
                    "signal_percentage": 0,
                    "signal_strength": -100,
                    "clients": 0,
                }
                continue

            if not current_entry:
                continue

            signal_match = re.match(r"^Signal\s*:\s*(\d+)%$", stripped, re.IGNORECASE)
            if signal_match:
                signal_percentage = int(signal_match.group(1))
                current_entry["signal_percentage"] = signal_percentage
                current_entry["signal_strength"] = WiFiScanService._percentage_to_dbm(signal_percentage)
                continue

            channel_match = re.match(
                r"^(Channel|Canal)\s*:\s*(\d+)$",
                stripped,
                re.IGNORECASE,
            )
            if channel_match:
                channel = int(channel_match.group(2))
                current_entry["channel"] = channel
                current_entry["frequency"] = WiFiScanService._channel_to_frequency(channel)

        if current_entry:
            networks.append(WiFiScanService._build_network_from_raw(current_entry))

        return WiFiScanService._deduplicate_by_bssid(networks)

    @staticmethod
    async def _scan_linux_networks(duration_seconds: int) -> List[WiFiNetwork]:
        """Scan des reseaux Wi-Fi reels sous Linux via nmcli."""
        await asyncio.sleep(min(duration_seconds / 10, 1))

        if not shutil.which("nmcli"):
            raise RuntimeError(
                "nmcli est introuvable. Installez NetworkManager/nmcli pour le scan reel Linux."
            )

        output = await WiFiScanService._run_command(
            [
                "nmcli",
                "-t",
                "--escape",
                "yes",
                "-f",
                "SSID,BSSID,CHAN,FREQ,SIGNAL,SECURITY",
                "dev",
                "wifi",
                "list",
            ],
            timeout=max(15, duration_seconds + 5),
        )

        networks: List[WiFiNetwork] = []
        for idx, line in enumerate(output.splitlines()):
            if not line.strip():
                continue

            fields = WiFiScanService._split_escaped_fields(line, delimiter=":")
            if len(fields) < 6:
                continue

            ssid = WiFiScanService._unescape_nmcli(fields[0]).strip() or "HiddenNetwork"
            bssid = WiFiScanService._unescape_nmcli(fields[1]).strip().upper()
            channel_str = WiFiScanService._unescape_nmcli(fields[2]).strip()
            freq_str = WiFiScanService._unescape_nmcli(fields[3]).strip()
            signal_str = WiFiScanService._unescape_nmcli(fields[4]).strip()
            security_str = WiFiScanService._unescape_nmcli(fields[5]).strip()

            if not bssid or not re.match(r"^[0-9A-F]{2}(:[0-9A-F]{2}){5}$", bssid):
                continue

            channel = int(channel_str) if channel_str.isdigit() else 1
            signal_percentage = int(signal_str) if signal_str.isdigit() else 0
            signal_percentage = max(0, min(signal_percentage, 100))

            networks.append(
                WiFiNetwork(
                    id=f"network_linux_{idx}_{datetime.now().timestamp()}",
                    ssid=ssid,
                    bssid=bssid,
                    channel=channel,
                    frequency=WiFiScanService._freq_to_band(freq_str, channel),
                    security=WiFiScanService._detect_security(security_str, security_str),
                    signal_strength=WiFiScanService._percentage_to_dbm(signal_percentage),
                    signal_percentage=signal_percentage,
                    clients=0,
                    last_seen=datetime.now(),
                )
            )

        return WiFiScanService._deduplicate_by_bssid(networks)

    @staticmethod
    async def _run_command(command: List[str], timeout: int = 20) -> str:
        """Execute une commande shell de facon asynchrone et retourne stdout."""
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            process.kill()
            await process.communicate()
            raise RuntimeError(f"Timeout commande ({timeout}s): {' '.join(command)}")

        out = stdout.decode("utf-8", errors="ignore")
        err = stderr.decode("utf-8", errors="ignore")

        if process.returncode != 0:
            raise RuntimeError(err.strip() or out.strip() or "Commande systeme en echec")

        return out

    @staticmethod
    def _detect_security(
        auth: str,
        encryption: str,
        empty_means_unknown: bool = False,
    ) -> SecurityLevel:
        """Mappe des informations systemes vers SecurityLevel."""
        auth_u = (auth or "").upper()
        enc_u = (encryption or "").upper()
        source = f"{auth_u} {enc_u}"
        compact = source.replace(" ", "").strip()

        if "WPA3" in source or "SAE" in source:
            return SecurityLevel.WPA3
        if "WPA2" in source:
            return SecurityLevel.WPA2
        if "WPA" in source:
            return SecurityLevel.WPA
        if "WEP" in source:
            return SecurityLevel.WEP
        if "OPEN" in source or "NONE" in source or compact in {"--", "----"}:
            return SecurityLevel.OPEN
        if not compact:
            return SecurityLevel.UNKNOWN if empty_means_unknown else SecurityLevel.OPEN
        return SecurityLevel.UNKNOWN

    @staticmethod
    def _dbm_to_percentage(dbm: int) -> int:
        """Convertit une force de signal dBm en pourcentage."""
        if dbm >= -30:
            return 100
        if dbm <= -90:
            return 0
        return max(0, min(100, 2 * (dbm + 100)))

    @staticmethod
    def _percentage_to_dbm(percentage: int) -> int:
        """Approximation de conversion pourcentage vers dBm."""
        percentage = max(0, min(100, percentage))
        return int((percentage / 2) - 100)

    @staticmethod
    def _channel_to_frequency(channel: int) -> str:
        """Retourne la bande en fonction du canal."""
        return "2.4GHz" if 1 <= channel <= 14 else "5GHz"

    @staticmethod
    def _freq_to_band(freq_raw: str, channel: int) -> str:
        """Normalise une frequence brute vers 2.4GHz/5GHz."""
        raw = (freq_raw or "").strip().lower()
        if raw.endswith("ghz"):
            return "5GHz" if raw.startswith("5") else "2.4GHz"

        try:
            freq_mhz = int(float(raw))
            return "2.4GHz" if freq_mhz < 3000 else "5GHz"
        except ValueError:
            return WiFiScanService._channel_to_frequency(channel)

    @staticmethod
    def _split_escaped_fields(line: str, delimiter: str = ":") -> List[str]:
        """Split pour sorties nmcli en preservant les delimiters echappes."""
        fields: List[str] = []
        current: List[str] = []
        escaped = False

        for char in line:
            if escaped:
                current.append(char)
                escaped = False
                continue

            if char == "\\":
                escaped = True
                continue

            if char == delimiter:
                fields.append("".join(current))
                current = []
                continue

            current.append(char)

        fields.append("".join(current))
        return fields

    @staticmethod
    def _unescape_nmcli(value: str) -> str:
        """Retire les sequences d'echappement nmcli les plus courantes."""
        return (value or "").replace("\\:", ":").replace("\\\\", "\\")

    @staticmethod
    def _build_network_from_raw(raw: Dict[str, object]) -> WiFiNetwork:
        """Construit un objet WiFiNetwork depuis un dict intermediaire."""
        return WiFiNetwork(
            id=f"network_{raw['bssid']}_{datetime.now().timestamp()}",
            ssid=str(raw.get("ssid", "HiddenNetwork")),
            bssid=str(raw["bssid"]),
            channel=int(raw.get("channel", 1)),
            frequency=str(raw.get("frequency", "2.4GHz")),
            security=raw.get("security", SecurityLevel.UNKNOWN),
            signal_strength=int(raw.get("signal_strength", -100)),
            signal_percentage=int(raw.get("signal_percentage", 0)),
            clients=int(raw.get("clients", 0)),
            last_seen=datetime.now(),
        )

    @staticmethod
    def _deduplicate_by_bssid(networks: List[WiFiNetwork]) -> List[WiFiNetwork]:
        """Elimine les doublons en gardant le signal le plus fort par BSSID."""
        unique: Dict[str, WiFiNetwork] = {}
        for network in networks:
            existing = unique.get(network.bssid)
            if existing is None or network.signal_strength > existing.signal_strength:
                unique[network.bssid] = network
        return list(unique.values())

    @staticmethod
    async def scan_specific_network(bssid: str, channel: int) -> Optional[dict]:
        """
        Récupère les détails d'un réseau spécifique.

        En mode réel, la recherche est faite sur un scan live court.
        """
        settings = get_settings()

        if settings.simulation_mode:
            await asyncio.sleep(0.5)
            for network in WiFiScanService.SIMULATED_NETWORKS:
                if network["bssid"].upper() == bssid.upper():
                    return {
                        **network,
                        "detailed_info": {
                            "manufacturer": "TP-Link",
                            "model": "TL-WR840N",
                            "firmware_version": "1.2.3",
                            "max_power": 20,
                            "country_code": "FR",
                        },
                    }
            return None

        networks = await WiFiScanService.scan_networks(duration_seconds=5)
        for network in networks:
            if network.bssid.upper() == bssid.upper():
                data = network.model_dump() if hasattr(network, "model_dump") else network.dict()
                data["detailed_info"] = {
                    "source": "live_scan",
                    "channel_requested": channel,
                    "platform": platform.system().lower(),
                }
                return data

        return None