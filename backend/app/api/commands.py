"""Routes API pour les commandes système"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.services.command_execution import CommandExecutionService

router = APIRouter(prefix="/api/commands", tags=["Commands"])


class AuthRequest(BaseModel):
    """Demande d'authentification"""
    password: str
    description: Optional[str] = None


class CommandRequest(BaseModel):
    """Demande d'exécution de commande"""
    command: str
    args: Optional[List[str]] = None
    session_id: str


@router.get("/allowed")
async def get_allowed_commands():
    """
    Récupère la liste des commandes autorisées
    
    Returns:
        Dict des commandes autorisées avec leurs descriptions
    """
    return {
        "commands": CommandExecutionService.ALLOWED_COMMANDS,
        "note": "Toutes les commandes requièrent une authentification admin préalable"
    }


@router.post("/auth")
async def authenticate_admin(auth: AuthRequest):
    """
    Authentifie l'utilisateur en tant qu'administrateur
    
    Args:
        auth: Objet contenant le mot de passe
        
    Returns:
        Session ID si authentification réussie
        
    Responses:
        200: Authentification réussie
        401: Authentification échouée
    """
    try:
        result = await CommandExecutionService.verify_admin_auth(auth.password)
        
        if result["success"]:
            return {
                "success": True,
                "session_id": result["session_id"],
                "message": result.get("message", "Authentification réussie"),
                "expires_in": result["expires_in"],
                "is_root": result.get("is_root", False),
                "is_admin": result.get("is_admin", False)
            }
        else:
            raise HTTPException(status_code=401, detail=result["error"])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute")
async def execute_command(request: CommandRequest):
    """
    Exécute une commande de manière sécurisée
    
    SÉCURITÉ: Authentification admin requise
    
    Args:
        request: Objet contenant:
            - command: Commande à exécuter (whitelist)
            - args: Arguments additionnels
            - session_id: ID de session authentifiée
        
    Returns:
        Résultat de l'exécution
        
    Responses:
        200: Exécution réussie
        401: Session invalide/expirée
        403: Commande non autorisée
    """
    try:
        result = await CommandExecutionService.execute_command(
            command=request.command,
            args=request.args,
            session_id=request.session_id
        )
        
        if result.get("require_auth"):
            raise HTTPException(status_code=401, detail=result["error"])
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute-safe")
async def execute_command_with_confirmation(
    command: str = Query(..., description="Commande à exécuter"),
    args: List[str] = Query(None, description="Arguments additionnels"),
    session_id: str = Query(..., description="ID de session authentifiée"),
    confirmed: bool = Query(False, description="L'utilisateur a confirmé?")
):
    """
    Exécute une commande après double confirmation
    
    SÉCURITÉ: Authentification admin + confirmation utilisateur requises
    
    Args:
        command: Commande à exécuter
        args: Arguments
        session_id: ID de session authentifiée
        confirmed: Confirmation de l'utilisateur
        
    Returns:
        Résultat ou erreur si non confirmé
        
    Responses:
        200: Exécution réussie ou demande de confirmation
        401: Session invalide/expirée
    """
    try:
        # Vérifier la session
        if not CommandExecutionService.verify_session(session_id):
            raise HTTPException(status_code=401, detail="Session expirée - Ré-authentifiez")
        
        if not confirmed:
            return {
                "success": False,
                "require_confirmation": True,
                "command_preview": f"{command} {' '.join(args or [])}",
                "warning": "⚠️ Cette commande système va s'exécuter. Êtes-vous sûr?"
            }
        
        result = await CommandExecutionService.execute_command(
            command=command,
            args=args,
            session_id=session_id
        )
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
