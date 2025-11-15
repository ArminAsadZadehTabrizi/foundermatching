# 🎥 Jitsi Video Meeting Integration

## Overview

After both users accept a time slot for a coffee chat, they automatically get a **Jitsi video meeting link** to conduct their video call. Jitsi is an open-source, free video conferencing solution that works directly in the browser without requiring any account or installation.

## How It Works

### 1. **Match Acceptance**
- User A submits a check-in expressing a need
- User B gets matched as an expert who can help
- User B accepts the match, creating a coffee chat

### 2. **Time Slot Proposal**
- User B (expert) proposes 3 time slots for the meeting
- These slots are displayed to User A

### 3. **Time Slot Selection**
- User A selects one of the proposed time slots
- **Automatic Jitsi Link Generation** happens here

### 4. **Video Meeting Link**
- A unique Jitsi meeting room is created: `https://meet.jit.si/FounderChat-{chat_id}`
- Both users can see the meeting link in the "Coffee Chats" tab
- The link is permanent and can be accessed anytime

### 5. **Joining the Meeting**
- Click the "🎥 Join Video Call" button
- Opens Jitsi in a new tab
- No account needed - just enter your name and join!

## Technical Implementation

### Backend (`app.py`)

```python
# Generate Jitsi meeting link
room_name = f"FounderChat-{chat_id}"
meeting_link = f"https://meet.jit.si/{room_name}"

# Store in database
db.update_coffee_chat(chat_id, {
    "status": "confirmed",
    "scheduled_time": selected_slot['slot_time'],
    "meeting_link": meeting_link
})
```

### Frontend (`app_new.js`)

When a coffee chat is confirmed, it displays:
- ✅ Meeting confirmed message
- 📅 Scheduled time
- 🎥 Jitsi video meeting link
- Direct "Join Video Call" button
- Helpful tip about browser access

## Why Jitsi?

1. **Free & Open Source**: No costs, no limits
2. **No Account Required**: Users can join instantly
3. **Browser-Based**: Works in Chrome, Firefox, Safari, Edge
4. **Privacy-Focused**: Open-source and self-hostable
5. **Feature-Rich**: Screen sharing, chat, recording, etc.
6. **Reliable**: Used by thousands of organizations worldwide

## User Experience

### Before Meeting
```
✅ Meeting Confirmed!
📅 Time: Mon, Dec 25, 2024, 2:00 PM

🎥 Video Meeting Link (Jitsi):
https://meet.jit.si/FounderChat-c12a34b5

[🎥 Join Video Call]

💡 Tip: You can join directly from your browser, no account needed!
```

### During Meeting
- Click "Join Video Call"
- Enter your name (optional)
- Allow camera/microphone permissions
- Start chatting with your matched founder!

## Features Available in Jitsi

- 🎥 HD video conferencing
- 🎤 Audio chat
- 💬 Text chat
- 🖥️ Screen sharing
- ✋ Raise hand
- 📊 Background blur/replacement
- 📹 Recording (optional)
- 🔇 Mute all
- 📱 Mobile app available

## Room Naming Convention

Format: `FounderChat-{chat_id}`

Example: `FounderChat-c12a34b5`

- **Unique**: Each coffee chat gets a unique room
- **Permanent**: The same link works for all meetings
- **Memorable**: Easy to share and remember
- **Secure**: Only people with the link can join

## Security & Privacy

1. **Link-Based Access**: Only users with the link can join
2. **No Recording by Default**: Users control recordings
3. **End-to-End Encryption**: Available for 1-on-1 calls
4. **Self-Contained**: Each chat has its own isolated room
5. **No Data Storage**: Jitsi doesn't store conversation data

## Future Enhancements

Potential improvements for the meeting feature:

- [ ] Add calendar integration (Google Calendar, Outlook)
- [ ] Send email reminders with meeting link
- [ ] Add meeting agenda/notes section
- [ ] Post-meeting feedback form
- [ ] Meeting duration tracking
- [ ] Automatic follow-up scheduling
- [ ] Integration with Slack/Discord for notifications
- [ ] Custom Jitsi instance (self-hosted) for branding

## Alternative Video Platforms

While we chose Jitsi, here are alternatives that could be integrated:

| Platform | Pros | Cons |
|----------|------|------|
| **Jitsi** | Free, no account, open-source | Basic UI |
| Google Meet | Familiar, reliable | Requires Google account |
| Zoom | Feature-rich | Account needed, time limits |
| Microsoft Teams | Enterprise features | Complex setup |
| Whereby | Simple, elegant | Limited free tier |
| Daily.co | Developer-friendly API | Paid plans only |

## API Endpoints

### Generate Meeting Link (Automatic)
```
POST /api/coffee-chats/{chat_id}/select-slot
```

**Request:**
```json
{
  "slot_id": "ps12a34b5",
  "user_id": "u12a34b5"
}
```

**Response:**
```json
{
  "message": "Time slot confirmed!",
  "scheduled_time": "2024-12-25T14:00:00Z",
  "meeting_link": "https://meet.jit.si/FounderChat-c12a34b5"
}
```

### Retrieve Coffee Chat Details
```
GET /api/coffee-chats/{user_id}
```

Returns all coffee chats including confirmed ones with meeting links.

## Testing the Feature

1. **Create Two Users**: Login as two different founders
2. **Submit Check-in**: User 1 submits a check-in with needs
3. **Accept Match**: User 2 accepts the match as an expert
4. **Propose Slots**: User 2 proposes 3 time slots
5. **Select Slot**: User 1 selects a time slot
6. **Get Link**: Both users see the Jitsi link
7. **Test Meeting**: Click "Join Video Call" to test

## Troubleshooting

### Link Not Showing
- Ensure the time slot was properly selected
- Check that the coffee chat status is "confirmed"
- Verify the meeting_link field is populated in the database

### Can't Join Meeting
- Check browser permissions for camera/microphone
- Try a different browser (Chrome recommended)
- Disable browser extensions that might block video
- Check internet connection

### Meeting Room Empty
- Verify both users have the correct link
- Check the scheduled time
- Ensure users are joining the same room URL

## Code Changes Summary

### Files Modified:
1. **`app.py`** (Line 549-559): Changed Google Meet mock to Jitsi
2. **`static/js/app_new.js`** (Lines 580-593, 699): Enhanced UI for Jitsi meeting
3. **`static/js/app.js`** (Lines 528-541, 641): Same changes for backward compatibility

### Key Changes:
- Meeting link format: `https://meet.jit.si/FounderChat-{chat_id}`
- Enhanced UI with prominent "Join Video Call" button
- Better success messages with clear instructions
- Visual improvements for confirmed meetings

---

**Built with ❤️ for the Founder Community**

For questions or support, contact the development team.





