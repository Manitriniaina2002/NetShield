"""Services pour la génération de rapports PDF"""
import os
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from app.models.scan import AuditReport
from app.config import get_settings


class PDFReportService:
    """Service de génération de rapports PDF professionnels"""
    
    @staticmethod
    def generate_audit_report(report: AuditReport) -> BytesIO:
        """
        Génère un rapport PDF d'audit Wi-Fi professionnel
        
        Args:
            report: Rapport d'audit à convertir en PDF
            
        Returns:
            Flux BytesIO contenant le PDF
        """
        # Créer le document PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )
        
        # Préparer le contenu
        elements = []
        styles = getSampleStyleSheet()
        settings = get_settings()
        
        # Styles personnalisés
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'Custom',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        )
        
        # ===== PAGE DE GARDE =====
        elements.append(Spacer(1, 1.5 * inch))
        
        # Titre
        title = Paragraph(report.report_title, title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Infos du rapport
        subtitle_data = [
            ["Projet:", report.project_name],
            ["Date:", report.report_date.strftime("%d/%m/%Y %H:%M")],
            ["Auteur:", report.author],
        ]
        
        subtitle_table = Table(subtitle_data, colWidths=[2*inch, 4*inch])
        subtitle_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1e40af')),
        ]))
        elements.append(subtitle_table)
        
        elements.append(Spacer(1, 0.5 * inch))
        
        # Logo / Watermark
        logo_text = Paragraph(
            f"<b>{settings.company_name}</b><br/>Wi-Fi Security Audit Lab",
            ParagraphStyle(
                'Logo',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_CENTER,
                textColor=colors.grey
            )
        )
        elements.append(logo_text)
        
        # Avertissement légal
        elements.append(Spacer(1, 0.5 * inch))
        legal = Paragraph(
            "<b>⚠️ AVERTISSEMENT LÉGAL</b>",
            ParagraphStyle(
                'LegalTitle',
                parent=styles['Normal'],
                fontSize=11,
                alignment=TA_CENTER,
                textColor=colors.red,
                fontName='Helvetica-Bold'
            )
        )
        elements.append(legal)
        
        legal_text = Paragraph(
            "Cet outil et ce rapport sont destinés <b>uniquement à des fins éducatives</b> "
            "et à des <b>tests de sécurité autorisés</b>. L'utilisateur assume "
            "l'entière responsabilité légale de l'utilisation de ce rapport.",
            normal_style
        )
        elements.append(legal_text)
        elements.append(PageBreak())
        
        # ===== TABLE OF CONTENTS (Simulée) =====
        elements.append(Paragraph("TABLE DES MATIÈRES", heading_style))
        toc_items = [
            "1. Résumé Exécutif",
            "2. Réseaux Détectés",
            "3. Vulnérabilités Identifiées",
            "4. Méthodologie de Test",
            "5. Recommandations de Sécurité",
            "6. Évaluation des Risques",
        ]
        for item in toc_items:
            elements.append(Paragraph(item, styles['Normal']))
        elements.append(PageBreak())
        
        # ===== 1. RÉSUMÉ EXÉCUTIF =====
        elements.append(Paragraph("1. RÉSUMÉ EXÉCUTIF", heading_style))
        elements.append(Paragraph(report.executive_summary, normal_style))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Score de risque
        risk_color = PDFReportService._get_risk_color(report.overall_risk_score)
        risk_summary = f"""
        <b>Score de Risque Global:</b> {report.overall_risk_score:.1f}/100<br/>
        <font color="{risk_color}"><b>{report.risk_assessment}</b></font>
        """
        elements.append(Paragraph(risk_summary, normal_style))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Statistiques
        stats_text = (
            f"<b>Réseaux analysés:</b> {report.total_networks}<br/>"
            f"<b>Vulnérabilités trouvées:</b> "
            f"Critiques: {report.critical_vulnerabilities}, "
            f"Élevées: {report.high_vulnerabilities}, "
            f"Moyennes: {report.medium_vulnerabilities}, "
            f"Faibles: {report.low_vulnerabilities}"
        )
        elements.append(Paragraph(stats_text, normal_style))
        elements.append(PageBreak())
        
        # ===== 2. RÉSEAUX DÉTECTÉS =====
        if report.scan_result:
            elements.append(Paragraph("2. RÉSEAUX DÉTECTÉS", heading_style))
            
            # Table des réseaux
            network_data = [["SSID", "BSSID", "Canal", "Sécurité", "Signal", "Clients"]]
            for network in report.scan_result.networks:
                network_data.append([
                    network.ssid[:20],
                    network.bssid,
                    str(network.channel),
                    network.security.value,
                    f"{network.signal_percentage}%" if network.signal_percentage else "N/A",
                    str(network.clients)
                ])
            
            network_table = Table(network_data, colWidths=[1.2*inch, 1.3*inch, 0.7*inch, 1*inch, 0.8*inch, 0.7*inch])
            network_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            elements.append(network_table)
            elements.append(PageBreak())
        
        # ===== 3. VULNÉRABILITÉS =====
        elements.append(Paragraph("3. VULNÉRABILITÉS IDENTIFIÉES", heading_style))
        
        if not report.vulnerabilities:
            elements.append(Paragraph("Aucune vulnérabilité critique identifiée.", normal_style))
        else:
            for idx, vuln in enumerate(report.vulnerabilities, 1):
                vuln_text = f"""
                <b>{idx}. {vuln.title}</b><br/>
                <font size="9">
                <b>Sévérité:</b> {vuln.severity}<br/>
                <b>Type:</b> {vuln.vulnerability_type.value}<br/>
                <b>Description:</b> {vuln.description}<br/>
                <b>Vecteur d'attaque:</b> {vuln.attack_vector}<br/>
                <b>Exploitabilité:</b> {vuln.exploitability}
                </font>
                """
                elements.append(Paragraph(vuln_text, normal_style))
                elements.append(Spacer(1, 0.1 * inch))
        
        elements.append(PageBreak())
        
        # ===== 4. MÉTHODOLOGIE =====
        elements.append(Paragraph("4. MÉTHODOLOGIE DE TEST", heading_style))
        methodology_text = f"""
        <b>Méthode:</b> {report.methodology}<br/>
        <b>Période de test:</b> {report.testing_period}<br/>
        <b>Mode:</b> Simulation contrôlée en laboratoire<br/>
        <br/>
        <b>Phases du test:</b><br/>
        1. Scan passif des réseaux Wi-Fi disponibles<br/>
        2. Analyse des protocoles de sécurité identifiés<br/>
        3. Identification des vulnérabilités connues<br/>
        4. Simulation d'attaques dans un environnement contrôlé<br/>
        5. Génération des recommandations<br/>
        """
        elements.append(Paragraph(methodology_text, normal_style))
        elements.append(PageBreak())
        
        # ===== 5. RECOMMANDATIONS =====
        elements.append(Paragraph("5. RECOMMANDATIONS DE SÉCURITÉ", heading_style))
        
        if not report.recommendations:
            elements.append(Paragraph("Aucune recommandation disponible.", normal_style))
        else:
            for idx, rec in enumerate(report.recommendations, 1):
                rec_text = f"""
                <b>{idx}. {rec.title}</b> ({rec.priority.value})<br/>
                <font size="9">
                <b>Description:</b> {rec.description}<br/>
                <b>Catégorie:</b> {rec.category}<br/>
                <b>Effort estimé:</b> {rec.estimated_effort}<br/>
                <b>Impact:</b> {rec.impact}<br/>
                <b>Étapes:</b><br/>
                """
                
                # Ajouter les étapes
                for step in rec.action_steps:
                    rec_text += f"• {step}<br/>"
                
                rec_text += "</font>"
                elements.append(Paragraph(rec_text, normal_style))
                elements.append(Spacer(1, 0.15 * inch))
        
        elements.append(PageBreak())
        
        # ===== 6. CONCLUSION =====
        elements.append(Paragraph("6. CONCLUSION ET ÉVALUATION DES RISQUES", heading_style))
        
        conclusion_text = f"""
        <b>Évaluation Global du Risque:</b> {report.risk_assessment}<br/>
        <b>Score de Risque:</b> {report.overall_risk_score:.1f}/100<br/>
        <br/>
        {report.observations or "Audit réalisé avec succès."}<br/>
        <br/>
        <b>Prochaines étapes:</b><br/>
        1. Implémenter les recommandations critiques dans les 48 heures<br/>
        2. Planifier les recommandations de priorité élevée<br/>
        3. Documenter les changements effectués<br/>
        4. Effectuer un audit de suivi dans 30 jours<br/>
        """
        elements.append(Paragraph(conclusion_text, normal_style))
        
        elements.append(Spacer(1, 0.5 * inch))
        
        # Signature
        footer_text = f"""
        <b>Rapport généré par:</b> NetShield - Wi-Fi Security Audit Lab<br/>
        <b>Date de génération:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}<br/>
        <b>Version du rapport:</b> 1.0<br/>
        <br/>
        ⚠️ Ce rapport contient des informations sensibles et confidentiel.
        """
        elements.append(Paragraph(footer_text, normal_style))
        
        # Construire le PDF
        doc.build(elements)
        pdf_buffer.seek(0)
        
        return pdf_buffer
    
    @staticmethod
    def _get_risk_color(score: float) -> str:
        """Retourne une couleur hex en fonction du score de risque"""
        if score >= 80:
            return "#dc2626"  # Rouge
        elif score >= 60:
            return "#ea580c"  # Orange
        elif score >= 40:
            return "#eab308"  # Jaune
        elif score >= 20:
            return "#84cc16"  # Vert clair
        else:
            return "#22c55e"  # Vert
    
    @staticmethod
    async def save_report_to_file(report: AuditReport, filename: str = None) -> str:
        """
        Sauvegarde le rapport PDF sur le disque
        
        Args:
            report: Rapport à sauvegarder
            filename: Nom du fichier (généré automatiquement si None)
            
        Returns:
            Chemin du fichier sauvegardé
        """
        settings = get_settings()
        
        # Créer le répertoire temp s'il n'existe pas
        os.makedirs(settings.pdf_temp_dir, exist_ok=True)
        
        # Générer le nom du fichier
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audit_report_{timestamp}.pdf"
        
        filepath = os.path.join(settings.pdf_temp_dir, filename)
        
        # Générer et sauvegarder le PDF
        pdf_buffer = PDFReportService.generate_audit_report(report)
        
        with open(filepath, "wb") as f:
            f.write(pdf_buffer.getvalue())
        
        return filepath
