# ☕ Coffee Chat Flow with Jitsi Integration

## Complete User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                    FOUNDER MATCHING SYSTEM                       │
│               Coffee Chat & Video Meeting Flow                   │
└─────────────────────────────────────────────────────────────────┘

STEP 1: CHECK-IN & MATCHING
═══════════════════════════════════════════════════════════════════

    👤 User A (Sarah)                    🤖 AI System
    
    Submits check-in:                   Analyzes text
    "I need help with                   ↓
    ML deployment..."                   Extracts needs:
                                        - ML deployment
                                        - Scaling issues
                                        ↓
                                        Semantic search
                                        ↓
                                        Finds matches
                                        ↓
                                        Match with User B!


STEP 2: MATCH NOTIFICATION
═══════════════════════════════════════════════════════════════════

    👤 User A (Sarah)                    👤 User B (Alex)
                                         
    Sees in "My Matches":               Sees in "Help Requests":
    ┌──────────────────┐                ┌──────────────────┐
    │ 💡 Alex Kim      │                │ 👥 Sarah Chen    │
    │ Can help with:   │                │ Needs help with: │
    │ ML deployment    │                │ ML deployment    │
    │                  │                │                  │
    │ Status: Pending  │                │ [✅ Accept]      │
    └──────────────────┘                │ [❌ Decline]     │
                                        └──────────────────┘
    Waiting...                          Decides to help!
                                        ↓
                                        Clicks "Accept"


STEP 3: COFFEE CHAT CREATED
═══════════════════════════════════════════════════════════════════

    👤 User A (Sarah)                    👤 User B (Alex)
    
    Status updated:                     Coffee chat created!
    ✅ Match accepted!                  ┌─────────────────────┐
    Check Coffee Chats tab              │ ☕ Coffee Chat with │
                                        │    Sarah Chen       │
                                        │                     │
                                        │ Status: Pending     │
                                        │        Slots        │
                                        │                     │
                                        │ [📅 Propose Slots]  │
                                        └─────────────────────┘
                                        ↓
                                        Clicks "Propose Slots"


STEP 4: TIME SLOT PROPOSAL
═══════════════════════════════════════════════════════════════════

    👤 User A (Sarah)                    👤 User B (Alex)
    
    Waiting for slots...                Opens modal:
                                        ┌──────────────────────┐
                                        │ Propose Time Slots   │
                                        │                      │
                                        │ Slot 1: Mon 2:00 PM  │
                                        │ Slot 2: Tue 3:00 PM  │
                                        │ Slot 3: Wed 4:00 PM  │
                                        │                      │
                                        │ [Propose Slots]      │
                                        └──────────────────────┘
                                        ↓
                                        Submits 3 slots


STEP 5: TIME SLOT SELECTION
═══════════════════════════════════════════════════════════════════

    👤 User A (Sarah)                    👤 User B (Alex)
    
    Sees proposed slots:                Status: Pending
    ┌────────────────────┐              Confirmation
    │ ☕ Coffee Chat with │
    │    Alex Kim        │              Waiting for Sarah
    │                    │              to select a slot...
    │ Please select:     │
    │ 📅 Mon 2:00 PM ◄───┼── Clicks
    │ 📅 Tue 3:00 PM     │
    │ 📅 Wed 4:00 PM     │
    └────────────────────┘
    ↓
    Selects Monday 2:00 PM


STEP 6: 🎥 JITSI LINK GENERATION (NEW!)
═══════════════════════════════════════════════════════════════════

    👤 User A (Sarah)                    🤖 System Action

    Confirms selection                  1. Accepts selected slot
    ↓                                   2. Declines other slots
    Alert shown:                        3. Generates Jitsi link:
    ┌────────────────────┐                 "FounderChat-c12a34b5"
    │ ✅ Slot confirmed! │              4. Saves to database
    │                    │              5. Updates chat status
    │ 🎥 Your Jitsi link:│                 to "confirmed"
    │ meet.jit.si/...    │
    └────────────────────┘


