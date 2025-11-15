# Supabase Migration Guide for Skill-Based Filtering

## ✅ Status: Supabase Code Updated

The Supabase database manager (`db_manager_supabase.py`) has been updated with the same skill-based filtering functionality as the local JSON version.

---

## 🔄 What Changed in Supabase Version

### 1. Updated Code (`db_manager_supabase.py`)

✅ **Added skills field** to user creation  
✅ **Added `update_user_skills()` method** for skill management  
✅ Same duplicate prevention logic as JSON version

---

## 🗄️ Database Schema Changes Required

You need to add a `skills` column to your Supabase `users` table:

### Option 1: SQL Migration Script

Run this SQL in your Supabase SQL Editor:

```sql
-- Add skills column to users table (JSONB type for PostgreSQL)
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS skills JSONB DEFAULT '[]'::jsonb;

-- Add comment for documentation
COMMENT ON COLUMN users.skills IS 'Array of user skills extracted from learnings: [{"label": "skill name", "category": "category"}]';

-- Optional: Create an index for faster querying by skill categories
CREATE INDEX IF NOT EXISTS idx_users_skills ON users USING GIN (skills);

-- Update existing users to have empty skills array if null
UPDATE users SET skills = '[]'::jsonb WHERE skills IS NULL;
```

### Option 2: Supabase Dashboard

1. Go to your Supabase project dashboard
2. Click **Table Editor** → **users** table
3. Click **Add Column**
4. Set:
   - **Name:** `skills`
   - **Type:** `jsonb`
   - **Default value:** `[]`
   - **Nullable:** No
5. Click **Save**

---

## 🔧 Switching to Supabase

### Current Setup

Your `app.py` currently uses the local JSON database:

```python
from db_manager import DatabaseManager
db = DatabaseManager("database.json")
```

### To Switch to Supabase

**Step 1: Set Environment Variables**

```bash
export SUPABASE_URL="your-project-url.supabase.co"
export SUPABASE_KEY="your-anon-or-service-key"
```

Or add to `.env` file:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
```

**Step 2: Update app.py**

Change the import in `app.py`:

```python
# OLD (local JSON):
from db_manager import DatabaseManager
db = DatabaseManager("database.json")

# NEW (Supabase):
from db_manager_supabase import DatabaseManager
db = DatabaseManager()  # No parameter needed, uses env vars
```

**Step 3: Install Dependencies**

```bash
pip install supabase
```

Or if using requirements:

```bash
# Add to requirements.txt
supabase>=2.0.0
```

---

## 🧪 Testing Supabase Integration

Create a test script to verify:

```python
#!/usr/bin/env python3
"""Test Supabase skill functionality"""

import os
from db_manager_supabase import DatabaseManager

# Ensure env vars are set
assert os.getenv("SUPABASE_URL"), "SUPABASE_URL not set"
assert os.getenv("SUPABASE_KEY"), "SUPABASE_KEY not set"

try:
    db = DatabaseManager()
    print("✅ Connected to Supabase")
    
    # Test fetching users
    users = db.get_all_users()
    print(f"✅ Found {len(users)} users")
    
    # Test skill update
    if users:
        test_user_id = users[0]['id']
        test_skills = [
            {"label": "Test skill", "category": "technical"}
        ]
        db.update_user_skills(test_user_id, test_skills)
        print(f"✅ Updated skills for user {test_user_id}")
        
        # Verify
        updated_user = db.get_user(test_user_id)
        print(f"✅ User now has {len(updated_user.get('skills', []))} skills")
    
    print("\n✅ All Supabase tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## 📊 Data Migration (Optional)

If you want to migrate existing data from JSON to Supabase:

```python
#!/usr/bin/env python3
"""Migrate data from local JSON to Supabase"""

from db_manager import DatabaseManager as LocalDB
from db_manager_supabase import DatabaseManager as SupabaseDB
import json

# Load local data
local_db = LocalDB("database.json")
supabase_db = SupabaseDB()

print("Migrating users with skills...")
users = local_db.get_all_users()

for user in users:
    try:
        # Check if user exists in Supabase
        existing = supabase_db.get_user(user['id'])
        
        if existing:
            # Update skills only
            skills = user.get('skills', [])
            if skills:
                supabase_db.update_user_skills(user['id'], skills)
                print(f"✓ Updated {user['name']}: {len(skills)} skills")
        else:
            # Create new user with skills
            supabase_db.create_user(
                name=user['name'],
                email=user['email'],
                company=user.get('company', ''),
                role=user.get('role', 'founder')
            )
            # Then update skills
            if user.get('skills'):
                supabase_db.update_user_skills(user['id'], user['skills'])
            print(f"✓ Created {user['name']}")
            
    except Exception as e:
        print(f"✗ Error with {user['name']}: {e}")

print("\n✅ Migration complete!")
```

---

## 🔍 Verifying the Skills Column

In Supabase SQL Editor, run:

```sql
-- Check that skills column exists
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'users' AND column_name = 'skills';

-- View users with their skills
SELECT id, name, email, skills, 
       jsonb_array_length(skills) as skill_count
FROM users
ORDER BY jsonb_array_length(skills) DESC;

-- Find users with specific skill category
SELECT name, email, skills
FROM users
WHERE skills @> '[{"category": "technical"}]'::jsonb;
```

---

## 🔐 Security Considerations

### Row Level Security (RLS)

Consider adding RLS policies for the skills column:

```sql
-- Allow users to read their own skills
CREATE POLICY "Users can read own skills"
ON users FOR SELECT
USING (auth.uid() = id);

-- Allow users to update their own skills
CREATE POLICY "Users can update own skills"
ON users FOR UPDATE
USING (auth.uid() = id);
```

### API Security

The skill filtering logic runs server-side in `app.py`, so:
- ✅ Users cannot see other users' full skill profiles
- ✅ Filtering happens on backend
- ✅ Only relevant matches are returned

---

## 📋 Checklist

Before switching to Supabase:

- [ ] Run SQL migration to add `skills` column
- [ ] Set `SUPABASE_URL` and `SUPABASE_KEY` environment variables
- [ ] Install `supabase` Python package
- [ ] Update `app.py` to import `db_manager_supabase`
- [ ] Test connection with test script
- [ ] (Optional) Migrate existing data from JSON
- [ ] Test skill update functionality
- [ ] Test filtering in "Help Requests" tab

---

## 🆚 Local JSON vs Supabase

| Feature | Local JSON | Supabase |
|---------|-----------|----------|
| Setup | ✅ Zero config | ⚠️ Requires credentials |
| Performance | ✅ Fast (small data) | ✅ Fast (any size) |
| Scalability | ❌ Limited | ✅ Production-ready |
| Multi-user | ❌ File locks | ✅ Concurrent access |
| Backup | ⚠️ Manual | ✅ Automatic |
| Queries | ⚠️ Load all → filter | ✅ Indexed queries |
| Skills Support | ✅ Implemented | ✅ Implemented |

**Recommendation:** 
- **Development/Demo:** Use local JSON (current setup)
- **Production:** Use Supabase

---

## ✅ Summary

✅ **Supabase code is updated** with skill functionality  
⚠️ **Database schema needs migration** (add `skills` column)  
⚠️ **App.py still using local JSON** (change import to switch)

Both database managers now have **feature parity** for skill-based filtering!

---

*Need help? Check the official docs:*
- 📚 [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
- 📚 [PostgreSQL JSONB](https://www.postgresql.org/docs/current/datatype-json.html)





