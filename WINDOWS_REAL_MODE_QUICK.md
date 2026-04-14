# 🪟 Windows Real Mode - Quick Start

## 60-Second Setup

### Step 1: Check Prerequisites
```cmd
python --version     # Should show Python 3.9+
node --version      # Should show v16+
```

### Step 2: Run the Script
```cmd
# Right-click start_real_mode.bat
# Select "Run as Administrator"
```

### Step 3: Open Browser
```
http://localhost:3000
```

---

## What Real Mode Does

| Action | What Happens |
|--------|-------------|
| Scan Networks | Uses `netsh wlan show networks` to find real WiFi networks |
| Get Adapter Info | Reads actual WiFi adapter details from Windows |
| Analyze Security | Examines real security settings detected by Windows |
| Generate Report | Creates PDF with authentic network data |

---

## Common Commands in Real Mode

### View WiFi Info
```cmd
ipconfig /all
```

### View Current WiFi
```cmd
netsh wlan show interfaces
```

### List Networks
```cmd
netsh wlan show networks mode=Bssid
```

### Renew Network
```cmd
ipconfig /release
ipconfig /renew
```

---

## File Mapping

| In App | Real Command | Windows Command |
|--------|-------------|-----------------|
| `ifconfig` | Network info | `ipconfig` |
| `netsh_wlan_show` | WiFi networks | `netsh wlan show networks mode=Bssid` |
| `netsh_wlan_interfaces` | WiFi adapter | `netsh wlan show interfaces` |
| `tasklist` | Processes | `tasklist` |

---

## Troubleshooting

**Problem**: "Administrator privileges required"
**Solution**: Right-click `start_real_mode.bat` → "Run as Administrator"

**Problem**: Python not found
**Solution**: Install from https://www.python.org → Check "Add Python to PATH"

**Problem**: No networks found
**Solution**: 
1. Make sure WiFi is enabled
2. Move closer to a router
3. Extend scan time to 20-30 seconds

**Problem**: Port 8000/3000 in use
**Solution**:
```cmd
netstat -ano | findstr :8000
taskkill /PID [PID] /F
```

---

## Configuration

**File**: `backend/.env`

Current settings:
```env
SIMULATION_MODE=False          ← ✅ Real mode active
BACKEND_PORT=8000              ← Backend API
BACKEND_HOST=127.0.0.1         ← Local access only
```

**To switch to Simulation** (fake data):
```env
SIMULATION_MODE=True
```

---

## Access Points

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

---

## Session Lifetime

- Admin sessions: **1 hour** (automatic renewal)
- Idle timeout: Auto-logout if browser closed
- Multi-window support: Yes (same session)

---

## Windows-Specific Notes

✅ **Supports**:
- Windows 7, 8, 10, 11
- Built-in WiFi adapters
- USB WiFi adapters
- Virtual WiFi (some versions)

❌ **Does NOT Support**:
- WiFi packet injection
- Monitor mode (Windows limitation)
- Handshake capture (Windows limitation)
- On-the-fly channel switching

---

## Performance

- Scan time: 10-30 seconds
- Typical networks detected: 3-15
- Memory usage: ~150MB
- CPU usage: Low (idle most of time)

---

## Legal

⚠️ **USE ONLY ON AUTHORIZED NETWORKS**

- ✅ Your home network
- ✅ Corporate network with permission
- ✅ Lab/Test environment you control
- ❌ Networks without written permission
- ❌ Unauthorized access prohibited

---

## Next Steps After First Run

1. Click **"Scan Networks"**
2. Wait for WiFi networks to appear
3. Click **"Vulnerabilities"** on a network
4. Click **"Recommendations"** for fixes
5. Generate PDF report for documentation

---

**Status**: ✅ Real Mode Configuration Complete
**Ready to Scan**: Run `start_real_mode.bat` as Administrator!
