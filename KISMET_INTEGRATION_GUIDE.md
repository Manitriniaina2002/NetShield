# Kismet Integration Guide

## Overview

NetShield now integrates with **Kismet**, a powerful and open-source WiFi scanning and intrusion detection tool. This integration provides:

- **Advanced WiFi Network Detection**: Detect more networks and devices with higher accuracy
- **Real-time Monitoring**: Track networks and devices in real-time
- **Threat Detection**: Automatic detection of suspicious activity and anomalies
- **Detailed Device Information**: Enhanced device metadata and vendor identification
- **Passive Scanning**: No active probing, safer for defensive testing

## Features

### 1. Enhanced Network Scanning
- **Coverage**: Detect networks on 2.4GHz, 5GHz, and 6GHz bands
- **Accuracy**: More precise signal strength and channel information
- **Speed**: Faster identification of networks and clients
- **Cloaking Detection**: Identify hidden SSIDs and spoofed networks

### 2. Device Discovery
- Track all connected clients
- Identify device types and manufacturers
- Monitor client roaming and signal strength
- Detect unusual device behavior

### 3. Security Alerts
- Monitor for jamming and interference
- Detect suspicious probe requests
- Track association hijacking attempts
- Identify rogue access points

---

## Installation

### Prerequisites

- **OS**: Linux-based system (Kali Linux, Ubuntu, etc.)
- **Python**: 3.10+
- **Network Adapter**: WiFi adapter in monitor mode (recommended)

### Step 1: Install Kismet

```bash
# On Kali Linux or Debian/Ubuntu
sudo apt-get update
sudo apt-get install kismet

# On other Linux distributions
# Visit: https://www.kismetwireless.net/
```

### Step 2: Install Python Dependencies

The Kismet integration requires `aiohttp`. It has been added to `requirements.txt`:

```bash
cd /home/kali/Desktop/NetShield/backend
pip install -r requirements.txt

# Or install manually:
pip install aiohttp>=3.9.0
```

### Step 3: Start Kismet Daemon

```bash
# Start Kismet in daemon mode (requires root)
sudo kismet

# Or start with specific options:
sudo kismet -c wlan0
```

Kismet typically runs on `http://localhost:2501` (configurable).

---

## API Endpoints

### 1. Scan Networks via Kismet

**POST** `/api/kismet/networks/scan`

Performs a WiFi scan powered by Kismet.

**Parameters:**
- `duration` (int, optional): Scan duration in seconds (10-120, default: 30)
- `kismet_url` (str, optional): Kismet server URL (default: `http://localhost:2501`)
- `name` (str, optional): Scan name (default: "Kismet Scan")

**Response:**
```json
{
  "id": "kismet_1705009342.1234",
  "scan_name": "Kismet Scan",
  "scan_timestamp": "2024-01-12T10:22:22Z",
  "networks_found": 15,
  "networks": [
    {
      "id": "kismet_AA:BB:CC:DD:EE:FF_1705009342.1234",
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
  ],
  "scan_duration": 30,
  "interface_used": "Kismet",
  "mode": "kismet"
}
```

### 2. Get Current Networks

**GET** `/api/kismet/networks`

Retrieves networks currently tracked by Kismet (without running a new scan).

**Parameters:**
- `kismet_url` (str, optional): Kismet server URL

**Response:**
```json
{
  "networks": [...],
  "count": 15,
  "timestamp": "2024-01-12T10:22:22Z"
}
```

### 3. Get Detected Devices

**GET** `/api/kismet/devices`

Retrieves all devices detected by Kismet.

**Parameters:**
- `kismet_url` (str, optional): Kismet server URL

**Response:**
```json
{
  "devices": [
    {
      "device_key": "kismet.phy80211.accesspoint:AP001",
      "device_name": "AP - MyNetwork",
      "device_type": "router",
      "mac_address": "AA:BB:CC:DD:EE:FF",
      "vendor": "Apple Inc.",
      "signal": -65,
      "first_seen": 1705009200,
      "last_seen": 1705009322
    }
  ],
  "count": 42,
  "timestamp": "2024-01-12T10:22:22Z"
}
```

### 4. Get Security Alerts

**GET** `/api/kismet/alerts`

Retrieves Kismet alert definitions (intrusion signatures, anomalies).

**Parameters:**
- `kismet_url` (str, optional): Kismet server URL

**Response:**
```json
{
  "alerts": [
    {
      "alert_name": "AIRJACK_DETECT",
      "description": "Airjack configuration string detected"
    },
    {
      "alert_name": "ASSOC_FLOODING",
      "description": "Association requests flooding detected"
    }
  ],
  "count": 48,
  "timestamp": "2024-01-12T10:22:22Z"
}
```

### 5. Get Kismet Status

**GET** `/api/kismet/status`

Checks if Kismet is running and retrieves server information.

**Parameters:**
- `kismet_url` (str, optional): Kismet server URL

