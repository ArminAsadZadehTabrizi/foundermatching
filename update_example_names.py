#!/usr/bin/env python3
"""
Update example user names and emails in Supabase database
Changes:
- Alex Chen (alex@startup.com) → Nik Kuchler (nik@startup.com)
- Maria Garcia (maria@techco.com) → Yassine Bekri (yassine@techco.com)
- John Smith (john@fintech.com) → Tolga Gunes (tolga@fintech.com)
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")
    print("Trying to use environment variables directly...")

# Check if we're using Supabase
if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
    print("⚠️  No Supabase credentials found in environment")
    print("This script is only needed if you're using Supabase.")
    print("If you're using the local database.json, the names have already been updated.")
    exit(0)

from db_manager_supabase import DatabaseManager

def update_names():
    """Update example user names and emails in Supabase"""
    print("🔄 Updating example user names and emails in Supabase...")
    print()
    
    try:
        db = DatabaseManager()
        
        # Update u001: Alex Chen (alex@startup.com) → Nik Kuchler (nik@startup.com)
        user = db.get_user("u001")
        if user:
            updates = {}
            if user["name"] != "Nik Kuchler":
                updates["name"] = "Nik Kuchler"
            if user["email"] != "nik@startup.com":
                updates["email"] = "nik@startup.com"
            
            if updates:
                db.supabase.table("users").update(updates).eq("id", "u001").execute()
                print(f"✅ Updated u001: {user['name']} ({user['email']}) → Nik Kuchler (nik@startup.com)")
            else:
                print(f"ℹ️  User u001 already up to date: {user['name']} ({user['email']})")
        else:
            print("⚠️  User u001 not found")
        
        # Update u002: Maria Garcia (maria@techco.com) → Yassine Bekri (yassine@techco.com)
        user = db.get_user("u002")
        if user:
            updates = {}
            if user["name"] != "Yassine Bekri":
                updates["name"] = "Yassine Bekri"
            if user["email"] != "yassine@techco.com":
                updates["email"] = "yassine@techco.com"
            
            if updates:
                db.supabase.table("users").update(updates).eq("id", "u002").execute()
                print(f"✅ Updated u002: {user['name']} ({user['email']}) → Yassine Bekri (yassine@techco.com)")
            else:
                print(f"ℹ️  User u002 already up to date: {user['name']} ({user['email']})")
        else:
            print("⚠️  User u002 not found")
        
        # Update u003: John Smith (john@fintech.com) → Tolga Gunes (tolga@fintech.com)
        user = db.get_user("u003")
        if user:
            updates = {}
            if user["name"] != "Tolga Gunes":
                updates["name"] = "Tolga Gunes"
            if user["email"] != "tolga@fintech.com":
                updates["email"] = "tolga@fintech.com"
            
            if updates:
                db.supabase.table("users").update(updates).eq("id", "u003").execute()
                print(f"✅ Updated u003: {user['name']} ({user['email']}) → Tolga Gunes (tolga@fintech.com)")
            else:
                print(f"ℹ️  User u003 already up to date: {user['name']} ({user['email']})")
        else:
            print("⚠️  User u003 not found")
        
        # Also update match suggestion reasons that mention "Maria"
        print()
        print("🔄 Updating match suggestion reasons...")
        matches = db.get_all_matches()
        updated_count = 0
        for match in matches:
            reason = match.get("reason", "")
            if "Maria has experience" in reason:
                new_reason = reason.replace("Maria has experience", "Yassine has experience")
                db.supabase.table("match_suggestions").update({"reason": new_reason}).eq("id", match["id"]).execute()
                updated_count += 1
        
        if updated_count > 0:
            print(f"✅ Updated {updated_count} match suggestion reason(s)")
        else:
            print("ℹ️  No match suggestions needed updating")
        
        print()
        print("🎉 Update complete!")
        print()
        print("Updated profiles:")
        print("  • Alex Chen (alex@startup.com) → Nik Kuchler (nik@startup.com)")
        print("  • Maria Garcia (maria@techco.com) → Yassine Bekri (yassine@techco.com)")
        print("  • John Smith (john@fintech.com) → Tolga Gunes (tolga@fintech.com)")
        
    except Exception as e:
        print(f"❌ Error updating names: {e}")
        return False
    
    return True

if __name__ == "__main__":
    update_names()