STEP 7: CONFIRMED MEETING - BOTH USERS SEE
═══════════════════════════════════════════════════════════════════

    👤 User A (Sarah)                    👤 User B (Alex)

    ┌─────────────────────────┐        ┌─────────────────────────┐
    │ ✅ Meeting Confirmed!   │        │ ✅ Meeting Confirmed!   │
    │                         │        │                         │
    │ 📅 Time:                │        │ 📅 Time:                │
    │    Monday, Dec 25       │        │    Monday, Dec 25       │
    │    2:00 PM              │        │    2:00 PM              │
    │                         │        │                         │
    │ 🎥 Video Link (Jitsi):  │        │ 🎥 Video Link (Jitsi):  │
    │ meet.jit.si/            │        │ meet.jit.si/            │
    │ FounderChat-c12a34b5    │        │ FounderChat-c12a34b5    │
    │                         │        │                         │
    │ [🎥 Join Video Call]    │        │ [🎥 Join Video Call]    │
    │                         │        │                         │
    │ 💡 Join from browser,   │        │ 💡 Join from browser,   │
    │    no account needed!   │        │    no account needed!   │
    └─────────────────────────┘        └─────────────────────────┘


STEP 8: VIDEO MEETING
═══════════════════════════════════════════════════════════════════

    👤 User A (Sarah)                    👤 User B (Alex)

    Clicks "Join Video Call"            Clicks "Join Video Call"
    ↓                                   ↓
    Opens Jitsi in new tab              Opens Jitsi in new tab
    ↓                                   ↓
    ┌───────────────────────────────────────────────────────┐
    │                    JITSI MEETING                       │
    │                                                        │
    │  ┌──────────────┐            ┌──────────────┐        │
    │  │              │            │              │        │
    │  │  👤 Sarah    │            │  👤 Alex     │        │
    │  │              │            │              │        │
    │  └──────────────┘            └──────────────┘        │
    │                                                        │
    │  "Hi Alex! Thanks for helping with ML deployment..."  │
    │                                                        │
    │  [🎤 Mute] [🎥 Camera] [🖥️ Share] [💬 Chat]         │
    └───────────────────────────────────────────────────────┘

    ✅ Discussion about ML deployment
    ✅ Screen sharing for code review
    ✅ Knowledge exchange completed!

```

## Summary Statistics

| Metric | Value |
|--------|-------|
| **User Actions** | 3-4 clicks per person |
| **Time to Meeting Link** | < 1 minute after slot selection |
| **Setup Required** | None (browser-based) |
| **Cost** | $0 (Jitsi is free) |
| **Meeting Features** | Video, audio, screen share, chat |

## Key Advantages

### 🚀 Speed
- From match to meeting link: **5 clicks**
- No account creation or app installation
- Instant access via browser

### 🎯 Simplicity
- Automatic link generation
- Clear visual flow
- No manual coordination needed

### 🔒 Privacy
- Unique room per chat
- Only link holders can join
- No conversation storage

### 💰 Cost-Effective
- Free for unlimited time
- No premium tier needed
- Open-source solution

## Technical Details

### Database Changes

```json
{
  "coffee_chats": [{
    "id": "c12a34b5",
    "status": "confirmed",
    "scheduled_time": "2024-12-25T14:00:00Z",
    "meeting_link": "https://meet.jit.si/FounderChat-c12a34b5",
    "requester_id": "u_sarah",
    "expert_id": "u_alex"
  }]
}
```

### API Flow

```
POST /api/coffee-chats/{chat_id}/select-slot
    ↓
Generate Jitsi Link
    ↓
Update Database
    ↓
Return meeting_link
    ↓
Frontend displays "Join Video Call" button
```

### Room Naming

Format: `FounderChat-{coffee_chat_id}`

Examples:
- `FounderChat-c12a34b5`
- `FounderChat-c98f76ed`
- `FounderChat-c45d23ab`

## Future Enhancements

### Short Term
- [ ] Email notifications with meeting link
- [ ] Calendar event generation (.ics file)
- [ ] Meeting reminders (1 hour before)
- [ ] Post-meeting feedback

### Medium Term
- [ ] Meeting notes/agenda
- [ ] Automatic follow-up scheduling
- [ ] Integration with Google Calendar
- [ ] Slack/Discord notifications

### Long Term
- [ ] Self-hosted Jitsi instance
- [ ] Custom branding for meetings
- [ ] Meeting analytics
- [ ] AI meeting summaries
- [ ] Automated action items

---

**🎉 Result**: Seamless video meetings between matched founders with zero friction!





