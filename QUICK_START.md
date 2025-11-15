# 🚀 Quick Start Guide

Get the Founder Matching Platform up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

### Step 1: Install Dependencies

```bash
cd /Users/Armin/hackathon
pip install -r requirements.txt
```

**Note**: This will install:
- Flask (web framework)
- Anthropic (AI API - optional)
- sentence-transformers (semantic search)
- All other dependencies

### Step 2: Set API Key (Optional)

The app works without an API key using fallback extraction, but for best results:

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

**Don't have an API key?** No problem! The app has a keyword-based fallback.

### Step 3: Run the Application

```bash
python app.py
```

You should see:

```
🚀 FOUNDER MATCHING SYSTEM - Complete Backend
===============================================================================
✅ Server starting...
📍 Port: 5000
🔑 API Key: ✓ Loaded (or ✗ Not found - using fallback)

📋 Available Endpoints:
  - POST /api/submit-checkin     - Submit weekly check-in
  - GET  /api/matches/<user_id>  - Get user matches
  - POST /api/matches/<id>/accept - Accept match
  ...
```

### Step 4: Open in Browser

Visit: **http://localhost:5000**

---

## 🎮 Demo Workflow

### Test 1: Submit a Check-in

1. **Click "Try Example"** button to load sample text
2. **Click "Analyze & Find Matches"**
3. **View extracted needs and learnings**
4. **See matched founders** with scores and reasons

### Test 2: View Your Matches

1. **Click "My Matches" tab**
2. **See founders who can help** you
3. **Check match scores** and reasoning

### Test 3: Accept a Help Request

1. **Click "Help Requests" tab**
2. **See founders seeking your help**
3. **Click "Accept & Schedule Chat"**
4. **Navigate to Coffee Chats**

### Test 4: Schedule a Coffee Chat

**As Expert**:
1. **Go to "Coffee Chats" tab**
2. **Click "Propose Time Slots"**
3. **Select 3 time slots**
4. **Submit**

**As Requester**:
1. **Go to "Coffee Chats" tab**
2. **View proposed slots**
3. **Click to select one**
4. **Get meeting link!**

### Test 5: Admin Dashboard

1. **Visit**: http://localhost:5000/admin
2. **View statistics** (users, needs, matches)
3. **Check category trends**
4. **Browse all community data**

---

## 🧪 Testing with cURL

### Test Extraction

```bash
curl -X POST http://localhost:5000/api/test-extraction \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I need help with ML deployment and scaling"
  }'
```

### Submit Check-in

```bash
curl -X POST http://localhost:5000/api/submit-checkin \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This week I worked on ML models but stuck on scaling",
    "user_id": "u001"
  }'
```

### Get Matches

```bash
curl http://localhost:5000/api/matches/u001
```

### Admin Stats

```bash
curl http://localhost:5000/api/admin/stats
```

---

## 📊 Sample Data

The app comes with pre-populated sample data in `database.json`:

- **3 users**: Nik Kuchler, Yassine Bekri, Tolga Gunes
- **2 needs**: ML deployment help, MLOps best practices
- **3 learnings**: Scaled ML models, CI/CD pipeline, Series A fundraising
- **1 match**: Yassine → Nik (92% match on ML scaling)
- **1 coffee chat**: Confirmed meeting at 2pm

You can test all features immediately!

---

## 🎯 Key Features to Test

### ✅ AI Extraction
Submit free-text → Get structured needs/learnings

### ✅ Semantic Matching
System finds relevant experts based on meaning, not keywords

### ✅ Coffee Chat Scheduling
Complete workflow: accept → propose slots → select → meeting link

### ✅ Admin Dashboard
Full visibility into community needs and matches

---

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Use a different port
export PORT=8000
python app.py
```

### Dependencies Not Installing

```bash
# Update pip first
pip install --upgrade pip

# Then retry
pip install -r requirements.txt
```

### "No module named 'sentence_transformers'"

```bash
# Install manually
pip install sentence-transformers
```

### App Works But AI Extraction is Simple

This means the Anthropic API key isn't set. The app uses keyword fallback.

To enable full AI extraction:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## 🚀 Next Steps

1. **Try the demo workflow** (5 minutes)
2. **Submit your own check-in** (test AI extraction)
3. **Explore the admin dashboard** (see community insights)
4. **Review the code** (MCP tools in `mcp_server.py`)
5. **Read full docs** (see `HACKATHON_README.md`)

---

## 📚 Documentation

- **Full README**: `HACKATHON_README.md`
- **API Docs**: See API Documentation section in README
- **Architecture**: See Architecture section in README

---

## 💡 Tips

1. **Use "Try Example" button** to quickly test extraction
2. **Check browser console** for API responses
3. **Admin dashboard auto-refreshes** every 30 seconds
4. **All data persists** in `database.json`

---

## 🆘 Need Help?

Check these files:
- `app.py` - Main Flask application
- `db_manager.py` - Database operations
- `mcp_server.py` - MCP tool implementations
- `static/js/app.js` - Frontend logic

---

**Happy Testing! 🎉**

Let founders help each other! 🚀










