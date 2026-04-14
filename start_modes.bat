@echo off
REM ============================================================================
REM NetShield - Mode Selector Menu
REM ============================================================================
REM 
REM Choose between SIMULATION MODE (safe learning) or REAL MODE (actual scanning)
REM
REM ============================================================================

setlocal enabledelayedexpansion

:menu
echo.
echo ============================================================================
echo NetShield - Select Operating Mode
echo ============================================================================
echo.
echo What mode would you like to run?
echo.
echo 1) SIMULATION MODE (Recommended for learning)
echo    - Safe, no admin required
echo    - Fake WiFi network data
echo    - Fast and instant results
echo    - Perfect for testing the interface
echo.
echo 2) REAL MODE (Requires admin privileges)
echo    - Real WiFi network scanning
echo    - Requires Administrator
echo    - Actual security analysis
echo    - For real audits and testing
echo.
echo 3) EXIT
echo.
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" goto simulation_mode
if "%choice%"=="2" goto real_mode
if "%choice%"=="3" goto exit_script
echo Invalid choice. Please try again.
goto menu

:simulation_mode
echo.
echo ============================================================================
echo Preparing SIMULATION MODE...
echo ============================================================================
echo.
echo Setting SIMULATION_MODE=True in backend\.env...

cd /d "%~dp0backend"

REM Create/update .env with simulation mode
(
    echo DEBUG=False
    echo CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
    echo BACKEND_HOST=127.0.0.1
    echo BACKEND_PORT=8000
    echo SIMULATION_MODE=True
    echo REQUIRE_CONFIRMATION=True
) > .env.new
move /y .env.new .env >nul 2>&1

echo.
echo [✓] Simulation mode configured
echo.
echo Now starting NetShield in SIMULATION MODE...
echo.
echo This mode is perfect for:
echo - Learning how NetShield works
echo - Testing the interface
echo - No network changes
echo.
timeout /t 2 /nobreak

REM Run simulation mode startup
call "%~dp0start.bat"
goto end_script

:real_mode
echo.
echo ============================================================================
echo Preparing REAL MODE...
echo ============================================================================
echo.

REM Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  ERROR: This requires Administrator privileges!
    echo.
    echo SOLUTION:
    echo   1. Right-click on this batch file (start_modes.bat)
    echo   2. Select "Run as Administrator"
    echo   3. Choose option 2 again
    echo.
    pause
    goto menu
)

echo [✓] Administrator privileges confirmed
echo.
echo Setting SIMULATION_MODE=False in backend\.env...

cd /d "%~dp0backend"

REM Create/update .env with real mode
(
    echo DEBUG=False
    echo CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
    echo BACKEND_HOST=127.0.0.1
    echo BACKEND_PORT=8000
    echo SIMULATION_MODE=False
    echo REQUIRE_CONFIRMATION=True
) > .env.new
move /y .env.new .env >nul 2>&1

echo.
echo [✓] Real mode configured
echo.
echo Now starting NetShield in REAL MODE...
echo.
echo This mode will:
echo - Scan real WiFi networks
echo - Analyze actual security settings
echo - Generate real audit reports
echo.
echo ⚠️  Your system will execute WiFi scanning commands!
echo.
timeout /t 3 /nobreak

REM Run real mode startup
call "%~dp0start_real_mode.bat"
goto end_script

:exit_script
echo.
echo ============================================================================
echo Thank you for using NetShield!
echo ============================================================================
echo.
goto end_script

:end_script
setlocal disableendexpansion
exit /b 0
