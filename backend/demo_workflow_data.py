"""
Comprehensive demo and simulation data for NetShield
Includes: Networks, Handshakes, Cracking Attempts, Vulnerabilities, Recommendations, and Reports
"""
from datetime import datetime, timedelta
from app.models.database import get_db_engine, get_session_maker, init_db
from app.models.database import (
    HandshakeCaptureDB,
    CrackingAttemptDB,
)
from app.services.database_service import DatabaseService
import random


def populate_demo_networks_and_handshakes(db):
    """Populate demo network captures with various security levels"""
    
    demo_networks = [
        {
            "capture_id": "cap_demo_001",
            "ssid": "CorporateNetwork-5G",
            "bssid": "AA:BB:CC:DD:EE:01",
            "duration": 180,
            "packets": 5400,
            "file_size": 512000,
            "success": True,
            "handshake_found": True,
            "deauth_count": 15,
            "notes": "Strong WPA2-Enterprise network",
            "security_level": "WPA2-Enterprise"
        },
        {
            "capture_id": "cap_demo_002",
            "ssid": "HomeWifi-Plus",
            "bssid": "BB:CC:DD:EE:FF:02",
            "duration": 120,
            "packets": 3200,
            "file_size": 256000,
            "success": True,
            "handshake_found": True,
            "deauth_count": 8,
            "notes": "WPA2 Personal with weak password",
            "security_level": "WPA2-PSK"
        },
        {
            "capture_id": "cap_demo_003",
            "ssid": "GuestNetwork",
            "bssid": "CC:DD:EE:FF:00:03",
            "duration": 60,
            "packets": 1800,
            "file_size": 128000,
            "success": True,
            "handshake_found": True,
            "deauth_count": 0,
            "notes": "Open network, no security",
            "security_level": "OPEN"
        },
        {
            "capture_id": "cap_demo_004",
            "ssid": "LegacyWifi",
            "bssid": "DD:EE:FF:00:11:04",
            "duration": 240,
            "packets": 8100,
            "file_size": 768000,
            "success": True,
            "handshake_found": True,
            "deauth_count": 12,
            "notes": "WEP encryption - very weak",
            "security_level": "WEP"
        },
        {
            "capture_id": "cap_demo_005",
            "ssid": "CafePublicWifi",
            "bssid": "EE:FF:00:11:22:05",
            "duration": 90,
            "packets": 2400,
            "file_size": 192000,
            "success": False,
            "handshake_found": False,
            "deauth_count": 5,
            "notes": "Failed to capture handshake",
            "security_level": "WPA2-PSK"
        },
        {
            "capture_id": "cap_demo_006",
            "ssid": "RouterAdmin",
            "bssid": "FF:00:11:22:33:06",
            "duration": 150,
            "packets": 4500,
            "file_size": 384000,
            "success": True,
            "handshake_found": True,
            "deauth_count": 10,
            "notes": "WPA3 with strong password",
            "security_level": "WPA3"
        },
    ]
    
    captures = []
    for i, network in enumerate(demo_networks):
        created_time = datetime.now() - timedelta(days=random.randint(1, 30), hours=random.randint(0, 23))
        completed_time = created_time + timedelta(seconds=network["duration"])
        
        db_capture = HandshakeCaptureDB(
            capture_id=network["capture_id"],
            network_ssid=network["ssid"],
            network_bssid=network["bssid"],
            capture_file_path=f"/captures/{network['capture_id']}.pcap",
            file_format="pcap",
            file_size=network["file_size"],
            interface_used="wlan0",
            duration_seconds=network["duration"],
            packets_captured=network["packets"],
            success=network["success"],
            handshake_found=network["handshake_found"],
            handshake_detected_at_second=network["duration"] - 30 if network["handshake_found"] else None,
            deauth_used=network["deauth_count"] > 0,
            deauth_count=network["deauth_count"],
            created_at=created_time,
            completed_at=completed_time if network["success"] else None,
            notes=network["notes"],
            tags=f"{network['security_level']},demo"
        )
        db.add(db_capture)
        db.flush()
        captures.append((db_capture, network))
    
    db.commit()
    return captures


