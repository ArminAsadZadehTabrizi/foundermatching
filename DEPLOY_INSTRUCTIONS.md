# 🚀 Google Cloud Deployment Instructions

This guide will help you deploy your Founder Matching Platform to Google Cloud Run in minutes.

## Prerequisites

1. **Google Cloud Account** - Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud Project** - Create a project in the [GCP Console](https://console.cloud.google.com)
3. **gcloud CLI** - Install from [here](https://cloud.google.com/sdk/docs/install)
4. **Supabase Project** - Your database (you should already have this set up)
5. **Gemini API Key** - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Quick Start (Recommended: Cloud Run)

### Step 1: Install and Configure gcloud CLI

```bash
# Install gcloud (if not already installed)
# Follow instructions at: https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 2: Set Environment Variables

Create a `.env` file or export these variables:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your values
nano .env
```

Required variables:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon/public key
- `GEMINI_API_KEY` - Your Google Gemini API key
- `SECRET_KEY` - Random string for session security
- `ADMIN_PASSWORD` - Password for admin dashboard

### Step 3: Deploy with the Script

```bash
# Make the script executable
chmod +x deploy-gcp.sh

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Deploy!
./deploy-gcp.sh
```

That's it! The script will:
- Build your Docker container
- Deploy to Google Cloud Run
- Set all environment variables
- Give you the live URL

### Step 4: Verify Deployment

After deployment, visit:
- **Main App**: `https://YOUR-SERVICE-URL`
- **Health Check**: `https://YOUR-SERVICE-URL/health`
- **Admin**: `https://YOUR-SERVICE-URL/admin/login`

## Manual Deployment (Alternative)

If you prefer to deploy manually:

```bash
# Set environment variables
export SUPABASE_URL="your-url"
export SUPABASE_KEY="your-key"
export GEMINI_API_KEY="your-key"
export SECRET_KEY="your-secret"
export ADMIN_PASSWORD="your-password"

# Deploy
gcloud run deploy founder-matching \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --set-env-vars "FLASK_ENV=production,SUPABASE_URL=$SUPABASE_URL,SUPABASE_KEY=$SUPABASE_KEY,GEMINI_API_KEY=$GEMINI_API_KEY,SECRET_KEY=$SECRET_KEY,ADMIN_PASSWORD=$ADMIN_PASSWORD"
```

## Updating Environment Variables

To update environment variables after deployment:

```bash
gcloud run services update founder-matching \
  --region us-central1 \
  --set-env-vars "GEMINI_API_KEY=new-key-here"
```

## Viewing Logs

```bash
# Stream logs in real-time
gcloud run services logs tail founder-matching --region us-central1

# Read recent logs
gcloud run services logs read founder-matching --region us-central1 --limit 100
```

## Setting Up Custom Domain

```bash
# Map your domain
gcloud run domain-mappings create \
  --service founder-matching \
  --domain yourdomain.com \
  --region us-central1

# Follow the DNS instructions provided
```

## Scaling Configuration

Cloud Run auto-scales, but you can configure:

```bash
gcloud run services update founder-matching \
  --region us-central1 \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 80
```

## Cost Estimation

Cloud Run pricing is pay-per-use:
- **Free tier**: 2 million requests/month
- **CPU**: ~$0.024/hour when active
- **Memory**: ~$0.003/GB-hour
- **Requests**: $0.40/million

**Estimated cost for moderate usage**: $5-15/month

## Security Best Practices

### 1. Use Secret Manager (Recommended for Production)

```bash
# Store secrets securely
echo -n "your-api-key" | gcloud secrets create gemini-api-key --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding gemini-api-key \
  --member=serviceAccount:$(gcloud run services describe founder-matching --region us-central1 --format='value(spec.template.spec.serviceAccountName)') \
  --role=roles/secretmanager.secretAccessor

# Update Cloud Run to use secret
gcloud run services update founder-matching \
  --region us-central1 \
  --update-secrets=GEMINI_API_KEY=gemini-api-key:latest
```

### 2. Enable HTTPS Only

Cloud Run automatically uses HTTPS, but ensure:
- All API calls use HTTPS
- Set secure cookies in production

### 3. Set Up Monitoring

```bash
# Create uptime check
gcloud monitoring uptime-checks create founder-matching-uptime \
  --display-name="Founder Matching Uptime" \
  --resource-type=uptime-url \
  --host=YOUR-SERVICE-URL \
  --path=/health
```

## Troubleshooting

### Build Fails

Check if all dependencies are in `requirements.txt`:
```bash
pip freeze > requirements.txt
```

### Container Crashes

View logs:
```bash
gcloud run services logs read founder-matching --region us-central1 --limit 50
```

Common issues:
- Missing environment variables
- Supabase connection failed
- Port not set to 8080

### Slow Cold Starts

Increase minimum instances:
```bash
gcloud run services update founder-matching \
  --region us-central1 \
  --min-instances 1
```

## CI/CD with GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - id: auth
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy founder-matching \
            --source . \
            --region us-central1 \
            --platform managed \
            --allow-unauthenticated \
            --set-env-vars "FLASK_ENV=production,SUPABASE_URL=${{ secrets.SUPABASE_URL }},SUPABASE_KEY=${{ secrets.SUPABASE_KEY }},GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}"
```

## Next Steps

1. ✅ Deploy to Cloud Run
2. ✅ Test all features (login, checkins, matching, coffee chats)
3. ✅ Set up monitoring and alerts
4. ✅ Configure custom domain (optional)
5. ✅ Set up CI/CD pipeline (optional)

## Support Resources

- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **GCP Console**: https://console.cloud.google.com
- **Cloud Run Logs**: Use `gcloud run services logs tail`

---

## Quick Reference Commands

```bash
# Deploy
./deploy-gcp.sh

# View logs
gcloud run services logs tail founder-matching --region us-central1

# Update env var
gcloud run services update founder-matching --region us-central1 --set-env-vars KEY=VALUE

# Get URL
gcloud run services describe founder-matching --region us-central1 --format='value(status.url)'

# Delete service
gcloud run services delete founder-matching --region us-central1
```

---

🎉 **Ready to go live? Run `./deploy-gcp.sh` now!**

