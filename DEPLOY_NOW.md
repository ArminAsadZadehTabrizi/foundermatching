# 🚀 Deploy to Google Cloud - Quick Start

**Get your app live in 5 minutes!**

## Step 1: Install gcloud CLI

If you haven't already:

**Mac:**
```bash
brew install google-cloud-sdk
```

**Windows/Linux:**
Download from: https://cloud.google.com/sdk/docs/install

## Step 2: Login and Setup

```bash
# Login
gcloud auth login

# Set your project (create one at console.cloud.google.com first)
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

## Step 3: Set Your Environment Variables

```bash
# Export your credentials
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-supabase-anon-key"
export GEMINI_API_KEY="your-gemini-api-key"
export ADMIN_PASSWORD="your-admin-password"
```

**Where to find these:**
- **SUPABASE_URL & KEY**: Supabase Dashboard → Project Settings → API
- **GEMINI_API_KEY**: https://makersuite.google.com/app/apikey
- **ADMIN_PASSWORD**: Choose any password for admin access

## Step 4: Deploy!

```bash
./deploy-gcp.sh
```

That's it! 🎉

The script will:
- Build your Docker container in the cloud
- Deploy to Cloud Run
- Set all environment variables
- Give you your live URL

## Your App URLs

After deployment, you'll get a URL like:
```
https://founder-matching-xxxxx-uc.a.run.app
```

Access points:
- **Main App**: `https://your-url/`
- **Founder Login**: `https://your-url/login`
- **Admin Dashboard**: `https://your-url/admin/login`
- **Health Check**: `https://your-url/health`

## Verify It Works

```bash
# Test health endpoint
curl https://your-url/health

# Should return: {"status":"ok"}
```

## View Logs

```bash
gcloud run services logs tail founder-matching --region us-central1
```

## Update Environment Variables Later

```bash
gcloud run services update founder-matching \
  --region us-central1 \
  --set-env-vars "GEMINI_API_KEY=new-key"
```

## Costs

Cloud Run has a generous free tier:
- 2 million requests/month free
- Pay only when active
- Estimated cost: $5-15/month for moderate use

## Need Help?

- 📖 Full guide: See `DEPLOY_INSTRUCTIONS.md`
- ✅ Checklist: See `DEPLOYMENT_CHECKLIST.md`
- 🔧 GCP Docs: See `GCP_DEPLOYMENT.md`

---

**Quick Command Summary:**

```bash
# 1. Setup
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Set env vars
export SUPABASE_URL="..."
export SUPABASE_KEY="..."
export GEMINI_API_KEY="..."
export ADMIN_PASSWORD="..."

# 3. Deploy
./deploy-gcp.sh

# 4. Check logs
gcloud run services logs tail founder-matching
```

🚀 **You're ready to go live!**

