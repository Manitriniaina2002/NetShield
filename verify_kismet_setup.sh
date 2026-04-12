#!/bin/bash
# Kismet Integration Verification Script for NetShield
# This script validates Kismet installation, configuration, and connectivity

set -e

echo "==================================================="
echo "NetShield Kismet Integration Verification"
echo "==================================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

KISMET_URL="${1:-http://localhost:2501}"
ERRORS=0
WARNINGS=0

# Helper functions
log_check() {
    echo -n "[*] Checking $1... "
}

log_success() {
    echo -e "${GREEN}✓${NC}"
}

log_fail() {
    echo -e "${RED}✗ FAIL${NC}"
    ERRORS=$((ERRORS + 1))
}

log_warn() {
    echo -e "${YELLOW}⚠ WARNING${NC}"
    WARNINGS=$((WARNINGS + 1))
}

log_info() {
    echo "[i] $1"
}

# Check 1: Python version
log_check "Python version (>=3.10)"
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [ "$(printf '%s\n' "3.10" "$PYTHON_VERSION" | sort -V | head -n1)" = "3.10" ]; then
    log_success
    log_info "Python $PYTHON_VERSION found"
else
    log_fail
    log_info "Found Python $PYTHON_VERSION, need 3.10 or higher"
fi

# Check 2: Backend directory structure
log_check "Backend directory structure"
if [ -d "backend" ] && [ -f "backend/requirements.txt" ]; then
    log_success
else
    log_fail
    log_info "Backend directory or requirements.txt not found"
fi

# Check 3: aiohttp installation
log_check "aiohttp Python package"
if python3 -c "import aiohttp" 2>/dev/null; then
    log_success
    AIOHTTP_VERSION=$(python3 -c 'import aiohttp; print(aiohttp.__version__)')
    log_info "aiohttp $AIOHTTP_VERSION installed"
else
    log_warn
    log_info "aiohttp not installed. Run: pip install -r backend/requirements.txt"
fi

# Check 4: Kismet binary
log_check "Kismet binary installation"
if command -v kismet &> /dev/null; then
    log_success
    KISMET_VERSION=$(kismet --version 2>&1 | head -1)
    log_info "$KISMET_VERSION"
else
    log_warn
    log_info "Kismet not found. Install with: sudo apt install kismet"
fi

# Check 5: Kismet daemon connectivity
log_check "Kismet daemon connectivity (URL: $KISMET_URL)"
if command -v curl &> /dev/null; then
    if curl -s "$KISMET_URL/system/status" > /dev/null 2>&1; then
        log_success
        STATUS=$(curl -s "$KISMET_URL/system/status" | python3 -c "import sys, json; print(json.load(sys.stdin).get('results', {}).get('kismet_version', 'unknown'))" 2>/dev/null || echo "unknown")
        log_info "Kismet daemon responding (version: $STATUS)"
    else
        log_fail
        log_info "Cannot reach Kismet at $KISMET_URL"
        log_info "Is Kismet daemon running? Try: sudo kismet"
    fi
else
    log_warn
    log_info "curl not found, cannot verify Kismet connectivity"
fi

# Check 6: Kismet API port accessibility
log_check "Kismet API port"
if command -v lsof &> /dev/null; then
    if lsof -i :2501 > /dev/null 2>&1; then
        log_success
        log_info "Port 2501 is in use by Kismet"
    else
        log_warn
        log_info "Port 2501 not in use. Kismet daemon may not be running"
    fi
else
    log_warn
    log_info "lsof not found, cannot verify port 2501"
fi

# Check 7: Network adapter configuration
log_check "WiFi network adapters"
if command -v ip &> /dev/null; then
    ADAPTERS=$(ip link show | grep -E '(wlan|wlp|wlo)' | awk '{print $2}' | sed 's/.*\(wl[^:]*\).*/\1/')
    if [ -n "$ADAPTERS" ]; then
        log_success
        log_info "Found adapters: $(echo $ADAPTERS | tr '\n' ' ')"
    else
        log_warn
        log_info "No WiFi adapters found. Ensure WiFi hardware is present"
    fi
else
    log_warn
    log_info "ip command not found, cannot check adapters"
fi

# Check 8: Frontend dependencies
log_check "Frontend npm dependencies"
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    log_success
    if [ -d "frontend/node_modules" ]; then
        log_info "npm dependencies installed"
    else
        log_warn
        log_info "npm dependencies not yet installed. Run: npm install in frontend/"
    fi
else
    log_fail
    log_info "frontend directory or package.json not found"
fi

# Check 9: FastAPI/Uvicorn installation
log_check "FastAPI and Uvicorn"
if python3 -c "import fastapi; import uvicorn" 2>/dev/null; then
    log_success
    FASTAPI_VERSION=$(python3 -c 'import fastapi; print(fastapi.__version__)')
    log_info "FastAPI $FASTAPI_VERSION installed"
else
    log_warn
    log_info "FastAPI/Uvicorn not installed. Run: pip install -r backend/requirements.txt"
fi

# Check 10: Kismet configuration file
log_check "Kismet configuration"
if [ -f "/etc/kismet/kismet.conf" ]; then
    log_success
    if grep -q "bind_httpd=0.0.0.0:2501" /etc/kismet/kismet.conf; then
        log_info "API endpoint configured at 0.0.0.0:2501"
    else
        log_warn
        log_info "Recommend: Set 'bind_httpd=0.0.0.0:2501' in /etc/kismet/kismet.conf"
    fi
elif [ -f "/etc/kismet/kismet_site.conf" ]; then
    log_warn
    log_info "Custom Kismet config found at /etc/kismet/kismet_site.conf"
else
    log_warn
    log_info "Kismet config not found at standard location"
fi

# Summary
echo ""
echo "==================================================="
echo "Verification Summary"
echo "==================================================="
echo -e "${GREEN}Passed:${NC} $(( 10 - ERRORS - WARNINGS )) checks"
if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}Warnings:${NC} $WARNINGS issues"
fi
if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}Errors:${NC} $ERRORS issues"
fi
echo ""

# Final recommendations
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ System appears ready for Kismet integration!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Start Kismet daemon: sudo kismet"
    echo "2. Start NetShield backend: python backend/main.py"
    echo "3. Start NetShield frontend: npm run dev (in frontend/)"
    echo "4. Open http://localhost:5173 in your browser"
    exit 0
else
    echo -e "${RED}✗ Please fix the errors above before proceeding${NC}"
    echo ""
    echo "Common fixes:"
    echo "• Install Python dependencies: pip install -r backend/requirements.txt"
    echo "• Install Kismet: sudo apt install kismet"
    echo "• Start Kismet daemon: sudo kismet"
    exit 1
fi
