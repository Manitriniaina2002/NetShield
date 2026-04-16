# Deploy with ngrok - Local Backend Exposed to Internet

## What is ngrok?
ngrok creates a secure tunnel from your local backend to the internet. Perfect for:
- Testing production setup locally
- Free tier available (always-free)
- No server costs
- Easy frontend integration

## Step 1: Install ngrok

**Windows (PowerShell):**
```powershell
choco install ngrok
# or manually: https://ngrok.com/download
```

**macOS:**
```bash
brew install ngrok/ngrok/ngrok
```

**Linux:**
```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
unzip ngrok-v3-stable-linux-amd64.zip
sudo mv ngrok /usr/local/bin
```

## Step 2: Create ngrok Account (Free)

1. Go to https://dashboard.ngrok.com/signup
2. Sign up (takes 30 seconds)
3. Copy your **Auth Token** from dashboard

## Step 3: Start Backend Locally

Open terminal and run:
```bash
cd c:\Users\MaZik\NetShield\backend
python main.py
# or: uvicorn main:app --reload --port 8000
```

Server runs on: `http://localhost:8000`

## Step 4: Start ngrok Tunnel

In a new terminal:
```bash
# Authenticate ngrok (one time)
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE

# Start tunnel
ngrok http 8000
```

You'll see:
```
Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        us (United States)
Latency                       50ms
Web Interface                 http://127.0.0.1:4040

Forwarding                    https://YOUR-RANDOM-ID.ngrok.io -> http://localhost:8000
```

**📋 Copy the ngrok URL:** `https://YOUR-RANDOM-ID.ngrok.io`

## Step 5: Deploy Frontend to Vercel

1. Go to https://vercel.com/new
2. Import **NetShield** repo
3. **Root Directory:** `frontend`
4. **Environment Variable:**
   ```
   VITE_API_BASE_URL=https://YOUR-RANDOM-ID.ngrok.io
   ```
   *(Use the ngrok URL from Step 4)*
5. Click **Deploy**

## Step 6: Test It Working

1. Frontend loads at: `https://yourapp.vercel.app`
2. Click **Scan WiFi** button
3. Check browser console for any errors
4. Verify backend receives requests at ngrok terminal (you'll see logs)

## Step 7: Keep It Running

**To keep ngrok running:**
- Keep the terminal with `ngrok http 8000` open
- Keep backend running on `localhost:8000`
- Frontend on Vercel stays live automatically

## Troubleshooting

**"Connection refused"?**
- Make sure backend is running: `python main.py`
- Make sure ngrok tunnel is active

**Frontend shows errors?**
- Check browser console (F12)
- Check ngrok logs in terminal
- Verify VITE_API_BASE_URL matches ngrok URL

**URL changes after restart?**
- Free tier generates new URL each time
- Upgrade to ngrok paid plan for static URL ($5/month)
- Or re-deploy frontend with new ngrok URL

## Benefits
✅ No server costs  
✅ Test production setup locally  
✅ Perfect for development  
✅ Can keep running 24/7 on your machine  

## Next Steps
When ready for permanent hosting, deploy backend to:
- Railway (free tier, not used up yet?)
- Render (free tier, need to upgrade?)
- Heroku ($5-7/month)
- AWS/Azure free tier

For now, **ngrok + Vercel = fully working deployment!** 🚀
