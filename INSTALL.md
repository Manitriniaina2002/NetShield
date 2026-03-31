# Installation et Guide de Démarrage

## 🎯 Prérequis Système

Avant de commencer, assurez-vous d'avoir :

- **Python 3.9 ou supérieur**
- **Node.js 16 ou supérieur**
- **npm 7 ou supérieur**
- **Une connexion Internet** (pour télécharger les dépendances)

### Vérifier vos versions

```bash
python --version    # Doit être >= 3.9
node --version      # Doit être >= 16
npm --version       # Doit être >= 7
```

---

## 📦 Installation Complète

### Étape 1: Cloner/Télécharger le projet

```bash
# Si depuis un repo git
git clone https://github.com/votre-repo/netshield.git
cd netshield

# Ou extraire l'archive ZIP fournie
```

### Étape 2: Installation du Backend

```bash
# Aller dans le répertoire backend
cd backend

# Créer un environnement virtuel Python
python -m venv venv

# Activer l'environnement
# Sur Windows :
venv\Scripts\activate

# Sur Linux/Mac :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# (Optionnel) Vérifier l'installation
pip list | grep fastapi
```

### Étape 3: Installation du Frontend

```bash
# Aller dans le répertoire frontend
cd frontend

# Installer les dépendances Node.js
npm install

# (Optionnel) Vérifier l'installation  
npm list react
```

---

## 🚀 Démarrage de l'Application

### Option 1: Scripts Automatiques (Recommandé)

#### Sur Windows
```batch
# Double-cliquez sur start.bat
# ou en ligne de commande :
start.bat
```

#### Sur Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Démarrage Manuel (En Cas de Problème)

#### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
python main.py
```

Vous devriez voir :
```
Uvicorn running on http://127.0.0.1:8000
```

#### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

Vous devriez voir :
```
VITE v5.0.0 ready in XXX ms

➜  Local:   http://localhost:3000
```

---

## ✅ Vérification de l'Installation

### 1. Vérifier le Backend

Ouvrez http://localhost:8000 dans votre navigateur

Vous devriez voir une réponse JSON :
```json
{
    "message": "Bienvenue sur NetShield...",
    "version": "1.0.0"
}
```

### 2. Vérifier l'API

Accédez à : http://localhost:8000/api/docs

Vous devriez voir la documentation Swagger interactive

### 3. Vérifier le Frontend

Ouvrez http://localhost:3000 dans votre navigateur

Vous devriez voir l'interface NetShield avec le header bleu

### 4. Test d'Intégration

1. Cliquez sur "🔍 Démarrer un Scan"
2. Attendez 10 secondes
3. Vérifiez que le tableau se remplit de données
4. Cliquez sur "Analyser" pour un réseau
5. Vérifiez les vulnérabilités et recommandations

---

## 🔧 Configuration

### Backend (.env)

Le fichier `backend/.env` contient :

```env
# Debug mode (False en production)
DEBUG=False

# CORS origins
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# Server
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

# Mode simulation (TOUJOURS True pour la sécurité)
SIMULATION_MODE=True

