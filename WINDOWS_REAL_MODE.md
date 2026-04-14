# 🪟 NetShield - Windows Real Mode Setup Guide

## Overview

NetShield can now operate in **Real Mode** on Windows, executing actual WiFi scanning commands on your system instead of simulating them.

**Real Mode** means:
- ✅ Real WiFi network scanning via Windows native tools
- ✅ Actual security analysis and vulnerability detection
- ✅ Requires Administrator privileges
- ✅ Works with any WiFi adapter on Windows 7+

---

## Prerequisites

### 1. System Requirements
- **OS**: Windows 7, 8, 10, 11 (64-bit recommended)
- **RAM**: 2GB minimum (4GB+ recommended)
- **WiFi Adapter**: Built-in or USB WiFi adapter

### 2. Required Software
- **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **Git** (optional) - [Download here](https://git-scm.com/)

### 3. Administrator Access
- You must be able to run programs as Administrator
- No special permissions needed beyond standard admin

---

## Installation Steps

### Step 1: Install Python 3.9+

1. Go to https://www.python.org/downloads/
2. Download the latest Python installer
3. **IMPORTANT**: During installation:
   - ✅ Check "Add Python to PATH"
   - ✅ Choose "Install for all users" (optional but recommended)
4. Click "Install"

**Verify installation:**
```cmd
python --version
```

### Step 2: Install Node.js 16+

1. Go to https://nodejs.org/
2. Download the LTS version
3. Run the installer and follow the default prompts
4. Accept all defaults (no special configuration needed)

**Verify installation:**
```cmd
node --version
npm --version
```

### Step 3: Clone or Download NetShield

Option A - With Git:
```cmd
git clone https://github.com/yourusername/NetShield.git
cd NetShield
```

Option B - Without Git:
- Download the ZIP file
- Extract it to a folder (e.g., `C:\NetShield`)
- Open Command Prompt or PowerShell in that folder

---

## Starting NetShield in Real Mode

### Quick Start (Easiest Method)

1. **Locate** the file: `start_real_mode.bat` in the NetShield folder
2. **Right-click** on `start_real_mode.bat`
3. Select **"Run as Administrator"**
4. Click **"Yes"** in the User Account Control popup
5. Wait for two terminal windows to open
6. Open your browser to http://localhost:3000

### What You Should See

```
============================================================================
NetShield - Wi-Fi Security Audit Lab - Windows Real Mode
============================================================================

[✓] Administrator privileges confirmed
[✓] Python 3.x.x found
[✓] Node.js vXX.X.X found

============================================================================
Starting Services...
============================================================================

[1/4] Virtual environment found
[2/4] Dependencies installed
[3/4] Starting Backend in REAL MODE...

Launching: python main.py
Environment: SIMULATION_MODE=False

[✓] Backend started (new window opened)
[4/4] Starting Frontend server...

[✓] Frontend dependencies ready

============================================================================
✅ NetShield Real Mode Started Successfully!
============================================================================

🌐 Frontend: http://localhost:3000
🔌 Backend:  http://localhost:8000/api/docs

⚠️  REAL MODE ACTIVE:
   - WiFi scanning will use REAL SYSTEM COMMANDS
   - Admin privileges are ACTIVE
   - Commands execute on your actual network adapter

🛑 To stop: Close both terminal windows
```

---

## Using NetShield in Real Mode

### 1. First Time Setup

When you first access the app:
1. Click on **"Scan Networks"**
2. Enter any password (at least 4 characters) for admin verification
3. Click **"Authenticate"**
4. The system will verify you have admin privileges
5. If successful, you can start scanning

### 2. Scanning Real WiFi Networks

**Start a Scan:**
1. Click **"Scan Networks"** button
2. Choose scan duration (10-30 seconds recommended)
3. Click **"Start Scan"**
4. Wait for results

**Results will show:**
- ✅ Network SSIDs (actual network names)
- ✅ BSSID (MAC addresses)
- ✅ Signal strength (real time)
- ✅ Security type (WPA2, WPA3, Open, etc.)
- ✅ Connected clients

### 3. Analyzing Networks

For each detected network, you can:
- **Vulnerabilities**: See security weaknesses
- **Recommendations**: Get hardening advice
- **Details**: View technical information
- **Report**: Generate PDF audit report

### 4. Hardware Information

Find WiFi adapter info:
```cmd
ipconfig /all
```

Look for section: "Wireless LAN adapter Wi-Fi"

---

## Troubleshooting

### Issue: "Administrator privileges required"

**Cause**: Script not run as Administrator

**Solution**:
1. Right-click `start_real_mode.bat`
2. Select "Run as Administrator"
3. Click "Yes" in User Account Control dialog

### Issue: Python/Node.js not found

**Cause**: Installation not in PATH

**Solution**:
1. Uninstall Python/Node.js
2. Reinstall with "Add to PATH" option checked
3. Restart your computer
4. Try again

### Issue: Port 8000 or 3000 already in use

**Cause**: Another application using these ports

**Solution**:
```cmd
REM Find process using port 8000
netstat -ano | findstr :8000

REM Kill process (replace PID with actual process ID)
taskkill /PID [PID] /F

REM Same for port 3000
netstat -ano | findstr :3000
taskkill /PID [PID] /F
```

Then restart NetShield.

### Issue: WiFi adapter not detected

**Cause**: WiFi disabled or adapter not properly installed

**Solution**:
1. Check Device Manager: Device Manager → Network adapters
2. Ensure WiFi adapter shows no errors (yellow triangle)
3. Enable WiFi: Click WiFi icon in system tray → Turn on
4. Try scan again

### Issue: "No networks found" or empty results

**Possible causes and solutions**:

1. **WiFi is disabled**: Enable WiFi in system tray
2. **Adapter problem**: Restart WiFi adapter
   ```cmd
   ipconfig /release
   ipconfig /renew
   ```
3. **No networks in range**: Move closer to WiFi router
4. **Too short scan time**: Use 20-30 seconds
5. **Firewall blocking**: Check Windows Defender Firewall
   - Go to Settings → Firewall → Allow apps through firewall
   - Ensure Python.exe is allowed

---

## Manual Start (If Batch Script Fails)

### Terminal 1 - Backend

```cmd
cd backend

# Create virtual environment (first time only)
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start backend
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2 - Frontend

```cmd
cd frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

Expected output:
```
  VITE v5.0.0 ready in XXX ms

  ➜  Local:   http://localhost:3000
```

---

## Real Mode vs Simulation Mode

| Feature | Real Mode | Simulation Mode |
|---------|-----------|-----------------|
| **WiFi Scanning** | Real networks | Fake data |
| **Admin Required** | Yes | No |
| **Accuracy** | 100% real | For learning only |
| **Speed** | 10-30 seconds | Instant |
| **Safety** | Safe (read-only) | N/A |
| **Use Case** | Real audits | Testing & learning |

---

## Configuration

### Environment File: `backend/.env`

The system is configured in: `backend/.env`

Current settings for Real Mode:
```env
SIMULATION_MODE=False          ← Real mode enabled
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
DEBUG=False
REQUIRE_CONFIRMATION=True
```

**To switch to Simulation Mode:**
```env
SIMULATION_MODE=True
```

---

## Command Reference

### Available Real Mode Commands (Windows)

| Command | Function | Example |
|---------|----------|---------|
| `netsh wlan show networks` | List WiFi networks | Built-in scan |
| `netsh wlan show interfaces` | WiFi adapter info | Get adapter status |
| `ipconfig /all` | Network configuration | View all network info |
| `ipconfig /renew` | Renew DHCP lease | Refresh network |

---

## Safety & Ethics

⚠️ **Important Reminders**:

1. **Legal Use Only**: Only scan networks you own or have permission to test
2. **No Attacks**: This tool is for reconnaissance and analysis only - it does NOT:
   - Crack passwords
   - Inject packets
   - Perform DoS attacks
   - Break encryption
3. **Consent Required**: Always have written permission before auditing any network
4. **Local Network Only**: This tool works best on networks in your local broadcast range

---

## Advanced Features

### WiFi Command Panel

In the app, navigate to **"Commands"** to execute raw WiFi commands:

1. Select a command from the dropdown
2. Add parameters if needed
3. Click "Execute"
4. View real-time command output

### Vulnerability Reports

Generate professional PDF reports:
1. Click **"Generate Report"**
2. Report includes:
   - Network inventory
   - Security analysis
   - Vulnerability assessment
   - Recommendations
   - Compliance notes

---

## Stopping NetShield

- **Simple**: Close both terminal windows
- **Windows**: Press `Ctrl+C` in terminal, then `Y` to confirm
- **Both windows**: Close Frontend and Backend terminals

---

## Performance Tips

1. **Faster Scanning**: Use 10-15 second scans instead of 30
2. **Multiple Scans**: Wait 5 seconds between consecutive scans
3. **Use WiFi 5GHz**: If available, scan both 2.4GHz and 5GHz
4. **Close Unused Apps**: Free up RAM for better performance

---

## Next Steps

1. ✅ Run your first real WiFi scan
2. ✅ Review detected networks and their security levels
3. ✅ Check vulnerabilities for each network
4. ✅ Generate your first audit report
5. ✅ Use recommendations to improve your own network security

---

## Support & Help

- **API Documentation**: http://localhost:8000/api/docs
- **Frontend Port**: http://localhost:3000
- **Backend Logs**: Check backend terminal window
- **Issues**: Check troubleshooting section above

---

## License & Disclaimer

⚠️ **This tool is for EDUCATIONAL and AUTHORIZED TESTING ONLY**

- ✅ Educational use
- ✅ Authorized penetration testing (with written consent)
- ✅ Internal security audits
- ❌ Unauthorized access forbidden
- ❌ Use on networks without permission forbidden

**You are responsible for your actions and for complying with all applicable laws.**

---

## Version Info

- **NetShield**: v1.0.0
- **Windows Real Mode**: v1.0.0
- **Last Updated**: 2026-04-13
- **OS Support**: Windows 7, 8, 10, 11

---

**Ready to audit? Run `start_real_mode.bat` as Administrator!** 🚀