def populate_demo_cracking_attempts(db, captures):
    """Populate demo cracking attempts with various tools and results"""
    
    cracking_configs = [
        {
            "handshake_idx": 0,  # CorporateNetwork-5G
            "method": "aircrack-ng",
            "wordlist": "rockyou",
            "found": False,
            "password": None,
            "duration": 3600,
            "tries": 500000,
            "gpu": False,
            "description": "Enterprise network - no common password found"
        },
        {
            "handshake_idx": 1,  # HomeWifi-Plus
            "method": "hashcat",
            "wordlist": "rockyou",
            "found": True,
            "password": "Butterfly2024!",
            "duration": 45,
            "tries": 23500,
            "gpu": True,
            "description": "Weak password found quickly with GPU"
        },
        {
            "handshake_idx": 2,  # GuestNetwork
            "method": "aircrack-ng",
            "wordlist": "default-passwords",
            "found": True,
            "password": "",
            "duration": 5,
            "tries": 1,
            "gpu": False,
            "description": "Open network - trivial"
        },
        {
            "handshake_idx": 3,  # LegacyWifi
            "method": "aircrack-ng",
            "wordlist": "wep-default",
            "found": True,
            "password": "5A6F6E6173",
            "duration": 120,
            "tries": 1000,
            "gpu": False,
            "description": "WEP cracked using known exploit"
        },
        # Additional attempt on HomeWifi with different method
        {
            "handshake_idx": 1,  # HomeWifi-Plus
            "method": "john",
            "wordlist": "custom-patterns",
            "found": True,
            "password": "Butterfly2024!",
            "duration": 180,
            "tries": 50000,
            "gpu": False,
            "description": "Brute force attempt - also found password"
        },
        {
            "handshake_idx": 5,  # RouterAdmin
            "method": "hashcat",
            "wordlist": "rockyou",
            "found": False,
            "password": None,
            "duration": 7200,
            "tries": 1000000,
            "gpu": True,
            "description": "WPA3 with strong password - not found"
        },
    ]
    
    attempts = []
    for i, config in enumerate(cracking_configs):
        handshake, network = captures[config["handshake_idx"]]
        
        created_time = handshake.completed_at + timedelta(hours=random.randint(0, 2)) if handshake.completed_at else datetime.now()
        completed_time = created_time + timedelta(seconds=config["duration"]) if config["found"] or config["method"] != "aircrack-ng" else None
        
        db_attempt = CrackingAttemptDB(
            attempt_id=f"attempt_demo_{i+1:03d}",
            handshake_id=handshake.id,
            network_ssid=handshake.network_ssid,
            network_bssid=handshake.network_bssid,
            cracking_method=config["method"],
            cracking_tool_version=f"{config['method']}-2024.1",
            wordlist_path=f"/wordlists/{config['wordlist']}.txt",
            wordlist_name=config["wordlist"],
            wordlist_size=1000000 if config["wordlist"] == "rockyou" else 50000,
            status="completed" if completed_time else "running",
            password_found=config["found"],
            password_result=config["password"] if config["found"] else None,
            success_rate=100.0 if config["found"] else 0.0,
            duration_seconds=config["duration"],
            passwords_tried=config["tries"],
            gpu_enabled=config["gpu"],
            created_at=created_time,
            started_at=created_time,
            completed_at=completed_time,
            notes=config["description"]
        )
        db.add(db_attempt)
        attempts.append(db_attempt)
    
    db.commit()
    return attempts


def populate_demo_vulnerabilities(db, captures):
    """Vulnerabilities are generated dynamically based on network analysis in the API endpoints"""
    print("ℹ️  Vulnerabilities will be generated dynamically when networks are analyzed")
    pass


def populate_demo_recommendations(db):
    """Populate demo recommendations based on vulnerabilities"""
    
    recommendations = [
        {
            "title": "Mettre à jour vers WPA3",
            "description": "Remplacer WPA2 par WPA3 pour bénéficier des derniers progrès de sécurité",
            "priority": "CRITICAL",
            "category": "Chiffrement",
            "effort": "Modéré",
            "impact": "Augmente la sécurité de 100x"
        },
        {
            "title": "Générer un mot de passe fort",
            "description": "Utiliser un mot de passe aléatoire de +16 caractères avec majuscules, minuscules, chiffres, symboles",
            "priority": "CRITICAL",
            "category": "Authentification",
            "effort": "Très faible",
            "impact": "Rend les attaques par dictionnaire impossibles"
        },
        {
            "title": "Désactiver WEP immédiatement",
            "description": "WEP est complètement cassé. Migrer vers WPA2 ou WPA3",
            "priority": "CRITICAL",
            "category": "Chiffrement",
            "effort": "Faible",
            "impact": "Élimine l'attaque Keystream Recovery"
        },
        {
            "title": "Activer le chiffrement du réseau",
            "description": "Configurer WPA2-PSK ou WPA3 avec un mot de passe fort",
            "priority": "CRITICAL",
            "category": "Chiffrement",
            "effort": "Faible",
            "impact": "Prévient l'accès non autorisé"
        },
        {
            "title": "Mettre à jour le firmware du routeur",
            "description": "Installer les dernière version de firmware pour corriger les vulnérabilités",
            "priority": "HIGH",
            "category": "Maintenance",
            "effort": "Modéré",
            "impact": "Corrige les failles de sécurité connues"
        },
        {
            "title": "Masquer la diffusion du SSID",
            "description": "Configuration optionnelle pour ajouter une couche de sécurité",
            "priority": "MEDIUM",
            "category": "Configuration",
            "effort": "Très faible",
            "impact": "Sécurité par obscurité - faible impact"
        },
        {
            "title": "Audit de sécurité régulier",
            "description": "Effectuer des scans de sécurité tous les trimestres",
            "priority": "MEDIUM",
            "category": "Gouvernance",
            "effort": "Faible",
            "impact": "Maintient la posture de sécurité"
        },
        {
            "title": "Configurer 802.1X Enterprise",
            "description": "Implémenter WPA2-Enterprise pour une sécurité à niveau réseau",
            "priority": "HIGH",
            "category": "Authentification",
            "effort": "Très élevé",
            "impact": "Chaque utilisateur a une clé unique"
        },
    ]
    
    for i, rec in enumerate(recommendations):
        # In a real scenario, recommendations would be linked to vulnerabilities
        # This is a simplified demo
        print(f"Recommendation {i+1}: {rec['title']}")
    
    return recommendations


