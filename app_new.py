#!/usr/bin/env python3
"""
Flask Backend for Founder Matching System
Complete API with all endpoints for hackathon requirements
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
from db_manager import DatabaseManager
from sentence_transformers import SentenceTransformer
import numpy as np
from anthropic import Anthropic

app = Flask(__name__)
CORS(app)

# Initialize database
db = DatabaseManager("database.json")

# Initialize AI client
anthropic_client = None
if os.getenv("ANTHROPIC_API_KEY"):
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load founder profiles for reference
with open('founders_db.json', 'r') as f:
    founder_profiles = json.load(f)['founders']
    FOUNDER_PROFILES_MAP = {f['id']: f for f in founder_profiles}


# =============== MCP TOOL IMPLEMENTATIONS ===============

def extract_needs_learnings_tool(text: str, user_id: str = "unknown") -> dict:
    """MCP Tool: Extract needs and learnings from text"""
    
    if anthropic_client:
        try:
            prompt = f"""You are analyzing a startup founder's weekly check-in. Extract concrete needs (things they need help with) and learnings/skills (things they learned or can help others with).

Rules:
- Identify 1-3 concrete Needs (challenges, blockers, help requests)
- Identify 1-3 Learnings or Skills (things they learned, completed, or can teach)
- Assign each a category from: sales, marketing, product, fundraising, branding, UX, technical, AI, hiring, strategy
- Be specific and actionable

Check-in text:
{text}

Respond with ONLY valid JSON in this exact format:
{{
  "needs": [
    {{"label": "specific need description", "category": "category_name"}}
  ],
  "learnings": [
    {{"label": "specific learning or skill", "category": "category_name"}}
  ]
}}"""

            response = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = json.loads(response.content[0].text)
            return result
        except Exception as e:
            print(f"AI extraction failed: {e}, using fallback")
    
    # Fallback: Simple keyword-based extraction
    text_lower = text.lower()
    needs = []
    learnings = []
    
    if any(word in text_lower for word in ["stuck", "struggling", "need help", "challenge", "problem", "issue"]):
        if "ml" in text_lower or "machine learning" in text_lower or "model" in text_lower:
            needs.append({"label": "Machine learning deployment and scaling", "category": "technical"})
        if "fundrais" in text_lower or "investor" in text_lower:
            needs.append({"label": "Fundraising and investor relations", "category": "fundraising"})
        if "market" in text_lower or "growth" in text_lower:
            needs.append({"label": "Growth and marketing strategy", "category": "marketing"})
    
    if any(word in text_lower for word in ["learned", "completed", "built", "launched", "achieved", "figured out"]):
        if "product" in text_lower or "feature" in text_lower:
            learnings.append({"label": "Product development and feature launch", "category": "product"})
        if "user" in text_lower or "customer" in text_lower:
            learnings.append({"label": "User research and customer feedback", "category": "UX"})
    
    if not needs:
        needs.append({"label": "General startup guidance", "category": "strategy"})
    if not learnings:
        learnings.append({"label": "Weekly progress and insights", "category": "product"})
    
    return {
        "needs": needs[:3],
        "learnings": learnings[:3]
    }


def compute_matches_tool(needs: list, learnings: list, limit: int = 3) -> dict:
    """MCP Tool: Compute matches between needs and learnings"""
    
    matches = []
    
    for need in needs:
        need_id = need.get("id", "")
        need_user_id = need.get("user_id", "")
        need_label = need.get("label", "")
        need_category = need.get("category", "")
        
        need_embedding = embedding_model.encode([need_label])[0]
        
        scored_learnings = []
        
        for learning in learnings:
            learning_user_id = learning.get("user_id", "")
            
            # Don't match a founder with themselves
            if learning_user_id == need_user_id:
                continue
            
            learning_label = learning.get("label", "")
            learning_category = learning.get("category", "")
            
            # Compute semantic similarity
            learning_embedding = embedding_model.encode([learning_label])[0]
            similarity = np.dot(need_embedding, learning_embedding) / (
                np.linalg.norm(need_embedding) * np.linalg.norm(learning_embedding)
            )
            
            # Category bonus
            category_bonus = 0.2 if need_category == learning_category else 0
            
            # Final score
            score = float(similarity) + category_bonus
            
            # Generate reason
            if need_category == learning_category:
                reason = f"Both focus on {need_category}. The expert's experience with '{learning_label}' directly addresses your need for '{need_label}'"
            else:
                reason = f"The expert's experience with '{learning_label}' can help with your need for '{need_label}'"
            
            scored_learnings.append({
                "need_id": need_id,
                "expert_user_id": learning_user_id,
                "score": round(score, 3),
                "reason": reason,
                "matched_learning": learning_label
            })
        
        # Sort by score and take top N
        scored_learnings.sort(key=lambda x: x["score"], reverse=True)
        matches.extend(scored_learnings[:limit])
    
    return {
        "total_matches": len(matches),
        "matches": matches
    }


# =============== API ENDPOINTS ===============

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/admin')
def admin():
    """Serve admin dashboard"""
    return render_template('admin.html')


# ========== USER ENDPOINTS ==========

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = db.get_all_users()
    return jsonify({"users": users})


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user"""
    user = db.get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.get_json()
    user = db.create_user(
        name=data.get('name'),
        email=data.get('email'),
        company=data.get('company', ''),
        role=data.get('role', 'founder')
    )
    return jsonify(user), 201


