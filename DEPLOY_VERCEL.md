# 🚀 Deploy to Vercel - Quick Guide

Deploy your Founder Matching app to Vercel in 2 minutes!

## Prerequisites

- Vercel account (free): https://vercel.com/signup
- Vercel CLI installed (optional but recommended)

## Option 1: Deploy via Vercel CLI (Fastest - 2 minutes)

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Deploy!

```bash
# From your project directory
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name? founder-matching
# - Directory? ./
# - Override settings? N
```

### Step 4: Add Environment Variables

After first deployment, add your environment variables:

```bash
vercel env add SUPABASE_URL
# Paste: https://etheitizrvrglzcnybng.supabase.co

vercel env add SUPABASE_KEY
# Paste your key

vercel env add GEMINI_API_KEY
# Paste your key

vercel env add SECRET_KEY
# Paste: (generate with: openssl rand -hex 32)

vercel env add ADMIN_PASSWORD
# Paste: admin123 (or your password)
```

### Step 5: Redeploy with Environment Variables

```bash
vercel --prod
```

Done! 🎉

---

## Option 2: Deploy via Vercel Dashboard (No CLI needed)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Ready for Vercel deployment"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/yourusername/founder-matching.git
git push -u origin main
```

### Step 2: Import to Vercel

1. Go to: https://vercel.com/new
2. Click "Import Git Repository"
3. Select your GitHub repo
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

### Step 3: Add Environment Variables

In the Vercel dashboard, add these environment variables:

```
SUPABASE_URL = https://etheitizrvrglzcnybng.supabase.co
SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GEMINI_API_KEY = AIzaSyARcLkFgXrLSoxJ09SW5lrt8YhjGTjxYWI
SECRET_KEY = (generate with: openssl rand -hex 32)
ADMIN_PASSWORD = admin123
FLASK_ENV = production
```

### Step 4: Deploy

Click "Deploy" and wait ~2 minutes!

---

## Your Live URLs

After deployment, you'll get:

- **Production**: `https://founder-matching.vercel.app`
- **Preview**: `https://founder-matching-xxxxx.vercel.app`

Test these endpoints:
- Health: `/health`
- Login: `/login`
- Admin: `/admin/login`

---

## Important Note About ML Models

⚠️ **Vercel has a 250MB limit for serverless functions.** 

The `sentence-transformers` library downloads ML models which might exceed this limit. If deployment fails due to size:

### Solution: Use a lighter embedding model or remove it

Edit `app.py` and change line 41:

```python
# Option 1: Use a smaller model
embedding_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # Much smaller

# Option 2: Disable embeddings temporarily (use category matching only)
# embedding_model = None
```

Or deploy to **Railway** or **Render** instead (no size limits).

---

## Alternative: Railway (No Size Limits)

If Vercel doesn't work due to ML model size:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

Railway is perfect for ML apps with large models!

---

## Troubleshooting

### Deployment succeeds but app crashes

Check logs in Vercel dashboard → Your Project → Deployments → View Function Logs

Common issues:
- Missing environment variables
- ML model too large (use Railway/Render instead)

### Build fails

Make sure `vercel.json` is present and correct.

### Environment variables not working

Make sure to redeploy after adding env vars:
```bash
vercel --prod
```

---

## Cost

- **Vercel Free Tier**:
  - 100GB bandwidth/month
  - 100 hours serverless function time
  - Perfect for demos and small apps
  - $0/month

**For production with ML models, consider Railway or Render (also free tiers available).**

---

## Quick Commands

```bash
# Deploy
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls

# Add env variable
vercel env add VARIABLE_NAME
```

---

🚀 **Ready? Run: `vercel` in your project directory!**

