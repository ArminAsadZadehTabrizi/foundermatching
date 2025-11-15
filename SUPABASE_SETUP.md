# 🚀 Supabase Database Setup Guide

Complete guide to switch from JSON to Supabase PostgreSQL database!

---

## ✅ Step-by-Step Setup

### 1️⃣ Create Supabase Project

1. Go to **https://supabase.com/**
2. Click "Start your project" and sign in
3. Click "New Project"
4. Fill in:
   - **Name**: `founder-matching`
   - **Database Password**: Create strong password (**SAVE THIS!**)
   - **Region**: Choose closest to you
   - **Plan**: Free tier
5. Click "Create new project"
6. ⏳ Wait 2-3 minutes...

---

### 2️⃣ Create Database Schema

1. In Supabase dashboard, click **"SQL Editor"** (left sidebar)
2. Click **"New query"**
3. Copy the SQL from earlier (the CREATE TABLE statements)
4. Click **"Run"** or press Cmd/Ctrl + Enter
5. ✅ You should see "Success"

---

### 3️⃣ Get Your API Credentials

1. Click ⚙️ **Settings** (bottom left)
2. Click **"API"** in settings menu
3. Copy these values:

**You need:**
- **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
- **anon/public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (long string)

---

### 4️⃣ Set Environment Variables

In your terminal:

```bash
cd /Users/Armin/hackathon

# Set Supabase credentials
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-anon-key-here"

# Optional: Set Anthropic key too
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

**Or create .env file:**

```bash
nano .env
```

Add these lines:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
ANTHROPIC_API_KEY=sk-ant-your-key
```

Save with Ctrl+X, Y, Enter

---

### 5️⃣ Install Dependencies

```bash
pip3 install supabase psycopg2-binary
```

---

### 6️⃣ Switch to Supabase

**Option A: Simple Rename (Recommended)**

```bash
# Backup old database manager
cp db_manager.py db_manager_json.py

# Use Supabase version
cp db_manager_supabase.py db_manager.py
```

**Option B: Modify app.py**

Change this line in `app.py`:
```python
# Old:
from db_manager import DatabaseManager

# New:
from db_manager_supabase import DatabaseManager
```

---

### 7️⃣ Test It!

```bash
PORT=8000 python3 app.py
```

Look for:
```
✅ Server starting...
📍 Port: 8000
```

No errors? ✅ You're connected to Supabase!

---

## 🧪 Verify Connection

### Test in Python:

```bash
python3
```

```python
import os
os.environ['SUPABASE_URL'] = 'your-url'
os.environ['SUPABASE_KEY'] = 'your-key'

from db_manager_supabase import DatabaseManager
db = DatabaseManager()

# Test query
users = db.get_all_users()
print(f"Found {len(users)} users!")
print(users)
```

If you see the users, ✅ it works!

---

## 🎯 What You Get with Supabase

### ✅ Benefits:

1. **Real PostgreSQL Database**
   - Production-ready
   - ACID compliant
   - SQL queries

2. **Cloud Hosted**
   - No local setup
   - Access from anywhere
   - Automatic backups

3. **Free Tier Includes**:
   - 500 MB database
   - Unlimited API requests
   - 2 GB file storage
   - Perfect for hackathon!

4. **Supabase Dashboard**:
   - View data in browser
   - Edit tables directly
   - Run SQL queries
   - Monitor usage

5. **Auto API**:
   - REST API auto-generated
   - Real-time subscriptions
   - Authentication built-in

---

## 📊 View Your Data

### In Supabase Dashboard:

1. Click **"Table Editor"** (left sidebar)
2. See all your tables:
   - users
   - needs
   - learnings
   - match_suggestions
   - coffee_chats
   - proposed_slots

3. Click any table to view/edit data
4. Add, edit, delete rows directly!

---

## 🔧 Troubleshooting

### Error: "SUPABASE_URL must be set"

Fix:
```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-key"
```

### Error: "No module named 'supabase'"

Fix:
```bash
pip3 install supabase
```

### Error: Connection timeout

- Check your internet connection
- Verify URL is correct
- Check Supabase project is active

### Can't find API key

1. Go to Supabase dashboard
2. Click Settings (⚙️)
3. Click "API"
4. Copy "anon public" key

---

## 🔄 Migrate Your JSON Data

Want to import your JSON data into Supabase?

```python
import json
from db_manager_supabase import DatabaseManager

db = DatabaseManager()

# Load JSON data
with open('database.json', 'r') as f:
    data = json.load(f)

# Import users
for user in data['users']:
    try:
        db.create_user(
            name=user['name'],
            email=user['email'],
            company=user.get('company', ''),
            role=user.get('role', 'founder')
        )
    except:
        pass  # User might already exist

# Import needs
for need in data['needs']:
    db.create_need(
        user_id=need['user_id'],
        label=need['label'],
        category=need['category']
    )

print("✅ Data migrated!")
```

---

## 🎬 For Your Demo

### What to Say:

> "We're using Supabase as our cloud database - a modern PostgreSQL platform that gives us:
> - Real-time database with automatic APIs
> - Built-in authentication and storage
> - Easily scales from prototype to production
> - Free tier perfect for startups
> 
> Our database schema includes 6 tables with proper foreign key relationships, indexes for performance, and sample data for testing."

### Show the Judges:

1. **Supabase Dashboard** - Show live data
2. **Table Editor** - Add a need in real-time
3. **SQL Editor** - Run a query to show matches
4. **API Logs** - Show real-time activity

---

## 🚀 Deploy to Production

When deploying to GCP:

```bash
# Set environment variables in Cloud Run
gcloud run deploy founder-matching \
  --source . \
  --set-env-vars SUPABASE_URL=your-url,SUPABASE_KEY=your-key
```

---

## 📈 Monitor Usage

In Supabase dashboard:
- **Database** → See storage usage
- **API** → View request logs
- **Logs** → Debug queries
- **Reports** → Usage analytics

---

## ✅ Checklist

Before running:
- [ ] Created Supabase project
- [ ] Ran SQL schema
- [ ] Got API URL and key
- [ ] Set environment variables
- [ ] Installed `supabase` package
- [ ] Switched db_manager
- [ ] Tested connection

---

## 🎉 You're Done!

Your app now uses:
- ✅ Real PostgreSQL database
- ✅ Cloud-hosted on Supabase
- ✅ Professional infrastructure
- ✅ Production-ready
- ✅ Free tier for hackathon

**Run it:**
```bash
export SUPABASE_URL="your-url"
export SUPABASE_KEY="your-key"
PORT=8000 python3 app.py
```

**Check it works:**
- Visit http://localhost:8000
- Login and submit check-in
- Data saves to Supabase! ✨

---

Need help? Let me know! 🚀






