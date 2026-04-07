# 🚀 NetShield Cracking Features - Getting Started

Welcome! The NetShield cracking features are **fully implemented and ready to use**.

## ⚡ 30-Second Quick Start

```bash
# Terminal 1: Start Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
SIMULATION_MODE=true python main.py

# Terminal 2: Start Frontend
cd frontend
npm install
npm run dev

# Open browser: http://localhost:5173
```

That's it! You'll see the Cracking panel ready to use.

---

## 📚 What's Been Implemented

### ✅ Backend Service
- Complete cracking service with job management
- Support for Aircrack-ng, Hashcat, and John the Ripper
- Background job execution
- Multi-platform support (Linux/Windows/macOS)
- GPU acceleration support

### ✅ REST API (9 Endpoints)
- GET `/api/cracking/status` - Check available tools
- GET `/api/cracking/wordlists` - List wordlists
- GET `/api/cracking/methods` - List methods
- POST `/api/cracking/start` - Start cracking job
- GET `/api/cracking/job/{id}` - Get job status  
- GET `/api/cracking/jobs` - List all jobs
- POST `/api/cracking/job/{id}/pause` - Pause job
- POST `/api/cracking/job/{id}/cancel` - Cancel job
- GET `/api/cracking/handshake-capture-guide` - Get guide

### ✅ Frontend Component  
- Real-time job monitoring (2-second updates)
- Method selection dropdown
- Wordlist selection
- GPU toggle option
- Pause/Cancel controls
- Progress tracking
- Password display (when found)

---

## 🔧 Configuration

### Development (No tools needed)
```bash
# .env or environment variable
SIMULATION_MODE=true  # Simulates cracking for testing
```

### Production (Tools required)
```bash
# Install tools
sudo apt-get install aircrack-ng hashcat

# Then run with real mode
SIMULATION_MODE=false python main.py
```

---

## 🧪 Testing

### Run All Tests
```bash
# Make sure backend is running first
python test_cracking_api.py
```

This will verify:
- ✅ API endpoints responding
- ✅ Job creation working
- ✅ Job status tracking
- ✅ Pause/cancel functionality
- ✅ Error handling

### Manual Testing
1. Open http://localhost:5173
2. Go to "Cracking" panel
3. Select a network (or use demo BSSID)
4. Choose method: "aircrack-ng"
5. Choose wordlist: "academic" (fastest for testing)
6. Click "Start Cracking"
7. Watch progress update in real-time

---

## 📖 Documentation

Start with **any** of these based on your needs:

### 🎯 Quick Start
- [CRACKING_QUICK_REFERENCE.md](CRACKING_QUICK_REFERENCE.md) - 2-min overview

### 📚 Complete Guides
- [CRACKING_GUIDE.md](CRACKING_GUIDE.md) - Full documentation with examples
- [CRACKING_INTEGRATION_GUIDE.md](CRACKING_INTEGRATION_GUIDE.md) - Integration & setup
- [CRACKING_IMPLEMENTATION_VERIFICATION.md](CRACKING_IMPLEMENTATION_VERIFICATION.md) - Verification checklist

### ✅ Implementation Status
- [CRACKING_IMPLEMENTATION_COMPLETE.md](CRACKING_IMPLEMENTATION_COMPLETE.md) - What's been done

### 🧪 Testing Tools
- [test_cracking_api.py](test_cracking_api.py) - API test suite (run it!)
- [validate_cracking_setup.sh](validate_cracking_setup.sh) - Validate setup

---

## 🎯 Common Workflows

### Workflow 1: Quick Test
```bash
# 1. Start backend in simulation mode
SIMULATION_MODE=true python main.py

# 2. Run tests
python test_cracking_api.py

# Expected: All tests pass ✅
```

### Workflow 2: Browser Testing
```bash
# 1. Backend
SIMULATION_MODE=true python main.py

# 2. Frontend (separate terminal)
npm run dev

# 3. Open http://localhost:5173
# 4. Go to Cracking panel and create a job
```

### Workflow 3: Real Tool Testing
```bash
# 1. Install tools
sudo apt-get install aircrack-ng

# 2. Run backend in real mode
SIMULATION_MODE=false python main.py

# 3. Start frontend
npm run dev

# 4. Create cracking jobs with real tools
```

---

## 🔍 API Quick Reference

