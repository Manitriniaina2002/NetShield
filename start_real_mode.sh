#!/bin/bash
# 🐧 Script de lancement NetShield en Mode Réel Linux

echo "=========================================="
echo "🐧 NetShield - Mode Réel Linux"
echo "=========================================="
echo ""

# Vérifier si on est root
if [ ! "$EUID" -eq 0 ]; then
  echo "❌ ERREUR: Ce script doit être exécuté en ROOT!"
  echo ""
  echo "Lancez avec:"
  echo "  sudo bash start_real_mode.sh"
  echo ""
  exit 1
fi

echo "✅ Vous êtes ROOT"
echo "✅ Mode réel activé dans .env (SIMULATION_MODE=False)"
echo ""

# Vérifier que .env existe, sinon le créer avec des valeurs par défaut
if [ ! -f "backend/.env" ]; then
  echo "⚠️  backend/.env non trouvé. Création d'un fichier par défaut..."
  cat > backend/.env << 'EOF'
DEBUG=False
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
SIMULATION_MODE=False
REQUIRE_CONFIRMATION=True
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://127.0.0.1:3000","http://127.0.0.1:5173"]
COMPANY_NAME=NetShield Labs
PDF_TEMP_DIR=./temp_reports
KISMET_USERNAME=netshield
KISMET_PASSWORD=netshield123!
EOF
  echo "✅ backend/.env créé"
fi

# Vérifier/forcer SIMULATION_MODE=False
if grep -q "^SIMULATION_MODE=" backend/.env; then
  if grep -q "SIMULATION_MODE=True" backend/.env; then
    echo "⚠️  SIMULATION_MODE est encore True. Modification..."
    sed -i 's/SIMULATION_MODE=True/SIMULATION_MODE=False/g' backend/.env
    echo "✅ SIMULATION_MODE changé à False"
    echo ""
  fi
else
  echo "SIMULATION_MODE=False" >> backend/.env
  echo "✅ SIMULATION_MODE ajouté à backend/.env"
  echo ""
fi

echo "📋 Configuration:"
echo "  • Mode: RÉEL (vraies commandes Linux)"
echo "  • Utilisateur: $(whoami)"
echo "  • UID: $(id -u)"
echo "  • Commandes autorisées: ifconfig, ip, airmon-ng, airodump-ng, ps, kill"
echo ""

# Activer virtualenv
echo "1️⃣  Activation de l'environnement virtuel..."
cd backend

if [ ! -d "venv" ]; then
  echo "   Création environnement virtuel..."
  python3 -m venv venv
fi

source venv/bin/activate
echo "   ✅ Environnement activé"
echo ""

# Installer dépendances
echo "2️⃣  Installation des dépendances..."
pip install -q -r requirements.txt 2>/dev/null
echo "   ✅ Dépendances installées"
echo ""

# Démarrer Kismet automatiquement si nécessaire
echo "3️⃣  Vérification Kismet..."
if lsof -i :2501 >/dev/null 2>&1; then
  echo "   ✅ Kismet déjà actif sur le port 2501"
else
  if systemctl list-unit-files | grep -q '^kismet.service'; then
    echo "   ▶ Démarrage du service kismet..."
    systemctl start kismet >/dev/null 2>&1 || true
  else
    echo "   ▶ Démarrage de kismet en arrière-plan..."
    nohup kismet >/tmp/netshield-kismet.log 2>&1 &
  fi

  # Attendre la disponibilité API Kismet
  KISMET_READY=0
  for _ in $(seq 1 15); do
    if curl -s --max-time 2 http://localhost:2501/system/status.json >/dev/null 2>&1; then
      KISMET_READY=1
      break
    fi
    sleep 1
  done

  if [ "$KISMET_READY" -eq 1 ]; then
    echo "   ✅ Kismet démarré (http://localhost:2501)"
  else
    echo "   ⚠️  Kismet n'a pas pu être démarré automatiquement"
    echo "   ℹ️  Lancez manuellement dans un autre terminal: sudo kismet"
    echo "   ℹ️  Logs possibles: /tmp/netshield-kismet.log ou journalctl -u kismet"
  fi
else
  echo "   ✅ Kismet déjà actif sur le port 2501"
fi

# Initialiser l'authentification Kismet (important!)
echo ""
echo "4️⃣  Configuration de l'authentification Kismet..."
KISMET_AUTH_INIT=$(curl -s -X POST -d 'username=netshield&password=netshield123!' \
  http://localhost:2501/session/set_password 2>/dev/null)

if echo "$KISMET_AUTH_INIT" | grep -q "configured\|Login"; then
  echo "   ✅ Authentification Kismet initialisée"
else
  echo "   ⚠️  Authentification Kismet: vérification en arrière-plan"
fi
echo ""

# Lancer le serveur
echo "5️⃣  Lancement du serveur..."
echo "   🔗 Backend: http://localhost:8000"
echo "   📚 API Docs: http://localhost:8000/api/docs"
echo ""
echo "   Autre terminal: cd frontend && npm run dev"
echo "   Puis: http://localhost:3000"
echo ""
echo "   (Ctrl+C pour arrêter)"
echo ""

python main.py
