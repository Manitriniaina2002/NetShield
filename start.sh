#!/bin/bash

# Script de démarrage complet de NetShield
# Utilisation: ./start.sh

echo "🚀 Démarrage de NetShield - Wi-Fi Security Audit Lab"
echo "=================================================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier Python
echo -e "\n${YELLOW}[1/4]${NC} Vérification de Python..."
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}✗${NC} Python 3 n'est pas installé"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python trouvé: $(python3 --version)"

# Vérifier Node.js
echo -e "\n${YELLOW}[2/4]${NC} Vérification de Node.js..."
if ! command -v node &> /dev/null
then
    echo -e "${RED}✗${NC} Node.js n'est pas installé"
    exit 1
fi
echo -e "${GREEN}✓${NC} Node.js trouvé: $(node --version)"

# Démarrer Backend
echo -e "\n${YELLOW}[3/4]${NC} Démarrage du Backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo -e "${GREEN}✓${NC} Backend prêt"
python3 main.py &
BACKEND_PID=$!
echo "PID Backend: $BACKEND_PID"

# Attendre que le backend démarre
sleep 3

# Démarrer Frontend
echo -e "\n${YELLOW}[4/4]${NC} Démarrage du Frontend..."
cd ../frontend
npm install -q
npm run dev &
FRONTEND_PID=$!
echo "PID Frontend: $FRONTEND_PID"

echo -e "\n${GREEN}✓ NetShield a démarré avec succès!${NC}"
echo ""
echo "🌐 Interface Web: http://localhost:3000"
echo "📚 API Documentation: http://localhost:8000/api/docs"
echo ""
echo "⚠️  AVERTISSEMENT: Cet outil est pour l'usage éducatif et autorisé uniquement"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter"

wait
