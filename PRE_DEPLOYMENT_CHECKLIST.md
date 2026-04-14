# Pre-Deployment Checklist

## Code Quality ✓

- [ ] Remove debug code and console.logs
- [ ] No hardcoded credentials or secrets
- [ ] All environment variables externalized
- [ ] TypeScript/code linting passes
- [ ] Tests pass locally
- [ ] No sensitive files in git

## Backend Preparation

- [ ] `requirements.txt` up to date
- [ ] `main.py` uses environment variables
- [ ] CORS configured for production domains
- [ ] Health endpoint functional (`/health`)
- [ ] Error handling in place
- [ ] Logging configured
- [ ] `.env.example` created (no secrets)

## Frontend Preparation  

- [ ] `vercel.json` configured
- [ ] `package.json` build script works
- [ ] API base URL uses environment variables
- [ ] `.env.example` created
- [ ] No hardcoded API URLs (except localhost)
- [ ] Build succeeds: `npm run build`
- [ ] All dependencies in `package.json`

## Infrastructure Setup

### Vercel
- [ ] GitHub repository public
- [ ] Vercel account created
- [ ] Project connected to GitHub
- [ ] Build settings configured
- [ ] Environment variables added
- [ ] Custom domain configured (optional)

### Render
- [ ] GitHub repository accessible
- [ ] Render account created  
- [ ] Project connected to GitHub
- [ ] Build command correct
- [ ] Start command correct
- [ ] Environment variables added
- [ ] Custom domain configured (optional)

## Configuration Files

- [ ] `vercel.json` in frontend root
- [ ] `render.yaml` in project root
- [ ] `docker-compose.yml` included
- [ ] `Dockerfile` in backend
- [ ] `.dockerignore` files created
- [ ] `.env.example` files created in both directories

## Testing

- [ ] Backend health check: `curl /health`
- [ ] Frontend loads without errors
- [ ] API calls work from frontend
- [ ] WiFi scanning works (if enabled)
- [ ] PDF generation works (if used)
- [ ] All features tested on staging

## Documentation

- [ ] `DEPLOYMENT_GUIDE.md` reviewed
- [ ] Environment variables documented
- [ ] Troubleshooting steps recorded
- [ ] Architecture documented
- [ ] API endpoints documented

## Security

- [ ] No secrets in environment variables
- [ ] CORS properly configured
- [ ] HTTPS enforced
- [ ] Debug mode disabled
- [ ] Logging doesn't expose sensitive data
- [ ] Input validation in place

## Monitoring

- [ ] Error logging configured
- [ ] Performance monitoring set up (optional)
- [ ] Uptime monitoring enabled (optional)
- [ ] Alert notifications configured (optional)

## DNS & Domains (Optional)

- [ ] Domain registered
- [ ] DNS configured for Vercel frontend
- [ ] DNS configured for Render backend
- [ ] SSL certificates provisioned
- [ ] HTTPS redirects working

## Go-Live

- [ ] All checks passed
- [ ] Backups created
- [ ] Rollback plan documented
- [ ] Team notified
- [ ] Deploy to production
- [ ] Monitor logs for errors
- [ ] Test all features again in production

---

## First Deployment Steps

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Monitor Vercel Build**
   - Dashboard → Deployments
   - Wait for build to complete (2-3 minutes)

3. **Monitor Render Build**
   - Dashboard → Services → netshield-backend
   - Wait for deployment (3-5 minutes)

4. **Test Endpoints**
   ```bash
   curl https://netshield-backend.onrender.com/health
   ```

5. **Test Full App**
   - Open https://yourapp.vercel.app
   - Check browser console (F12)
   - Try a WiFi scan

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS Error | Update `CORS_ORIGINS` in Render env vars |
| Network Error | Check backend URL in `VITE_API_BASE_URL` |
| Build Failed | Check logs, verify dependencies |
| Health Check Failed | Check Render logs for error messages |

---

For detailed deployment instructions, see `DEPLOYMENT_GUIDE.md`.
