# 🚀 Comment Exécuter NetShield

Deux méthodes pour démarrer l'application.

## Méthode 1: Scripts Automatiques (RECOMMANDÉ)

### Windows
```batch
double-cliquez sur start.bat
```

ou en ligne de commande:
```batch
start.bat
```

### Linux / Mac
```bash
chmod +x start.sh
./start.sh
```

Les scripts démarrent automatiquement:
1. ✅ Backend (http://localhost:8000)
2. ✅ Frontend (http://localhost:3000)
3. ✅ Ouvre l'interface dans le navigateur

**Durée**: ~8-10 secondes

---

## Méthode 2: Démarrage Manuel

Utile si les scripts ne fonctionnent pas.

### Terminal 1 - Démarrer le Backend

```bash
cd backend

# Créer l'environnement virtuel (une fois)
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Installer les dépendances (une fois)
pip install -r requirements.txt

# Démarrer le serveur
python main.py
```

Vous devriez voir:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Press CTRL+C to quit
```

### Terminal 2 - Démarrer le Frontend

```bash
cd frontend

# Installer les dépendances (une fois)
npm install

# Démarrer le serveur
npm run dev
```

Vous devriez voir:
```
  VITE v5.0.0 ready in XXX ms

  ➜  Local:   http://localhost:3000
  ➜  press h to show help
```

### Accéder à l'Application

Ouvrez votre navigateur et allez à:
```
http://localhost:3000
```

---

## Arrêter l'Application

### Si scripts automatiques:
- Fermer les fenêtres de commande du backend et frontend
- Ou appuyer sur Ctrl+C dans chaque terminal

### Si démarrage manuel:
- Appuyer sur **Ctrl+C** dans chaque terminal

---

## Vérification que tout Fonctionne

### 1. Backend répond?
```bash
curl http://localhost:8000/health
```

Réponse attendue:
```json
{"status": "healthy", "app_name": "NetShield..."}
```

### 2. API Documentation?
Ouvrir: http://localhost:8000/api/docs

Vous devriez voir la documentation Swagger.

### 3. Frontend charge?
Ouvrir: http://localhost:3000

Vous devriez voir l'interface NetShield avec:
- Header bleu avec logo "NS"
- Texte "NetShield - Wi-Fi Security Audit Lab"
- Bouton "🔍 Démarrer un Scan"
- Onglets: Vue d'ensemble, Vulnérabilités, Recommandations, Rapport

### 4. Scan fonctionne?
1. Cliquer "🔍 Démarrer un Scan"
2. Attendre ~10 secondes
3. Vérifier que 6 réseaux apparaissent dans le tableau

---

## Dépannage

### La commande `start.bat` ne fonctionne pas (Windows)

**Solution 1:** Ouvrir CMD dans le répertoire NetShield
```bash
cd C:\Users\MaZik\NetShield
start.bat
```

**Solution 2:** Ouvrir PowerShell avec le chemin complet
```powershell
& "C:\Users\MaZik\NetShield\start.bat"
```

**Solution 3:** Démarrage manuel (voir Méthode 2)

### `python: command not found` (Linux/Mac)

Python n'est pas installé ou pas dans le PATH.

```bash
# Installer Python via Homebrew (Mac)
brew install python3

# Installer Python via apt (Linux Ubuntu)
sudo apt-get install python3

# Vérifier installation
python3 --version
```

### `npm: command not found`

Node.js/npm n'est pas installé.

```bash
# Télécharger depuis: https://nodejs.org/
# Ou installer avec package manager

# Mac avec Homebrew:
brew install node

# Linux Ubuntu:
sudo apt-get install nodejs npm

# Vérifier installation
node --version
npm --version
```

### Port 8000 déjà utilisé

Une autre application utilise le port 8000.

```bash
# Option 1: Arrêter l'autre application
# Option 2: Modifier le port
cd backend
# Modifier main.py: port=8001 et relancer

# Option 3: Tuer le processus
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :8000
kill -9 <PID>
```

### Port 3000 déjà utilisé

Similaire au port 8000 mais pour le frontend.

```bash
# Modifier vite.config.js
server: {
  port: 3001,  # Changer de port
  ...
}
```

### CORS Error (Frontend ne peut pas atteindre Backend)

Vérifier que les deux services s'exécutent.

```bash
# Vérifier backend
curl http://localhost:8000/health

# Vérifier frontend
curl http://localhost:3000

# Les deux doivent répondre
```

---

## Configuration Avancée

### Changer le port Backend

Modifier `backend/main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=9000  # Changer le port ici
    )
```

### Changer le port Frontend

Modifier `frontend/vite.config.js`:
```javascript
server: {
  port: 4000,  // Changer le port ici
  ...
}
```

### Mode DEBUG

Modifier `backend/.env`:
```env
DEBUG=True  # Active les messages debug
```

---

## Performance et Optimisations

### Si démarrage lent (>15 sec)

1. **Vérifier les spécifications machine:**
   - CPU: Dual-core minimum
   - RAM: 2GB minimum
   - Disque: 500MB libre

2. **Optimisations:**
```bash
# Nettoyer cache npm (frontend)
cd frontend
npm cache clean --force
rm -rf node_modules
npm install

# Nettoyer cache Python (backend)
cd backend
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete
pip cache purge
```

### Si réponses lentes (> 2 sec)

Généralement mode simulation ne devrait pas être lent.

```bash
# Vérifier utilisation CPU/RAM
# Windows: Ouvrir Task Manager
# Linux: top ou htop
# Mac: Activity Monitor

# Si utilisation très élevée:
# - Fermer autres applications
# - Redémarrer le service
```

---

## Utilisation en Production

### Déploiement simple

1. **Backend (Heroku/Railway):**
```bash
# Créer Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT

# Déployer
git push heroku main
```

2. **Frontend (Vercel/Netlify):**
```bash
# Build
npm run build

# Upload dist/ folder
# Déployer
```

### Déploiement Docker

```dockerfile
# backend.Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app/
COPY main.py .
CMD ["python", "main.py"]

# docker-compose.yml
version: '3'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

---

## Logs et Debugging

### Afficher logs Backend

Voir la console où `python main.py` s'exécute:
```
INFO:     Application startup complete
INFO:     POST /api/scan/networks
INFO:     Executed in 0.123 seconds
```

### Afficher logs Frontend

Ouvrir Dev Tools (F12) → Console → Vérifier les logs

### Logs fichier

Modifier `backend/main.py`:
```python
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## Points de Contrôle

✅ **Avant de commencer:**
- [ ] Python 3.9+ installé
- [ ] Node.js 16+ installé
- [ ] 500MB d'espace libre
- [ ] Ports 8000 et 3000 libres

✅ **Après démarrage:**
- [ ] Backend s'exécute (console affiche messages)
- [ ] Frontend s'exécute (console affiche "ready in X ms")
- [ ] http://localhost:8000/health répond
- [ ] http://localhost:3000 affiche interface
- [ ] Scan retourne 6 réseaux

✅ **Après premier audit:**
- [ ] Vulnérabilités affichées
- [ ] Recommandations générées
- [ ] PDF peut être généré
- [ ] JSON peut être exporté

---

**Application prête à être utilisée! 🚀**
