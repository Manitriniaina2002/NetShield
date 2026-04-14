"""SQLite Database Models for NetShield."""
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()


class HandshakeCaptureDB(Base):
    """Modèle de base de données pour les captures de handshakes."""
    __tablename__ = "handshake_captures"
    
    id = Column(Integer, primary_key=True, index=True)
    capture_id = Column(String(50), unique=True, index=True)
    network_ssid = Column(String(255), index=True)
    network_bssid = Column(String(17), index=True)  # Format AA:BB:CC:DD:EE:FF
    capture_file_path = Column(String(500))
    file_format = Column(String(10), default="pcap")  # pcap, cap, pcapng, hccapx
    file_size = Column(Integer, default=0)
    
    # Capture metadata
    interface_used = Column(String(50))
    duration_seconds = Column(Integer, default=0)
    packets_captured = Column(Integer, default=0)
    success = Column(Boolean, default=False)
    handshake_found = Column(Boolean, default=False)
    handshake_detected_at_second = Column(Integer, nullable=True)
    
    # Deauth info
    deauth_used = Column(Boolean, default=False)
    deauth_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Notes and metadata
    notes = Column(Text, nullable=True)
    tags = Column(String(255), nullable=True)  # Comma-separated tags
    
    # Cracking results
    cracking_attempts = relationship("CrackingAttemptDB", back_populates="handshake")
    
    class Config:
        from_attributes = True


class CrackingAttemptDB(Base):
    """Modèle de base de données pour les tentatives de craquage."""
    __tablename__ = "cracking_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(String(50), unique=True, index=True)
    handshake_id = Column(Integer, ForeignKey("handshake_captures.id"), index=True)
    
    network_ssid = Column(String(255), index=True)
    network_bssid = Column(String(17), index=True)
    
    # Cracking method
    cracking_method = Column(String(50), index=True)  # aircrack-ng, hashcat, john
    cracking_tool_version = Column(String(50), nullable=True)
    
    # Wordlist used
    wordlist_path = Column(String(500))
    wordlist_name = Column(String(100))
    wordlist_size = Column(Integer, default=0)  # Number of passwords
    
    # Results
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    password_found = Column(Boolean, default=False)
    password_result = Column(String(255), nullable=True)
    success_rate = Column(Float, default=0.0)
    
    # Performance
    duration_seconds = Column(Integer, default=0)
    passwords_tried = Column(Integer, default=0)
    gpu_enabled = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    handshake = relationship("HandshakeCaptureDB", back_populates="cracking_attempts")
    
    class Config:
        from_attributes = True


class ScanResultDB(Base):
    """Modèle de base de données pour les résultats de scan."""
    __tablename__ = "scan_results"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String(50), unique=True, index=True)
    
    # Scan info
    scan_type = Column(String(50))  # standard, kismet, advanced
    duration_seconds = Column(Integer, default=0)
    networks_found = Column(Integer, default=0)
    
    # Data
    scan_data = Column(Text)  # JSON-serialized network data
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    class Config:
        from_attributes = True


class VulnerabilityReportDB(Base):
    """Modèle de base de données pour les rapports de vulnérabilité."""
    __tablename__ = "vulnerability_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String(50), unique=True, index=True)
    
    # Report info
    network_bssid = Column(String(17))
    network_ssid = Column(String(255))
    
    # Vulnerabilities data (JSON)
    vulnerabilities_json = Column(Text)  # JSON-serialized
    recommendations_json = Column(Text)  # JSON-serialized
    
    # Summary
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    risk_score = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    class Config:
        from_attributes = True


class AppSessionDB(Base):
    """Modèle de base de données pour les sessions d'application."""
    __tablename__ = "app_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), unique=True, index=True)
    
    # Session info
    total_networks_scanned = Column(Integer, default=0)
    total_handshakes_captured = Column(Integer, default=0)
    total_cracking_attempts = Column(Integer, default=0)
    passwords_found = Column(Integer, default=0)
    
    # Mode
    simulation_mode = Column(Boolean, default=False)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    class Config:
        from_attributes = True


def get_db_engine(database_url: str = "sqlite:///./netshield.db"):
    """Crée et retourne le moteur SQLAlchemy."""
    # S'assurer que le répertoire existe
    db_dir = os.path.dirname(database_url.replace("sqlite:///", ""))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
        echo=False
    )
    return engine


def init_db(engine):
    """Initialise les tables de la base de données."""
    Base.metadata.create_all(bind=engine)


def get_session_maker(engine):
    """Retourne une SessionLocal factory."""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
