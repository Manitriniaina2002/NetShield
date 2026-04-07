#!/bin/bash
# Quick Validation Script for NetShield Cracking Features
# Run this on Linux/macOS to validate the entire cracking system

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║   NetShield Cracking Features - Quick Validation       ║"
echo "╚════════════════════════════════════════════════════════╝"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python
echo -e "\n${BLUE}[1/5] Checking Python Installation...${NC}"
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python not found${NC}"
    exit 1
else
    PYTHON=$(command -v python3 || command -v python)
    PYTHON_VERSION=$($PYTHON --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
fi

# Check pip
echo -e "\n${BLUE}[2/5] Checking pip Installation...${NC}"
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo -e "${RED}✗ pip not found${NC}"
    exit 1
else
    PIP=$(command -v pip3 || command -v pip)
    echo -e "${GREEN}✓ pip found${NC}"
fi

# Check required Python packages
echo -e "\n${BLUE}[3/5] Checking Python Dependencies...${NC}"
cd backend

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    $PYTHON -m venv venv
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    source venv/Scripts/activate  # Windows Git Bash
fi

# Install requirements
$PIP install -q -r requirements.txt

# Check cracking tools
echo -e "\n${BLUE}[4/5] Checking Cracking Tools...${NC}"

TOOLS_AVAILABLE=0

if command -v aircrack-ng &> /dev/null; then
    VERSION=$(aircrack-ng --version 2>&1 | head -n 1)
    echo -e "${GREEN}✓ aircrack-ng: $VERSION${NC}"
    ((TOOLS_AVAILABLE++))
else
    echo -e "${YELLOW}✗ aircrack-ng not found (optional)${NC}"
fi

if command -v hashcat &> /dev/null; then
    VERSION=$(hashcat --version 2>&1)
    echo -e "${GREEN}✓ hashcat: $VERSION${NC}"
    ((TOOLS_AVAILABLE++))
else
    echo -e "${YELLOW}✗ hashcat not found (optional)${NC}"
fi

if command -v john &> /dev/null; then
    echo -e "${GREEN}✓ john found${NC}"
    ((TOOLS_AVAILABLE++))
else
    echo -e "${YELLOW}✗ john not found (optional)${NC}"
fi

# Check Node.js for frontend
echo -e "\n${BLUE}[5/5] Checking Frontend Dependencies...${NC}"
cd ../frontend

if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}✗ Node.js not found (skipping frontend check)${NC}"
else
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js: $NODE_VERSION${NC}"
    
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing node modules...${NC}"
        npm install -q
    fi
    
    echo -e "${GREEN}✓ Frontend dependencies ready${NC}"
fi

# Final summary
echo -e "\n╔════════════════════════════════════════════════════════╗"
echo -e "║              Validation Summary                         ║"
echo -e "╚════════════════════════════════════════════════════════╝"

if [ $TOOLS_AVAILABLE -gt 0 ]; then
    echo -e "${GREEN}✓ System ready with $TOOLS_AVAILABLE cracking tools${NC}"
else
    echo -e "${YELLOW}⚠ No cracking tools found (run in SIMULATION_MODE)${NC}"
fi

echo -e "\n${BLUE}Next Steps:${NC}"
echo "1. Start backend: cd backend && python main.py"
echo "2. Start frontend: cd frontend && npm run dev"
echo "3. Run tests: python test_cracking_api.py"
echo "4. Visit: http://localhost:5173"
echo ""
