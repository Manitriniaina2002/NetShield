# NetShield Cracking Features - Quick Reference Card

## 🎯 What's Implemented

### Backend Service (`app/services/cracking.py`)
```python
CrackingService
├── create_job()                    # Create new cracking job
├── launch_cracking_job_background() # Start job in background
├── get_job_status()                # Get current job status
├── list_jobs()                     # List all active jobs
├── pause_job()                     # Pause a running job
├── cancel_job()                    # Cancel a job
├── start_aircrack_job()            # Execute aircrack-ng
├── start_hashcat_job()             # Execute hashcat
├── generate_common_wordlist()      # Generate common passwords
└── generate_academic_wordlist()    # Generate academic wordlist
```

### API Endpoints (`app/api/cracking.py`)
```
GET  /api/cracking/status                  → Get available tools
GET  /api/cracking/wordlists               → List wordlists
GET  /api/cracking/methods                 → List cracking methods
POST /api/cracking/start                   → Start new job
GET  /api/cracking/job/{job_id}            → Get job status
GET  /api/cracking/jobs                    → List all jobs
POST /api/cracking/job/{job_id}/pause      → Pause job
POST /api/cracking/job/{job_id}/cancel     → Cancel job
GET  /api/cracking/handshake-capture-guide → Capture instructions
```

### Frontend Component (`CrackingPanel.jsx`)
```javascript
CrackingPanel
├── Job Creation
│   ├── Network selection
│   ├── Method selection
│   ├── Wordlist selection
│   └── GPU toggle
├── Job Monitoring
│   ├── Real-time polling (2s interval)
│   ├── Progress display
│   ├── Status updates
│   └── Password display (if found)
└── Job Controls
    ├── Pause button
    └── Cancel button
```

---

## 🚀 Quick Start (5 minutes)

### Development Mode (No tools needed)
```bash
# Terminal 1: Backend
cd backend
SIMULATION_MODE=true python main.py

# Terminal 2: Frontend  
cd frontend
npm run dev

# Access: http://localhost:5173
```

### Production Mode (Tools required)
```bash
# Install tools
sudo apt-get install aircrack-ng hashcat

# Terminal 1: Backend
cd backend
SIMULATION_MODE=false python main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

## 📊 Cracking Methods

| Method | Speed | GPU Support | Platforms | Best For |
|--------|-------|-------------|-----------|----------|
| **Aircrack-ng** | Slow | No | Linux/macOS | Academic labs |
| **Hashcat** | Very Fast | Yes | Linux/Windows/macOS | Production |
| **John** | Fast | No | All | Validation |

---

## 📝 Wordlists

| Wordlist | Size | Speed | Use Case |
|----------|------|-------|----------|
| **Common** | 1,200 | Very Fast | Quick tests |
| **Academic** | 5,000 | Fast | Labs/demos |
| **RockYou** | 14M+ | Slow | Full cracking |

---

## 🧪 API Examples

### Start Job
```bash
curl -X POST http://localhost:8000/api/cracking/start \
  -H "Content-Type: application/json" \
  -d '{
    "network_bssid": "AA:BB:CC:DD:EE:FF",
    "method": "aircrack-ng",
    "wordlist": "academic",
    "gpu_enabled": false
  }'
```

### Check Status
```bash
curl http://localhost:8000/api/cracking/job/job_id_here
```

### Cancel Job
```bash
curl -X POST http://localhost:8000/api/cracking/job/job_id_here/cancel
```

---

## 📋 Job Lifecycle

```
1. Create Job
   ↓
2. Launch in Background
   ↓
3. Monitor Progress (polling)
   ↓
4a. Complete ✓   OR   4b. Pause ⏸  OR  4c. Cancel ✗
   ↓