# Confirmation avant actions sensibles
REQUIRE_CONFIRMATION=True
```

### Frontend (vite.config.js)

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

---

## 📁 Structure du Projet

```
NetShield/
├── backend/                         # API Backend (Python/FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py               # Configuration
│   │   ├── api/                    # Routes API
│   │   │   ├── scan.py
│   │   │   ├── vulnerabilities.py
│   │   │   ├── recommendations.py
│   │   │   ├── reports.py
│   │   │   └── commands.py
│   │   ├── models/                 # Modèles Pydantic
│   │   │   ├── wifi.py
│   │   │   ├── vulnerability.py
│   │   │   ├── recommendation.py
│   │   │   └── scan.py
│   │   ├── services/               # Logique métier
│   │   │   ├── wifi_scan.py
│   │   │   ├── vulnerability_analysis.py
│   │   │   ├── recommendation.py
│   │   │   ├── pdf_report.py
│   │   │   └── command_execution.py
│   │   └── utils/
│   │       └── helpers.py
│   ├── main.py                     # Point d'entrée
│   ├── requirements.txt             # Dépendances Python
│   ├── .env                         # Variables d'environnement
│   └── .gitignore
│
├── frontend/                        # Interface UI (React/Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── NetworkTable.jsx
│   │   │   ├── VulnerabilityPanel.jsx
│   │   │   └── RecommendationPanel.jsx
│   │   ├── api.js                  # Client API
│   │   ├── constants.js            # Constantes
│   │   ├── index.css               # Styles global
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   └── .gitignore
│
├── README.md                        # Documentation complète
├── QUICKSTART.md                    # Guide rapide
├── INSTALL.md                       # Ce fichier
├── start.bat                        # Script démarrage Windows
├── start.sh                         # Script démarrage Linux/Mac
└── .gitignore
```

---

## 🐛 Troubleshooting

### Backend ne démarre pas

**Erreur: "Python not found"**
- Vérifier que Python est installé: `python --version`
- Ajouter Python au PATH (Windows): Réinstaller en cochant "Add to PATH"

**Erreur: "ModuleNotFoundError: No module named 'fastapi'"**
```bash
cd backend
source venv/bin/activate  # ou venv\Scripts\activate
pip install -r requirements.txt
```

**Erreur: "Address already in use"**
- Le port 8000 est déjà utilisé
- Utiliser : `python main.py --port 8001`

### Frontend ne démarre pas

**Erreur: "npm command not found"**
- Node.js/npm n'est pas installé
- Télécharger: https://nodejs.org/

**Erreur: "ERR! code ERESOLVE"**
```bash
npm install --legacy-peer-deps
```

### Pas de connexion entre Frontend et Backend

**Vérifier:**
1. Le backend s'exécute: http://localhost:8000/health
2. Le frontend s'exécute: http://localhost:3000
3. Les CORS sont configurés correctement dans `backend/app/config.py`
4. Pas de firewall bloquant

**Solution:**
```python
# backend/app/config.py
cors_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
```

### Les données ne charger pas

1. Vérifier les logs du backend
2. Vérifier la console du navigateur (F12)
3. Vérifier que l'API répond: http://localhost:8000/api/docs
4. Essayer un scan manuel

---

## 🎯 Test de Fonctionnalité

### Test 1: Scan Wi-Fi
```
1. Accéder à http://localhost:3000
2. Cliquer "🔍 Démarrer un Scan"
3. Vérifier que des réseaux apparaissent
```

### Test 2: Analyse de Vulnérabilité
```
1. Après le scan, des réseaux doivent s'afficher
2. Cliquer sur "Analyser" pour un réseau
3. Vérifier que des vulnérabilités sont identifiées
```

### Test 3: Recommandations
```
1. Aller à l'onglet "Recommandations"
2. Vérifier que des actions correctives sont proposées
```

### Test 4: Rapport PDF
```
1. Aller à l'onglet "Rapport"
2. Cliquer "Générer PDF"
3. Vérifier que le fichier se télécharge
4. Ouvrir et vérifier le contenu
```

---

## 📊 Performances

### Ressources système recommandées
- **CPU**: Dual-core 2 GHz minimum
- **RAM**: 2 GB minimum (4 GB recommandé)
- **Disque**: 500 MB libre
- **Bande passante**: Non critique (mode simulation)

### Temps de démarrage typiques
- Backend: 2-3 secondes
- Frontend: 3-5 secondes
- Scan complet: 10-15 secondes
- Génération PDF: 2-5 secondes

---

## 🔐 Modes de Sécurité

### Mode Simulation (Par défaut)
- ✅ Sûr pour tout environnement
- ✅ Pas de commands réelles
- ✅ Données synthétiques réalistes
- Recommandé pour production/education

### Mode Réel (Linux uniquement)
- Nécessite root/sudo
- Nécessite airmon-ng et airodump-ng
- Affecter votre système!
```bash
# ACTIVATION (À NE PAS FAIRE LÉGÈREMENT)
# Modifier backend/.env: SIMULATION_MODE=False
# Installer: sudo apt-get install aircrack-ng
```

---

## 📚 Ressources Supplémentaires

- **Documentation API**: http://localhost:8000/api/docs
- **React Docs**: https://react.dev/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Tailwind CSS**: https://tailwindcss.com/
- **Vite**: https://vitejs.dev/

---

## 📞 Support

En cas de problème :

1. **Vérifier ce guide**
2. **Consulter README.md**
3. **Vérifier les logs** (console backend/frontend)
4. **Nettoyer et réinstaller** (si fichiers corrompus)

```bash
# Nettoyage complet
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../frontend  
rm -rf node_modules package-lock.json
npm install
```

---

## ✨ Prochaines Étapes

1. ✅ Installation terminée
2. 🚀 Démarrer l'application
3. 🧪 Faire un scan de test
4. 📄 Générer un premier rapport
5. 📖 Consulter la documentation
6. 🎓 Apprendre les concepts Wi-Fi

---

**🎉 Installation terminée! Bon audit!**
