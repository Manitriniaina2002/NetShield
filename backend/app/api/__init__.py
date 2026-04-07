"""Module d'initialisation des routes API"""
from fastapi import APIRouter
from .scan import router as scan_router
from .vulnerabilities import router as vulnerabilities_router
from .recommendations import router as recommendations_router
from .reports import router as reports_router
from .commands import router as commands_router
from .cracking import router as cracking_router

# Créer le routeur API principal
api_router = APIRouter()

# Inclure tous les sous-routeurs
api_router.include_router(scan_router)
api_router.include_router(vulnerabilities_router)
api_router.include_router(recommendations_router)
api_router.include_router(reports_router)
api_router.include_router(commands_router)
api_router.include_router(cracking_router)

__all__ = ["api_router"]
