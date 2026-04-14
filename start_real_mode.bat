@echo off
REM ============================================================================
REM NetShield - Windows Real Mode Startup
REM ============================================================================
REM 
REM This script starts NetShield in REAL MODE for WiFi scanning on Windows
REM Requires: Administrator privileges
REM
REM ⚠️ IMPORTANT: Right-click and select "Run as Administrator" to execute this script
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo NetShield - Wi-Fi Security Audit Lab - Windows Real Mode
echo ============================================================================
echo.

REM Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  ERROR: This script requires Administrator privileges!
    echo.
    echo SOLUTION: 
    echo   1. Right-click on this file
    echo   2. Select "Run as Administrator"
    echo   3. Click "Yes" in the User Account Control dialog
    echo.
    pause
    exit /b 1
)

echo [✓] Administrator privileges confirmed
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found in PATH
    echo.
    echo SOLUTION:
    echo   1. Install Python 3.9+ from https://www.python.org
    echo   2. During installation, CHECK "Add Python to PATH"
    echo   3. Restart your computer and try again
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [✓] %PYTHON_VERSION% found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js not found in PATH
    echo.
    echo SOLUTION:
    echo   1. Install Node.js 16+ from https://nodejs.org
    echo   2. During installation, use default settings
    echo   3. Restart your computer and try again
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo [✓] Node.js !NODE_VERSION! found

echo.
echo ============================================================================
echo Starting Services...
echo ============================================================================
echo.

REM Navigate to backend
cd /d "%~dp0backend" || (
    echo ❌ ERROR: Could not navigate to backend folder
    pause
    exit /b 1
)

REM Create virtual environment if not exists
if not exist "venv\" (
    echo [1/4] Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [✓] Virtual environment created
) else (
    echo [✓] Virtual environment found
)

REM Activate virtual environment and install requirements
echo [2/4] Setting up Python dependencies...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

pip install -q -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: Some packages may not have installed correctly
    echo Proceeding anyway...
)
echo [✓] Dependencies installed

REM Start Backend with Real Mode
echo.
echo [3/4] Starting Backend in REAL MODE...
echo.
echo Launching: python main.py
echo Environment: SIMULATION_MODE=false
echo.
timeout /t 2 /nobreak

start "NetShield Backend - Real Mode" cmd /k "set SIMULATION_MODE=false& python main.py"
if errorlevel 1 (
    echo ❌ ERROR: Failed to start backend
    pause
    exit /b 1
)

echo [✓] Backend started (new window opened)
timeout /t 5 /nobreak

REM Navigate to frontend
cd /d "%~dp0frontend" || (
    echo ❌ ERROR: Could not navigate to frontend folder
    pause
    exit /b 1
)

REM Install frontend dependencies
echo [4/4] Starting Frontend server...
call npm install --silent
if errorlevel 1 (
    echo ⚠️  Warning: npm install had issues
)

echo.
echo [✓] Frontend dependencies ready
echo.
echo ============================================================================
echo ✅ NetShield Real Mode Started Successfully!
echo ============================================================================
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔌 Backend:  http://localhost:8000/api/docs
echo.
echo ⚠️  REAL MODE ACTIVE:
echo   - WiFi scanning will use REAL SYSTEM COMMANDS
echo   - Admin privileges are ACTIVE
echo   - Commands execute on your actual network adapter
echo.
echo 🛑 To stop: Close both terminal windows
echo.
timeout /t 3 /nobreak

REM Start Frontend (keep terminal open)
npm run dev

setlocal disableendexpansion
