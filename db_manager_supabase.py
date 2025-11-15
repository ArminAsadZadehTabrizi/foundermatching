"""
Supabase Database Manager for Founder Matching System
Handles all database operations with Supabase PostgreSQL
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid
from supabase import create_client, Client

class DatabaseManager:
    """Manages all database operations with Supabase"""
    
    def __init__(self):
        # Get Supabase credentials from environment
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.supabase: Client = create_client(supabase_url, supabase_key)
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID with prefix"""
        return f"{prefix}{uuid.uuid4().hex[:8]}"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.utcnow().isoformat() + "Z"
    
    # ============ USER OPERATIONS ============
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        response = self.supabase.table("users").select("*").eq("id", user_id).execute()
        if response.data:
            user = response.data[0]
            # Add default values for gamification fields if they don't exist (for existing users)
            if 'xp' not in user or user.get('xp') is None:
                user['xp'] = 0
            if 'level' not in user or user.get('level') is None:
                user['level'] = 1
            if 'badges' not in user or user.get('badges') is None:
                user['badges'] = []
            if 'bio' not in user or user.get('bio') is None:
                user['bio'] = ''
            if 'total_checkins' not in user or user.get('total_checkins') is None:
                user['total_checkins'] = 0
            if 'total_matches' not in user or user.get('total_matches') is None:
                user['total_matches'] = 0
            if 'total_chats' not in user or user.get('total_chats') is None:
                user['total_chats'] = 0
            return user
        return None
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        response = self.supabase.table("users").select("*").execute()
        users = response.data
        # Add default values for gamification fields if they don't exist (for existing users)
        for user in users:
            if 'xp' not in user or user.get('xp') is None:
                user['xp'] = 0
            if 'level' not in user or user.get('level') is None:
                user['level'] = 1
            if 'badges' not in user or user.get('badges') is None:
                user['badges'] = []
            if 'bio' not in user or user.get('bio') is None:
                user['bio'] = ''
            if 'total_checkins' not in user or user.get('total_checkins') is None:
                user['total_checkins'] = 0
            if 'total_matches' not in user or user.get('total_matches') is None:
                user['total_matches'] = 0
            if 'total_chats' not in user or user.get('total_chats') is None:
                user['total_chats'] = 0
        return users
    
    def create_user(self, name: str, email: str, company: str = "", role: str = "founder") -> Dict:
        """Create a new user"""
        user = {
            "id": self._generate_id("u"),
            "name": name,
            "email": email,
            "company": company,
            "role": role,
            "skills": [],  # Store inferred skills from learnings
            "xp": 0,  # Experience points for gamification
            "level": 1,  # User level
            "badges": [],  # Earned badges
            "bio": "",  # User biography
            "total_checkins": 0,
            "total_matches": 0,
            "total_chats": 0,
            "created_at": self._get_timestamp()
        }
        response = self.supabase.table("users").insert(user).execute()
        return response.data[0]
    
    # ============ NEED OPERATIONS ============
    
    def get_need(self, need_id: str) -> Optional[Dict]:
        """Get need by ID"""
        response = self.supabase.table("needs").select("*").eq("id", need_id).execute()
        return response.data[0] if response.data else None
    
    def get_needs_by_user(self, user_id: str) -> List[Dict]:
        """Get all needs for a user"""
        response = self.supabase.table("needs").select("*").eq("user_id", user_id).execute()
        return response.data
    
    def get_all_active_needs(self) -> List[Dict]:
        """Get all active needs"""
        response = self.supabase.table("needs").select("*").eq("status", "active").execute()
        return response.data
    
    def create_need(self, user_id: str, label: str, category: str) -> Dict:
        """Create a new need"""
        need = {
            "id": self._generate_id("n"),
            "user_id": user_id,
            "label": label,
            "category": category,
            "status": "active",
            "created_at": self._get_timestamp()
        }
        response = self.supabase.table("needs").insert(need).execute()
        return response.data[0]
    
    def update_need_status(self, need_id: str, status: str):
        """Update need status"""
        self.supabase.table("needs").update({"status": status}).eq("id", need_id).execute()
        return True
    
    # ============ LEARNING OPERATIONS ============
    
    def get_learning(self, learning_id: str) -> Optional[Dict]:
        """Get learning by ID"""
        response = self.supabase.table("learnings").select("*").eq("id", learning_id).execute()
        return response.data[0] if response.data else None
    
    def get_learnings_by_user(self, user_id: str) -> List[Dict]:
        """Get all learnings for a user"""
        response = self.supabase.table("learnings").select("*").eq("user_id", user_id).execute()
        return response.data
    
    def get_all_active_learnings(self) -> List[Dict]:
        """Get all active learnings"""
        response = self.supabase.table("learnings").select("*").eq("status", "active").execute()
        return response.data
    
    def create_learning(self, user_id: str, label: str, category: str) -> Dict:
        """Create a new learning"""
        learning = {
            "id": self._generate_id("l"),
            "user_id": user_id,
            "label": label,
            "category": category,
            "status": "active",
            "created_at": self._get_timestamp()
        }
        response = self.supabase.table("learnings").insert(learning).execute()
        return response.data[0]
    
    # ============ MATCH OPERATIONS ============
    
    def get_match(self, match_id: str) -> Optional[Dict]:
        """Get match by ID"""
        response = self.supabase.table("match_suggestions").select("*").eq("id", match_id).execute()
        return response.data[0] if response.data else None
    
    def get_matches_for_user(self, user_id: str) -> List[Dict]:
        """Get all matches where user is the one needing help"""
        response = self.supabase.table("match_suggestions").select("*").eq("need_user_id", user_id).execute()
        return response.data
    
    def get_matches_for_expert(self, user_id: str) -> List[Dict]:
        """Get all matches where user is the expert who can help"""
        response = self.supabase.table("match_suggestions").select("*").eq("expert_user_id", user_id).execute()
        return response.data
    
    def get_all_matches(self) -> List[Dict]:
        """Get all match suggestions"""
        response = self.supabase.table("match_suggestions").select("*").execute()
        return response.data
    
    def create_match(self, need_id: str, need_user_id: str, expert_user_id: str, 
                     score: float, reason: str) -> Dict:
        """Create a new match suggestion"""
        match = {
            "id": self._generate_id("m"),
            "need_id": need_id,
            "need_user_id": need_user_id,
            "expert_user_id": expert_user_id,
            "score": score,
            "reason": reason,
            "status": "pending",
            "created_at": self._get_timestamp()
        }
        response = self.supabase.table("match_suggestions").insert(match).execute()
        return response.data[0]
    
    def update_match_status(self, match_id: str, status: str):
        """Update match status (pending, accepted, declined)"""
        self.supabase.table("match_suggestions").update({"status": status}).eq("id", match_id).execute()
        return True
    
    # ============ COFFEE CHAT OPERATIONS ============
    
    def get_coffee_chat(self, chat_id: str) -> Optional[Dict]:
        """Get coffee chat by ID"""
        response = self.supabase.table("coffee_chats").select("*").eq("id", chat_id).execute()
        return response.data[0] if response.data else None
    
    def get_coffee_chats_by_user(self, user_id: str) -> List[Dict]:
        """Get all coffee chats for a user (as requester or expert)"""
        response = self.supabase.table("coffee_chats").select("*").or_(
            f"requester_id.eq.{user_id},expert_id.eq.{user_id}"
        ).execute()
        return response.data
    
    def get_all_coffee_chats(self) -> List[Dict]:
        """Get all coffee chats"""
        response = self.supabase.table("coffee_chats").select("*").execute()
        return response.data
    
    def create_coffee_chat(self, match_id: str, requester_id: str, expert_id: str) -> Dict:
        """Create a new coffee chat"""
        chat = {
            "id": self._generate_id("c"),
            "match_id": match_id,
            "requester_id": requester_id,
            "expert_id": expert_id,
            "status": "pending_slots",
            "scheduled_time": None,
            "duration_minutes": 30,
            "meeting_link": None,
            "created_at": self._get_timestamp(),
            "updated_at": self._get_timestamp()
        }
        response = self.supabase.table("coffee_chats").insert(chat).execute()
        return response.data[0]
    
    def update_coffee_chat(self, chat_id: str, updates: Dict):
        """Update coffee chat"""
        updates["updated_at"] = self._get_timestamp()
        self.supabase.table("coffee_chats").update(updates).eq("id", chat_id).execute()
        return True
    
    # ============ TIME SLOT OPERATIONS ============
    
    def get_slots_for_chat(self, chat_id: str) -> List[Dict]:
        """Get all proposed time slots for a coffee chat"""
        response = self.supabase.table("proposed_slots").select("*").eq("coffee_chat_id", chat_id).execute()
        return response.data
    
    def create_slot(self, chat_id: str, proposed_by: str, slot_time: str) -> Dict:
        """Create a proposed time slot"""
        slot = {
            "id": self._generate_id("ps"),
            "coffee_chat_id": chat_id,
            "proposed_by": proposed_by,
            "slot_time": slot_time,
            "status": "pending",
            "created_at": self._get_timestamp()
        }
        response = self.supabase.table("proposed_slots").insert(slot).execute()
        return response.data[0]
    
    def update_slot_status(self, slot_id: str, status: str):
        """Update time slot status"""
        self.supabase.table("proposed_slots").update({"status": status}).eq("id", slot_id).execute()
        return True
    
    # ============ BATCH OPERATIONS ============
    
    def create_needs_and_learnings(self, user_id: str, needs: List[Dict], learnings: List[Dict]) -> Dict:
        """Create multiple needs and learnings at once"""
        created_needs = []
        created_learnings = []
        
        for need in needs:
            created_needs.append(self.create_need(user_id, need["label"], need["category"]))
        
        for learning in learnings:
            created_learnings.append(self.create_learning(user_id, learning["label"], learning["category"]))
        
        return {
            "needs": created_needs,
            "learnings": created_learnings
        }
    
    def update_user_skills(self, user_id: str, skills: List[Dict]):
        """Update user's inferred skills from their learnings"""
        user = self.get_user(user_id)
        if not user:
            return False
        
        # Merge new skills with existing, avoiding duplicates
        existing_skills = user.get("skills", [])
        skill_labels = {s["label"] for s in existing_skills}
        
        for skill in skills:
            if skill["label"] not in skill_labels:
                existing_skills.append(skill)
                skill_labels.add(skill["label"])
        
        # Update in Supabase
        self.supabase.table("users").update({"skills": existing_skills}).eq("id", user_id).execute()
        return True
    
    def get_dashboard_stats(self) -> Dict:
        """Get aggregated stats for admin dashboard"""
        users = self.get_all_users()
        needs = self.get_all_active_needs()
        learnings = self.get_all_active_learnings()
        matches = self.get_all_matches()
        chats = self.get_all_coffee_chats()
        
        pending_matches = [m for m in matches if m.get("status") == "pending"]
        confirmed_chats = [c for c in chats if c.get("status") == "confirmed"]
        
        return {
            "total_users": len(users),
            "total_needs": len(needs),
            "total_learnings": len(learnings),
            "total_matches": len(matches),
            "pending_matches": len(pending_matches),
            "total_chats": len(chats),
            "confirmed_chats": len(confirmed_chats)
        }
    
    # ============ GAMIFICATION OPERATIONS ============
    
    def award_xp(self, user_id: str, xp_amount: int, reason: str = "") -> Dict:
        """Award XP to a user and check for level ups"""
        user = self.get_user(user_id)
        if not user:
            return None
        
        current_xp = user.get("xp", 0)
        current_level = user.get("level", 1)
        new_xp = current_xp + xp_amount
        
        # Calculate new level using progressive XP requirement
        # Level 1->2: 100 XP, Level 2->3: 150 XP, Level 3->4: 200 XP, etc.
        # Formula: XP for level n = 25(n-1)(n+2)
        # Solve for n: n = floor((-1 + sqrt(225 + 4*xp) / 5) / 2) + 1
        import math
        new_level = int((-1 + math.sqrt(225 + 4 * new_xp) / 5) / 2) + 1
        new_level = max(1, new_level)  # Ensure level is at least 1
        
        # Check for new badges
        badges = user.get("badges", [])
        new_badges = []
        
        # Badge logic
        if new_xp >= 100 and "First Steps" not in badges:
            badges.append("First Steps")
            new_badges.append("First Steps")
        if new_xp >= 500 and "Rising Star" not in badges:
            badges.append("Rising Star")
            new_badges.append("Rising Star")
        if new_xp >= 1000 and "Community Leader" not in badges:
            badges.append("Community Leader")
            new_badges.append("Community Leader")
        
        # Update user
        updates = {
            "xp": new_xp,
            "level": new_level,
            "badges": badges
        }
        self.supabase.table("users").update(updates).eq("id", user_id).execute()
        
        return {
            "xp_gained": xp_amount,
            "total_xp": new_xp,
            "level": new_level,
            "leveled_up": new_level > current_level,
            "new_badges": new_badges
        }
    
    def update_user_stats(self, user_id: str, stat_name: str, increment: int = 1):
        """Update user activity stats"""
        user = self.get_user(user_id)
        if not user:
            return False
        
        current_value = user.get(stat_name, 0)
        updates = {stat_name: current_value + increment}
        self.supabase.table("users").update(updates).eq("id", user_id).execute()
        return True
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users by XP"""
        response = self.supabase.table("users").select("*").order("xp", desc=True).limit(limit).execute()
        return response.data
    
    def update_user_bio(self, user_id: str, bio: str):
        """Update user biography"""
        self.supabase.table("users").update({"bio": bio}).eq("id", user_id).execute()
        return True
    
    def get_community_stats(self) -> Dict:
        """Get weekly community statistics"""
        from datetime import datetime, timedelta
        
        # Get all users, needs, learnings, matches from last 7 days
        users = self.get_all_users()
        needs = self.get_all_active_needs()
        learnings = self.get_all_active_learnings()
        matches = self.get_all_matches()
        chats = self.get_all_coffee_chats()
        
        # Calculate date 7 days ago
        week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"
        
        # Filter by date
        users_this_week = [u for u in users if u.get("created_at", "") >= week_ago]
        needs_this_week = [n for n in needs if n.get("created_at", "") >= week_ago]
        learnings_this_week = [l for l in learnings if l.get("created_at", "") >= week_ago]
        matches_this_week = [m for m in matches if m.get("created_at", "") >= week_ago]
        chats_this_week = [c for c in chats if c.get("created_at", "") >= week_ago]
        
        # Get skill category distribution
        skill_categories = {}
        for learning in learnings:
            cat = learning.get("category", "other")
            skill_categories[cat] = skill_categories.get(cat, 0) + 1
        
        # Sort and get top 5
        top_skills = sorted(skill_categories.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Get most active users
        active_users = []
        for user in users:
            activity_score = (
                user.get("total_checkins", 0) * 3 +
                user.get("total_matches", 0) * 2 +
                user.get("total_chats", 0) * 5
            )
            if activity_score > 0:
                active_users.append({
                    "id": user["id"],
                    "name": user["name"],
                    "activity_score": activity_score,
                    "level": user.get("level", 1),
                    "xp": user.get("xp", 0)
                })
        
        active_users.sort(key=lambda x: x["activity_score"], reverse=True)
        
        return {
            "total_users": len(users),
            "new_users_this_week": len(users_this_week),
            "needs_this_week": len(needs_this_week),
            "learnings_this_week": len(learnings_this_week),
            "matches_this_week": len(matches_this_week),
            "chats_this_week": len(chats_this_week),
            "top_skills": [{"category": cat, "count": count} for cat, count in top_skills],
            "most_active_users": active_users[:5],
            "total_xp_awarded": sum(u.get("xp", 0) for u in users)
        }


