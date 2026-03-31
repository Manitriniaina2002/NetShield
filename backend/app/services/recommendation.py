"""Services pour les recommandations de sécurité"""
from typing import List
from app.models.recommendation import Recommendation, PriorityLevel
from app.models.vulnerability import VulnerabilityType, Vulnerability
from app.models.wifi import SecurityLevel, WiFiNetwork


class RecommendationService:
    """Service de génération automatique des recommandations de sécurité"""
    
    RECOMMENDATIONS_DATABASE = {
        VulnerabilityType.OPEN_NETWORK: {
            "priority": PriorityLevel.CRITICAL,
            "category": "Chiffrement Wi-Fi",
            "title": "Activer le chiffrement Wi-Fi",
            "description": "Le réseau n'a aucun chiffrement. Cela doit être activé immédiatement.",
            "action_steps": [
                "Accéder à l'interface du routeur (généralement http://192.168.1.1)",
                "Se connecter avec les identifiants administrateur",
                "Naviguer vers Settings → Wireless → Security",
                "Sélectionner WPA2 (ou WPA3 si disponible)",
                "Définir un mot de passe sans fil fort (minimum 12 caractères)",
                "Enregistrer les modifications et redémarrer le routeur"
            ],
            "estimated_effort": "Faible (5-10 minutes)",
            "tools_required": [],
            "impact": "Prévient ~99% des attaques Wi-Fi élémentaires"
        },
        
        VulnerabilityType.WEP_ENCRYPTION: {
            "priority": PriorityLevel.CRITICAL,
            "category": "Chiffrement Wi-Fi",
            "title": "Migrer depuis WEP vers WPA2/WPA3",
            "description": "WEP est techniquement dépassé et cassé. Migration obligatoire.",
            "action_steps": [
                "Sauvegarder la configuration actuelle du routeur",
                "Accéder à l'interface d'administration du routeur",
                "Aller à Wireless Settings → Security",
                "Remplacer WEP par WPA2 (ou WPA3 si le matériel le supporte)",
                "Entrer un nouveau mot de passe fort et unique",
                "Appliquer les modifications",
                "Tous les clients doivent se reconnecter avec le nouveau mot de passe"
            ],
            "estimated_effort": "Faible à Modéré (15-30 minutes)",
            "tools_required": ["Accès administrateur au routeur"],
            "impact": "Augmente la sécurité de ~1000x par rapport au WEP"
        },
        
        VulnerabilityType.WEAK_ENCRYPTION: {
            "priority": PriorityLevel.HIGH,
            "category": "Chiffrement Wi-Fi",
            "title": "Mettre à niveau vers WPA2 ou WPA3",
            "description": "Le protocole actuel (WPA/TKIP) a des faiblesses knowned.",
            "action_steps": [
                "Vérifier que le routeur supporte WPA2 ou mieux",
                "Si le firmware est obsolète, le mettre à jour d'abord",
                "Accéder à la configuration de sécurité Wi-Fi",
                "Changer vers WPA2 (AES) ou WPA3 si disponible",
                "Appliquer un mot de passe fort (>12 caractères)",
                "Redémarrer le routeur et tous les clients"
            ],
            "estimated_effort": "Modéré (20-40 minutes)",
            "tools_required": ["Accès routeur", "Mise à jour firmware éventuelle"],
            "impact": "Augmente la sécurité de 100 à 1000x"
        },
        
        VulnerabilityType.WEAK_PASSWORD: {
            "priority": PriorityLevel.HIGH,
            "category": "Authentification Wi-Fi",
            "title": "Définir un mot de passe Wi-Fi fort",
            "description": "Un mot de passe faible compromet même le meilleur chiffrement.",
            "action_steps": [
                "Accéder aux paramètres de sécurité Wi-Fi du routeur",
                "Générer ou entrer un mot de passe fort contenant :",
                "  - Au minimum 12-16 caractères",
                "  - Majuscules (A-Z)",
                "  - Minuscules (a-z)",
                "  - Chiffres (0-9)",
                "  - Caractères spéciaux (!@#$%^&*)",
                "Éviter les mots du dictionnaire, noms propres, numéros consécutifs",
                "Noter le mot de passe dans un gestionnaire sécurisé",
                "Appliquer et redémarrer"
            ],
            "estimated_effort": "Très faible (5 minutes)",
            "tools_required": ["Gestionnaire de mots de passe recommandé"],
            "impact": "Rend les attaques par dictionnaire impossibles avec un bon mot de passe"
        },
        
        VulnerabilityType.BROADCAST_SSID: {
            "priority": PriorityLevel.MEDIUM,
            "category": "Configuration Wi-Fi",
            "title": "Optionnel : Masquer la diffusion du SSID",
            "description": "Masquer le SSID ajoute une couche de discrétion supplémentaire.",
            "action_steps": [
                "Accéder aux paramètres Wi-Fi du routeur",
                "Trouver l'option 'Broadcast SSID' ou 'SSID Visibility'",
                "Désactiver/Masquer la diffusion du SSID",
                "Enregistrer les modifications",
                "NOTE : Cela réduit plutôt la convivialité qu'améliore vraiment la sécu"
            ],
            "estimated_effort": "Très faible (3 minutes)",
            "tools_required": [],
            "impact": "Très faible (sécurité par obscurité, pas vraiment efficace)"
        },
        
        VulnerabilityType.WPS_ENABLED: {
            "priority": PriorityLevel.HIGH,
            "category": "Configuration Wi-Fi",
            "title": "Désactiver le WPS (Wi-Fi Protected Setup)",
            "description": "WPS a des faiblesses de sécurité connues et doit être désactivé.",
            "action_steps": [
                "Accéder à l'interface d'administration du routeur",
                "Naviguer vers Wireless Settings",
                "Trouver WPS (Wi-Fi Protected Setup)",
                "Désactiver complètement WPS",
                "Enregistrer et redémarrer le routeur"
            ],
            "estimated_effort": "Très faible (3-5 minutes)",
            "tools_required": [],
            "impact": "Prévient les attaques par force brute sur WPS PIN"
        },
        
        VulnerabilityType.MAC_FILTERING_DISABLED: {
            "priority": PriorityLevel.MEDIUM,
            "category": "Contrôle d'accès",
            "title": "Implémenter le filtrage MAC (optionnel)",
            "description": "Le filtrage MAC ajoute une couche supplémentaire de contrôle d'accès.",
            "action_steps": [
                "Lister toutes les adresses MAC autorisées (ordinateurs, téléphones, tablettes)",
                "Accéder aux paramètres de contrôle d'accès du routeur",
                "Activer le filtrage MAC",
                "Ajouter les MAC autorisées à la liste blanche",
                "Enregistrer",
                "NOTE : Cela peut complexifier la gestion du réseau"
            ],
            "estimated_effort": "Modéré (15-30 minutes)",
            "tools_required": ["Liste des appareils autorisés"],
            "impact": "Ajoute une barrière supplémentaire (mais peut être bypassée)"
        },
        
        VulnerabilityType.OUTDATED_FIRMWARE: {
            "priority": PriorityLevel.HIGH,
            "category": "Maintenance",
            "title": "Mettre à jour le firmware du routeur",
            "description": "les mises à jour firmware corrigent les vulnérabilités de sécurité kritiques.",
            "action_steps": [
                "Vérifier la version actuelle du firmware (Administration → About)",
                "Visiter le site du fabricant du routeur",
                "Télécharger la dernière version de firmware stable",
                "Accéder à Administration → Firmware Upgrade",
                "Uploader le fichier firmware",
                "Appliquer et attendre 5-10 minutes pour le redémarrage",
                "NE PAS couper l'alimentation pendant la mise à jour!"
            ],
            "estimated_effort": "Modéré (20-30 minutes)",
            "tools_required": ["Accès à Internet", "Accès administrateur"],
            "impact": "Corrige de nombreuses vulnerabilités de sécurité connues"
        }
    }
    
    # Recommandations générales pour tous les réseaux
    GENERAL_RECOMMENDATIONS = [
        {
            "title": "Segmentation du réseau (VLAN)",
            "description": "Séparer le trafic IoT, invités et critique de confiance.",
            "action_steps": [
                "Configurer les VLANs sur le routeur ou les switchs administrés",
                "Créer un VLAN pour les appareils IoT",
                "Créer un VLAN pour les invités",
                "Configurer les règles de firewall entre VLANs",
                "Isoler les serveurs critiques"
            ],
            "priority": PriorityLevel.MEDIUM,
            "category": "Architecture réseau",
            "estimated_effort": "Élevé (1-3 heures)",
            "impact": "Limite les dégâts en cas de compromission d'un réseau"
        },
        {
            "title": "Surveillance du trafic Wi-Fi",
            "description": "Mettre en place une surveillance pour détecter les activités anormales.",
            "action_steps": [
                "Installer un système de surveillance (IDS/IPS)",
                "Configurer les alertes pour les connexions suspectes",
                "Vérifier régulièrement les logs d'accès",
                "Surveiller la bande passante anormale",
                "Mettre en place des alertes de déconnexion suspecte"
            ],
            "priority": PriorityLevel.MEDIUM,
            "category": "Monitoring",
            "estimated_effort": "Élevé (2-4 heures)",
            "impact": "Permet de détecter les intrusions rapidement"
        },
        {
            "title": "Authentification fortifiée (WPA3-Enterprise)",
            "description": "Déployer l'authentification d'entreprise avec serveur RADIUS.",
            "action_steps": [
                "Déployer un serveur RADIUS (FreeRADIUS ou similaire)",
                "Configurer les certificats de serveur",
                "Activer WPA2-Enterprise ou WPA3-Enterprise sur le routeur",
                "Créer les comptes utilisateurs dans RADIUS",
                "Configurer les clients pour se connecter avec authentification EAP"
            ],
            "priority": PriorityLevel.MEDIUM,
            "category": "Authentification",
            "estimated_effort": "Très élevé (4-8 heures)",
            "impact": "Chaque utilisateur a une clé de session unique"
        },
        {
            "title": "Audit de sécurité régulier",
            "description": "Effectuer des audits de sécurité Wi-Fi régulièrement.",
            "action_steps": [
                "Planifier les audits tous les trimestres",
                "Scanner pour les nouveaux réseaux rogue",
                "Vérifier la conformité des configurations",
                "Documenter les résultats",
                "Former le personnel aux risques"
            ],
            "priority": PriorityLevel.MEDIUM,
            "category": "Gouvernance",
            "estimated_effort": "Modéré (4-8 heures/trimestre)",
            "impact": "Maintient le niveau de sécurité sur la durée"
        }
    ]
    
    @staticmethod
    async def generate_recommendations(
        vulnerabilities: List[Vulnerability],
        networks: List[WiFiNetwork]
    ) -> List[Recommendation]:
        """
        Génère automatiquement des recommandations basées sur les vulnérabilités
        
        Args:
            vulnerabilities: Liste des vulnérabilités identifiées
            networks: Liste des réseaux analysés
            
        Returns:
            Liste des recommandations générées
        """
        recommendations = []
        processed_types = set()
        
        # Ajouter les recommandations spécifiques aux vulnérabilités
        for vuln in vulnerabilities:
            if vuln.vulnerability_type not in processed_types:
                if vuln.vulnerability_type in RecommendationService.RECOMMENDATIONS_DATABASE:
                    rec_data = RecommendationService.RECOMMENDATIONS_DATABASE[vuln.vulnerability_type]
                    
                    rec = Recommendation(
                        id=f"rec_{vuln.vulnerability_type.value}",
                        title=rec_data["title"],
                        description=rec_data["description"],
                        action_steps=rec_data["action_steps"],
                        priority=rec_data["priority"],
                        category=rec_data["category"],
                        affected_vulnerability=vuln.vulnerability_type.value,
                        estimated_effort=rec_data["estimated_effort"],
                        tools_required=rec_data.get("tools_required", []),
                        impact=rec_data["impact"]
                    )
                    recommendations.append(rec)
                    processed_types.add(vuln.vulnerability_type)
        
        # Ajouter les recommandations générales
        for idx, gen_rec in enumerate(RecommendationService.GENERAL_RECOMMENDATIONS):
            rec = Recommendation(
                id=f"gen_rec_{idx}",
                title=gen_rec["title"],
                description=gen_rec["description"],
                action_steps=gen_rec["action_steps"],
                priority=gen_rec["priority"],
                category=gen_rec["category"],
                estimated_effort=gen_rec["estimated_effort"],
                tools_required=[],
                impact=gen_rec["impact"]
            )
            recommendations.append(rec)
        
        return recommendations
