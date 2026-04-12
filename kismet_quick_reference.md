# Kismet Integration - Quick Reference

## What's New?

NetShield now integrates with **Kismet**, a professional wireless network detection and intrusion detection framework. This provides advanced scanning capabilities beyond standard WiFi tools.

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
cd /home/kali/Desktop/NetShield/backend
pip install -r requirements.txt
```

### 2. Start Kismet Daemon
```bash
sudo kismet
```

### 3. Verify Setup
```bash
bash verify_kismet_setup.sh
```

### 4. Run Integration Tests
```bash
python test_kismet_integration.py
```

### 5. Run NetShield
```bash
# Terminal 1: Backend
python backend/main.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

---

## API Quick Reference

### Backend Endpoints

All endpoints prefixed with `/api/kismet/`

| Method | Endpoint | Purpose | Parameters |
|--------|----------|---------|------------|
| `POST` | `/networks/scan` | Full WiFi scan via Kismet | `duration=30` (sec), `name` |
| `GET` | `/networks` | Get tracked networks (no scan) | `kismet_url` (optional) |
| `GET` | `/devices` | Get all detected devices | `kismet_url` (optional) |
| `GET` | `/alerts` | Get alert definitions | `kismet_url` (optional) |
| `GET` | `/status` | Check Kismet health | `kismet_url` (optional) |

### Frontend JavaScript API

```javascript
import { kismetAPI } from './api'

// Start scan (30 second duration)
const result = await kismetAPI.scanNetworks(30)

// Get current networks (no scan)
const networks = await kismetAPI.getNetworks()

// Get all detected devices
const devices = await kismetAPI.getDevices()

// Get security alerts
const alerts = await kismetAPI.getAlerts()

// Check Kismet status
const status = await kismetAPI.getStatus()
```

---

## Response Format Example

### Network Response
```json
{
  "id": "kismet_BSSID_timestamp",
  "ssid": "MyNetwork",
  "bssid": "AA:BB:CC:DD:EE:FF",
  "channel": 6,
  "frequency": "2.4GHz",
  "security": "WPA2",
  "signal_strength": -65,
  "signal_percentage": 70,
  "clients": 5,
  "last_seen": "2024-01-12T10:22:22Z"
}
```

---

## Troubleshooting

### Connection Refused
```bash
# Ensure Kismet is running
sudo kismet

# Verify port 2501 is listening
lsof -i :2501
```

### Permission Issues
```bash
# Run as root
sudo python backend/main.py

# Or add user to kismet group
sudo usermod -aG kismet $USER
```

### No Networks Detected
```bash
# Check WiFi adapter is enabled
ip link show

# Check Kismet is tracking networks
curl http://localhost:2501/networks/summary

# Restart Kismet
sudo systemctl restart kismet
```

---

## File Structure

```
NetShield/
├── KISMET_INTEGRATION_GUIDE.md       # Full documentation
├── kismet_quick_reference.md         # This file
├── verify_kismet_setup.sh            # Verification script
├── test_kismet_integration.py        # Integration test suite
│
├── backend/
│   ├── requirements.txt              # ₊ Added: aiohttp>=3.9.0
│   ├── app/
│   │   ├── api/
│   │   │   ├── kismet.py            # NEW: 5 REST endpoints
│   │   │   └── __init__.py          # ₊ Updated: register kismet router
│   │   └── services/
│   │       └── kismet_service.py    # NEW: Async Kismet client
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   └── api.js                   # ₊ Updated: Added kismetAPI object
│   └── package.json
```

---

## Key Components

### Backend Service (`backend/app/services/kismet_service.py`)
- **Purpose**: Async client for Kismet daemon communication
- **Features**: 
  - Non-blocking async/await pattern
  - Automatic network parsing to WiFiNetwork models
  - Security detection (WPA3/WPA2/WPA/WEP)
  - Error handling and logging

### Backend API (`backend/app/api/kismet.py`)
- **Purpose**: REST endpoints for frontend integration
- **Features**:
  - 5 endpoints (scan, networks, devices, alerts, status)
  - Proper HTTP status codes
  - Comprehensive error handling
  - Consistent response format

