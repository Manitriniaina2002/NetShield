"""Modèles pour les réseaux Wi-Fi"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class SecurityLevel(str, Enum):
    """Niveaux de sécurité"""
    OPEN = "Open"
    WEP = "WEP"
    WPA = "WPA"
    WPA2 = "WPA2"
    WPA3 = "WPA3"
    UNKNOWN = "Unknown"


class RiskLevel(str, Enum):
    """Niveaux de risque"""
    CRITICAL = "🔴 Critique"
    HIGH = "🟠 Élevé"
    MEDIUM = "🟡 Moyen"
    LOW = "🟢 Faible"
    SECURE = "🟢 Sécurisé"


class WiFiNetwork(BaseModel):
    """Modèle d'un réseau Wi-Fi"""
    
    id: Optional[str] = Field(default_factory=lambda: None)
    ssid: str = Field(default="Unknown", description="Nom du réseau SSID")
    bssid: str = Field(..., description="MAC address du routeur")
    channel: int = Field(default=6, description="Canal Wi-Fi (1-14)")
    frequency: Optional[str] = Field(None, description="Fréquence (2.4GHz ou 5GHz)")
    security: SecurityLevel = Field(default=SecurityLevel.WPA2, description="Type de sécurité")
    signal_strength: int = Field(default=-75, ge=-100, le=0, description="Force du signal en dBm")
    signal_percentage: Optional[int] = Field(None, description="Pourcentage de signal")
    clients: int = Field(default=0, description="Nombre de clients connectés")
    last_seen: Optional[datetime] = Field(default_factory=datetime.now)
    
    @property
    def risk_level(self) -> RiskLevel:
        """Calcule le niveau de risque basé sur la sécurité"""
        if self.security in [SecurityLevel.OPEN, SecurityLevel.WEP]:
            return RiskLevel.CRITICAL
        elif self.security == SecurityLevel.WPA:
            return RiskLevel.HIGH
        elif self.security == SecurityLevel.WPA2:
            return RiskLevel.MEDIUM
        elif self.security == SecurityLevel.WPA3:
            return RiskLevel.SECURE
        return RiskLevel.MEDIUM
    
    @property
    def signal_bar(self) -> str:
        """Affiche une barre de signal ASCII"""
        percentage = 0
        if self.signal_strength <= -30:
            percentage = 100
        elif self.signal_strength >= -90:
            percentage = 0
        else:
            percentage = 2 * (self.signal_strength + 100)
        
        filled = int(percentage / 20)
        empty = 5 - filled
        return "█" * filled + "░" * empty
    
    class Config:
        json_schema_extra = {
            "example": {
                "ssid": "MyNetwork",
                "bssid": "AA:BB:CC:DD:EE:FF",
                "channel": 6,
                "frequency": "2.4GHz",
                "security": "WPA2",
                "signal_strength": -65,
                "clients": 3
            }
        }
