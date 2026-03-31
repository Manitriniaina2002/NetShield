"""Application MainFastAPI NetShield"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.api import api_router
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Créer l'application FastAPI
app = FastAPI(
    title="NetShield - Wi-Fi Security Audit Lab",
    description="Application d'audit de sécurité Wi-Fi pour fins éducatives et defensives",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Récupérer les paramètres
settings = get_settings()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware de logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware pour logger les requêtes"""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


# Routes principales
@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "Bienvenue sur NetShield - Wi-Fi Security Audit Lab",
        "version": settings.app_version,
        "docs": "/api/docs",
        "legal_notice": settings.legal_notice
    }


@app.get("/health")
async def health_check():
    """Vérification de l'état de l'application"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "simulation_mode": settings.simulation_mode
    }


@app.get("/api/info")
async def app_info():
    """Informations sur l'application"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Plateforme d'audit Wi-Fi professionnelle pour fins éducatives",
        "features": [
            "Scan Wi-Fi intelligent",
            "Analyse de vulnérabilités",
            "Simulations d'attaques",
            "Recommandations de sécurité automatiques",
            "Génération de rapports PDF professionnels",
            "Terminal intégré",
            "Gestion des interfaces réseau"
        ],
        "legal_notice": settings.legal_notice,
        "simulation_mode": settings.simulation_mode
    }


# Inclure les routes API
app.include_router(api_router)


# Gestion des erreurs globale
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Gestionnaire d'erreur global"""
    logger.error(f"Erreur non gérée: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Une erreur interne s'est produite",
            "error": str(exc) if settings.debug else "Internal server error"
        }
    )


# Events de démarrage/arrêt
@app.on_event("startup")
async def startup_event():
    """Événement de démarrage"""
    logger.info(f"Démarrage de {settings.app_name} v{settings.app_version}")
    logger.info(f"Mode simulation: {settings.simulation_mode}")
    logger.info(f"Debug: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Événement d'arrêt"""
    logger.info(f"Arrêt de {settings.app_name}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
