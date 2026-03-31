# NetShield - Architecture et Documentation Technique

## 🏗️ Architecture Générale

```
┌─────────────────────────────────────────────────────────────┐
│                     Applications Web                         │
│            (React 18 + Vite + TailwindCSS)                   │
│              http://localhost:3000                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/REST
                     │
┌────────────────────┴────────────────────────────────────────┐
│                   FastAPI Backend                           │
│    (Python 3.9+ avec frameworks asynchrone)                 │
│              http://localhost:8000                          │
│  ┌─────────────┬──────────────┬──────────────┐             │
│  │  API Routes │   Services   │   Models     │             │
│  │  + Security │  + Logic     │  + Validation│             │
│  └─────────────┴──────────────┴──────────────┘             │
└─────────────────────────────────────────────────────────────┘
                     │
                     │ Simulation Mode
                     │
         ┌───────────┴───────────┐
         │                       │
    Data Synthétique       Rapports PDF
    + Résultats Tests      + JSON Export
```

---

## 🔄 Flux de Données

### Audit Wi-Fi Complet

```
1. Utilisateur "Démarrer Scan"
         ↓
2. Frontend → POST /api/scan/networks
         ↓
3. Backend service: WiFiScanService.scan_networks()
         ↓
4. Retour liste réseaux (mode simulation: ~6 réseaux)
         ↓
5. Frontend affiche tableau NetworkTable
         ↓
6. Utilisateur clique "Analyser"
         ↓
7. Frontend → POST /api/vulnerabilities/analyze-batch
         ↓
8. Backend: VulnerabilityAnalysisService.analyze_all_networks()
         ↓
9. Retour vulnérabilités identifiées par réseau
         ↓
10. Frontend → POST /api/recommendations/generate
         ↓
11. Backend: RecommendationService.generate_recommendations()
         ↓
12. Retour recommandations générées
         ↓
13. Frontend affiche rapports et graphiques
         ↓
14. Utilisateur génère PDF
         ↓
15. Frontend → POST /api/reports/pdf
         ↓
16. Backend: PDFReportService.generate_audit_report()
         ↓
17. Téléchargement du PDF
```

---

## 📦 Structure Backend Détaillée

### Models (app/models/)
```
WiFiNetwork
├── ssid: str
├── bssid: str (MAC address)
├── channel: int (1-14)
├── security: SecurityLevel (Open/WEP/WPA/WPA2/WPA3)
├── signal_strength: int (dBm -30 to -90)
└── clients: int

Vulnerability
├── network_bssid: str
├── vulnerability_type: VulnerabilityType
├── severity: str (Critique/Élevée/Moyen/Faible)
├── title: str
├── description: str
├── attack_vector: str
└── exploitability: str

Recommendation
├── title: str
├── description: str
├── action_steps: List[str]
├── priority: PriorityLevel
├── category: str
├── estimated_effort: str
└── impact: str

AuditReport
├── networks: List[WiFiNetwork]
├── vulnerabilities: List[Vulnerability]
├── recommendations: List[Recommendation]
├── overall_risk_score: float (0-100)
└── executive_summary: str
```

### Services (app/services/)

**WiFiScanService**
- Scan passif des réseaux Wi-Fi
- Mode simulation avec données réalistes
- Support des interfaces réseau (futur)

**VulnerabilityAnalysisService**
- Analyse chaque réseau selon son type de sécurité
- Database de vulnérabilités connues
- Scoring automatique

**RecommendationService**
- Génération d'actions correctives
- Priorisation selon la sévérité
- Recommandations générales + spécifiques

**PDFReportService**
- Génération PDF professionnels avec reportlab
- Design styles et couleurs
- Tableaux et mises en forme

**CommandExecutionService**
- Exécution sécurisée commandes système
- Whitelist de commandes autorisées
- Simulation mode par défaut

### API Routes (app/api/)

```
/api/scan/
  POST   /networks          Scan Wi-Fi
  GET    /networks/{bssid}  Détails réseau

/api/vulnerabilities/
  POST   /analyze/{bssid}   Analyser un réseau
  POST   /analyze-batch     Analyser plusieurs
  GET    /statistics        Stats vulnérabilités

/api/recommendations/
  POST   /generate          Générer recommandations
  GET    /by-priority/{p}   Filtrer par priorité
  GET    /by-category/{c}   Filtrer par catégorie

/api/reports/
  POST   /pdf               Générer PDF
  POST   /json              Exporter JSON
  POST   /save              Sauvegarder fichier

/api/commands/
  GET    /allowed           Commandes autorisées
  POST   /execute           Exécuter commande
  POST   /execute-safe      Avec confirmation
```

---

## 🎨 Structure Frontend Détaillée

### Composants (src/components/)

**Header**
- Logo + nom application
- Menu mentions légales
- Toggle dark mode

**Dashboard (Page principale)**
- Stats summary (4 cartes)
- Navigation par onglets
- Gestion d'état (useState, useEffect)
- Intégration API

