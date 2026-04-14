# Quick Start Testing Guide

## ✅ Systems Running

- **Backend**: http://127.0.0.1:8000 (Terminal ID: 099d4077-8205-4b64-ab4a-ecb63766791d)
- **Frontend**: http://localhost:3000 (Terminal ID: 98b7ee19-dcac-4520-851b-61ab8577d6a7)
- **Browser**: Open to http://localhost:3000

---

## 🎯 What to Test

### Test 1: View Dashboard
1. Look at the frontend (should show WiFi networks)
2. Database is empty so no stored captures yet ✓

### Test 2: Check API Working
Frontend should already be calling:
- `/api/stored/statistics` - returns `{ total_captures: 0, ... }`  
- `/api/stored/handshakes` - returns `[]`

Both return successfully ✓

### Test 3: Simulate Handshake Capture
1. In frontend, select a WiFi network
2. Click "Capture Handshake"
3. In backend terminal, should see capture progress
4. When complete → auto-saved to database

### Test 4: View Stored Captures
1. Go to **CrackingPanel**
2. Click **"💾 Captures"** tab
3. See list of stored handshakes
4. Statistics show count

### Test 5: Select & Crack
1. Click handshake in list
2. Auto-switches to **"Lancer"** tab ✓
3. Handshake details shown ✓
4. Configure cracking (method, wordlist, GPU)
5. Click "Lancer le Craquage"
6. Job appears in **"◇ Travaux"** tab

### Test 6: Verify Database Storage
Query database:
```powershell
sqlite3 .\backend\netshield.db "SELECT COUNT(*) FROM handshake_captures;"
sqlite3 .\backend\netshield.db "SELECT * FROM handshake_captures LIMIT 1;"
```

---

## ✅ What's Already Working

✅ Backend fully initialized  
✅ Database schema created  
✅ API endpoints responding  
✅ Frontend loaded  
✅ React components ready  
✅ All imports working  
✅ No compilation errors  

---

## 📋 Files Modified This Session

### Backend
- `backend/requirements.txt` - Added sqlalchemy
- `backend/main.py` - Fixed database initialization

### Created (Already done)
- `backend/app/models/database.py` - ORM models
- `backend/app/services/database_service.py` - CRUD service
- `backend/app/api/stored_handshakes.py` - API routes
- `frontend/src/components/StoredHandshakesPanel.jsx` - React component

### Modified (Already done)
- `backend/app/api/cracking.py` - Add handshake_id parameter
- `backend/app/services/handshake_capture.py` - Save to DB
- `frontend/src/components/CrackingPanel.jsx` - Add stored tab
- `frontend/src/api.js` - Add API methods

---

## 🔍 How to Verify Complete Integration

### Via Browser Console
```javascript
// Check if APIs exist
console.log(wifiAPI.getStoredHandshakes)     // Should not be undefined
console.log(wifiAPI.startCrackingJob)        // Should work with handshake_id

// Fetch statistics
fetch('http://127.0.0.1:8000/api/stored/statistics')
  .then(r => r.json())
  .then(d => console.log(d))
  // Should show all zeros initially
```

### Via Backend Logs
Watch terminal - you should see:
```
INFO: Database initialized successfully
INFO: Started server process [17324]
INFO: Application startup complete
```

### Via Database
After first capture, check database:
```powershell
sqlite3 .\backend\netshield.db
.tables
SELECT COUNT(*) as total_captures FROM handshake_captures;
```

---

## 🚀 Next Actions for User

1. **Keep systems running** (both terminals open)
2. **Open browser** to http://localhost:3000 (already done ✓)
3. **Interact with frontend** - try capturing or selecting networks
4. **Click "💾 Captures" tab** in CrackingPanel
5. **Test stored handshake workflow**
6. **Check browser console** for any errors
7. **Check backend terminal** for log outputs

---

## 📊 Expected Behavior

### First Load
- Statistics show all zeros (no captures yet)
- "💾 Captures" tab empty
- API responds 200 OK

### After Capture
- New handshake appears in list
- Statistics increment
- Can select and start cracking

### After Cracking
- Job tracked in database
- Results appear in statistics
- Can query cracking history

---

## 🐛 Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'sqlalchemy'`
- Solution: Already fixed! `pip install sqlalchemy` done

**Issue**: Database connection error
- Solution: Check `backend/netshield.db` exists after first request
- If missing: Restart backend (`Ctrl+C` then `python main.py`)

**Issue**: Frontend not loading
- Solution: Check terminal - Vite should show "ready"
- Ctrl+C and run `npm run dev` again

**Issue**: API not responding
- Solution: Check backend terminal for errors
- Verify running on `http://127.0.0.1:8000`

---

## ✨ Key Features Enabled

1. **Persistent Storage** - Captures saved to SQLite database
2. **Browser UI** - New "💾 Captures" tab to browse captured handshakes
3. **Easy Reuse** - Select stored capture → auto-configure for cracking
4. **Statistics** - Track total captures, success rate, password findings
5. **History** - Each capture stores all cracking attempts and results
6. **Multi-Network** - Track captures across multiple WiFi networks

---

## 📱 System Architecture

```
┌─────────────────────────────────────┐
│  Browser (localhost:3000)           │
│  ├─ Dashboard                       │
│  ├─ CrackingPanel                   │
│  │  ├─ jobs tab                     │
│  │  ├─ workflow tab                 │
│  │  ├─ strategies tab               │
│  │  ├─ 💾 Captures tab (NEW!)      │
│  │  └─ Lancer tab                   │
│  └─ StoredHandshakesPanel (NEW!)   │
└─────────────────────────────────────┘
         ↓ (HTTP requests)
┌─────────────────────────────────────┐
│  Backend (localhost:8000)           │
│  ├─ /api/cracking/start             │
│  ├─ /api/stored/* (7 endpoints)     │
│  ├─ /api/handshake/capture/start    │
│  └─ DatabaseService                 │
└─────────────────────────────────────┘
         ↓ (SQLAlchemy ORM)
┌─────────────────────────────────────┐
│  SQLite Database                    │
│  ├─ handshake_captures              │
│  ├─ cracking_attempts               │
│  ├─ scan_results                    │
│  └─ ...                             │
└─────────────────────────────────────┘
```

---

## ⏱️ Estimated Testing Time

- **Quick check**: 5 minutes (verify tabs, API endpoints)
- **Full workflow**: 15-20 minutes (capture → store → select → crack)
- **Deep testing**: 30+ minutes (multi-network, history, statistics)

---

## 📝 Test Checklist

- [ ] Frontend loads at localhost:3000
- [ ] CrackingPanel has "💾 Captures" tab
- [ ] StoredHandshakesPanel renders with statistics
- [ ] Can select a network
- [ ] Can start handshake capture
- [ ] Capture appears in "💾 Captures" tab
- [ ] Statistics update after capture
- [ ] Can click handshake to select it
- [ ] Auto-switches to "Lancer" tab
- [ ] Selected handshake details shown
- [ ] Can configure cracking options
- [ ] Can start cracking job with stored handshake
- [ ] Job appears in "◇ Travaux" tab
- [ ] Database tables created successfully
- [ ] API endpoints all responding

---

Ready to test! The systems are fully initialized and waiting for user interaction. 🎯
