# 🚀 Pre-Deployment Checklist

Use this checklist before deploying to Google Cloud.

## ✅ Prerequisites

- [ ] Google Cloud account created
- [ ] Google Cloud project created
- [ ] `gcloud` CLI installed and configured
- [ ] Supabase database set up and tables created
- [ ] Gemini API key obtained from Google AI Studio

## 🔑 Environment Variables Ready

Make sure you have these values:

- [ ] `SUPABASE_URL` - From your Supabase project settings
- [ ] `SUPABASE_KEY` - From your Supabase project settings (anon/public key)
- [ ] `GEMINI_API_KEY` - From Google AI Studio
- [ ] `SECRET_KEY` - Generated random string (or will be auto-generated)
- [ ] `ADMIN_PASSWORD` - Your chosen admin password

## 📋 Database Setup Verification

Check your Supabase database has these tables:

- [ ] `users` table
- [ ] `needs` table
- [ ] `learnings` table
- [ ] `matches` table
- [ ] `coffee_chats` table
- [ ] `slots` table

## 🛠️ Local Testing (Optional but Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SUPABASE_URL="your-url"
export SUPABASE_KEY="your-key"
export GEMINI_API_KEY="your-key"

# Run locally
python app.py

# Test in browser
# Visit http://localhost:5000
```

Test these features locally:
- [ ] Login/signup works
- [ ] Submit check-in extracts needs/learnings
- [ ] Matching generates recommendations
- [ ] Coffee chat scheduling works
- [ ] Admin dashboard accessible

## 🚀 Deployment Steps

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3. Export Environment Variables

```bash
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-key"
export GEMINI_API_KEY="your-gemini-key"
export SECRET_KEY="$(openssl rand -hex 32)"
export ADMIN_PASSWORD="your-chosen-password"
```

### 4. Deploy

```bash
./deploy-gcp.sh
```

### 5. Verify Deployment

After deployment:
- [ ] Visit the provided URL
- [ ] Health check responds: `YOUR-URL/health`
- [ ] Can access login page: `YOUR-URL/login`
- [ ] Admin login works: `YOUR-URL/admin/login`

## 🧪 Post-Deployment Testing

Test these endpoints:

```bash
# Set your Cloud Run URL
export APP_URL="your-cloud-run-url"

# Health check
curl $APP_URL/health

# Should return: {"status":"ok"}
```

Test in browser:
- [ ] Create a test account
- [ ] Submit a check-in
- [ ] Verify needs/learnings are extracted
- [ ] Check if matches appear
- [ ] Test accepting a match
- [ ] Test coffee chat scheduling
- [ ] Verify XP and level up works
- [ ] Check admin dashboard

## 📊 Monitoring Setup

- [ ] Set up Cloud Monitoring for uptime
- [ ] Configure log-based alerts for errors
- [ ] Set up budget alerts

```bash
# View logs
gcloud run services logs tail founder-matching --region us-central1
```

## 🔐 Security Checklist

- [ ] Environment variables set (not hardcoded)
- [ ] Secret key is random and secure
- [ ] Admin password is strong
- [ ] HTTPS is enabled (automatic with Cloud Run)
- [ ] Supabase RLS policies configured (if using Row Level Security)
- [ ] CORS configured properly for your domain

## 💰 Cost Management

- [ ] Set up billing alerts
- [ ] Configure auto-scaling limits
- [ ] Review pricing in GCP console

Cloud Run settings to check:
- Min instances: 0 (for cost savings)
- Max instances: 10 (prevent runaway costs)
- Memory: 2Gi (sufficient for ML models)
- CPU: 2 (fast enough for AI processing)

## 🎯 Optional Enhancements

- [ ] Set up custom domain
- [ ] Configure CDN for static assets
- [ ] Set up CI/CD with GitHub Actions
- [ ] Add error tracking (Sentry)
- [ ] Set up database backups
- [ ] Configure email notifications
- [ ] Add rate limiting

## 🆘 Common Issues

### Issue: Build fails
**Solution**: Check requirements.txt includes all dependencies

### Issue: Container crashes on startup
**Solution**: Verify all environment variables are set
```bash
gcloud run services describe founder-matching --region us-central1
```

### Issue: Supabase connection fails
**Solution**: Check SUPABASE_URL and SUPABASE_KEY are correct

### Issue: AI features not working
**Solution**: Verify GEMINI_API_KEY is valid and has quota

### Issue: 502 Bad Gateway
**Solution**: Check logs for startup errors
```bash
gcloud run services logs read founder-matching --region us-central1 --limit 50
```

## 📞 Support

- Cloud Run Documentation: https://cloud.google.com/run/docs
- Supabase Documentation: https://supabase.com/docs
- Gemini API Documentation: https://ai.google.dev/docs

## ✅ Final Pre-Launch Checklist

- [ ] All environment variables confirmed
- [ ] Local testing passed
- [ ] Deployment successful
- [ ] Health check responds
- [ ] All features tested in production
- [ ] Monitoring configured
- [ ] Budget alerts set
- [ ] Admin access confirmed
- [ ] Documentation updated
- [ ] Team members notified

---

**Ready to deploy?**

1. Complete this checklist
2. Export your environment variables
3. Run: `./deploy-gcp.sh`
4. Test everything
5. 🎉 You're live!

