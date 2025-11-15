# Skill-Based Filtering Update

## Overview
Updated the weekly check-in flow to use a single free-text field with AI-powered extraction of needs and skills. The system now automatically stores user skills and filters help requests to show only relevant matches.

## Changes Made

### 1. Database Schema Updates (`db_manager.py`)

**Added Skills Storage:**
- Users now have a `skills` field to store inferred skills from their learnings
- New method `update_user_skills()` to merge new skills with existing ones, avoiding duplicates

```python
# Users now include:
{
  "id": "u12345",
  "name": "John Doe",
  "email": "john@example.com",
  "company": "StartupCo",
  "role": "founder",
  "skills": [
    {"label": "Machine learning deployment", "category": "technical"},
    {"label": "Product development", "category": "product"}
  ],
  "created_at": "2025-11-15T10:00:00Z"
}
```

### 2. Backend Updates (`app.py`)

**Check-in Endpoint Enhancement:**
- After extracting needs and learnings from check-in text, the system now:
  1. Stores needs and learnings in the database
  2. **NEW**: Updates user's skill profile with extracted learnings
  3. Computes matches
  4. Returns the updated skill profile in the response

**Smart Filtering for Help Requests:**
- Updated `GET /api/matches/expert/<user_id>` endpoint
- Now filters help requests based on user's stored skills
- Matching logic:
  - ✓ Category match: If need category matches any skill category
  - ✓ Keyword match: If skill label words overlap with need label words
  - Only shows requests where the user is a relevant expert

**New Endpoint:**
- `GET /api/users/<user_id>/skills` - Returns user's skill profile

### 3. Frontend Updates

**Templates (`templates/index.html`):**
- Already had single text field ✓
- Added prominent info banner on "Help Requests" tab explaining skill-based filtering
- Message: "We only show you help requests where your skills and learnings are relevant"

**JavaScript (`static/js/app.js`):**
- Fixed all references to use `getCurrentUserId()` instead of undefined `CURRENT_USER_ID`
- Updated `loadHelpRequests()` to fetch and display only skill-filtered requests
- Enhanced submission results display to show:
  - Extracted needs
  - Extracted learnings
  - **NEW**: User's complete skill profile (showing top 5 with count)
  - Matched founders

### 4. MCP Tool (Already Working)

The existing `extract_needs_learnings` MCP tool already extracts:
- Needs (what help they need)
- Learnings/Skills (what they can offer)
- Categories for each item

No changes needed - it's already configured to use Claude AI for extraction!

## How It Works Now

### User Flow:

1. **Submit Check-in:**
   - User enters free-text describing their week
   - Example: "I deployed our ML model to production and figured out containerization with Docker. Now I'm stuck on scaling issues..."

2. **AI Extraction:**
   - System uses Claude AI to extract structured data:
     - Needs: "Help with ML model scaling"
     - Learnings: "Docker containerization", "ML deployment"
   - Fallback to keyword-based extraction if AI unavailable

3. **Skill Profile Update:**
   - Learnings are automatically stored as user's skills
   - Skills accumulate over time, building expertise profile

4. **Smart Filtering:**
   - When viewing "Help Requests" tab
   - System only shows requests where user's skills are relevant
   - Matches by category AND keywords

5. **Results Display:**
   - Shows extracted needs and learnings
   - Displays user's growing skill profile
   - Lists potential matches

## Benefits

✅ **Single Input Field** - Simpler, more natural user experience
✅ **AI-Powered Extraction** - Accurate categorization of needs and skills
✅ **Automatic Skill Building** - User profile grows with each check-in
✅ **Relevant Matches Only** - No noise, only help requests user can actually address
✅ **Scalable** - As community grows, filtering prevents overwhelming users

## Example

**Check-in Text:**
```
This week I launched our MVP and got 100 signups! 
I learned a lot about A/B testing and conversion optimization. 
Now I'm stuck on fundraising - I need help preparing my pitch deck 
and understanding term sheets.
```

**Extracted:**
- Needs: "Fundraising strategy", "Pitch deck preparation" (category: fundraising)
- Learnings: "A/B testing", "Conversion optimization" (category: marketing)

**Skills Stored:**
- User's profile now includes marketing skills
- Next time someone needs help with A/B testing, this user will see the request!

## Technical Notes

- Skills are deduplicated by label to avoid redundancy
- Filtering uses both exact category matching and fuzzy keyword matching
- All user sessions are managed server-side for security
- Backwards compatible with existing database entries (skills default to empty array)

## API Endpoints Updated

- `POST /api/submit-checkin` - Now updates user skills
- `GET /api/matches/expert/<user_id>` - Now returns filtered matches
- `GET /api/users/<user_id>/skills` - New endpoint to view skills

## Files Modified

1. `/Users/Armin/hackathon/db_manager.py` - Database schema and skills management
2. `/Users/Armin/hackathon/app.py` - Backend logic and filtering
3. `/Users/Armin/hackathon/templates/index.html` - UI updates
4. `/Users/Armin/hackathon/static/js/app.js` - Frontend logic

---

**Status:** ✅ Complete - All features implemented and tested
**No Linting Errors:** All code passes validation





