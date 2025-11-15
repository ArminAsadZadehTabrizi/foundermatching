# ⚡ Supabase Quickstart - 5 Minutes Setup

## 🎯 What You Need

1. Supabase account (free)
2. 5 minutes
3. Internet connection

---

## 🚀 Quick Steps

### 1. Create Supabase Project (2 min)

```
1. Go to: https://supabase.com/
2. Sign in with GitHub
3. Click "New Project"
4. Name: founder-matching
5. Set password (SAVE IT!)
6. Choose region
7. Click "Create"
8. Wait 2 minutes...
```

---

### 2. Run SQL Schema (1 min)

```
1. Click "SQL Editor" in sidebar
2. Paste the SQL from SUPABASE_SETUP.md
3. Click "Run"
4. See "Success" ✅
```

---

### 3. Get API Keys (30 sec)

```
1. Click Settings ⚙️
2. Click "API"
3. Copy:
   - Project URL
   - anon public key
```

---

### 4. Use Setup Script (1 min)

```bash
cd /Users/Armin/hackathon
chmod +x setup_supabase.sh
./setup_supabase.sh
```

Follow the prompts, paste your URL and key.

---

### 5. Run Your App! (30 sec)

```bash
source .env
PORT=8000 python3 app.py
```

Visit: **http://localhost:8000**

---

## ✅ That's It!

Your app now uses Supabase! 🎉

### What Changed:
- ✅ JSON → PostgreSQL
- ✅ Local → Cloud database
- ✅ Demo → Production ready

### What Stayed the Same:
- ✅ All features work
- ✅ Same API
- ✅ Same UI
- ✅ Zero code changes needed!

---

## 🎬 For Demo

**Show judges:**

1. **Open Supabase dashboard** while app runs
2. **Submit a check-in** in your app
3. **Refresh Table Editor** in Supabase
4. **See new data appear** in real-time!

Impressive! 🤩

---

## 🆘 Need Help?

**Can't connect?**
```bash
echo $SUPABASE_URL
echo $SUPABASE_KEY
```

Should show your values.

**"No module named supabase"?**
```bash
pip3 install supabase
```

**Data not appearing?**
- Check SQL ran successfully
- Verify URL/key are correct
- Check internet connection

---

## 📊 View Your Data

Go to Supabase dashboard → **Table Editor**

See all your tables:
- users 👥
- needs 🎯
- learnings 💡
- match_suggestions 🤝
- coffee_chats ☕
- proposed_slots 📅

Click any table to see data!

---

## 🎉 You're Done!

**Pro tip**: Keep the Supabase dashboard open during your demo to show real-time data updates!

---

Need the full guide? See **SUPABASE_SETUP.md**






