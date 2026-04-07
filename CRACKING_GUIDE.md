# NetShield - Advanced Cracking Features

## Overview

NetShield now includes advanced password cracking capabilities for academic Wi-Fi security testing. This documentation covers the cracking service, available tools, and usage patterns for multi-system deployment.

## Table of Contents

1. [Cracking Methods](#cracking-methods)
2. [API Endpoints](#api-endpoints)
3. [Setup by Platform](#setup-by-platform)
4. [Workflow Examples](#workflow-examples)
5. [Academic Use Cases](#academic-use-cases)
6. [Safety & Ethics](#safety--ethics)

---

## Cracking Methods

### 1. Aircrack-ng
**Best for**: WEP/WPA/WPA2 academic labs, Linux environments  
**Speed**: CPU-based (slow but reliable)  
**Platforms**: Linux, macOS, WSL2 on Windows  
**Requirements**: `aircrack-ng`, `airodump-ng`, libpcap

```bash
# Installation (Ubuntu/Debian)
sudo apt-get install aircrack-ng

# Usage: WPA2 cracking from handshake
aircrack-ng -w rockyou.txt -b AA:BB:CC:DD:EE:FF capture.cap
```

**Pros**:
- Well-documented for academic use
- Works with pre-captured handshake files (.cap, .pcap)
- Low resource requirements

**Cons**:
- Very slow (hours to days depending on password)
- CPU-intensive
- Not available natively on Windows

---

### 2. Hashcat
**Best for**: High-speed GPU cracking, WPA2/WPA3, production pentests  
**Speed**: GPU-accelerated (100-1000x faster than CPU)  
**Platforms**: Linux, Windows, macOS  
**Requirements**: `hashcat`, NVIDIA/AMD GPU drivers (optional), CUDA/OpenCL

```bash
# Installation (Ubuntu with NVIDIA GPU)
sudo apt-get install hashcat nvidia-driver-525

# Usage: WPA2 cracking with GPU
hashcat -m 2500 -w 3 --potfile-disable hash.hccapx rockyou.txt

# WPA3 cracking
hashcat -m 16800 -w 3 --potfile-disable hash.hccapx rockyou.txt
```

**Pros**:
- Extremely fast with GPU
- Cross-platform support
- Supports WPA3 (mode 16800)
- Can use rules and masks

**Cons**:
- Requires GPU (NVIDIA CUDA / AMD OpenCL)
- Steeper learning curve
- File format conversion needed (.cap → .hccapx)

---

### 3. John the Ripper
**Best for**: Cross-platform cracking, validation, hybrid attacks  
**Speed**: Moderate (CPU-based)  
**Platforms**: Linux, Windows, macOS  
**Requirements**: `john`

```bash
# Installation
sudo apt-get install john

# Usage: WPA2 handshake cracking
john --format=wpapsk --wordlist=rockyou.txt hash.hccapx
```

---

## API Endpoints

### 1. Get Cracking Status
```http
GET /api/cracking/status
```
Returns available tools and platform information.

**Response**:
```json
{
  "available_tools": {
    "aircrack_ng": {
      "available": true,
      "description": "Craquage de clés WEP/WPA/WPA2 par force brute",
      "platforms": ["linux", "macos"]
    },
    "hashcat": {
      "available": true,
      "gpu_support": true,
      "description": "Craquage GPU ultra-rapide"
    }
  },
  "platform": "linux"
}
```

---

### 2. List Available Wordlists
```http
GET /api/cracking/wordlists
```

**Response**:
```json
{
  "common": {
    "description": "1200 mots de passe courants",
    "size": 1200,
    "suitable_for": "Tests rapides, académique"
  },
  "rockyou": {
    "description": "14+ millions de mots de passe",
    "size": 14344391,
    "suitable_for": "Craquage complet, Pentest réel"
  },
  "academic": {
    "description": "5000 mots pour exercices académiques",
    "size": 5000,
    "suitable_for": "Laboratoire, démonstration"
  }
}
```

---

### 3. Start Cracking Job
```http
POST /api/cracking/start
Content-Type: application/json

{
  "network_bssid": "AA:BB:CC:DD:EE:FF",
  "method": "hashcat",
  "wordlist": "common",
  "gpu_enabled": true
}
```

**Response**:
```json
{
  "job_id": "a7f2c9e1",
  "network_bssid": "AA:BB:CC:DD:EE:FF",
  "network_ssid": "Network_AABBCCDDEE",
  "method": "hashcat",
  "status": "pending",
  "progress": 0,
  "message": "Travail de craquage lancé"
}
```

---

### 4. Get Job Status
```http
GET /api/cracking/job/a7f2c9e1
```

**Response** (in progress):
```json
{
  "job_id": "a7f2c9e1",
  "network_bssid": "AA:BB:CC:DD:EE:FF",
  "status": "running",
  "progress": 45,
  "attempts": 6355384,
  "wordlist_size": 14344391,
  "wordlist_name": "rockyou",
  "gpu_enabled": true
}
```

**Response** (completed):
```json
{
  "job_id": "a7f2c9e1",
  "network_bssid": "AA:BB:CC:DD:EE:FF",
  "status": "completed",
  "progress": 100,
  "password_found": "SecurePassword123!",
  "attempts": 14344391,
  "start_time": "2026-04-07T10:30:00",
  "end_time": "2026-04-07T10:45:32"
}
```

---

### 5. List All Jobs
```http
GET /api/cracking/jobs
```

**Response**:
```json
{
  "total": 3,
  "jobs": [
    {
      "job_id": "a7f2c9e1",
      "network_bssid": "AA:BB:CC:DD:EE:FF",
      "status": "running",
      "progress": 45,
      "method": "hashcat"
    },
    {
      "job_id": "b8g3d0f2",
      "network_bssid": "11:22:33:44:55:66",
      "status": "completed",
      "progress": 100,
      "password_found": "Password@123",
      "method": "aircrack-ng"
    }
  ]
}
```

---

### 6. Get Handshake Capture Guide
```http
GET /api/cracking/handshake-capture-guide
```

Returns step-by-step instructions for capturing WPA/WPA2 handshakes on different platforms.

---

## Setup by Platform

### Linux (Native - Recommended)
```bash
# Install cracking tools
sudo apt-get update
sudo apt-get install aircrack-ng hashcat

# Verify GPU support (NVIDIA)
nvidia-smi
hashcat -I

# Start NetShield backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### macOS
```bash
# Install via Homebrew
brew install aircrack-ng hashcat

# GPU support (limited on macOS - use Metal)
hashcat -D 2  # Metal support

# Run backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Windows + WSL2 (Recommended for Windows)
```powershell
# Install WSL2 with Ubuntu
wsl --install -d Ubuntu-22.04

# Inside WSL2 terminal
sudo apt-get update
sudo apt-get install aircrack-ng hashcat

# GPU pass-through setup (for NVIDIA)
# Follow: https://docs.nvidia.com/cuda/wsl-user-guide/

# Run backend from WSL2
cd /mnt/c/Users/YourUser/NetShield/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Workflow Examples

### Example 1: Quick Test with Common Wordlist (Simulation Mode)

```bash
# Start backend (simulation mode)
SIMULATION_MODE=true python main.py

# Scan networks
curl http://localhost:8000/api/scan/networks

# Start cracking job
curl -X POST http://localhost:8000/api/cracking/start \
  -H "Content-Type: application/json" \
  -d '{
    "network_bssid": "AA:BB:CC:DD:EE:FF",
    "method": "aircrack-ng",
    "wordlist": "common",
    "gpu_enabled": false
  }'

# Check status
curl http://localhost:8000/api/cracking/job/job_id
```

### Example 2: Multi-Machine Deployment

**Machine 1 (Windows Admin)**: Handshake capture + conversion
```powershell
# From WSL2 terminal
airodump-ng wlan0mon -c 6 -w capture -b AA:BB:CC:DD:EE:FF
# Waits for 4-way handshake
aircrack-ng -J capture.hccapx capture.cap  # Convert to hashcat format
```

**Machine 2 (Linux with GPU)**: Real-time cracking
```bash
# Copy capture.hccapx from Machine 1
scp user@machine1:/tmp/capture.hccapx .

# Run cracking
hashcat -m 2500 -w 3 --potfile-disable capture.hccapx rockyou.txt

# Monitor progress
watch -n 1 'hashcat -m 2500 status'
```

### Example 3: Academic Lab Exercise

```python
# Lab: Crack 5 WPA2 networks with different password strengths
# File: academic_lab.py

import requests
import time

BASE_URL = "http://localhost:8000/api"
NETWORKS_TO_CRACK = [
    {"bssid": "AA:BB:CC:DD:EE:01", "ssid": "Easy_Pass"},
    {"bssid": "AA:BB:CC:DD:EE:02", "ssid": "Medium_Pass"},
    {"bssid": "AA:BB:CC:DD:EE:03", "ssid": "Hard_Pass"},
    {"bssid": "AA:BB:CC:DD:EE:04", "ssid": "Very_Hard"},
    {"bssid": "AA:BB:CC:DD:EE:05", "ssid": "Impossible_WPA3"},
]

# Start cracking jobs
jobs = []
for network in NETWORKS_TO_CRACK:
    if "WPA3" not in network["ssid"]:
        response = requests.post(f"{BASE_URL}/cracking/start", json={
            "network_bssid": network["bssid"],
            "method": "aircrack-ng",
            "wordlist": "academic",
            "gpu_enabled": False
        })
        job_id = response.json()["job_id"]
        jobs.append((job_id, network))

# Monitor progress
while jobs:
    for job_id, network in jobs[:]:
        response = requests.get(f"{BASE_URL}/cracking/job/{job_id}")
        job = response.json()
        
        print(f"[{network['ssid']}] Progress: {job['progress']}% - Status: {job['status']}")
        
        if job['status'] == 'completed':
            if job.get('password_found'):
                print(f"  ✓ Password: {job['password_found']}")
            jobs.remove((job_id, network))
    
    if jobs:
        time.sleep(5)
```

---

## Academic Use Cases

### 1. Security Fundamentals (Beginner)
- Understand WEP encryption weaknesses
- Learn handshake capture concept
- Run basic dictionary attacks on WEP

**Tools**: Aircrack-ng  
**Wordlist**: common (1200 passwords)  
**Time**: 30 minutes to 2 hours

### 2. Applied Cryptography (Intermediate)
- Study WPA2-PSK vs Pre-Shared Key concepts
- Capture live handshakes
- Analyze computational complexity of cracking

**Tools**: Hashcat  
**Wordlist**: academic (5000 passwords)  
**Time**: 2-4 hours

### 3. Advanced Network Security (Advanced)
- Cross-platform tool deployment
- GPU acceleration vs CPU tradeoffs
- WPA3 security architecture analysis
- PMKID attack vectors

**Tools**: Hashcat + Aircrack-ng  
**Wordlist**: rockyou.txt + rules  
**Time**: Full lab session + homework

### 4. Capstone Project
- Multi-network audit pipeline
- Report generation with findings
- Remediation recommendations

**Deliverables**:
- Network audit report (PDF)
- Cracking methodology documentation
- Security recommendations

---

## Safety & Ethics

### Legal Requirements
✅ **Authorized Use Only**:
- Your own networks or authorized lab environments
- Written permission from network owner
- Academic institution approved settings

❌ **Prohibited**:
- Unauthorized network testing
- Targeting third-party networks without consent
- Violation of local/national laws

### Best Practices
1. **Isolation**: Test only in controlled lab environments
2. **Documentation**: Log all testing with timestamp and authorization
3. **Confidentiality**: Store captured data securely
4. **Destruction**: Delete captured handshakes after analysis
5. **Ethics**: Understand responsible disclosure

### University Approval
```
NetShield is designed for academic courses on:
- Computer Network Security
- Wireless Security
- Applied Cryptography
- Cybersecurity Fundamentals

Student Usage Agreement:
- I will only test authorized networks
- I understand the legal implications
- I will follow institutional guidelines
- I take full responsibility for my actions
```

---

## Troubleshooting

### Hashcat Performance Issues
```bash
# Check GPU detection
hashcat -I

# Use benchmark to verify
hashcat -b -m 2500

# If slow: verify CUDA drivers
nvidia-smi

# For AMD GPU
rocm-smi
```

### Aircrack-ng Handshake Issues
```bash
# Verify handshake capture
aircrack-ng capture.cap
# Should show "WPA (1 entry)" or similar

# Convert for hashcat
aircrack-ng -J capture.hccapx capture.cap

# Test wordlist syntax
cat rockyou.txt | head -10
```

### WSL2 USB Adapter Not Detected
```bash
# List devices in WSL2
lsusb
usbipd list

# Attach USB device
usbipd attach --busid=2-2
```

---

## References

- [Aircrack-ng Documentation](https://www.aircrack-ng.org/doku.php)
- [Hashcat Wiki](https://hashcat.net/wiki/)
- [WPA3 Security Analysis](https://w1.fi/wpa3/)
- [802.11 Protocol Overview](https://en.wikipedia.org/wiki/IEEE_802.11)
- [NIST Wi-Fi Security Guidelines](https://nvlpubs.nist.gov/)

---

## Support

For issues or questions:
1. Check the [main README](README.md)
2. Review [API_TESTS.md](API_TESTS.md) for endpoint testing
3. Consult course materials and instructor resources
4. Report bugs to the project repository

**Last Updated**: April 7, 2026  
**Version**: 1.0.0 - Advanced Cracking Features
