"""Routes API pour la génération de rapports"""
from fastapi import APIRouter, HTTPException, Response
from app.models.scan import AuditReport
from app.services.pdf_report import PDFReportService
import json

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.post("/pdf")
async def generate_pdf_report(report: AuditReport):
    """
    Génère un rapport PDF d'audit Wi-Fi
    
    Args:
        report: Données du rapport
        
    Returns:
        PDF généré
    """
    try:
        pdf_buffer = PDFReportService.generate_audit_report(report)
        
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=audit_report.pdf"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
async def save_report(report: AuditReport, filename: str = None):
    """
    Sauvegarde le rapport PDF sur disque
    
    Args:
        report: Données du rapport
        filename: Nom du fichier (optionnel)
        
    Returns:
        Chemin du fichier sauvegardé
    """
    try:
        filepath = await PDFReportService.save_report_to_file(report, filename)
        
        return {
            "success": True,
            "filepath": filepath,
            "message": f"Rapport sauvegardé: {filepath}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/json")
async def export_report_json(report: AuditReport):
    """
    Exporte le rapport au format JSON
    
    Args:
        report: Données du rapport
        
    Returns:
        JSON du rapport
    """
    try:
        report_dict = report.dict()
        
        return Response(
            content=json.dumps(report_dict, indent=2, default=str),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=audit_report.json"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/{report_id}")
async def get_report_summary(report_id: str, reports: dict):
    """
    Récupère un résumé d'un rapport (si en mémoire)
    
    Args:
        report_id: ID du rapport
        reports: Dict des rapports en mémoire
        
    Returns:
        Résumé du rapport
    """
    try:
        if report_id not in reports:
            raise HTTPException(status_code=404, detail="Rapport non trouvé")
        
        report = reports[report_id]
        
        return {
            "id": report_id,
            "title": report.report_title,
            "date": report.report_date,
            "total_networks": report.total_networks,
            "vulnerabilities_count": len(report.vulnerabilities),
            "critical_vulnerabilities": report.critical_vulnerabilities,
            "overall_risk_score": report.overall_risk_score
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
