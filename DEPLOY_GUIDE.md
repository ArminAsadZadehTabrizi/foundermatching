# 🚀 Google Cloud Deployment Guide

Deploy your Founder Matching Agent to Google Cloud Platform in minutes!

---

## 🎯 Two Deployment Options

### Option 1: App Engine (Easiest) ⭐ RECOMMENDED
- ✅ Simplest deployment
- ✅ Auto-scaling included
- ✅ Free tier available
- ✅ Perfect for demos and MVPs

### Option 2: Cloud Run (More Flexible)
- ✅ Container-based
- ✅ Pay per use
- ✅ More control
- ✅ Good for production

---

## 📋 Prerequisites

### 1. Create Google Cloud Project
1. Go to: https://console.cloud.google.com/
2. Create new project (or select existing)
3. Note your PROJECT_ID

### 2. Install Google Cloud SDK

**macOS:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Or download from**: https://cloud.google.com/sdk/docs/install

### 3. Initialize gcloud
```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

---

## 🚀 Option 1: Deploy to App Engine (Easiest)

### Step 1: Prepare Files
All files are already created! ✅
- `app.yaml` - App Engine configuration
- `requirements-deploy.txt` - Dependencies
- `.gcloudignore` - Files to ignore

### Step 2: Deploy
```bash
cd /Users/Armin/hackathon

# Deploy to App Engine
gcloud app deploy app.yaml

# When prompted:
# - Choose region (e.g., us-central)
# - Type 'y' to confirm
```

### Step 3: Open Your App
```bash
gcloud app browse
```

**Your app is now live!** 🎉

### Step 4: Share the URL
Your app will be at:
```
https://YOUR_PROJECT_ID.appspot.com
```

---

## 🐳 Option 2: Deploy to Cloud Run

### Step 1: Build Container
```bash
cd /Users/Armin/hackathon

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/founder-matching
```

### Step 2: Deploy to Cloud Run
```bash
gcloud run deploy founder-matching \
  --image gcr.io/YOUR_PROJECT_ID/founder-matching \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

### Step 3: Get Your URL
After deployment, you'll see:
```
Service URL: https://founder-matching-xxxxx-uc.a.run.app
```

**That's your live URL!** 🎉

---

## 💰 Pricing (Both Options)

### App Engine (Free Tier)
- **28 instance hours/day FREE**
- **1GB outbound data/day FREE**
- **Perfect for hackathons and demos**

### Cloud Run (Pay Per Use)
- **2 million requests/month FREE**
- **360,000 GB-seconds/month FREE**
- **180,000 vCPU-seconds/month FREE**
- **Also perfect for demos!**

**Both are essentially FREE for hackathon demos!** ✅

---

## 🔧 Configuration Files Explained

### `app.yaml` (App Engine)
```yaml
runtime: python39              # Python version
entrypoint: gunicorn app:app   # How to run your app
instance_class: F1             # Small instance (free tier)
automatic_scaling:             # Auto-scale settings
  min_instances: 0             # Scale to zero when idle
  max_instances: 10            # Max 10 instances
```

### `Dockerfile` (Cloud Run)
```dockerfile
FROM python:3.9-slim           # Base image
WORKDIR /app                   # Working directory
COPY files...                  # Copy your code
RUN pip install...             # Install dependencies
CMD gunicorn...                # Start server
```

### `.gcloudignore`
Tells Google Cloud what files NOT to upload:
- Development files
- Test scripts
- Local config

---

## ✅ Post-Deployment Checklist

After deploying, test:

- [ ] Homepage loads: `https://your-url/`
- [ ] Health check works: `https://your-url/health`
- [ ] Try Example button works
- [ ] Submit a check-in
- [ ] Results display correctly
- [ ] Mobile view works
- [ ] Share URL with friends/judges

---

## 🎯 For Hackathon Judges

### Share Your Live URL

**App Engine:**
```
https://YOUR_PROJECT_ID.appspot.com
```

**Cloud Run:**
```
https://founder-matching-xxxxx-uc.a.run.app
```

### Custom Domain (Optional)
```bash
# Map custom domain (if you have one)
gcloud app domain-mappings create demo.yourdomain.com
```

---

## 📊 Monitoring Your App

### View Logs
```bash
# App Engine
gcloud app logs tail -s default

# Cloud Run
gcloud run services logs tail founder-matching
```

### View Metrics
Go to: https://console.cloud.google.com/
- Navigate to your service
- Click "Metrics" or "Logs"

