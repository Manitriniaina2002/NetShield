"""Fichier utils Python (placeholder pour développement futur)"""

def validate_mac_address(mac: str) -> bool:
    """Valide un format d'adresse MAC"""
    import re
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return re.match(pattern, mac) is not None


def format_mac_address(mac: str) -> str:
    """Formate une adresse MAC au format standard"""
    return mac.upper().replace('-', ':')


def calculate_risk_score(vulnerabilities: list) -> float:
    """Calcule un score de risque basé sur les vulnérabilités"""
    if not vulnerabilities:
        return 0.0
    
    critical_count = len([v for v in vulnerabilities if v.get('severity') == 'Critique'])
    high_count = len([v for v in vulnerabilities if v.get('severity') == 'Élevée'])
    medium_count = len([v for v in vulnerabilities if v.get('severity') == 'Moyen'])
    
    score = (critical_count * 25) + (high_count * 10) + (medium_count * 5)
    return min(100, score)
