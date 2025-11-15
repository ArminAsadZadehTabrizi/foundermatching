#!/usr/bin/env python3
"""
Migration script to add gamification fields to existing users
Run this once to update all existing users in the database
"""

import os
from dotenv import load_dotenv
from db_manager_supabase import DatabaseManager

# Load environment variables
load_dotenv()

def migrate_users():
    """Add gamification fields to existing users"""
    print("🔄 Starting user migration...")
    
    db = DatabaseManager()
    
    # Get all users
    users = db.supabase.table("users").select("*").execute()
    
    updated_count = 0
    skipped_count = 0
    
    for user in users.data:
        user_id = user['id']
        needs_update = False
        updates = {}
        
        # Check each field and add if missing
        if 'xp' not in user or user.get('xp') is None:
            updates['xp'] = 0
            needs_update = True
        
        if 'level' not in user or user.get('level') is None:
            updates['level'] = 1
            needs_update = True
        
        if 'badges' not in user or user.get('badges') is None:
            updates['badges'] = []
            needs_update = True
        
        if 'bio' not in user or user.get('bio') is None:
            updates['bio'] = ''
            needs_update = True
        
        if 'total_checkins' not in user or user.get('total_checkins') is None:
            updates['total_checkins'] = 0
            needs_update = True
        
        if 'total_matches' not in user or user.get('total_matches') is None:
            updates['total_matches'] = 0
            needs_update = True
        
        if 'total_chats' not in user or user.get('total_chats') is None:
            updates['total_chats'] = 0
            needs_update = True
        
        if needs_update:
            # Update the user
            db.supabase.table("users").update(updates).eq("id", user_id).execute()
            print(f"✅ Updated user: {user['name']} ({user_id})")
            updated_count += 1
        else:
            print(f"⏭️  Skipped user: {user['name']} (already has all fields)")
            skipped_count += 1
    
    print(f"\n🎉 Migration complete!")
    print(f"   Updated: {updated_count} users")
    print(f"   Skipped: {skipped_count} users")
    print(f"   Total: {len(users.data)} users")

if __name__ == '__main__':
    try:
        migrate_users()
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()