**NetworkTable**
- Tableau des réseaux
- Colonnes: SSID, BSSID, Canal, Sécurité, Signal, Clients
- Bouton "Analyser" par réseau
- Code couleur sécurité

**VulnerabilityPanel**
- Liste des vulnérabilités
- Groupé par réseau (BSSID)
- Icônes sévérité
- Description complète

**RecommendationPanel**
- Classement par priorité
- Catégories (Chiffrement, Config, Authentification)
- Étapes à suivre
- Effort/Impact estimé

### Services Frontend

**api.js**
- Client Axios configuré
- Base URL: http://localhost:8000/api
- Méthodes pour chaque endpoint
- Gestion d'erreurs

**constants.js**
- Niveaux sécurité + couleurs
- Niveaux risque + couleurs
- Fonctions utilitaires (signal, bar)

### Styles (src/index.css)

- Tailwind CSS configuration
- Classes personnalisées (.card, .btn, .input)
- Animations
- Responsive design

---

## 🔐 Sécurité

### Mode Simulation
- Par défaut: SIMULATION_MODE=True
- Aucune commande réelle exécutée
- Données synthétiques réalistes
- Safe pour tout environnement

### Mode Réel (Résumé)
- Configuration: SIMULATION_MODE=False
- Nécessite: Linux + root + aircrack-ng
- Exécution vraie des audits
- ⚠️ Usage très restreint

### Mesures de Sécurité
```python
# Whitelist de commandes
ALLOWED_COMMANDS = {
    "ifconfig": "...",
    "airmon-ng": "...",
    "airodump-ng": "..."
}

# Confirmation avant commandes sensibles
REQUIRE_CONFIRMATION = True

# Logging complet
logging.info(f"{method} {endpoint}")
```

### CORS
```python
# Seulement origines locales autorisées
allow_origins = [
    "http://localhost:3000",
    "http://localhost:5173"
]
```

---

## 🐛 Debugging

### Backend Logs
```python
# File: app/main.py
import logging
logger = logging.getLogger(__name__)
logger.info("Message")
logger.error("Erreur")
```

### Frontend Logs
```javascript
// Console du navigateur (F12)
console.log("Message")
console.error("Erreur")
```

### API Testing
```bash
# Swagger UI
http://localhost:8000/api/docs

# Direct curl testing
curl http://localhost:8000/api/info
```

---

## 📊 Base de Données (Futur)

Structure proposée (PostgreSQL/SQLite) :

```sql
-- Tables
networks          # Historique des scans
vulnerabilities   # Vulnérabilités détectées
recommendations   # Recommandations générées
audit_reports     # Rapports générés
users            # Gestion des rôles (optionnel)

-- Relations
audit_reports ←→ vulnerabilities
audit_reports ←→ recommendations
audit_reports ←→ networks
```

---

## 🚀 Déploiement

### Mode Production

#### Backend
```bash
# Pas de reload
uvicorn main:app --host 0.0.0.0 --port 8000

# Avec Gunicorn (optionnel)
pip install gunicorn
gunicorn -w 4 main:app
```

#### Frontend
```bash
# Build optimisé
npm run build

# Servir dist/ avec nginx/apache
# ou déployer sur Vercel/Netlify
```

#### Docker (Future)
```dockerfile
# backend.Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

---

## 📈 Performances

### Optimisations Frontend
- Code splitting automatique (Vite)
- CSS optimisé (Tailwind)
- Lazy loading des composants

### Optimisations Backend
- Async/await pour I/O
- Caching des résultats
- Compression HTTP
- GZIP responses

### Benchmarks Typiques
- Page load: 2-3 secondes
- Scan: 10-15 secondes
- Analyse: 1-2 secondes
- PDF gen: 2-5 secondes

---

## 🔄 Cycle de Développement

### Ajouter une Nouvelle Vulnérabilité

```python
# 1. Ajouter dans app/models/vulnerability.py
class VulnerabilityType(str, Enum):
    NOUVELLE_VULN = "nouvelle_vuln"

# 2. Implémenter dans app/services/vulnerability_analysis.py
if network.security == SecurityLevel.WPA:
    vuln = Vulnerability(
        type=VulnerabilityType.NOUVELLE_VULN,
        ...
    )

# 3. Générer recommandation dans app/services/recommendation.py
RECOMMENDATIONS_DATABASE[VulnerabilityType.NOUVELLE_VULN] = {
    "title": "...",
    ...
}

# 4. L'API l'inclura automatiquement
```

### Ajouter un Nouveau Endpoint

```python
# 1. Créer route dans app/api/nouveau.py
@router.get("/endpoint")
async def mon_endpoint():
    return {...}

# 2. Inclure dans app/api/__init__.py
api_router.include_router(nouveau_router)

# 3. Consommer en frontend
api.get('/api/endpoint')
```

---

**Documentation Technique - NetShield v1.0.0**
