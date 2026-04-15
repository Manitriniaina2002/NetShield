# Deploy to Fly.io - Step by Step

## Prerequisites
- Fly.io account: https://fly.io/auth/signup
- GitHub repo: Already pushed ✅

## Quick Deploy (Copy & Paste Commands)

### Option 1: Deploy via Fly.io Dashboard (Easiest - No CLI needed)

1. Go to https://fly.io/dashboard
2. Click **+ New App**
3. Select **Create New App**
4. Choose **Deploy from Source Code**
5. Authorize GitHub
6. Select **NetShield** repository
7. Set App Name: `netshield-backend`
8. Choose Region (closest to you)
9. Click **Deploy**

**Done!** Fly.io will automatically read `fly.toml` and deploy.

---

### Option 2: Deploy via CLI Commands

Install Fly CLI (choose one):

**Via Chocolatey (Windows):**
```powershell
choco install flyctl
```

**Via Direct Download:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

Then deploy:
```powershell
cd c:\Users\MaZik\NetShield

# Login to Fly.io
flyctl auth login

# Deploy backend
flyctl launch --name netshield-backend

# Or if already configured:
flyctl deploy

# View logs
flyctl logs
```

---

## After Deployment

1. **Get Backend URL:**
   ```powershell
   flyctl status
   ```
   Look for hostname like: `netshield-backend.fly.dev`

2. **Deploy Frontend to Vercel:**
   - Go to https://vercel.com/new
   - Import GitHub repo: `NetShield`
   - Root Directory: `frontend`
   - Set Environment Variable:
     ```
     VITE_API_BASE_URL=https://netshield-backend.fly.dev
     ```
   - Click Deploy

3. **Test Connection:**
   ```bash
   # Check backend health
   curl https://netshield-backend.fly.dev/api/health
   
   # Should return: {"status": "healthy"}
   ```

---

## Troubleshooting

**Backend won't start?**
```powershell
flyctl logs
```

**Environment variables not set?**
```powershell
flyctl secrets set SIMULATION_MODE=false DEBUG=false LOG_LEVEL=INFO
```

**Redeploy after changes:**
```powershell
git push
flyctl deploy
```

---

## Links

- Backend: `https://netshield-backend.fly.dev`
- Backend API: `https://netshield-backend.fly.dev/api`
- Health Check: `https://netshield-backend.fly.dev/api/health`
- Frontend: Will be at `https://[your-project].vercel.app`