# ========== NEEDS & LEARNINGS SUBMISSION ==========

@app.route('/api/submit-checkin', methods=['POST'])
def submit_checkin():
    """Submit weekly check-in and extract needs/learnings"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        user_id = data.get('user_id', 'u001')  # Default for demo
        
        if not text or len(text.strip()) < 20:
            return jsonify({"error": "Please provide a longer check-in"}), 400
        
        # Step 1: Extract needs and learnings using MCP tool
        extraction = extract_needs_learnings_tool(text, user_id)
        
        # Step 2: Save to database
        result = db.create_needs_and_learnings(
            user_id=user_id,
            needs=extraction['needs'],
            learnings=extraction['learnings']
        )
        
        # Step 3: Get all active needs and learnings for matching
        all_needs = db.get_all_active_needs()
        all_learnings = db.get_all_active_learnings()
        
        # Step 4: Compute matches using MCP tool
        matches_result = compute_matches_tool(all_needs, all_learnings, limit=3)
        
        # Step 5: Save top matches to database
        for match in matches_result['matches'][:5]:
            if match['expert_user_id'] != user_id:  # Don't create self-matches
                db.create_match(
                    need_id=match['need_id'],
                    need_user_id=user_id,
                    expert_user_id=match['expert_user_id'],
                    score=match['score'],
                    reason=match['reason']
                )
        
        # Step 6: Get user details for matches
        user_matches = db.get_matches_for_user(user_id)
        enriched_matches = []
        
        for match in user_matches[:3]:
            expert = db.get_user(match['expert_user_id'])
            if expert:
                enriched_matches.append({
                    "match_id": match['id'],
                    "expert": expert,
                    "score": match['score'],
                    "reason": match['reason'],
                    "status": match['status']
                })
        
        return jsonify({
            "summary": f"Extracted {len(result['needs'])} needs and {len(result['learnings'])} learnings from your check-in",
            "needs": result['needs'],
            "learnings": result['learnings'],
            "matches": enriched_matches
        })
    
    except Exception as e:
        print(f"Error in submit_checkin: {e}")
        return jsonify({"error": str(e)}), 500


# ========== MATCH ENDPOINTS ==========

@app.route('/api/matches/<user_id>', methods=['GET'])
def get_user_matches(user_id):
    """Get matches for a user"""
    matches = db.get_matches_for_user(user_id)
    
    # Enrich with user details
    enriched = []
    for match in matches:
        expert = db.get_user(match['expert_user_id'])
        need = db.get_need(match['need_id'])
        if expert and need:
            enriched.append({
                **match,
                "expert": expert,
                "need": need
            })
    
    return jsonify({"matches": enriched})


@app.route('/api/matches/expert/<user_id>', methods=['GET'])
def get_expert_matches(user_id):
    """Get matches where user is the expert"""
    matches = db.get_matches_for_expert(user_id)
    
    # Enrich with user details
    enriched = []
    for match in matches:
        requester = db.get_user(match['need_user_id'])
        need = db.get_need(match['need_id'])
        if requester and need:
            enriched.append({
                **match,
                "requester": requester,
                "need": need
            })
    
    return jsonify({"matches": enriched})


@app.route('/api/matches/<match_id>/accept', methods=['POST'])
def accept_match(match_id):
    """Expert accepts a match and creates coffee chat"""
    match = db.get_match(match_id)
    if not match:
        return jsonify({"error": "Match not found"}), 404
    
    # Update match status
    db.update_match_status(match_id, "accepted")
    
    # Create coffee chat
    chat = db.create_coffee_chat(
        match_id=match_id,
        requester_id=match['need_user_id'],
        expert_id=match['expert_user_id']
    )
    
    return jsonify({
        "message": "Match accepted! Please propose time slots.",
        "coffee_chat": chat
    })


@app.route('/api/matches/<match_id>/decline', methods=['POST'])
def decline_match(match_id):
    """Expert declines a match"""
    db.update_match_status(match_id, "declined")
    return jsonify({"message": "Match declined"})


# ========== COFFEE CHAT & SCHEDULING ENDPOINTS ==========

@app.route('/api/coffee-chats/<user_id>', methods=['GET'])
def get_user_chats(user_id):
    """Get all coffee chats for a user"""
    chats = db.get_coffee_chats_by_user(user_id)
    
    # Enrich with user details
    enriched = []
    for chat in chats:
        requester = db.get_user(chat['requester_id'])
        expert = db.get_user(chat['expert_id'])
        slots = db.get_slots_for_chat(chat['id'])
        
        enriched.append({
            **chat,
            "requester": requester,
            "expert": expert,
            "proposed_slots": slots
        })
    
    return jsonify({"coffee_chats": enriched})


@app.route('/api/coffee-chats/<chat_id>/propose-slots', methods=['POST'])
def propose_time_slots(chat_id):
    """Expert proposes time slots"""
    data = request.get_json()
    slots = data.get('slots', [])  # Array of ISO datetime strings
    user_id = data.get('user_id')
    
    chat = db.get_coffee_chat(chat_id)
    if not chat:
        return jsonify({"error": "Coffee chat not found"}), 404
    
    if chat['expert_id'] != user_id:
        return jsonify({"error": "Only the expert can propose slots"}), 403
    
    # Create slot entries
    created_slots = []
    for slot_time in slots:
        slot = db.create_slot(chat_id, user_id, slot_time)
        created_slots.append(slot)
    
    # Update chat status
    db.update_coffee_chat(chat_id, {"status": "pending_confirmation"})
    
    return jsonify({
        "message": "Time slots proposed successfully",
        "slots": created_slots
    })


@app.route('/api/coffee-chats/<chat_id>/select-slot', methods=['POST'])
def select_time_slot(chat_id):
    """Requester selects a time slot"""
    data = request.get_json()
    slot_id = data.get('slot_id')
    user_id = data.get('user_id')
    
    chat = db.get_coffee_chat(chat_id)
    if not chat:
        return jsonify({"error": "Coffee chat not found"}), 404
    
    if chat['requester_id'] != user_id:
        return jsonify({"error": "Only the requester can select a slot"}), 403
    
    # Get the selected slot
    slots = db.get_slots_for_chat(chat_id)
    selected_slot = None
    for slot in slots:
        if slot['id'] == slot_id:
            selected_slot = slot
            db.update_slot_status(slot_id, "accepted")
        else:
            db.update_slot_status(slot['id'], "declined")
    
    if not selected_slot:
        return jsonify({"error": "Slot not found"}), 404
    
    # Generate meeting link (mock)
    meeting_link = f"https://meet.google.com/{chat_id[:4]}-{chat_id[4:8]}-{chat_id[8:12]}"
    
    # Update chat with confirmed time and meeting link
    db.update_coffee_chat(chat_id, {
        "status": "confirmed",
        "scheduled_time": selected_slot['slot_time'],
        "meeting_link": meeting_link
    })
    
    return jsonify({
        "message": "Time slot confirmed!",
        "scheduled_time": selected_slot['slot_time'],
        "meeting_link": meeting_link
    })


@app.route('/api/coffee-chats/<chat_id>/cancel', methods=['POST'])
def cancel_coffee_chat(chat_id):
    """Cancel a coffee chat"""
    db.update_coffee_chat(chat_id, {"status": "cancelled"})
    return jsonify({"message": "Coffee chat cancelled"})


# ========== ADMIN DASHBOARD ENDPOINTS ==========

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get dashboard statistics"""
    stats = db.get_dashboard_stats()
    
    # Add category breakdown
    all_needs = db.get_all_active_needs()
    all_learnings = db.get_all_active_learnings()
    
    need_categories = {}
    for need in all_needs:
        cat = need.get('category', 'other')
        need_categories[cat] = need_categories.get(cat, 0) + 1
    
    learning_categories = {}
    for learning in all_learnings:
        cat = learning.get('category', 'other')
        learning_categories[cat] = learning_categories.get(cat, 0) + 1
    
    stats['need_categories'] = need_categories
    stats['learning_categories'] = learning_categories
    
    return jsonify(stats)


