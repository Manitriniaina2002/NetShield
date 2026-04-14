"""API routes pour la gestion des handshakes stockés dans la base de données."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.database import get_db_engine, get_session_maker, init_db
from app.services.database_service import DatabaseService

router = APIRouter(prefix="/api/stored", tags=["stored-handshakes"])

# Initialize database on first import
try:
    engine = get_db_engine()
    init_db(engine)
    SessionLocal = get_session_maker(engine)
except Exception as e:
    print(f"Database initialization warning: {e}")
    SessionLocal = None


def get_db():
    """Dependency pour obtenir une session de base de données."""
    if SessionLocal is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models for responses
class StoredHandshakeResponse(BaseModel):
    """Réponse pour un handshake stocké."""
    id: int
    capture_id: str
    network_ssid: str
    network_bssid: str
    file_format: str
    file_size: int
    success: bool
    handshake_found: bool
    duration_seconds: int
    packets_captured: int
    deauth_used: bool
    deauth_count: int
    created_at: str
    completed_at: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('created_at', 'completed_at', mode='before')
    @classmethod
    def format_datetime(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v


class CrackingResultResponse(BaseModel):
    """Réponse pour un résultat de craquage."""
    id: int
    attempt_id: str
    network_ssid: str
    network_bssid: str
    cracking_method: str
    wordlist_name: str
    status: str
    password_found: bool
    password_result: Optional[str] = None
    duration_seconds: int
    passwords_tried: int
    gpu_enabled: bool
    created_at: str
    completed_at: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('created_at', 'completed_at', mode='before')
    @classmethod
    def format_datetime(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v


class StatisticsResponse(BaseModel):
    """Réponse pour les statistiques."""
    total_captures: int
    successful_captures: int
    handshakes_found: int
    capture_success_rate: float
    total_cracking_attempts: int
    successful_cracks: int
    crack_success_rate: float
    unique_networks: int


@router.get("/handshakes")
async def get_all_stored_handshakes(
    db: Session = Depends(get_db),
    successful_only: bool = False,
    limit: int = 100
) -> List[StoredHandshakeResponse]:
    """Récupère tous les handshakes stockés."""
    handshakes = DatabaseService.get_all_handshakes(
        db,
        successful_only=successful_only,
        limit=limit
    )
    return handshakes


@router.get("/handshakes/network/{network_bssid}")
async def get_handshakes_by_network(
    network_bssid: str,
    db: Session = Depends(get_db),
    network_ssid: Optional[str] = None,
    successful_only: bool = True,
    limit: int = 100
) -> List[StoredHandshakeResponse]:
    """Récupère tous les handshakes d'un réseau spécifique."""
    handshakes = DatabaseService.get_handshakes_by_network(
        db,
        network_bssid=network_bssid,
        network_ssid=network_ssid,
        successful_only=successful_only,
        limit=limit
    )
    return handshakes


@router.get("/handshakes/{capture_id}")
async def get_handshake_details(
    capture_id: str,
    db: Session = Depends(get_db)
) -> StoredHandshakeResponse:
    """Récupère les détails d'un handshake spécifique."""
    handshake = DatabaseService.get_handshake_by_id(db, capture_id)
    
    if not handshake:
        raise HTTPException(status_code=404, detail="Handshake not found")
    
    return handshake


@router.get("/handshakes/{capture_id}/cracking-history")
async def get_cracking_history(
    capture_id: str,
    db: Session = Depends(get_db),
    limit: int = 50
) -> List[CrackingResultResponse]:
    """Récupère l'historique de craquage pour un handshake."""
    handshake = DatabaseService.get_handshake_by_id(db, capture_id)
    
    if not handshake:
        raise HTTPException(status_code=404, detail="Handshake not found")
    
    attempts = DatabaseService.get_cracking_attempts_by_handshake(
        db,
        handshake_id=handshake.id,
        limit=limit
    )
    return attempts


@router.get("/cracking-results/network/{network_bssid}")
async def get_successful_cracks(
    network_bssid: str,
    db: Session = Depends(get_db),
    limit: int = 50
) -> List[CrackingResultResponse]:
    """Récupère les craquages réussis pour un réseau."""
    attempts = DatabaseService.get_successful_cracking_attempts(
        db,
        network_bssid=network_bssid,
        limit=limit
    )
    return attempts


@router.get("/statistics")
async def get_global_statistics(
    db: Session = Depends(get_db)
) -> StatisticsResponse:
    """Récupère les statistiques globales."""
    stats = DatabaseService.get_statistics(db)
    return StatisticsResponse(**stats)


@router.delete("/handshakes/{capture_id}")
async def delete_stored_handshake(
    capture_id: str,
    db: Session = Depends(get_db)
) -> dict:
    """Supprime un handshake stocké."""
    success = DatabaseService.delete_handshake(db, capture_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Handshake not found")
    
    return {"status": "deleted", "capture_id": capture_id}


@router.post("/cleanup/old-captures")
async def cleanup_old_captures(
    days: int = 30,
    db: Session = Depends(get_db)
) -> dict:
    """Supprime les handshakes de plus de N jours."""
    deleted_count = DatabaseService.clear_old_captures(db, days=days)
    
    return {
        "status": "completed",
        "deleted_count": deleted_count,
        "days_threshold": days
    }