### Start a Job
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
curl http://localhost:8000/api/cracking/job/{job_id}
```

### List All Jobs
```bash
curl http://localhost:8000/api/cracking/jobs
```

---

## ⚙️ Supported Cracking Methods

| Method | Speed | GPU | Platform | Best For |
|--------|-------|-----|----------|----------|
| **Aircrack-ng** | 🐢 Slow | ❌ | Linux/macOS | Labs |
| **Hashcat** | 🚀 Very Fast | ✅ | All | Production |
| **John** | 🐇 Fast | ❌ | All | Validation |

---

## 📊 Wordlists Available

| Wordlist | Size | Speed | Use |
|----------|------|-------|-----|
| **Common** | 1,200 | ⚡ Fast | Quick tests |
| **Academic** | 5,000 | 🚀 Normal | Labs (recommended) |
| **RockYou** | 14M+ | 🐢 Slow | Full cracking |

---

## 🐛 Troubleshooting

### "Connection refused"
```bash
# Make sure backend is running
SIMULATION_MODE=true python main.py
```

### "Tools not found" 
```bash
# Install tools
sudo apt-get install aircrack-ng hashcat

# Or use simulation mode
SIMULATION_MODE=true python main.py
```

### "Jobs not updating"
- Check browser console for errors (F12)
- Ensure backend is responding: `curl http://localhost:8000/api/cracking/status`
- Try restarting both services

### More Help
Check [CRACKING_INTEGRATION_GUIDE.md](CRACKING_INTEGRATION_GUIDE.md) for detailed troubleshooting.

---

## 📁 Key Files

```
Backend:
├── app/services/cracking.py      ← Service implementation
├── app/api/cracking.py            ← API endpoints
└── main.py                        ← FastAPI app

Frontend:
├── src/components/CrackingPanel.jsx  ← UI component
├── src/api.js                       ← API client
└── src/App.jsx                      ← Main app

Testing:
├── test_cracking_api.py            ← API tests
└── validate_cracking_setup.sh      ← Setup check

Docs:
├── CRACKING_GUIDE.md               ← Full guide
├── CRACKING_QUICK_REFERENCE.md     ← Quick ref
├── CRACKING_INTEGRATION_GUIDE.md   ← Integration
└── CRACKING_IMPLEMENTATION_COMPLETE.md ← Status
```

---

## 🚀 Next Steps

### Step 1: Quick Verification (5 min)
```bash
cd backend && python test_cracking_api.py
```

### Step 2: Browser Test (5 min)
```bash
# Start both services and open http://localhost:5173
```

### Step 3: Real Tool Setup (5 min)
```bash
sudo apt-get install aircrack-ng
SIMULATION_MODE=false python main.py
```

### Step 4: Production Deployment (varies)
- See [CRACKING_INTEGRATION_GUIDE.md](CRACKING_INTEGRATION_GUIDE.md) for Docker setup

---

## ✨ Features Highlight

✅ **Multi-method** support  
✅ **Real-time monitoring** (2-second polling)  
✅ **Background execution** (non-blocking)  
✅ **Job management** (pause, cancel)  
✅ **GPU acceleration** support  
✅ **Simulation mode** for testing  
✅ **Cross-platform** (Linux/Windows/macOS)  
✅ **Professional UI** with real-time updates  

---

## 📞 Need Help?

1. **Quick questions?** → [CRACKING_QUICK_REFERENCE.md](CRACKING_QUICK_REFERENCE.md)
2. **Setup issues?** → [CRACKING_INTEGRATION_GUIDE.md](CRACKING_INTEGRATION_GUIDE.md)
3. **API details?** → [CRACKING_GUIDE.md](CRACKING_GUIDE.md)
4. **Testing?** → Run `python test_cracking_api.py`

---

## 🎓 Example: Complete Workflow

```python
# Python example using the API
import requests
import time

BASE_URL = "http://localhost:8000"
NETWORK = "AA:BB:CC:DD:EE:FF"

# 1. Start cracking job
response = requests.post(f"{BASE_URL}/api/cracking/start", json={
    "network_bssid": NETWORK,
    "method": "aircrack-ng",
    "wordlist": "academic",
    "gpu_enabled": False
})

job_id = response.json()["job_id"]
print(f"Started job: {job_id}")

# 2. Monitor progress
while True:
    status = requests.get(f"{BASE_URL}/api/cracking/job/{job_id}").json()
    print(f"Progress: {status['progress']}% - {status['status']}")
    
    if status['status'] == 'completed':
        if status.get('password_found'):
            print(f"✅ Password found: {status['password_found']}")
        else:
            print(f"❌ No password found")
        break
    
    time.sleep(2)
```

---

## 📋 Checklist Before Going Live

- [ ] Backend starts without errors
- [ ] Frontend loads at http://localhost:5173  
- [ ] Cracking panel visible and functional
- [ ] Can start a test job
- [ ] Job updates in real-time
- [ ] Test suite passes (`test_cracking_api.py`)
- [ ] Tools installed (optional, for real mode)
- [ ] Documentation reviewed

---

**Status: ✅ READY TO USE**

The NetShield cracking features are fully implemented, tested, and documented. Start with the 30-second quick start above and reference the documentation as needed.

Happy cracking! 🔓

---

**Version:** 1.0  
**Last Updated:** 2024  
**Implementation Status:** ✅ 100% Complete
