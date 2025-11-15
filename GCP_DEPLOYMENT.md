# 🌐 Google Cloud Platform Deployment Guide

Deploy the Founder Matching Platform to GCP in minutes!

## Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed and configured
- Project created in GCP

## Option 1: Google Cloud Run (Recommended)

**Best for**: Serverless, auto-scaling, pay-per-use

### Step 1: Prepare Environment

```bash
# Authenticate with GCP
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 2: Create Dockerfile (Already Included)

The project includes a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
ENV FLASK_ENV=production

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
```

### Step 3: Deploy to Cloud Run

```bash
# Deploy directly from source
gcloud run deploy founder-matching \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --set-env-vars FLASK_ENV=production
```

**With Anthropic API Key**:

```bash
gcloud run deploy founder-matching \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --set-env-vars FLASK_ENV=production,ANTHROPIC_API_KEY=your-key-here
```

### Step 4: Access Your App

After deployment completes, you'll get a URL like:
```
https://founder-matching-xxxxxxxxxxxx-uc.a.run.app
```

Visit this URL to access your deployed app!

---

## Option 2: Google App Engine

**Best for**: Simple deployment, managed infrastructure

### Step 1: Prepare app.yaml (Already Included)

The project includes `app.yaml`:

```yaml
runtime: python39
entrypoint: gunicorn -b :$PORT app:app

env_variables:
  FLASK_ENV: 'production'
  # ANTHROPIC_API_KEY: 'your-key-here'  # Uncomment and add key

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
```

### Step 2: Deploy

```bash
# Initialize App Engine (first time only)
gcloud app create --region=us-central

# Deploy
gcloud app deploy app.yaml

# Open in browser
gcloud app browse
```

---

## Option 3: Compute Engine (VM)

**Best for**: Full control, persistent storage

### Step 1: Create VM Instance

```bash
gcloud compute instances create founder-matching-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=20GB \
  --tags=http-server,https-server
```

### Step 2: SSH into VM

```bash
gcloud compute ssh founder-matching-vm --zone=us-central1-a
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get install -y python3-pip git

# Clone your code (or upload)
git clone YOUR_REPO_URL
cd hackathon

# Install dependencies
pip3 install -r requirements.txt
```

### Step 4: Run Application

```bash
# Run in background
nohup python3 app.py &

# Or use gunicorn
gunicorn -b 0.0.0.0:5000 app:app
```

### Step 5: Configure Firewall

```bash
# Allow HTTP traffic
gcloud compute firewall-rules create allow-http \
  --allow tcp:5000 \
  --source-ranges 0.0.0.0/0 \
  --target-tags http-server
```

---

## Database Options for Production

### Option A: Cloud SQL (PostgreSQL)

For production, replace JSON with PostgreSQL + pgvector:

```bash
# Create Cloud SQL instance
gcloud sql instances create founder-db \
  --database-version=POSTGRES_14 \
  --cpu=2 \
  --memory=4GB \
  --region=us-central1

# Create database
gcloud sql databases create founder_matching --instance=founder-db

# Connect from Cloud Run
gcloud run services update founder-matching \
  --add-cloudsql-instances=YOUR_PROJECT:us-central1:founder-db
```

Update `db_manager.py` to use SQLAlchemy + PostgreSQL.

### Option B: Firestore (NoSQL)

For document-based storage:

```bash
# Enable Firestore
gcloud firestore databases create --region=us-central1
```

Update `db_manager.py` to use Firestore SDK.

---

## Environment Variables

### Set via Cloud Run

```bash
gcloud run services update founder-matching \
  --set-env-vars ANTHROPIC_API_KEY=sk-ant-xxx,DATABASE_URL=postgres://...
```

### Set via App Engine

Edit `app.yaml`:

```yaml
env_variables:
  ANTHROPIC_API_KEY: 'sk-ant-xxx'
  DATABASE_URL: 'postgres://...'
```

### Set via Compute Engine

```bash
export ANTHROPIC_API_KEY="sk-ant-xxx"
```

---

## Monitoring & Logging

### Enable Cloud Logging

```bash
# View logs for Cloud Run
gcloud run services logs read founder-matching

# View logs for App Engine
gcloud app logs tail -s default

# View logs for Compute Engine
gcloud compute instances get-serial-port-output founder-matching-vm
```

