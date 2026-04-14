"""API routes for demo workflow and simulation data."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models.database import get_session_maker, get_db_engine
from app.services.database_service import DatabaseService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/demo", tags=["demo-workflow"])

# Database dependency
def get_db():
    """Get database session"""
    try:
        engine = get_db_engine()
        SessionLocal = get_session_maker(engine)
        db = SessionLocal()
        yield db
    finally:
        db.close()


class DemoNetworkInfo(BaseModel):
    capture_id: str
    ssid: str
    bssid: str
    security_level: str
    capture_status: str
    handshake_status: str
    packets: int
    duration: int
    file_size: int


class DemoCrackingAttempt(BaseModel):
    attempt_id: str
    network_ssid: str
    method: str
    wordlist: str
    success: bool
    password: str | None
    duration: int
    passwords_tried: int
    gpu_enabled: bool


class DemoWorkflowStep(BaseModel):
    step: int
    title: str
    description: str
    networks_involved: List[str]
    key_findings: List[str]


class DemoWorkflowSummary(BaseModel):
    workflow_title: str
    total_steps: int
    networks_scanned: int
    handshakes_captured: int
    successful_captures: float
    cracking_attempts: int
    passwords_found: int
    crack_success_rate: float
    vulnerabilities_found: int
    critical_issues: int
    overall_risk_score: float
    steps: List[DemoWorkflowStep]


@router.get("/workflow/summary", response_model=DemoWorkflowSummary)
async def get_demo_workflow_summary(db: Session = Depends(get_db)):
    """
    Récupère un résumé du workflow complet de démonstration
    incluant les étapes de scan, capture, craquage et analyse.
    """
    try:
        # Get statistics
        handshakes = DatabaseService.get_all_handshakes(db, limit=100)
        demo_handshakes = [h for h in handshakes if "demo" in (h.tags or "").lower()]
        
        successful = sum(1 for h in demo_handshakes if h.success)
        total = len(demo_handshakes)
        
        # Workflow steps
        steps = [
            DemoWorkflowStep(
                step=1,
                title="Network Scanning & Discovery",
                description="Passive WiFi network discovery using airodump-ng, identifying 6 target networks with various security configurations",
                networks_involved=["CorporateNetwork-5G", "HomeWifi-Plus", "GuestNetwork", "LegacyWifi", "CafePublicWifi", "RouterAdmin"],
                key_findings=[
                    "Identified 1 Open network (GuestNetwork)",
                    "Found 1 WEP-encrypted network (LegacyWifi)",
                    "Detected 2 WPA2-PSK networks",
                    "Located 1 WPA2-Enterprise network (CorporateNetwork)",
                    "Discovered 1 WPA3 network (RouterAdmin)"
                ]
            ),
            DemoWorkflowStep(
                step=2,
                title="Handshake Capture & Deauthentication",
                description="Active handshake capture using aireplay-ng deauthentication attacks to force clients to reconnect",
                networks_involved=["CorporateNetwork-5G", "HomeWifi-Plus", "LegacyWifi", "RouterAdmin"],
                key_findings=[
                    f"Successfully captured {successful}/{total} handshakes ({100*successful/total:.1f}% success rate)",
                    "Used deauthentication on 4 networks",
                    "Captured 5,400 packets from CorporateNetwork",
                    "CafePublicWifi capture failed - network may be offline"
                ]
            ),
            DemoWorkflowStep(
                step=3,
                title="Password Cracking Attempts",
                description="Multi-tool password cracking using aircrack-ng, hashcat (GPU), and john the ripper with various wordlists",
                networks_involved=["HomeWifi-Plus", "LegacyWifi"],
                key_findings=[
                    "Successfully cracked HomeWifi-Plus password in 45 seconds (Password: Butterfly2024!)",
                    "Cracked WEP password using keystream recovery in 120 seconds",
                    "CorporateNetwork-5G: No common password found (500k attempts)",
                    "RouterAdmin WPA3: Not cracked (1M attempts, strong password)"
                ]
            ),
            DemoWorkflowStep(
                step=4,
                title="Vulnerability Analysis",
                description="Analysis of security configurations and identification of exploitation vectors",
                networks_involved=["GuestNetwork", "LegacyWifi", "HomeWifi-Plus"],
                key_findings=[
                    "Critical: Open network (GuestNetwork) - no encryption",
                    "Critical: WEP encryption (LegacyWifi) - completely broken",
                    "Critical: Weak password (HomeWifi-Plus) - found in dictionary",
                    "Medium: WPA2-Enterprise may have certificate validation issues",
                    "Low: WPA3 configuration is secure"
                ]
            ),
            DemoWorkflowStep(
                step=5,
                title="Security Recommendations",
                description="Prioritized, actionable security recommendations for each network",
                networks_involved=["All Networks"],
                key_findings=[
                    "Immediate: Migrate from WEP to WPA2/WPA3",
                    "Immediate: Enable encryption on guest network",
                    "High: Implement strong password policy (16+ chars)",
                    "High: Update firmware on all routers",
                    "Medium: Regular security audits (quarterly)"
                ]
            ),
            DemoWorkflowStep(
                step=6,
                title="Report Generation & Remediation Plan",
                description="Comprehensive audit report with executive summary, detailed findings, and remediation timeline",
                networks_involved=["All Networks"],
                key_findings=[
                    f"Overall Risk Score: 72.5/100 (HIGH)",
                    "4 Critical vulnerabilities identified",
                    "2 High-priority issues",
                    "Estimated remediation time: 8-16 hours",
                    "Estimated security improvement: 85% risk reduction"
                ]
            )
        ]
        
        return DemoWorkflowSummary(
            workflow_title="NetShield Comprehensive WiFi Security Audit - Full Workflow Demo",
            total_steps=6,
            networks_scanned=6,
            handshakes_captured=successful,
            successful_captures=100 * successful / total if total > 0 else 0,
            cracking_attempts=2,
            passwords_found=2,
            crack_success_rate=100.0,
            vulnerabilities_found=6,
            critical_issues=3,
            overall_risk_score=72.5,
            steps=steps
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving demo workflow: {str(e)}")


@router.get("/networks", response_model=List[DemoNetworkInfo])
async def get_demo_networks(db: Session = Depends(get_db)):
    """Récupère les réseaux de démonstration capturés"""
    try:
        handshakes = DatabaseService.get_all_handshakes(db, limit=100)
        demo_networks = [h for h in handshakes if "demo" in (h.tags or "").lower()]
        
        networks = []
        for h in demo_networks:
            networks.append(DemoNetworkInfo(
                capture_id=h.capture_id,
                ssid=h.network_ssid,
                bssid=h.network_bssid,
                security_level=(h.tags or "").split(",")[0] if h.tags else "Unknown",
                capture_status="✓ Succès" if h.success else "✗ Échoué",
                handshake_status="✓ Trouvé" if h.handshake_found else "✗ Non trouvé",
                packets=h.packets_captured,
                duration=h.duration_seconds,
                file_size=h.file_size
            ))
        
        return networks
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cracking-results", response_model=List[DemoCrackingAttempt])
async def get_demo_cracking_results(db: Session = Depends(get_db)):
    """Récupère les résultats de craquage de démonstration"""
    try:
        handshakes = DatabaseService.get_all_handshakes(db, limit=100)
        demo_handshakes = [h for h in handshakes if "demo" in (h.tags or "").lower()]
        
        attempts = []
        for handshake in demo_handshakes:
            for cracking in handshake.cracking_attempts:
                attempts.append(DemoCrackingAttempt(
                    attempt_id=cracking.attempt_id,
                    network_ssid=cracking.network_ssid,
                    method=cracking.cracking_method,
                    wordlist=cracking.wordlist_name,
                    success=cracking.password_found,
                    password=cracking.password_result if cracking.password_found else None,
                    duration=cracking.duration_seconds,
                    passwords_tried=cracking.passwords_tried,
                    gpu_enabled=cracking.gpu_enabled
                ))
        
        return sorted(attempts, key=lambda x: (not x.success, x.method))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_demo_statistics(db: Session = Depends(get_db)):
    """Récupère les statistiques globales de la démonstration"""
    try:
        handshakes = DatabaseService.get_all_handshakes(db, limit=100)
        demo_handshakes = [h for h in handshakes if "demo" in (h.tags or "").lower()]
        
        total_captures = len(demo_handshakes)
        successful_captures = sum(1 for h in demo_handshakes if h.success)
        handshakes_found = sum(1 for h in demo_handshakes if h.handshake_found)
        
        total_attempts = sum(len(h.cracking_attempts) for h in demo_handshakes)
        successful_cracks = sum(1 for h in demo_handshakes for c in h.cracking_attempts if c.password_found)
        
        return {
            "total_networks_scanned": total_captures,
            "successful_captures": successful_captures,
            "capture_success_rate": 100 * successful_captures / total_captures if total_captures > 0 else 0,
            "handshakes_found": handshakes_found,
            "handshake_find_rate": 100 * handshakes_found / total_captures if total_captures > 0 else 0,
            "total_cracking_attempts": total_attempts,
            "successful_cracks": successful_cracks,
            "crack_success_rate": 100 * successful_cracks / total_attempts if total_attempts > 0 else 0,
            "critical_vulnerabilities": 3,
            "high_vulnerabilities": 2,
            "medium_vulnerabilities": 3,
            "low_vulnerabilities": 2,
            "overall_risk_score": 72.5,
            "audit_completion": "100%"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
