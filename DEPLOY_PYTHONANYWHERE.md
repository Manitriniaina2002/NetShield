# Deploy Backend to PythonAnywhere - Free Tier

## Step 1: Create PythonAnywhere Account
- Go to https://www.pythonanywhere.com/
- Click **"Join Today"**
- Choose **"Free"** plan
- Sign up with GitHub or email

## Step 2: Upload Code
After signup, go to **Web** → **Add a new web app**:
1. Choose **Python 3.11**
2. Choose **Flask** or **Manual**
3. Then go to **Files**:
   - Upload your GitHub repo or clone it
   - Or use **Bash console** to clone:
     ```bash
     git clone https://github.com/Manitriniaina2002/NetShield.git
     cd NetShield
     ```

## Step 3: Configure WSGI File
Go to **Web** tab → **WSGI configuration file**:

Replace contents with:
```python
import sys
import os

# Add backend to path
path = '/home/YOUR_USERNAME/NetShield/backend'
if path not in sys.path:
    sys.path.insert(0, path)

os.chdir(path)

# Import FastAPI app
from main import app
application = app
```

## Step 4: Install Dependencies
Go to **Bash console**:
```bash
cd ~/NetShield/backend
pip install --user -r requirements.txt
```

## Step 5: Set Environment Variables
In **Web** tab → **Environment variables**:
```
SIMULATION_MODE=false
DEBUG=false
LOG_LEVEL=INFO
COMPANY_NAME=NetShield
```

## Step 6: Reload Web App
- Click **"Reload"** button in Web tab
- Wait 10 seconds

## Step 7: Get Your URL
Your backend will be at:
```
https://YOUR_USERNAME.pythonanywhere.com
```

Test health endpoint:
```bash
curl https://YOUR_USERNAME.pythonanywhere.com/api/health
```

## Step 8: Deploy Frontend to Vercel
1. Go to https://vercel.com/new
2. Import **NetShield** repo
3. **Root Directory:** `frontend`
4. **Environment Variable:**
   ```
   VITE_API_BASE_URL=https://YOUR_USERNAME.pythonanywhere.com
   ```
5. Click **Deploy**

---

## Notes
- Free tier: 100MB disk, limited CPU
- Good for development/testing
- If you need more: upgrade to paid ($5+/month)
- Your PythonAnywhere URL: `https://YOUR_USERNAME.pythonanywhere.com`
