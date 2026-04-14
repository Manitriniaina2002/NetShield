"""Service de gestion de la base de données SQLite."""
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import (
    HandshakeCaptureDB,
    CrackingAttemptDB,
    ScanResultDB,
    VulnerabilityReportDB,
    AppSessionDB
)


class DatabaseService:
    """Service pour gérer toutes les opérations de base de données."""
    
    @staticmethod
    def save_handshake_capture(
        db: Session,
        capture_id: str,
        network_ssid: str,
        network_bssid: str,
        capture_file_path: Optional[str] = None,
        file_format: str = "pcap",
        file_size: int = 0,
        interface_used: str = "wlan0",
        duration_seconds: int = 0,
        packets_captured: int = 0,
        success: bool = False,
        handshake_found: bool = False,
        handshake_detected_at_second: Optional[int] = None,
        deauth_used: bool = False,
        deauth_count: int = 0,
        notes: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> HandshakeCaptureDB:
        """Sauvegarde une capture de handshake dans la base de données."""
        
        db_capture = HandshakeCaptureDB(
            capture_id=capture_id,
            network_ssid=network_ssid,
            network_bssid=network_bssid,
            capture_file_path=capture_file_path,
            file_format=file_format,
            file_size=file_size,
            interface_used=interface_used,
            duration_seconds=duration_seconds,
            packets_captured=packets_captured,
            success=success,
            handshake_found=handshake_found,
            handshake_detected_at_second=handshake_detected_at_second,
            deauth_used=deauth_used,
            deauth_count=deauth_count,
            notes=notes,
            tags=tags,
            completed_at=datetime.utcnow() if success else None,
        )
        
        db.add(db_capture)
        db.commit()
        db.refresh(db_capture)
        return db_capture
    
    @staticmethod
    def get_handshake_by_id(db: Session, capture_id: str) -> Optional[HandshakeCaptureDB]:
        """Récupère un handshake par son ID."""
        return db.query(HandshakeCaptureDB).filter(
            HandshakeCaptureDB.capture_id == capture_id
        ).first()

    @staticmethod
    def get_handshake_by_db_id(db: Session, handshake_id: int) -> Optional[HandshakeCaptureDB]:
        """Récupère un handshake par son identifiant numérique en base."""
        return db.query(HandshakeCaptureDB).filter(
            HandshakeCaptureDB.id == handshake_id
        ).first()
    
    @staticmethod
    def get_handshakes_by_network(
        db: Session,
        network_bssid: str,
        network_ssid: Optional[str] = None,
        successful_only: bool = True,
        limit: int = 100
    ) -> List[HandshakeCaptureDB]:
        """Récupère tous les handshakes d'un réseau."""
        query = db.query(HandshakeCaptureDB).filter(
            HandshakeCaptureDB.network_bssid == network_bssid
        )
        
        if network_ssid:
            query = query.filter(HandshakeCaptureDB.network_ssid == network_ssid)
        
        if successful_only:
            query = query.filter(HandshakeCaptureDB.success == True)
        
        return query.order_by(HandshakeCaptureDB.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_all_handshakes(
        db: Session,
        successful_only: bool = False,
        limit: int = 500
    ) -> List[HandshakeCaptureDB]:
        """Récupère tous les handshakes."""
        query = db.query(HandshakeCaptureDB)
        
        if successful_only:
            query = query.filter(HandshakeCaptureDB.success == True)
        
        return query.order_by(HandshakeCaptureDB.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def update_handshake_capture(
        db: Session,
        capture_id: str,
        success: bool = False,
        handshake_found: bool = False,
        duration_seconds: int = 0,
        packets_captured: int = 0,
        handshake_detected_at_second: Optional[int] = None,
        file_path: Optional[str] = None,
        file_size: int = 0,
        notes: Optional[str] = None,
    ) -> Optional[HandshakeCaptureDB]:
        """Met à jour un handshake existant."""
        db_capture = db.query(HandshakeCaptureDB).filter(
            HandshakeCaptureDB.capture_id == capture_id
        ).first()
        
        if not db_capture:
            return None
        
        db_capture.success = success
        db_capture.handshake_found = handshake_found
        db_capture.duration_seconds = duration_seconds
        db_capture.packets_captured = packets_captured
        db_capture.handshake_detected_at_second = handshake_detected_at_second
        
        if file_path:
            db_capture.capture_file_path = file_path
        
        if file_size > 0:
            db_capture.file_size = file_size
        
        if notes:
            db_capture.notes = notes
        
        if success:
            db_capture.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_capture)
        return db_capture
    
    @staticmethod
    def save_cracking_attempt(
        db: Session,
        attempt_id: str,
        network_ssid: str,
        network_bssid: str,
        cracking_method: str,
        wordlist_path: str,
        wordlist_name: str,
        handshake_id: Optional[int] = None,
        wordlist_size: int = 0,
        gpu_enabled: bool = False,
        notes: Optional[str] = None,
    ) -> CrackingAttemptDB:
        """Sauvegarde une tentative de craquage."""
        
        db_attempt = CrackingAttemptDB(
            attempt_id=attempt_id,
            network_ssid=network_ssid,
            network_bssid=network_bssid,
            cracking_method=cracking_method,
            wordlist_path=wordlist_path,
            wordlist_name=wordlist_name,
            handshake_id=handshake_id,
            wordlist_size=wordlist_size,
            gpu_enabled=gpu_enabled,
            notes=notes,
        )
        
        db.add(db_attempt)
        db.commit()
        db.refresh(db_attempt)
        return db_attempt
    
    @staticmethod
    def update_cracking_attempt(
        db: Session,
        attempt_id: str,
        status: str = "pending",
        password_found: bool = False,
        password_result: Optional[str] = None,
        duration_seconds: int = 0,
        passwords_tried: int = 0,
        success_rate: float = 0.0,
    ) -> Optional[CrackingAttemptDB]:
        """Met à jour une tentative de craquage."""
        db_attempt = db.query(CrackingAttemptDB).filter(
            CrackingAttemptDB.attempt_id == attempt_id
        ).first()
        
        if not db_attempt:
            return None
        
        db_attempt.status = status
        db_attempt.password_found = password_found
        db_attempt.password_result = password_result
        db_attempt.duration_seconds = duration_seconds
        db_attempt.passwords_tried = passwords_tried
        db_attempt.success_rate = success_rate
        
        if status == "running":
            db_attempt.started_at = datetime.utcnow()
        elif status == "completed":
            db_attempt.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_attempt)
        return db_attempt
    
    @staticmethod
    def get_cracking_attempts_by_handshake(
        db: Session,
        handshake_id: int,
        limit: int = 100
    ) -> List[CrackingAttemptDB]:
        """Récupère tous les craquages d'un handshake."""
        return db.query(CrackingAttemptDB).filter(
            CrackingAttemptDB.handshake_id == handshake_id
        ).order_by(CrackingAttemptDB.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_successful_cracking_attempts(
        db: Session,
        network_bssid: str,
        limit: int = 100
    ) -> List[CrackingAttemptDB]:
        """Récupère les craquages réussis pour un réseau."""
        return db.query(CrackingAttemptDB).filter(
            CrackingAttemptDB.network_bssid == network_bssid,
            CrackingAttemptDB.password_found == True
        ).order_by(CrackingAttemptDB.completed_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_statistics(db: Session) -> Dict[str, Any]:
        """Récupère les statistiques globales."""
        total_captures = db.query(HandshakeCaptureDB).count()
        successful_captures = db.query(HandshakeCaptureDB).filter(
            HandshakeCaptureDB.success == True
        ).count()
        handshakes_found = db.query(HandshakeCaptureDB).filter(
            HandshakeCaptureDB.handshake_found == True
        ).count()
        
        total_attempts = db.query(CrackingAttemptDB).count()
        successful_cracks = db.query(CrackingAttemptDB).filter(
            CrackingAttemptDB.password_found == True
        ).count()
        
        unique_networks = db.query(HandshakeCaptureDB.network_bssid).distinct().count()
        
        return {
            "total_captures": total_captures,
            "successful_captures": successful_captures,
            "handshakes_found": handshakes_found,
            "capture_success_rate": (
                (successful_captures / total_captures * 100) if total_captures > 0 else 0
            ),
            "total_cracking_attempts": total_attempts,
            "successful_cracks": successful_cracks,
            "crack_success_rate": (
                (successful_cracks / total_attempts * 100) if total_attempts > 0 else 0
            ),
            "unique_networks": unique_networks,
        }
    
    @staticmethod
    def save_scan_result(
        db: Session,
        scan_id: str,
        scan_type: str,
        duration_seconds: int,
        networks_found: int,
        scan_data: List[Dict[str, Any]],
    ) -> ScanResultDB:
        """Sauvegarde un résultat de scan."""
        
        db_scan = ScanResultDB(
            scan_id=scan_id,
            scan_type=scan_type,
            duration_seconds=duration_seconds,
            networks_found=networks_found,
            scan_data=json.dumps(scan_data),
        )
        
        db.add(db_scan)
        db.commit()
        db.refresh(db_scan)
        return db_scan
    
    @staticmethod
    def delete_handshake(db: Session, capture_id: str) -> bool:
        """Supprime un handshake et ses craquages associés."""
        db_capture = db.query(HandshakeCaptureDB).filter(
            HandshakeCaptureDB.capture_id == capture_id
        ).first()
        
        if not db_capture:
            return False
        
        # Delete associated cracking attempts
        db.query(CrackingAttemptDB).filter(
            CrackingAttemptDB.handshake_id == db_capture.id
        ).delete()
        
        # Delete the capture
        db.delete(db_capture)
        db.commit()
        return True
    
    @staticmethod
    def clear_old_captures(db: Session, days: int = 30) -> int:
        """Supprime les captures de plus de N jours."""
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Delete associated attempts first
        old_captures = db.query(HandshakeCaptureDB).filter(
            HandshakeCaptureDB.created_at < cutoff_date
        ).all()
        
        for capture in old_captures:
            db.query(CrackingAttemptDB).filter(
                CrackingAttemptDB.handshake_id == capture.id
            ).delete()
        
        # Delete captures
        deleted_count = db.query(HandshakeCaptureDB).filter(
            HandshakeCaptureDB.created_at < cutoff_date
        ).delete()
        
        db.commit()
        return deleted_count
