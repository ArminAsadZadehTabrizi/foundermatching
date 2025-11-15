#!/bin/bash
# Google Cloud Run Deployment Script
# This script deploys your Founder Matching app to Cloud Run

set -e  # Exit on error

echo "🚀 Deploying Founder Matching Platform to Google Cloud Run..."
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found!"
    echo "📥 Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✅ gcloud CLI found"
echo ""

# Check for required environment variables
if [ -z "$SUPABASE_URL" ]; then
    echo "⚠️  SUPABASE_URL not set. You'll need to set it after deployment."
fi

if [ -z "$SUPABASE_KEY" ]; then
    echo "⚠️  SUPABASE_KEY not set. You'll need to set it after deployment."
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY not set. You'll need to set it after deployment."
fi

# Get current project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ No project set!"
    echo "📝 Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📦 Project: $PROJECT_ID"
echo ""

# Set default values
REGION=${REGION:-us-central1}
SERVICE_NAME=${SERVICE_NAME:-founder-matching}

echo "🔨 Deploying to Google Cloud Run..."
echo "   Region: $REGION"
echo "   Service: $SERVICE_NAME"
echo ""

# Build environment variables string
ENV_VARS="FLASK_ENV=production"

if [ ! -z "$SUPABASE_URL" ]; then
    ENV_VARS="$ENV_VARS,SUPABASE_URL=$SUPABASE_URL"
fi

if [ ! -z "$SUPABASE_KEY" ]; then
    ENV_VARS="$ENV_VARS,SUPABASE_KEY=$SUPABASE_KEY"
fi

if [ ! -z "$GEMINI_API_KEY" ]; then
    ENV_VARS="$ENV_VARS,GEMINI_API_KEY=$GEMINI_API_KEY"
fi

if [ ! -z "$SECRET_KEY" ]; then
    ENV_VARS="$ENV_VARS,SECRET_KEY=$SECRET_KEY"
else
    # Generate a random secret key
    SECRET_KEY=$(openssl rand -hex 32)
    ENV_VARS="$ENV_VARS,SECRET_KEY=$SECRET_KEY"
    echo "🔑 Generated SECRET_KEY: $SECRET_KEY"
fi

if [ ! -z "$ADMIN_PASSWORD" ]; then
    ENV_VARS="$ENV_VARS,ADMIN_PASSWORD=$ADMIN_PASSWORD"
fi

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars "$ENV_VARS"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "🌐 Getting service URL..."
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)')
    echo ""
    echo "🎉 Your app is live at:"
    echo "   $SERVICE_URL"
    echo ""
    echo "📋 Useful URLs:"
    echo "   Main App:       $SERVICE_URL"
    echo "   Founder Login:  $SERVICE_URL/login"
    echo "   Admin Login:    $SERVICE_URL/admin/login"
    echo "   Health Check:   $SERVICE_URL/health"
    echo ""
    echo "🔧 To update environment variables later, run:"
    echo "   gcloud run services update $SERVICE_NAME --region $REGION --set-env-vars KEY=VALUE"
    echo ""
else
    echo ""
    echo "❌ Deployment failed!"
    echo "📋 Check the logs above for errors"
    exit 1
fi