@app.route('/api/admin/needs', methods=['GET'])
def get_all_needs():
    """Get all needs"""
    needs = db.get_all_active_needs()
    
    # Enrich with user info
    enriched = []
    for need in needs:
        user = db.get_user(need['user_id'])
        enriched.append({
            **need,
            "user": user
        })
    
    return jsonify({"needs": enriched})


@app.route('/api/admin/learnings', methods=['GET'])
def get_all_learnings():
    """Get all learnings"""
    learnings = db.get_all_active_learnings()
    
    # Enrich with user info
    enriched = []
    for learning in learnings:
        user = db.get_user(learning['user_id'])
        enriched.append({
            **learning,
            "user": user
        })
    
    return jsonify({"learnings": enriched})


@app.route('/api/admin/matches', methods=['GET'])
def get_all_matches_admin():
    """Get all matches"""
    matches = db.get_all_matches()
    
    # Enrich with details
    enriched = []
    for match in matches:
        requester = db.get_user(match['need_user_id'])
        expert = db.get_user(match['expert_user_id'])
        need = db.get_need(match['need_id'])
        
        enriched.append({
            **match,
            "requester": requester,
            "expert": expert,
            "need": need
        })
    
    return jsonify({"matches": enriched})


@app.route('/api/admin/coffee-chats', methods=['GET'])
def get_all_chats_admin():
    """Get all coffee chats"""
    chats = db.get_all_coffee_chats()
    
    # Enrich
    enriched = []
    for chat in chats:
        requester = db.get_user(chat['requester_id'])
        expert = db.get_user(chat['expert_id'])
        
        enriched.append({
            **chat,
            "requester": requester,
            "expert": expert
        })
    
    return jsonify({"coffee_chats": enriched})


# ========== UTILITY ENDPOINTS ==========

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "ok"})


@app.route('/api/test-extraction', methods=['POST'])
def test_extraction():
    """Test the extraction tool"""
    data = request.get_json()
    text = data.get('text', '')
    
    result = extract_needs_learnings_tool(text)
    return jsonify(result)


if __name__ == '__main__':
    import sys
    
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "=" * 80)
    print("🚀 FOUNDER MATCHING SYSTEM - Complete Backend")
    print("=" * 80)
    print("\n✅ Server starting...")
    print(f"📍 Port: {port}")
    print(f"🔑 API Key: {'✓ Loaded' if anthropic_client else '✗ Not found (using fallback)'}")
    print("\n📋 Available Endpoints:")
    print("  - POST /api/submit-checkin     - Submit weekly check-in")
    print("  - GET  /api/matches/<user_id>  - Get user matches")
    print("  - POST /api/matches/<id>/accept - Accept match")
    print("  - POST /api/coffee-chats/<id>/propose-slots - Propose time slots")
    print("  - POST /api/coffee-chats/<id>/select-slot - Select time slot")
    print("  - GET  /api/admin/stats - Admin dashboard")
    print("\n🛑 Press Ctrl+C to stop\n")
    
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)