### Frontend API (`frontend/src/api.js`)
- **Purpose**: JavaScript methods to call Kismet endpoints
- **Features**:
  - Promise-based (async/await compatible)
  - Default parameters for ease of use
  - Axios-based HTTP requests

---

## Configuration

### Kismet Daemon Port
Default: `http://localhost:2501`

Custom URL (in requests):
```javascript
// Use custom Kismet URL
await kismetAPI.scanNetworks(30, 'http://192.168.1.100:2501')
```

### Environment Variables (Optional)
```bash
# .env (backend)
KISMET_URL=http://localhost:2501
KISMET_API_KEY=your_optional_key
```

---

## Testing

### Unit Tests
```bash
# Run integration test suite
python test_kismet_integration.py

# Export results to JSON
python test_kismet_integration.py --export results.json

# Custom Kismet URL
python test_kismet_integration.py --kismet-url http://192.168.1.100:2501
```

### Manual Testing
```bash
# Check Kismet status
curl http://localhost:2501/system/status

# Get networks
curl http://localhost:2501/networks/summary

# Test backend endpoint
curl http://localhost:8000/api/kismet/status

# Start scan (30 seconds)
curl -X POST http://localhost:8000/api/kismet/networks/scan?duration=30
```

---

## Performance Considerations

| Operation | Time | Notes |
|-----------|------|-------|
| Network scan (30s) | ~30s | Kismet collects data during scan |
| Get networks | <100ms | Real-time from Kismet cache |
| Get devices | <100ms | Real-time from Kismet cache |
| Get alerts | <50ms | Static definitions |
| Get status | <50ms | Health check |

### Optimization Tips
- Use `getNetworks()` for real-time data (no scan overhead)
- Cache results locally to reduce API calls
- Use WebSocket support (future enhancement) for real-time streaming

---

## Security Notes

⚠️ **Disclaimer**: WiFi scanning may be regulated in your jurisdiction.

- Only scan networks you own or have permission to scan
- Use for defensive and educational purposes only
- Respect organizational policies and local laws
- NetShield is not responsible for misuse

---

## Next Steps

1. **Install**: `pip install -r backend/requirements.txt`
2. **Verify**: `bash verify_kismet_setup.sh`
3. **Test**: `python test_kismet_integration.py`
4. **Run**: Follow Quick Start above
5. **Create UI**: Add Kismet scan option to Dashboard component

---

## Dashboard Integration Example

```jsx
import { kismetAPI } from '../api'
import { useEffect, useState } from 'react'

export function DashboardWithKismet() {
  const [scanMode, setScanMode] = useState('standard') // or 'kismet'
  const [networks, setNetworks] = useState([])

  const startScan = async () => {
    if (scanMode === 'kismet') {
      // Use Kismet
      const result = await kismetAPI.scanNetworks(30)
      setNetworks(result.data.networks)
    } else {
      // Use standard WiFi scan
      const result = await wifiAPI.scan()
      setNetworks(result.data.networks)
    }
  }

  return (
    <div>
      <select value={scanMode} onChange={(e) => setScanMode(e.target.value)}>
        <option value="standard">Standard WiFi Scan</option>
        <option value="kismet">Advanced Kismet Scan</option>
      </select>
      <button onClick={startScan}>Start Scan</button>
      {/* Display networks... */}
    </div>
  )
}
```

---

## Additional Resources

- **Kismet Official**: https://www.kismetwireless.net/
- **Kismet REST API**: https://www.kismetwireless.net/docs/dev/webapi/
- **Full Guide**: [KISMET_INTEGRATION_GUIDE.md](KISMET_INTEGRATION_GUIDE.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Support

For issues or questions:
1. Check [KISMET_INTEGRATION_GUIDE.md](KISMET_INTEGRATION_GUIDE.md) Troubleshooting section
2. Run verification script: `bash verify_kismet_setup.sh`
3. Run integration tests: `python test_kismet_integration.py`
4. Check backend logs: `python backend/main.py` (watch for errors)
5. Check Kismet logs: `journalctl -u kismet` or `/var/log/kismet/`

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Status**: Production Ready ✓
