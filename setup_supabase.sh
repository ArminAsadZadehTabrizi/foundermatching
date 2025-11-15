#!/bin/bash

echo "🚀 Supabase Setup Script for Founder Matching Platform"
echo "========================================================"
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "✅ Found existing .env file"
    source .env
else
    echo "📝 Creating new .env file..."
fi

# Get Supabase URL
if [ -z "$SUPABASE_URL" ]; then
    echo ""
    echo "Enter your Supabase Project URL:"
    echo "(e.g., https://xxxxxxxxxxxxx.supabase.co)"
    read -p "URL: " SUPABASE_URL
    echo "SUPABASE_URL=$SUPABASE_URL" >> .env
fi

# Get Supabase Key
if [ -z "$SUPABASE_KEY" ]; then
    echo ""
    echo "Enter your Supabase anon/public key:"
    echo "(Found in Settings > API)"
    read -p "Key: " SUPABASE_KEY
    echo "SUPABASE_KEY=$SUPABASE_KEY" >> .env
fi

# Optional: Anthropic key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "Enter your Anthropic API key (optional, press Enter to skip):"
    read -p "Key: " ANTHROPIC_API_KEY
    if [ ! -z "$ANTHROPIC_API_KEY" ]; then
        echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" >> .env
    fi
fi

echo ""
echo "✅ Environment variables saved to .env"
echo ""

# Install dependencies
echo "📦 Installing Supabase dependencies..."
pip3 install supabase psycopg2-binary

echo ""
echo "🔄 Switching to Supabase database manager..."

# Backup old db_manager if it exists
if [ -f db_manager.py ]; then
    if [ ! -f db_manager_json.py ]; then
        cp db_manager.py db_manager_json.py
        echo "✅ Backed up JSON database manager to db_manager_json.py"
    fi
fi

# Copy Supabase version
cp db_manager_supabase.py db_manager.py
echo "✅ Activated Supabase database manager"

echo ""
echo "🧪 Testing connection..."
python3 -c "
import os
with open('.env', 'r') as f:
    for line in f:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

from db_manager import DatabaseManager
try:
    db = DatabaseManager()
    users = db.get_all_users()
    print(f'✅ Connected! Found {len(users)} users in database')
except Exception as e:
    print(f'❌ Connection failed: {e}')
    print('Please check your SUPABASE_URL and SUPABASE_KEY')
"

echo ""
echo "========================================================"
echo "🎉 Setup Complete!"
echo "========================================================"
echo ""
echo "To start your app:"
echo "  source .env"
echo "  PORT=8000 python3 app.py"
echo ""
echo "Then visit: http://localhost:8000"
echo ""






