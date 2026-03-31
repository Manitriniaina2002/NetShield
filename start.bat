@echo off
REM Script de démarrage pour Windows

echo.
echo ========================================================
echo NetShield - Wi-Fi Security Audit Lab
echo ========================================================
echo.

REM Checker Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou non configure dans PATH
    pause
    exit /b 1
)
echo [OK] Python trouve

REM Checker Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Node.js n'est pas installe ou non configure dans PATH
    pause
    exit /b 1
)
echo [OK] Node.js trouve
echo.

REM Demarrer Backend
echo [1/2] Demarrage du Backend...
cd backend

if not exist "venv\" (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -q -r requirements.txt

start "NetShield Backend" python main.py
echo [OK] Backend demarre (window separee)
timeout /t 3 /nobreak

REM Demarrer Frontend
echo.
echo [2/2] Demarrage du Frontend...
cd ..\frontend
call npm install --silent
start "NetShield Frontend" cmd /k npm run dev

echo.
echo ========================================================
echo [SUCCESS] NetShield a demarré!
echo ========================================================
echo.
echo Web Interface: http://localhost:3000
echo API Docs: http://localhost:8000/api/docs
echo.
echo Fermer les fenetres pour arreter
pause
