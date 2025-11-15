# 🚂 Deploy to Railway - Perfect for ML Apps!

Railway is ideal for your Founder Matching app because:
- ✅ No size limits (ML models work great!)
- ✅ Generous free tier ($5/month credit)
- ✅ Super fast deployment
- ✅ Great for Python/Flask apps

## Quick Deploy (Via Web - 3 minutes)

### Step 1: Push to GitHub (if not already done)

```bash
# Initialize git
git init
git add .
git commit -m "Ready for Railway deployment"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/yourusername/founder-matching.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to: **https://railway.app/**
2. Click **"Start a New Project"**
3. Click **"Deploy from GitHub repo"**
4. Select your repository
5. Click **"Deploy Now"**

Railway will automatically:
- Detect it's a Python app
- Install dependencies from requirements.txt
- Start your app with gunicorn

### Step 3: Add Environment Variables

After deployment starts:

1. Click on your project
2. Go to **"Variables"** tab
3. Add these variables:

```
SUPABASE_URL = https://etheitizrvrglzcnybng.supabase.co
SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GEMINI_API_KEY = AIzaSyARcLkFgXrLSoxJ09SW5lrt8YhjGTjxYWI
ADMIN_PASSWORD = admin123
SECRET_KEY = (generate: openssl rand -hex 32)
FLASK_ENV = production
PORT = 8080
```

4. Click **"Add"** for each

### Step 4: Redeploy

After adding variables:
1. Go to **"Deployments"** tab
2. Click on the latest deployment
3. Click **"Redeploy"**

### Step 5: Get Your URL

1. Go to **"Settings"** tab
2. Scroll to **"Domains"**
3. Click **"Generate Domain"**
4. Your app will be live at: `https://your-app.up.railway.app`

---

## Alternative: Deploy via CLI

If you prefer the command line:

```bash
# Login to Railway
railway login

# Initialize project
railway init

# Link to your Railway project (or create new one)
railway link

# Add environment variables
railway variables --set SUPABASE_URL="https://etheitizrvrglzcnybng.supabase.co"
railway variables --set SUPABASE_KEY="your-key"
railway variables --set GEMINI_API_KEY="your-key"
railway variables --set ADMIN_PASSWORD="admin123"
railway variables --set SECRET_KEY="$(openssl rand -hex 32)"
railway variables --set FLASK_ENV="production"

# Deploy!
railway up
```

---

## Your Live App

After deployment:
- **Main App**: `https://your-app.up.railway.app`
- **Health Check**: `https://your-app.up.railway.app/health`
- **Founder Login**: `https://your-app.up.railway.app/login`
- **Admin**: `https://your-app.up.railway.app/admin/login`

---

## Monitoring & Logs

1. Go to your project dashboard
2. Click on your service
3. View **"Logs"** tab for real-time logs
4. View **"Metrics"** tab for CPU/Memory usage

---

## Cost

Railway Free Tier:
- **$5 free credit per month**
- **500 hours execution time**
- **100 GB outbound bandwidth**

Estimated cost for your app: **$0-5/month** (within free tier for small/medium usage)

---

## Advantages Over Vercel

✅ **No size limits** - ML models work perfectly
✅ **No memory limits** - sentence-transformers loads fine
✅ **Persistent storage** - Great for databases
✅ **WebSocket support** - Can add real-time features
✅ **Better for Python** - Optimized for Python apps

---

## Troubleshooting

### Build fails

Check logs in Railway dashboard. Common issues:
- Missing dependency in requirements.txt
- Python version mismatch (Railway uses 3.9-3.12)

### App crashes on startup

1. Check environment variables are set
2. View logs for error messages
3. Verify Supabase connection

### Can't access app

1. Make sure domain is generated in Settings
2. Check if deployment succeeded
3. View logs for errors

---

## Quick Reference

| Action | Command (CLI) | Web Dashboard |
|--------|---------------|---------------|
| Deploy | `railway up` | Push to GitHub → Auto-deploy |
| Logs | `railway logs` | Logs tab in dashboard |
| Variables | `railway variables` | Variables tab |
| Open app | `railway open` | Click generated domain |

---

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Add environment variables
3. ✅ Generate domain
4. ✅ Test all features
5. ✅ Share your live URL!

---

🚂 **Ready to deploy? Visit https://railway.app/ now!**

