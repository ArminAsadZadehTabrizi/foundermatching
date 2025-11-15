#!/bin/bash
# Quick deployment script for Google Cloud

echo "🚀 Deploying Founder Matching Agent to Google Cloud..."
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found!"
    echo "📥 Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✅ gcloud CLI found"
echo ""

# Check if logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo "🔐 Please login to Google Cloud..."
    gcloud auth login
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
echo "🔨 Deploying to Google App Engine..."
echo ""

# Deploy
gcloud app deploy app.yaml --quiet

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "🌐 Your app is live at:"
    echo "   https://$PROJECT_ID.appspot.com"
    echo ""
    echo "🚀 Opening in browser..."
    gcloud app browse
else
    echo ""
    echo "❌ Deployment failed!"
    echo "📋 Check the logs above for errors"
    exit 1
fi