5. Cleanup
```

---

## 🔍 Testing

### Run All Tests
```bash
python test_cracking_api.py
```

### Manual Test in Browser
1. Open http://localhost:5173
2. Click "Cracking" panel
3. Select network
4. Click "Start Cracking"
5. Watch progress update in real-time

---

## ⚙️ Configuration

### Backend .env
```env
SIMULATION_MODE=true          # true for testing, false for real tools
DEBUG_MODE=true               # Enable debug logging
LOG_LEVEL=DEBUG               # DEBUG, INFO, WARNING, ERROR
CORS_ORIGINS=["*"]           # Allow all origins
```

### Frontend src/api.js
```javascript
const API_BASE_URL = 'http://localhost:8000/api'
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Start backend: `python main.py` |
| "Tools not found" | Install: `sudo apt-get install aircrack-ng` |
| "Jobs not updating" | Check polling interval in CrackingPanel.jsx |
| "CORS error" | Verify CORS_ORIGINS includes frontend URL |
| "Real mode failing" | Set SIMULATION_MODE=true for testing |

---

## 📁 File Structure

```
NetShield/
├── backend/
│   ├── app/
│   │   ├── services/cracking.py      ← Core service
│   │   ├── api/cracking.py            ← API endpoints
│   │   └── api/__init__.py            ← Router registration
│   ├── main.py                        ← FastAPI app
│   └── requirements.txt               ← Dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── CrackingPanel.jsx     ← UI component
│   │   ├── api.js                     ← API client
│   │   └── App.jsx                    ← Main component
│   └── package.json                   ← Dependencies
├── test_cracking_api.py              ← Test script
├── validate_cracking_setup.sh        ← Setup validator
├── CRACKING_GUIDE.md                 ← Full documentation
├── CRACKING_INTEGRATION_GUIDE.md     ← Integration guide
└── CRACKING_IMPLEMENTATION_VERIFICATION.md
```

---

## ✨ Features Highlight

✅ **Multi-Method Support**
- Aircrack-ng, Hashcat, John the Ripper

✅ **Real-Time Monitoring**
- 2-second polling interval
- Live progress updates
- Password display when cracked

✅ **Job Management**
- Create, pause, cancel jobs
- Multiple concurrent jobs
- Auto-cleanup of old jobs

✅ **Wordlist Support**
- Common passwords
- Academic wordlist
- RockYou dictionary
- Custom wordlist support

✅ **Cross-Platform**
- Linux (native)
- macOS (Homebrew)
- Windows (WSL2)

✅ **Simulation Mode**
- Test without real tools
- Realistic progress simulation
- Perfect for development/CI

---

## 🎓 Example Use Cases

### Academic Lab
```python
# Crack 5 networks with different difficulties
for network in networks:
    start_cracking_job(network, method='aircrack-ng', wordlist='academic')
    poll_status_until_complete()
    print(f"Password: {job.password_found}")
```

### Penetration Test  
```python
# High-speed cracking with GPU
start_cracking_job(
    network=target_network,
    method='hashcat',
    wordlist='rockyou',
    gpu_enabled=True
)
```

### CI/CD Pipeline
```bash
# Automated testing with simulation
SIMULATION_MODE=true python test_cracking_api.py
```

---

## 📞 Support Resources

| Resource | Location |
|----------|----------|
| Full Guide | [CRACKING_GUIDE.md](CRACKING_GUIDE.md) |
| Integration | [CRACKING_INTEGRATION_GUIDE.md](CRACKING_INTEGRATION_GUIDE.md) |
| Verification | [CRACKING_IMPLEMENTATION_VERIFICATION.md](CRACKING_IMPLEMENTATION_VERIFICATION.md) |
| Test Script | [test_cracking_api.py](test_cracking_api.py) |
| Validator | [validate_cracking_setup.sh](validate_cracking_setup.sh) |
| Architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |

---

## 📊 Status Summary

| Component | Status | Tests |
|-----------|--------|-------|
| Backend Service | ✅ Complete | ✅ Passing |
| API Endpoints | ✅ Complete | ✅ Passing |
| Frontend Component | ✅ Complete | ✅ Passing |
| Integration | ✅ Complete | ✅ Passing |
| Documentation | ✅ Complete | ✅ Verified |

---

**Quick Links:**
- Start Testing: `python test_cracking_api.py`
- Validate Setup: `bash validate_cracking_setup.sh`
- View Full Guide: `cat CRACKING_GUIDE.md`

---

**Version:** 1.0  
**Implementation Status:** ✅ COMPLETE  
**Last Verified:** 2024