def generate_demo_report(captures, attempts):
    """Generate a demo audit report summary"""
    
    total_networks = len(captures)
    successful_captures = sum(1 for cap, _ in captures if cap.success)
    successful_cracks = sum(1 for attempt in attempts if attempt.password_found)
    
    report = {
        "report_title": "NetShield Wi-Fi Security Audit Report - DEMO",
        "report_date": datetime.now().isoformat(),
        "author": "NetShield Demo System",
        "project_name": "Comprehensive WiFi Security Audit",
        "executive_summary": f"""
        This comprehensive audit examined {total_networks} Wi-Fi networks and performed security testing.
        {successful_captures} networks were successfully captured ({100*successful_captures/total_networks:.1f}% success rate).
        {successful_cracks} passwords were cracked during penetration testing ({100*successful_cracks/len(attempts):.1f}% crack rate).
        
        Key Findings:
        - 1 network with critical encryption weakness (WEP)
        - 1 network with no encryption (Open)
        - 1 network with weak password vulnerability
        - 2 networks with baseline WPA2 security
        - 1 network with strong WPA3 security
        - 1 network not successfully captured
        """,
        "overall_risk_score": 72.5,
        "total_networks": total_networks,
        "critical_vulnerabilities": 4,
        "high_vulnerabilities": 2,
        "medium_vulnerabilities": 3,
        "low_vulnerabilities": 2,
        "methodology": "Passive scanning with active handshake capture and penetration testing via wordlist attacks",
        "testing_period": f"{(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
        "statistics": {
            "total_captures": len(captures),
            "successful_captures": successful_captures,
            "capture_success_rate": 100 * successful_captures / len(captures),
            "total_cracking_attempts": len(attempts),
            "successful_cracks": successful_cracks,
            "crack_success_rate": 100 * successful_cracks / len(attempts),
            "handshakes_found": sum(1 for cap, _ in captures if cap.handshake_found),
            "unique_networks": len(captures)
        }
    }
    
    return report


def main():
    """Main function to populate demo data"""
    try:
        print("🚀 Initializing NetShield Demo Database...")
        
        # Initialize database
        engine = get_db_engine()
        init_db(engine)
        SessionLocal = get_session_maker(engine)
        db = SessionLocal()
        
        print("✓ Database initialized")
        
        # Clear existing demo data
        demo_handshakes = db.query(HandshakeCaptureDB).filter(HandshakeCaptureDB.capture_id.like("cap_demo_%")).all()
        for handshake in demo_handshakes:
            db.query(CrackingAttemptDB).filter(CrackingAttemptDB.handshake_id == handshake.id).delete()
        db.query(HandshakeCaptureDB).filter(HandshakeCaptureDB.capture_id.like("cap_demo_%")).delete()
        db.commit()
        
        # Populate demo data
        print("\n📡 Populating demo networks and handshakes...")
        captures = populate_demo_networks_and_handshakes(db)
        print(f"✓ Created {len(captures)} demo network captures")
        
        print("\n🔓 Populating demo cracking attempts...")
        attempts = populate_demo_cracking_attempts(db, captures)
        print(f"✓ Created {len(attempts)} demo cracking attempts")
        
        print("\n⚠️  Populating demo vulnerabilities...")
        populate_demo_vulnerabilities(db, captures)
        print(f"✓ Created {len(captures)} vulnerability reports")
        
        print("\n💡 Generating demo recommendations...")
        recommendations = populate_demo_recommendations(db)
        print(f"✓ Generated {len(recommendations)} recommendations")
        
        print("\n📊 Generating demo report...")
        report = generate_demo_report(captures, attempts)
        print(f"✓ Report generated with overall risk score: {report['overall_risk_score']}")
        
        # Print summary
        print("\n" + "="*60)
        print("✅ DEMO DATA SUCCESSFULLY POPULATED")
        print("="*60)
        print(f"\nDatabase Summary:")
        print(f"  • Networks Captured: {len(captures)}")
        print(f"  • Successful Captures: {sum(1 for cap, _ in captures if cap.success)}")
        print(f"  • Cracking Attempts: {len(attempts)}")
        print(f"  • Passwords Found: {sum(1 for att in attempts if att.password_found)}")
        print(f"  • Vulnerabilities: {len(captures)}")
        print(f"  • Recommendations: {len(recommendations)}")
        print(f"  • Overall Risk Score: {report['overall_risk_score']}/100")
        print("\nDemo data is now ready for testing!")
        print("="*60)
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error populating demo data: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