### Set up Monitoring

```bash
# Enable Cloud Monitoring
gcloud services enable monitoring.googleapis.com

# Create uptime check
gcloud monitoring uptime-checks create http founder-matching \
  --display-name="Founder Matching Uptime" \
  --uri=https://your-app-url.run.app/health
```

---

## Cost Optimization

### Cloud Run Pricing
- **Free tier**: 2 million requests/month
- **CPU**: $0.00002400/vCPU-second
- **Memory**: $0.00000250/GiB-second
- **Requests**: $0.40/million

**Estimated monthly cost**: $5-10 for moderate usage

### App Engine Pricing
- **Free tier**: 28 instance hours/day
- **Standard instance**: ~$0.05/hour

**Estimated monthly cost**: $10-20

### Optimization Tips

1. **Set min instances to 0** for Cloud Run (save on idle time)
2. **Use request timeouts** to prevent long-running requests
3. **Enable caching** for static assets
4. **Compress responses** with gzip

---

## Custom Domain

### Add Custom Domain to Cloud Run

```bash
# Map domain
gcloud run domain-mappings create \
  --service founder-matching \
  --domain founders.yourdomain.com \
  --region us-central1

# Follow DNS instructions provided
```

### Add SSL Certificate

Cloud Run automatically provisions SSL certificates!

---

## CI/CD Pipeline

### GitHub Actions

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
      - uses: actions/checkout@v2
      
      - id: auth
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy founder-matching \
            --source . \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated
```

---

## Health Checks

The app includes a `/health` endpoint:

```python
@app.route('/health')
def health():
    return jsonify({"status": "ok"})
```

Configure Cloud Run health checks:

```bash
gcloud run services update founder-matching \
  --set-env-vars HEALTH_CHECK_PATH=/health
```

---

## Scaling Configuration

### Auto-scaling Settings

```bash
# Cloud Run
gcloud run services update founder-matching \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 80

# App Engine (in app.yaml)
automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
  target_throughput_utilization: 0.6
```

---

## Security Best Practices

1. **Use Secret Manager** for API keys
2. **Enable IAM authentication** for sensitive endpoints
3. **Set up VPC** for database connections
4. **Enable Cloud Armor** for DDoS protection
5. **Use Cloud CDN** for static assets

### Store Secrets in Secret Manager

```bash
# Create secret
echo -n "sk-ant-xxx" | gcloud secrets create anthropic-api-key --data-file=-

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding anthropic-api-key \
  --member=serviceAccount:YOUR_SERVICE_ACCOUNT \
  --role=roles/secretmanager.secretAccessor

# Mount in Cloud Run
gcloud run services update founder-matching \
  --update-secrets=ANTHROPIC_API_KEY=anthropic-api-key:latest
```

---

## Troubleshooting

### Deployment Fails

Check logs:
```bash
gcloud run services logs read founder-matching --limit 50
```

### App Crashes on Startup

Common issues:
- Missing dependencies in `requirements.txt`
- Wrong Python version in Dockerfile
- Database connection errors

### Slow Performance

Solutions:
- Increase memory allocation
- Add caching layer (Redis)
- Optimize database queries
- Use CDN for static assets

---

## Production Checklist

- [ ] Environment variables configured
- [ ] Database migrated to Cloud SQL or Firestore
- [ ] API keys stored in Secret Manager
- [ ] Health checks configured
- [ ] Monitoring and alerting set up
- [ ] Custom domain mapped
- [ ] SSL certificate active
- [ ] Auto-scaling configured
- [ ] Backups enabled (for database)
- [ ] CI/CD pipeline configured
- [ ] Error tracking (Sentry) integrated
- [ ] Load testing completed

---

## Next Steps

1. ✅ Deploy to staging environment
2. ✅ Run integration tests
3. ✅ Set up monitoring
4. ✅ Configure backups
5. ✅ Deploy to production
6. ✅ Monitor and optimize

---

## Support

- **GCP Documentation**: https://cloud.google.com/docs
- **Cloud Run**: https://cloud.google.com/run/docs
- **App Engine**: https://cloud.google.com/appengine/docs

---

**Ready to deploy? Run:**

```bash
gcloud run deploy founder-matching --source . --region us-central1 --allow-unauthenticated
```

🚀 **Let's go live!**










