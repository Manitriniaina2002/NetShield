# NetShield Deployment Guide

Complete guide for deploying NetShield to production on Vercel (frontend) and Render (backend).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
3. [Backend Deployment (Render)](#backend-deployment-render)
4. [Environment Configuration](#environment-configuration)
5. [Docker Deployment (Alternative)](#docker-deployment-alternative)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts
- **GitHub Account**: For repository hosting
- **Vercel Account**: For frontend deployment (free tier available)
- **Render Account**: For backend deployment (free tier available)
- **Domain (Optional)**: Custom domain for your app

### Local Setup
```bash
# Clone repository
git clone https://github.com/yourusername/NetShield.git
cd NetShield

# Verify local setup works
npm run build  # In frontend directory
python -m pip install -r backend/requirements.txt
```

---

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend Repository

1. Ensure `frontend/vercel.json` exists (already included)
2. Update `frontend/package.json` - already configured
3. Create `.env.production` in frontend:
   ```
   VITE_API_BASE_URL=<your-backend-url>
   ```

### Step 2: Connect to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click "New Project"
3. Select your NetShield repository
4. Configure project settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 3: Set Environment Variables

In Vercel project settings → Environment Variables:

```
VITE_API_BASE_URL = https://your-render-backend.onrender.com
```

### Step 4: Deploy

- Click "Deploy"
- Vercel will automatically build and deploy
- Your frontend will be available at: `https://yourapp.vercel.app`

### Automatic Deployments

Vercel automatically deploys when you push to your main branch.

---

## Backend Deployment (Render)

### Step 1: Prepare Backend Repository

1. Ensure these files exist:
   - `backend/requirements.txt` (dependencies)
   - `render.yaml` (deployment config - already included)
   - `backend/.env.example` (reference - already included)

2. Make sure `main.py` is in the `backend/` directory

### Step 2: Connect to Render

1. Go to [render.com](https://render.com) and sign in with GitHub
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure settings:
   - **Name**: `netshield-backend`
   - **Environment**: Python
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: (leave empty or use `.`)

### Step 3: Set Environment Variables

In Render dashboard → Environment:

```
SIMULATION_MODE=false
DEBUG=false
LOG_LEVEL=INFO
CORS_ORIGINS=["https://yourapp.vercel.app","http://localhost:3000"]
COMPANY_NAME=NetShield Labs
BACKEND_PORT=$PORT
```

### Step 4: Deploy

1. Render will show deployment logs
2. Wait for "Build & Deployment Successful"
3. Your backend will be available at: `https://netshield-backend.onrender.com`

### Connect Frontend to Backend

After backend is deployed:

1. Go to Vercel project settings
2. Update environment variable:
   ```
   VITE_API_BASE_URL=https://netshield-backend.onrender.com
   ```
3. Redeploy frontend (automatic with git push)

---

## Environment Configuration

### Backend Environment Variables

Create `.env` file in `backend/` (use `.env.example` as template):

```bash
# Production settings
SIMULATION_MODE=false          # Enable real WiFi scanning
DEBUG=false                    # Disable debug mode
LOG_LEVEL=INFO                 # Logging level

# Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# CORS - Update with your frontend URL
CORS_ORIGINS=["https://yourapp.vercel.app","http://localhost:3000"]

# Reporting
COMPANY_NAME=NetShield Labs
PDF_TEMP_DIR=./temp_reports
```

### Frontend Environment Variables

Create `.env.production` in `frontend/`:

```bash
VITE_API_BASE_URL=https://netshield-backend.onrender.com
```

---

## Docker Deployment (Alternative)

### Local Docker Development

```bash
# Build images
docker-compose build

# Run services
docker-compose up

# Frontend: http://localhost:5173
# Backend: http://localhost:8000
```

### Deploy to Docker Registry

```bash
# Build backend image
docker build -t netshield-backend ./backend

# Tag for registry
docker tag netshield-backend yourdockeruser/netshield-backend:latest

# Push to Docker Hub
docker push yourdockeruser/netshield-backend:latest
```

### Deploy via Render (Docker)

1. In Render, select "BlueprintWebService" from render.yaml
2. Or manually configure a "Docker Service"
3. Use Render's Docker deployment guides

---

## Testing Deployment

### Health Check

```bash
# Test backend health
curl https://netshield-backend.onrender.com/health

# Expected response:
# {"status":"ok","timestamp":"2024-04-14T...","mode":"real"}
```

### API Test

```bash
# Test API connection
curl https://netshield-backend.onrender.com/api/info

# Should return API info and version
```

### Frontend Test

1. Open https://yourapp.vercel.app
2. Check browser console for errors (F12)
3. Try starting a WiFi scan
4. Verify data loads from backend

---

## Troubleshooting

### Frontend Not Connecting to Backend

**Error**: `Network Error` or `ERR_CONNECTION_REFUSED`

**Solution**:
1. Verify `VITE_API_BASE_URL` is set correctly in Vercel
2. Check backend is running on Render
3. Update CORS_ORIGINS in backend to include frontend URL
4. Clear browser cache (Ctrl+Shift+Del)

### Backend Health Check Fails

**Error**: `Health check failed` on Render

**Solution**:
1. Check startup logs in Render dashboard
2. Verify Python version is 3.11+
3. Ensure requirements.txt installs successfully
4. Check environment variables are set correctly

### CORS Errors

**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
1. Add frontend URL to `CORS_ORIGINS` in backend
2. Format: JSON array or comma-separated
3. Restart backend after changing

### WiFi Scanning Not Working

**Error**: Scans timeout or return no networks

**Solution**:
1. WiFi scanning requires admin privileges (local only)
2. Production backend: WiFi scanning may be limited
3. Set `SIMULATION_MODE=false` only if hardware supports it
4. Check `SIMULATION_MODE` environment variable

### Build Failures

**Frontend build fails on Vercel**:
- Check `npm run build` works locally
- Verify all dependencies in package.json
- Check for TypeScript errors

**Backend build fails on Render**:
- Run `pip install -r backend/requirements.txt` locally
- Check Python version compatibility
- Verify all system dependencies installed

---

## Monitoring & Logs

### Vercel Logs
- Dashboard → Deployments → View logs
- Real-time logs during deployment

### Render Logs
- Dashboard → Services → netshield-backend
- Logs tab shows deployment and runtime logs
- Check for error messages

### Local Debugging

```bash
# Backend with verbose logging
DEBUG=true LOG_LEVEL=DEBUG uvicorn main:app --reload

# Frontend with debug
npm run dev
```

---

## Security Considerations

1. **SIMULATION_MODE**: Set to `false` in production for real WiFi scanning
2. **Debug Mode**: Always set `DEBUG=false` in production
3. **CORS**: Only allow trusted frontend origins
4. **Environment Variables**: Never commit `.env` files to git
5. **HTTPS**: Always use HTTPS URLs in production
6. **API Keys**: Store sensitive data in environment variables

---

## Common Deployment URLs

After successful deployment:

- **Frontend (Vercel)**: `https://yourapp.vercel.app`
- **Backend (Render)**: `https://netshield-backend.onrender.com`
- **API Documentation**: `https://netshield-backend.onrender.com/api/docs`
- **API ReDoc**: `https://netshield-backend.onrender.com/api/redoc`

---

## Support & Next Steps

- Check GitHub Issues for common problems
- Review Render documentation: [render.com/docs](https://render.com/docs)
- Review Vercel documentation: [vercel.com/docs](https://vercel.com/docs)
- For WiFi issues, see `REAL_MODE_CONFIG.md`

---

## Post-Deployment Checklist

- [ ] Frontend deployed on Vercel
- [ ] Backend deployed on Render
- [ ] Environment variables configured
- [ ] CORS origins updated
- [ ] Health check passing
- [ ] API documentation accessible
- [ ] WiFi scanning functional
- [ ] PDF reports working
- [ ] Custom domain configured (optional)
- [ ] Monitoring/logs set up

---

*Last Updated: 2026-04-14*
*Version: 1.0.0*