### Check Status
```bash
# App Engine
gcloud app browse

# Cloud Run
gcloud run services list
```

---

## 🔄 Update Your App

Made changes? Redeploy:

### App Engine:
```bash
gcloud app deploy
```

### Cloud Run:
```bash
# Rebuild and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/founder-matching
gcloud run deploy founder-matching \
  --image gcr.io/YOUR_PROJECT_ID/founder-matching \
  --platform managed \
  --region us-central1
```

---

## 🐛 Troubleshooting

### "Project not found"
```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID
```

### "Permission denied"
```bash
# Re-authenticate
gcloud auth login
```

### "Build failed"
```bash
# Check your files exist
ls -la app.py templates/ static/

# Check requirements file
cat requirements-deploy.txt
```

### "App not accessible"
```bash
# For Cloud Run, make sure it's public
gcloud run services add-iam-policy-binding founder-matching \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=us-central1
```

### App crashes on startup
```bash
# Check logs
gcloud app logs tail -s default

# Common issues:
# - Missing files (check .gcloudignore)
# - Wrong Python version (use 3.9)
# - Missing dependencies (check requirements-deploy.txt)
```

---

## 🎨 Environment Variables (Optional)

If you add API keys later:

### App Engine:
Edit `app.yaml`:
```yaml
env_variables:
  ANTHROPIC_API_KEY: 'your-key-here'
  FLASK_ENV: 'production'
```

### Cloud Run:
```bash
gcloud run services update founder-matching \
  --set-env-vars="ANTHROPIC_API_KEY=your-key-here"
```

---

## 📱 Test on Mobile

Once deployed, test on your phone:
1. Open browser on phone
2. Visit your live URL
3. Try the full flow
4. Take screenshots for presentation!

---

## 🎬 Demo Flow with Live URL

### During Hackathon:

1. **Show local version first**:
   ```bash
   python3 app.py
   # Demo on localhost:5000
   ```

2. **Then reveal live version**:
   ```
   "And it's already deployed to Google Cloud!"
   [Open live URL]
   "Judges can try it on their phones right now!"
   ```

3. **Share QR code** (optional):
   - Generate QR code for your URL
   - Display it on screen
   - Judges scan and try it!

---

## 💡 Pro Tips

### Speed Up Deployment
```bash
# Create alias
echo 'alias deploy="gcloud app deploy --quiet"' >> ~/.zshrc
source ~/.zshrc

# Now just type:
deploy
```

### Multiple Versions
```bash
# Deploy without promoting (test version)
gcloud app deploy --no-promote --version=test

# View all versions
gcloud app versions list

# Split traffic between versions
gcloud app services set-traffic default --splits=v1=.5,v2=.5
```

### Save Deployment Settings
Create `deploy.sh`:
```bash
#!/bin/bash
echo "🚀 Deploying Founder Matching Agent..."
gcloud app deploy --quiet
gcloud app browse
```

---

## 📊 Cost Estimate

### For Hackathon Demo (48 hours):
- **Expected traffic**: 100-500 requests
- **Cost**: $0.00 (within free tier)

### For Beta (1 month, 1000 users):
- **App Engine**: $0-5/month
- **Cloud Run**: $0-3/month

**Both are incredibly cheap!** 💰

---

## 🎉 Quick Deploy Summary

### Fastest Path to Live:

```bash
# 1. Setup (once)
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Deploy (30 seconds)
cd /Users/Armin/hackathon
gcloud app deploy

# 3. Open
gcloud app browse

# Done! 🎉
```

---

## 🏆 You're Live!

Your app is now:
- ✅ Accessible worldwide
- ✅ Auto-scaling
- ✅ On Google's infrastructure
- ✅ Free (within limits)
- ✅ Production-ready

**Share your URL with the world!** 🌍

---

## 📚 Additional Resources

- [App Engine Docs](https://cloud.google.com/appengine/docs)
- [Cloud Run Docs](https://cloud.google.com/run/docs)
- [Pricing Calculator](https://cloud.google.com/products/calculator)
- [Free Tier Details](https://cloud.google.com/free)

---

## 🎯 Need Help?

Common commands:
```bash
# View all gcloud commands
gcloud --help

# View app info
gcloud app describe

# View services
gcloud app services list

# Delete app (if needed)
gcloud app services delete default
```

---

**Ready to deploy? Start here:**

```bash
cd /Users/Armin/hackathon
gcloud app deploy
```

Good luck! 🚀🎉










