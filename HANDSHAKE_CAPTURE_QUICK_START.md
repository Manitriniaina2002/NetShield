# Handshake Capture Tool - Quick Start Guide

## Overview
The Handshake Capture Tool in NetShield allows you to capture WiFi handshakes for password cracking analysis.

## Step-by-Step Usage

### 1. Launch the Application
```bash
# On Windows
start_real_mode.bat

# On Linux/macOS
./start.sh
```

### 2. Perform Initial WiFi Scan
- Click **"Démarrer un scan"** button to detect networks
- Wait for scan to complete (10-15 seconds)
- Networks will appear in the overview

### 3. Navigate to Handshake Capture
- Click the **"Capture de Handshake"** tab in the navigation bar
- You'll see all detected networks listed

### 4. Select a Target Network
- Click on a network in the list to select it
- Selected network will be highlighted in blue
- The network SSID, BSSID, signal strength, and channel are displayed

### 5. Configure Capture Settings
```
Duration: Time to capture in seconds
Min: 10 seconds
Recommended: 60 seconds (1 minute)
Max: 600 seconds (10 minutes)
```

For fastest handshake capture:
- **Short duration (30-60s)**: If clients actively connecting
- **Medium duration (2-3 min)**: Standard audit scenario
- **Long duration (5-10 min)**: Quiet networks with few clients

### 6. Start the Capture
- Click **"Démarrer la capture"** button
- Status will change to "running"
- Progress bar will display capture progress
- Packet count updates in real-time

### 7. Monitor the Capture
The interface shows:
```
Status:         [pending | running | completed | failed]
Progress:       0-100%
Packets:        Number of packets captured
Handshake:      [En attente... | Détecté ✓]
```

### 8. Cancel (if needed)
- Click **"Annuler"** button to stop capture early
- Useful if target network not responding

### 9. Use for Cracking
Once capture completes with handshake detected:
- Click **"Utiliser pour le cracking"** button
- This passes the capture data to the Cracking Panel
- Select cracking method (Aircrack-ng, Hashcat, John)
- Select wordlist and start cracking

## Keyboard Shortcuts
- `Tab` - Switch between tabs
- `Enter` - Start capture (when network selected)
- `Escape` - Cancel current operation

## Troubleshooting

### Problem: "Aucune interface WiFi disponible"
**Cause**: No wireless adapter detected
**Solution**: 
- Check adapter is enabled in device manager
- Try "Rafraîchir interfaces" button
- Ensure WiFi drivers installed

### Problem: Capture completes but no handshake found
**Cause**: No clients connected during capture
**Solution**:
- Wait for client activity (phone connecting, laptop searching)
- Increase capture duration
- Move router/target network to different location
- Try de-authenticating devices with Commands tab

### Problem: Capture times out
**Cause**: Tool not responding
**Solution**:
- Check WSL2 is properly installed (Windows)
- Verify aircrack-ng installed: `wsl apt-cache policy aircrack-ng`
- Enable simulation mode in .env: `SIMULATION_MODE=True`

### Problem: "Capture non disponible" error
**Cause**: WSL or Linux tools not found
**Solution**:
```bash
# On Windows/WSL:
wsl bash
sudo apt-get update
sudo apt-get install -y aircrack-ng hashcat john

# On Linux:
sudo apt-get install -y aircrack-ng hashcat john

# On macOS:
brew install aircrack-ng hashcat john
```

## Advanced Usage

### Capture Multiple Networks
- Capture one network
- Use for cracking
- Return to Handshake tab
- Select different network
- Repeat

### Export Capture Files
- Captured files stored as PCAP format
- Can be used with external tools (Wireshark, tshark)
- Files deleted after session (can be preserved)

### Integration with Cracking
```
Capture Handshake (5 min)
        ↓
Detect PMKID (optional)
        ↓
Use for Cracking
        ↓
Select Method (Aircrack-ng/Hashcat/John)
        ↓
Choose Wordlist
        ↓
Start Cracking Job
        ↓
Monitor Progress
        ↓
Password Found ✓
```

## Performance Tips

### Faster Handshake Detection
1. **Position 1**: Connect a phone/laptop first
2. **Then start capture**: Handshake appears immediately
3. **Monitor**: Signal bars show connection activity

### Efficient Scanning
1. Start with short duration (30s)
2. If no handshake, try longer (60s+)
3. Most handshakes captured in first 30 seconds

### Resource Management
- Don't run multiple captures simultaneously
- Close browser tabs not in use
- Use simulation mode for testing UI (`SIMULATION_MODE=True`)

## API Reference

For developers integrating handshake capture:

```javascript
// Start capture
POST /api/handshake/capture/start
{
  "network": {...},
  "duration": 60
}

// Check status
GET /api/handshake/capture/status/{captureId}

// List active
GET /api/handshake/capture/list

// Cancel
POST /api/handshake/capture/cancel/{captureId}

// Get interfaces
GET /api/handshake/interfaces
```

## FAQ

**Q: What's a WPA handshake?**
A: A 4-way authentication exchange between device and WiFi. Needed to crack WPA passwords.

**Q: Can I capture without clients connected?**
A: Handshakes occur when clients connect. You need active connection attempts during capture.

**Q: What file formats are supported?**
A: PCAP (native), CAP, PCAPNG - all compatible with cracking tools.

**Q: How long does cracking take?**
A: Depends on password length and wordlist size. Usually 1 minute to 1 hour.

**Q: Can I use my own capture files?**
A: Yes, but they must be PCAP/CAP format with valid 4-way handshakes.

**Q: Is this legal to use?**
A: Only on networks you own or have written permission to test. Unauthorized network access is illegal.

---

**For Support**: Check the main NetShield documentation in README.md
**Need Help**: Review CRACKING_GUIDE.md for related features
