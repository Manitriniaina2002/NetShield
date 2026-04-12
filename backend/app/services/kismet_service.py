"""Service d'intégration Kismet pour scanning Wi-Fi avancé."""
import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from urllib.parse import urljoin

from app.config import get_settings
from app.models.wifi import SecurityLevel, WiFiNetwork


class KismetService:
    """Service Kismet pour récupérer des données Wi-Fi en temps réel."""

    def __init__(self, api_url: str = "http://localhost:2501", api_key: Optional[str] = None):
        """
        Initialise le service Kismet.

        Args:
            api_url: URL de l'API Kismet (défaut: localhost:2501)
            api_key: Clé API Kismet (optionnel)
        """
        self.api_url = api_url
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None

    async def connect(self) -> bool:
        """
        Établit la connexion avec le serveur Kismet.

        Returns:
            True si connecté, False sinon
        """
        try:
            self.session = aiohttp.ClientSession()
            async with self.session.get(f"{self.api_url}/system/status") as resp:
                if resp.status == 200:
                    return True
        except Exception as e:
            print(f"[Kismet] Connexion failed: {str(e)}")
            if self.session:
                await self.session.close()
        return False

    async def disconnect(self):
        """Ferme la connexion avec Kismet."""
        if self.session:
            await self.session.close()

    async def __aenter__(self):
        """Context manager entry."""
        if await self.connect():
            return self
        raise ConnectionError(f"Cannot connect to Kismet at {self.api_url}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.disconnect()

    async def get_devices(self) -> List[Dict[str, Any]]:
        """
        Récupère tous les appareils détectés par Kismet.

        Returns:
            Liste des appareils
        """
        if not self.session:
            await self.connect()

        try:
            async with self.session.get(f"{self.api_url}/devices/summary") as resp:
                if resp.status == 200:
                    devices = await resp.json()
                    return devices if isinstance(devices, list) else []
        except Exception as e:
            print(f"[Kismet] Failed to fetch devices: {str(e)}")
        return []

    async def get_networks(self) -> List[Dict[str, Any]]:
        """
        Récupère tous les réseaux Wi-Fi détectés.

        Returns:
            Liste des réseaux Wi-Fi
        """
        if not self.session:
            await self.connect()

        try:
            # Kismet endpoint pour récupérer les réseaux
            async with self.session.get(f"{self.api_url}/phy/phy80211/networks") as resp:
                if resp.status == 200:
                    networks = await resp.json()
                    return networks if isinstance(networks, list) else []
        except Exception as e:
            print(f"[Kismet] Failed to fetch networks: {str(e)}")
        return []

    async def scan_networks(self, duration: int = 30) -> List[WiFiNetwork]:
        """
        Lance un scan Wi-Fi via Kismet et retourne les réseaux détectés.

        Args:
            duration: Durée du scan en secondes

        Returns:
            Liste des réseaux WiFiNetwork
        """
        if not self.session:
            if not await self.connect():
                return []

        try:
            # Démarrer un nouveau scan
            async with self.session.post(
                f"{self.api_url}/phy/phy80211/networks"
            ) as resp:
                if resp.status not in [200, 201]:
                    print(f"[Kismet] Scan initiation failed: {resp.status}")
                    return []

            # Attendre la fin du scan
            await asyncio.sleep(duration)

            # Récupérer les réseaux détectés
            networks_raw = await self.get_networks()
            networks: List[WiFiNetwork] = []

            for net_data in networks_raw:
                try:
                    network = self._parse_kismet_network(net_data)
                    if network:
                        networks.append(network)
                except Exception as e:
                    print(f"[Kismet] Failed to parse network: {str(e)}")
                    continue

            return networks

        except Exception as e:
            print(f"[Kismet] Scan failed: {str(e)}")
            return []

    def _parse_kismet_network(self, raw_data: Dict[str, Any]) -> Optional[WiFiNetwork]:
        """
        Parse les données brutes de Kismet en WiFiNetwork.

        Args:
            raw_data: Données brutes de Kismet

        Returns:
            Réseau WiFiNetwork ou None si erreur
        """
        try:
            # Extraire les informations principales
            bssid = raw_data.get("kismet.device.base.macaddr", "").upper()
            ssid = raw_data.get("kismet.device.base.name", "HiddenNetwork")

            # Kismet retourne souvent BSSID en format XX:XX:XX:XX:XX:XX
            if not bssid or len(bssid) < 17:
                return None

            # Signal strength (Kismet en dBm)
            signal_dbm = raw_data.get("kismet.device.base.signal.last_signal", -100)
            if isinstance(signal_dbm, dict):
                signal_dbm = signal_dbm.get("kismet.common.signal.signal_dbm", -100)

            signal_dbm = max(-100, min(0, int(signal_dbm)))

            # Convertir en pourcentage
            signal_percentage = self._dbm_to_percentage(signal_dbm)

            # Canal
            channel = raw_data.get("kismet.device.base.channel", 1)
            if isinstance(channel, dict):
                channel = channel.get("kismet.common.channel.channel", 1)
            channel = int(channel) if channel else 1

            # Sécurité (à partir des données Kismet)
            security = self._detect_kismet_security(raw_data)

            # Nombre de clients/appareils associés
            clients = raw_data.get("kismet.device.base.num_children", 0)

            # Fréquence
            frequency = self._channel_to_frequency(channel)

            return WiFiNetwork(
                id=f"kismet_{bssid}_{datetime.now().timestamp()}",
                ssid=ssid or "HiddenNetwork",
                bssid=bssid,
                channel=channel,
                frequency=frequency,
                security=security,
                signal_strength=signal_dbm,
                signal_percentage=signal_percentage,
                clients=clients,
                last_seen=datetime.now(),
            )

        except Exception as e:
            print(f"[Kismet Parser] Error: {str(e)}")
            return None

    @staticmethod
    def _dbm_to_percentage(dbm: int) -> int:
        """Convertit dBm en pourcentage."""
        if dbm <= -100:
            return 0
        if dbm >= -30:
            return 100
        return 2 * (dbm + 100)

    @staticmethod
    def _channel_to_frequency(channel: int) -> str:
        """Convertit le canal en fréquence."""
        if 1 <= channel <= 14:
            return "2.4GHz"
        elif 36 <= channel <= 165:
            return "5GHz"
        elif 1 <= channel <= 6:
            return "2.4GHz"
        else:
            return "Unknown"

    @staticmethod
    def _detect_kismet_security(data: Dict[str, Any]) -> SecurityLevel:
        """Détecte le niveau de sécurité à partir des données Kismet."""
        try:
            # Rechercher les informations de sécurité
            wps = data.get("kismet.device.base.wps_state", "")
            encryption = data.get("kismet.device.base.encryption", "")

            if isinstance(encryption, dict):
                # Kismet structure complexe
                if any("WPA3" in str(v) for v in encryption.values()):
                    return SecurityLevel.WPA3
                if any("WPA2" in str(v) for v in encryption.values()):
                    return SecurityLevel.WPA2
                if any("WPA" in str(v) for v in encryption.values()):
                    return SecurityLevel.WPA
                if any("WEP" in str(v) for v in encryption.values()):
                    return SecurityLevel.WEP
            else:
                encryption_str = str(encryption).upper()
                if "WPA3" in encryption_str:
                    return SecurityLevel.WPA3
                if "WPA2" in encryption_str:
                    return SecurityLevel.WPA2
                if "WPA" in encryption_str:
                    return SecurityLevel.WPA
                if "WEP" in encryption_str:
                    return SecurityLevel.WEP

            # Si aucun chiffrement trouvé
            return SecurityLevel.OPEN

        except Exception:
            return SecurityLevel.UNKNOWN

    async def get_alerts(self) -> List[Dict[str, Any]]:
        """
        Récupère les alertes Kismet (attaques détectées, anomalies).

        Returns:
            Liste des alertes
        """
        if not self.session:
            await self.connect()

        try:
            async with self.session.get(f"{self.api_url}/alerts/definition") as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception as e:
            print(f"[Kismet] Failed to fetch alerts: {str(e)}")
        return []

    async def get_server_info(self) -> Dict[str, Any]:
        """
        Récupère les informations du serveur Kismet.

        Returns:
            Informations du serveur
        """
        if not self.session:
            await self.connect()

        try:
            async with self.session.get(f"{self.api_url}/system/status") as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception as e:
            print(f"[Kismet] Failed to fetch server info: {str(e)}")
        return {}