**Response:**
```json
{
  "status": "online",
  "server_info": {
    "kismet_version": "2024-01-01",
    "server_uuid": "00000000-0000-0000-0000-000000000000",
    "http_session_timeout": 7200,
    "devices_count": 42
  },
  "timestamp": "2024-01-12T10:22:22Z"
}
```

---

## Frontend Integration

The Kismet API is exposed through the `kismetAPI` object in `frontend/src/api.js`:

```javascript
import { kismetAPI } from './api'

// Scan networks via Kismet
const scanResult = await kismetAPI.scanNetworks(30, 'http://localhost:2501')

// Get current networks
const networks = await kismetAPI.getNetworks()

// Get detected devices
const devices = await kismetAPI.getDevices()

// Get alerts
const alerts = await kismetAPI.getAlerts()

// Check Kismet status
const status = await kismetAPI.getStatus()
```

### Example Components

#### Kismet Scanner Component
```jsx
import { kismetAPI } from '../api'

export function KismetScanner() {
  const [scanning, setScanning] = useState(false)
  const [networks, setNetworks] = useState([])

  const startScan = async () => {
    setScanning(true)
    try {
      const result = await kismetAPI.scanNetworks(30)
      setNetworks(result.data.networks)
    } catch (error) {
      console.error('Kismet scan failed:', error)
    } finally {
      setScanning(false)
    }
  }

  return (
    <div>
      <Button onClick={startScan} disabled={scanning}>
        {scanning ? 'Scanning via Kismet...' : 'Start Kismet Scan'}
      </Button>
      {/* Display networks... */}
    </div>
  )
}
```

---

## Configuration

### Kismet Server Settings

Edit Kismet configuration at `/etc/kismet/kismet.conf`:

```bash
# Enable REST API on port 2501
bind_httpd=0.0.0.0:2501

# Set SSL/HTTPS (optional)
# https_port=2502

# Add API key if required
http_key=your_api_key_here
```

### NetShield Settings

Add to `.env` (backend):

```env
KISMET_URL=http://localhost:2501
KISMET_API_KEY=your_optional_api_key
```

---

## Troubleshooting

### Connection Issues

**Error**: "Cannot connect to Kismet at http://localhost:2501"

**Solutions**:
1. Ensure Kismet daemon is running: `sudo kismet`
2. Check port: `lsof -i :2501`
3. Verify firewall allows port 2501
4. Check Kismet logs: `/var/log/kismet/` or `journalctl -u kismet`

### Permission Issues

**Error**: "Permission denied" when scanning

**Solutions**:
1. Run backend as root: `sudo python main.py`
2. Or use `sudo` for Kismet: `sudo kismet`
3. Add user to `kismet` group: `sudo usermod -aG kismet $USER`

### No Networks Detected

**Solutions**:
1. Ensure WiFi adapter is in monitor mode (if required)
2. Check adapter is enabled: `ip link show`
3. Restart Kismet: `sudo systemctl restart kismet`
4. Check Kismet is tracking networks: Visit web UI at `http://localhost:2501`

---

## Performance

| Feature | Kismet | nmcli |
|---------|--------|-------|
| Detection Speed | Fast | Very Fast |
| Accuracy | Very High | Good |
| Device Tracking | Yes | Limited |
| Real-time Monitoring | Yes | No |
| Threat Detection | Yes | No |
| Resource Usage | Medium | Low |

---

## Security Notes

⚠️ **Important**: Kismet scanning may be subject to local laws and regulations.

- Only scan networks you own or have explicit permission to scan
- Use NetShield only for defensive and educational purposes
- Ensure compliance with your organization's policies
- Never use for malicious network access

---

## Advanced Features

### Custom Kismet Queries

You can extend the `KismetService` to support custom queries:

```python
# In backend/app/services/kismet_service.py

async def custom_query(self, endpoint: str) -> List[Dict]:
    """Execute custom Kismet API query"""
    async with self.session.get(f"{self.api_url}/{endpoint}") as resp:
        if resp.status == 200:
            return await resp.json()
    return []
```

### Real-time WebSocket Updates

Future enhancement to add WebSocket support for real-time network updates:

```python
async def stream_networks(self) -> AsyncGenerator:
    """Stream network updates in real-time"""
    # Implementation for WebSocket streaming
```

---

## References

- **Kismet Official**: https://www.kismetwireless.net/
- **Kismet REST API**: https://www.kismetwireless.net/docs/dev/webapi/
- **NetShield Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Version History

- **v1.0.0** (Jan 2024): Initial Kismet integration
  - Network scanning via Kismet
  - Device detection
  - Alert retrieval
  - Full REST API support

---

## Contributing

To extend Kismet integration:

1. Add new methods to `KismetService` class
2. Create new API routes in `backend/app/api/kismet.py`
3. Expose via frontend `kismetAPI` object
4. Document in this guide

---

## License

NetShield is provided for educational and defensive security testing only.

See [LICENSE](LICENSE) for full terms.
