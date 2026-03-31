"""Modèles pour les scans et rapports"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .wifi import WiFiNetwork
from .vulnerability import Vulnerability
from .recommendation import Recommendation


class ScanResult(BaseModel):
    """Résultat d'un scan Wi-Fi"""
    
    id: Optional[str] = Field(default_factory=lambda: None)
    scan_name: str = Field(..., description="Nom du scan")
    scan_timestamp: datetime = Field(default_factory=datetime.now)
    networks_found: int = Field(0, description="Nombre de réseaux découverts")
    networks: List[WiFiNetwork] = Field(default_factory=list)
    scan_duration: int = Field(0, description="Durée du scan en secondes")
    interface_used: Optional[str] = Field(None, description="Interface réseau utilisée")
    mode: str = Field("simulation", description="Mode du scan (simulation/monitor)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "scan_name": "Audit-Lab-2024",
                "networks_found": 5,
                "scan_duration": 30,
                "mode": "simulation"
            }
        }


class AuditReport(BaseModel):
    """Rapport d'audit complet"""
    
    id: Optional[str] = Field(default_factory=lambda: None)
    report_title: str = Field(..., description="Titre du rapport")
    report_date: datetime = Field(default_factory=datetime.now)
    author: str = Field(default="NetShield Auditor", description="Auteur de l'audit")
    project_name: str = Field(..., description="Nom du projet")
    
    # Données de scan
    scan_result: Optional[ScanResult] = Field(None)
    
    # Vulnérabilités et recommandations
    vulnerabilities: List[Vulnerability] = Field(default_factory=list)
    recommendations: List[Recommendation] = Field(default_factory=list)
    
    # Statistiques
    total_networks: int = Field(0)
    critical_vulnerabilities: int = Field(0)
    high_vulnerabilities: int = Field(0)
    medium_vulnerabilities: int = Field(0)
    low_vulnerabilities: int = Field(0)
    
    # Résumé exécutif
    executive_summary: str = Field(..., description="Résumé exécutif")
    risk_assessment: str = Field(..., description="Évaluation du risque global")
    overall_risk_score: float = Field(..., ge=0, le=100, description="Score de risque global (0-100)")
    
    # Méthodologie
    methodology: str = Field(default="Scan passif avec simulation d'attaques")
    testing_period: str = Field(default="2024-01-01 to 2024-01-31")
    
    # Observations supplémentaires
    observations: Optional[str] = Field(None)
    notes: Optional[str] = Field(None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_title": "Audit WI-FI - Entreprise XYZ",
                "project_name": "Security Assessment Q1 2024",
                "total_networks": 5,
                "overall_risk_score": 65.5
            }
        }
