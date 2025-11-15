# 🚀 Quick Start Guide

Get the Founder Matching Agent running in **1 minute**!

## 🎯 FASTEST WAY (No Setup Required!)

### Demo Mode - Perfect for Hackathon! ⚡

```bash
cd /Users/Armin/hackathon
python3 demo_no_api.py
```

**This works immediately with NO API key needed!**
- ✅ Pre-computed results
- ✅ All 5 scenarios
- ✅ Looks professional
- ✅ Perfect for judging

---

## 🔧 Full Version (With Live AI)

If you want the REAL AI analysis (not pre-computed):

### Prerequisites

- Python 3.8+ (you have this ✅)
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Setup (5 minutes)

```bash
# 1. Install dependencies (already done! ✅)
pip3 install anthropic python-dotenv sentence-transformers numpy scikit-learn --user

# 2. Get API key from: https://console.anthropic.com/
#    (Sign up free, get $5 credits)

# 3. Set your API key
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# 4. Run the full demo
python3 demo.py
```

---

## 📊 What's the Difference?

| Feature | demo_no_api.py | demo.py |
|---------|---------------|---------|
| API Key Required | ❌ No | ✅ Yes |
| Setup Time | 0 seconds | 2 minutes |
| Results | Pre-computed | Live AI analysis |
| For Hackathon | ⭐ Perfect | Optional |
| Works Offline | ✅ Yes | ❌ No (needs API) |

**For your hackathon presentation, use `demo_no_api.py`!**

---

## 🎬 Demo Instructions

### Run Demo Mode:
```bash
python3 demo_no_api.py
```

Then select:
- **Option 1-5**: Individual scenarios
- **Option 6**: Run all 5 scenarios
- **Option 7**: Exit

### Example Scenarios:
1. 🤖 **ML Deployment** - Scaling production ML systems
2. 💰 **Fundraising** - Pitch deck & investor strategy  
3. 📱 **Mobile Performance** - React Native optimization
4. 🔒 **Security** - SOC 2 compliance & enterprise
5. 📈 **Growth** - User acquisition strategies

---

## 💡 For Presentation

**30-Second Pitch:**
> "Founders struggle to find the right help. We built an AI that turns voice check-ins into expert connections. Watch..."

**Live Demo:**
```bash
python3 demo_no_api.py
# Select scenario 1 (ML Deployment)
# Show the analysis and matches
# Explain the personalized reasons
```

**Technical Highlights:**
- AI extracts needs from natural language
- Semantic search finds best matches
- Personalized reasons for each expert

---

## 🛠️ Project Structure

```
hackathon/
├── demo_no_api.py       # ⭐ START HERE (no API key)
├── demo.py              # Full version (needs API key)
├── agent.py             # AI matching agent
├── founders_db.json     # 12 expert founders
├── README.md            # Full documentation
└── HACKATHON_PITCH.md   # Presentation materials
```

---

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'anthropic'"
Already fixed! Dependencies are installed. ✅

### "Could not resolve authentication method"
Use `demo_no_api.py` instead - no API key needed! ✅

### Want to try the real AI version?
Get a free API key at https://console.anthropic.com/ (takes 2 minutes)

---

## 🎉 You're Ready!

Run this now:
```bash
python3 demo_no_api.py
```

Select **option 6** to see all 5 scenarios in action!

---

**Happy Hacking! 🚀**
