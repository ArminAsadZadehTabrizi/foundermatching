"""
Database Manager for Founder Matching System
Handles all database operations with JSON-based storage
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid


class DatabaseManager:
    """Manages all database operations"""
    
    def __init__(self, db_path="database.json"):
        self.db_path = db_path
        self.data = self._load_db()
    
    def _load_db(self) -> dict:
        """Load database from JSON file"""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        else:
            # Initialize empty database
            return {
                "users": [],
                "needs": [],
                "learnings": [],
                "match_suggestions": [],
                "coffee_chats": [],
                "proposed_slots": []
            }
    
    def _save_db(self):
        """Save database to JSON file"""
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID with prefix"""
        return f"{prefix}{uuid.uuid4().hex[:8]}"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.utcnow().isoformat() + "Z"
    
    # ============ USER OPERATIONS ============
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        for user in self.data["users"]:
            if user["id"] == user_id:
                return user
        return None
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        return self.data["users"]
    
    def create_user(self, name: str, email: str, company: str = "", role: str = "founder") -> Dict:
        """Create a new user"""
        user = {
            "id": self._generate_id("u"),
            "name": name,
            "email": email,
            "company": company,
            "role": role,
            "skills": [],  # Store inferred skills from learnings
            "created_at": self._get_timestamp()
        }
        self.data["users"].append(user)
        self._save_db()
        return user
    
    # ============ NEED OPERATIONS ============
    
    def get_need(self, need_id: str) -> Optional[Dict]:
        """Get need by ID"""
        for need in self.data["needs"]:
            if need["id"] == need_id:
                return need
        return None
    
    def get_needs_by_user(self, user_id: str) -> List[Dict]:
        """Get all needs for a user"""
        return [n for n in self.data["needs"] if n["user_id"] == user_id]
    
    def get_all_active_needs(self) -> List[Dict]:
        """Get all active needs"""
        return [n for n in self.data["needs"] if n.get("status") == "active"]
    
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
        self.data["needs"].append(need)
        self._save_db()
        return need
    
    def update_need_status(self, need_id: str, status: str):
        """Update need status"""
        for need in self.data["needs"]:
            if need["id"] == need_id:
                need["status"] = status
                self._save_db()
                return True
        return False
    
    # ============ LEARNING OPERATIONS ============
    
    def get_learning(self, learning_id: str) -> Optional[Dict]:
        """Get learning by ID"""
        for learning in self.data["learnings"]:
            if learning["id"] == learning_id:
                return learning
        return None
    
    def get_learnings_by_user(self, user_id: str) -> List[Dict]:
        """Get all learnings for a user"""
        return [l for l in self.data["learnings"] if l["user_id"] == user_id]
    
    def get_all_active_learnings(self) -> List[Dict]:
        """Get all active learnings"""
        return [l for l in self.data["learnings"] if l.get("status") == "active"]
    
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
        self.data["learnings"].append(learning)
        self._save_db()
        return learning
    
    # ============ MATCH OPERATIONS ============
    
    def get_match(self, match_id: str) -> Optional[Dict]:
        """Get match by ID"""
        for match in self.data["match_suggestions"]:
            if match["id"] == match_id:
                return match
        return None
    
    def get_matches_for_user(self, user_id: str) -> List[Dict]:
        """Get all matches where user is the one needing help"""
        return [m for m in self.data["match_suggestions"] if m["need_user_id"] == user_id]
    
    def get_matches_for_expert(self, user_id: str) -> List[Dict]:
        """Get all matches where user is the expert who can help"""
        return [m for m in self.data["match_suggestions"] if m["expert_user_id"] == user_id]
    
    def get_all_matches(self) -> List[Dict]:
        """Get all match suggestions"""
        return self.data["match_suggestions"]
    
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
        self.data["match_suggestions"].append(match)
        self._save_db()
        return match
    
    def update_match_status(self, match_id: str, status: str):
        """Update match status (pending, accepted, declined)"""
        for match in self.data["match_suggestions"]:
            if match["id"] == match_id:
                match["status"] = status
                self._save_db()
                return True
        return False
    
    # ============ COFFEE CHAT OPERATIONS ============
    
    def get_coffee_chat(self, chat_id: str) -> Optional[Dict]:
        """Get coffee chat by ID"""
        for chat in self.data["coffee_chats"]:
            if chat["id"] == chat_id:
                return chat
        return None
    
    def get_coffee_chats_by_user(self, user_id: str) -> List[Dict]:
        """Get all coffee chats for a user (as requester or expert)"""
        return [c for c in self.data["coffee_chats"] 
                if c["requester_id"] == user_id or c["expert_id"] == user_id]
    
    def get_all_coffee_chats(self) -> List[Dict]:
        """Get all coffee chats"""
        return self.data["coffee_chats"]
    
    def create_coffee_chat(self, match_id: str, requester_id: str, expert_id: str) -> Dict:
        """Create a new coffee chat"""
        chat = {
            "id": self._generate_id("c"),
            "match_id": match_id,
            "requester_id": requester_id,
            "expert_id": expert_id,
            "status": "pending_slots",  # pending_slots, pending_confirmation, confirmed, completed, cancelled
            "scheduled_time": None,
            "duration_minutes": 30,
            "meeting_link": None,
            "created_at": self._get_timestamp(),
            "updated_at": self._get_timestamp()
        }
        self.data["coffee_chats"].append(chat)
        self._save_db()
        return chat
    
    def update_coffee_chat(self, chat_id: str, updates: Dict):
        """Update coffee chat"""
        for chat in self.data["coffee_chats"]:
            if chat["id"] == chat_id:
                chat.update(updates)
                chat["updated_at"] = self._get_timestamp()
                self._save_db()
                return True
        return False
    
    # ============ TIME SLOT OPERATIONS ============
    
    def get_slots_for_chat(self, chat_id: str) -> List[Dict]:
        """Get all proposed time slots for a coffee chat"""
        return [s for s in self.data["proposed_slots"] if s["coffee_chat_id"] == chat_id]
    
    def create_slot(self, chat_id: str, proposed_by: str, slot_time: str) -> Dict:
        """Create a proposed time slot"""
        slot = {
            "id": self._generate_id("ps"),
            "coffee_chat_id": chat_id,
            "proposed_by": proposed_by,
            "slot_time": slot_time,
            "status": "pending",  # pending, accepted, declined
            "created_at": self._get_timestamp()
        }
        self.data["proposed_slots"].append(slot)
        self._save_db()
        return slot
    
    def update_slot_status(self, slot_id: str, status: str):
        """Update time slot status"""
        for slot in self.data["proposed_slots"]:
            if slot["id"] == slot_id:
                slot["status"] = status
                self._save_db()
                return True
        return False
    
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
        for user in self.data["users"]:
            if user["id"] == user_id:
                # Merge new skills with existing, avoiding duplicates
                existing_skills = user.get("skills", [])
                skill_labels = {s["label"] for s in existing_skills}
                
                for skill in skills:
                    if skill["label"] not in skill_labels:
                        existing_skills.append(skill)
                        skill_labels.add(skill["label"])
                
                user["skills"] = existing_skills
                self._save_db()
                return True
        return False
    
    def get_dashboard_stats(self) -> Dict:
        """Get aggregated stats for admin dashboard"""
        return {
            "total_users": len(self.data["users"]),
            "total_needs": len([n for n in self.data["needs"] if n.get("status") == "active"]),
            "total_learnings": len([l for l in self.data["learnings"] if l.get("status") == "active"]),
            "total_matches": len(self.data["match_suggestions"]),
            "pending_matches": len([m for m in self.data["match_suggestions"] if m.get("status") == "pending"]),
            "total_chats": len(self.data["coffee_chats"]),
            "confirmed_chats": len([c for c in self.data["coffee_chats"] if c.get("status") == "confirmed"])
        }






