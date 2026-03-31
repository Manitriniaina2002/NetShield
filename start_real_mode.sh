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

# Vérifier que .env existe
if [ ! -f "backend/.env" ]; then
  echo "❌ backend/.env non trouvé!"
  exit 1
fi

# Vérifier SIMULATION_MODE=False
if grep -q "SIMULATION_MODE=True" backend/.env; then
  echo "⚠️  SIMULATION_MODE est encore True. Modification..."
  sed -i 's/SIMULATION_MODE=True/SIMULATION_MODE=False/g' backend/.env
  echo "✅ SIMULATION_MODE changé à False"
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

# Lancer le serveur
echo "3️⃣  Lancement du serveur..."
echo "   🔗 Backend: http://localhost:8000"
echo "   📚 API Docs: http://localhost:8000/api/docs"
echo ""
echo "   Autre terminal: cd frontend && npm run dev"
echo "   Puis: http://localhost:3000"
echo ""
echo "   (Ctrl+C pour arrêter)"
echo ""

python main.py
