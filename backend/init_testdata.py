#!/usr/bin/env python
"""Initialize database with test data"""
from app.models.database import get_db_engine, get_session_maker, HandshakeCaptureDB, CrackingAttemptDB
from datetime import datetime, timedelta

engine = get_db_engine()
SessionLocal = get_session_maker(engine)
db = SessionLocal()

# Add test handshake captures
captures = [
    HandshakeCaptureDB(
        capture_id="cap_001",
        network_ssid="HomeWiFi",
        network_bssid="AA:BB:CC:DD:EE:01",
        capture_file_path="/captures/homewifi.cap",
        file_size=102400,
        file_format="pcap",
        deauth_used=True,
        deauth_count=5,
        packets_captured=1500,
        duration_seconds=120,
        success=True,
        handshake_found=True,
        created_at=datetime.utcnow() - timedelta(hours=2)
    ),
    HandshakeCaptureDB(
        capture_id="cap_002",
        network_ssid="Office-Network",
        network_bssid="AA:BB:CC:DD:EE:02",
        capture_file_path="/captures/office.cap",
        file_size=256000,
        file_format="pcap",
        deauth_used=True,
        deauth_count=10,
        packets_captured=3200,
        duration_seconds=180,
        success=True,
        handshake_found=True,
        created_at=datetime.utcnow() - timedelta(hours=1)
    ),
    HandshakeCaptureDB(
        capture_id="cap_003",
        network_ssid="Guest-WiFi",
        network_bssid="AA:BB:CC:DD:EE:03",
        capture_file_path="/captures/guest.cap",
        file_size=51200,
        file_format="pcap",
        deauth_used=False,
        deauth_count=0,
        packets_captured=800,
        duration_seconds=60,
        success=False,
        handshake_found=False,
        created_at=datetime.utcnow() - timedelta(minutes=30)
    )
]

for capture in captures:
    db.add(capture)

db.commit()

# Add test cracking attempts
attempt1 = CrackingAttemptDB(
    attempt_id="attempt_001",
    handshake_id=1,
    network_ssid="HomeWiFi",
    network_bssid="AA:BB:CC:DD:EE:01",
    cracking_method="aircrack-ng",
    wordlist_path="/wordlists/rockyou.txt",
    wordlist_name="rockyou",
    wordlist_size=14344391,
    status="completed",
    password_found=True,
    password_result="SecurePass123!",
    passwords_tried=15000,
    gpu_enabled=False,
    duration_seconds=120,
    created_at=datetime.utcnow() - timedelta(hours=1)
)

attempt2 = CrackingAttemptDB(
    attempt_id="attempt_002",
    handshake_id=2,
    network_ssid="Office-Network",
    network_bssid="AA:BB:CC:DD:EE:02",
    cracking_method="hashcat",
    wordlist_path="/wordlists/academic.txt",
    wordlist_name="academic",
    wordlist_size=5000,
    status="completed",
    password_found=True,
    password_result="Password2024",
    passwords_tried=5000,
    gpu_enabled=True,
    duration_seconds=45,
    created_at=datetime.utcnow() - timedelta(minutes=45)
)

db.add(attempt1)
db.add(attempt2)
db.commit()

print("✓ Test data added successfully!")
print(f"  - 3 handshake captures (2 successful, 1 failed)")
print(f"  - 2 cracking attempts (both successful)")
print(f"  - Statistics will show: 3 total, 2 successful, 2 passwords found")

db.close()

