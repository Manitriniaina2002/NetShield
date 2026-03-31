"""Services pour les scans Wi-Fi"""
import random
from datetime import datetime
from typing import List
from app.models.wifi import WiFiNetwork, SecurityLevel, RiskLevel


class WiFiScanService:
    """Service de scan Wi-Fi (mode simulation)"""
    
    # Données de test pour simulation
    SIMULATED_NETWORKS = [
        {
            "ssid": "FreeFi_Public",
            "bssid": "AA:11:22:33:44:55",
            "channel": 6,
            "frequency": "2.4GHz",
            "security": SecurityLevel.OPEN,
            "signal_strength": -45,
            "clients": 12
        },
        {
            "ssid": "CoffeShop_WiFi",
            "bssid": "BB:22:33:44:55:66",
            "channel": 11,
            "frequency": "2.4GHz",
            "security": SecurityLevel.WEP,
            "signal_strength": -55,
            "clients": 8
        },
        {
            "ssid": "HomeNetwork",
            "bssid": "CC:33:44:55:66:77",
            "channel": 1,
            "frequency": "2.4GHz",
            "security": SecurityLevel.WPA,
            "signal_strength": -35,
            "clients": 5
        },
        {
            "ssid": "SecureOffice",
            "bssid": "DD:44:55:66:77:88",
            "channel": 48,
            "frequency": "5GHz",
            "security": SecurityLevel.WPA2,
            "signal_strength": -50,
            "clients": 15
        },
        {
            "ssid": "ModernHome",
            "bssid": "EE:55:66:77:88:99",
            "channel": 36,
            "frequency": "5GHz",
            "security": SecurityLevel.WPA3,
            "signal_strength": -40,
            "clients": 3
        },
        {
            "ssid": "HiddenNetwork",
            "bssid": "FF:66:77:88:99:AA",
            "channel": 6,
            "frequency": "2.4GHz",
            "security": SecurityLevel.WPA2,
            "signal_strength": -70,
            "clients": 2
        }
    ]
    
    @staticmethod
    async def scan_networks(duration_seconds: int = 10) -> List[WiFiNetwork]:
        """
        Simule un scan Wi-Fi (simulation passive)
        
        Args:
            duration_seconds: Durée du scan simulé
            
        Returns:
            Liste des réseaux détectés
        """
        import asyncio
        
        # Simuler un léger délai de scan
        await asyncio.sleep(min(duration_seconds / 10, 2))
        
        networks = []
        for i, net_data in enumerate(WiFiScanService.SIMULATED_NETWORKS):
            # Variation aléatoire du signal pour simuler les fluctuations
            signal_variation = random.randint(-5, 5)
            
            network = WiFiNetwork(
                id=f"network_{i}_{datetime.now().timestamp()}",
                ssid=net_data["ssid"],
                bssid=net_data["bssid"],
                channel=net_data["channel"],
                frequency=net_data["frequency"],
                security=net_data["security"],
                signal_strength=net_data["signal_strength"] + signal_variation,
                signal_percentage=WiFiScanService._dbm_to_percentage(
                    net_data["signal_strength"]
                ),
                clients=net_data["clients"],
                last_seen=datetime.now()
            )
            networks.append(network)
        
        return networks
    
    @staticmethod
    def _dbm_to_percentage(dbm: int) -> int:
        """Convertit une force de signal dBm en pourcentage"""
        if dbm >= -30:
            return 100
        elif dbm <= -90:
            return 0
        else:
            return 2 * (dbm + 100)
    
    @staticmethod
    async def scan_specific_network(bssid: str, channel: int) -> dict:
        """
        Scan un réseau spécifique pour récupérer les détails
        
        Args:
            bssid: MAC address du routeur
            channel: Canal Wi-Fi
            
        Returns:
            Détails du réseau
        """
        import asyncio
        
        # Simuler le scan ciblé
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
                        "country_code": "FR"
                    }
                }
        
        return None
