"""Modèles de données"""
from .wifi import WiFiNetwork, SecurityLevel
from .scan import ScanResult, AuditReport
from .vulnerability import Vulnerability, VulnerabilityType
from .recommendation import Recommendation

__all__ = [
    "WiFiNetwork",
    "SecurityLevel",
    "ScanResult",
    "AuditReport",
    "Vulnerability",
    "VulnerabilityType",
    "Recommendation",
]
