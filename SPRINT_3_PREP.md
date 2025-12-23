# Sprint 3 Preparation Guide
**AI-Powered Mindfulness Practices & Journal Prompts**

---

## 🎯 Sprint 3 Goals

Build an AI-powered feature that:
1. Takes the user's mood from their daily check-in
2. Generates a personalized mindfulness practice (breathing, meditation, movement, etc.)
3. Creates a reflective journal prompt
4. Displays both on the practice page

---

## 📋 What Needs to Be Done

### 1. OpenAI API Setup
- [ ] Get OpenAI API key from https://platform.openai.com/api-keys
- [ ] Add to `.env` file: `OPENAI_API_KEY=your-actual-key-here`
- [ ] Install OpenAI Python package: `pip install openai`
- [ ] Update `requirements.txt`

### 2. Database Models

**Create two new models:**

```python
class Practice(db.Model):
    """AI-generated mindfulness practice"""
    id = db.Column(db.Integer, primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('user_checkins.id'))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    practice_type = db.Column(db.String(50))  # breathing, meditation, movement, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JournalPrompt(db.Model):
    """AI-generated journal prompt"""
    id = db.Column(db.Integer, primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('user_checkins.id'))
    prompt_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 3. AI Service Module

**Create `app/ai_service.py`:**
- Function to call OpenAI API
- Mood-based prompt engineering
- Parse AI response
- Error handling

### 4. Update `/practice` Route

**Current state:** Placeholder page
**New functionality:**
- Get user's latest check-in (mood + body feeling)
- Call AI service to generate practice + prompt
- Save to database
- Pass to template

### 5. Update Practice Template

**Enhance `practice.html`:**
- Display AI-generated practice (title + description)
- Show journal prompt
- Add "Continue to Journal" button
- Beautiful, calming design

---

## 🤖 AI Prompt Design

### System Prompt Template
```
You are a mindful wellness coach. Based on the user's mood, suggest:
1. A short mindfulness practice (2-3 minutes)
2. A reflective journal prompt

User's mood: {mood}
Body feeling: {body_feeling}

Respond in JSON format:
{
  "practice": {
    "title": "Practice name",
    "description": "Step-by-step instructions",
    "type": "breathing|meditation|movement|grounding"
  },
  "journal_prompt": "A thoughtful question or reflection prompt"
}
```

### Mood-to-Practice Mapping

**Happy (😊):**
- Practice: Gratitude meditation, energizing movement
- Prompt: "What brought you joy today?"

**Calm (😌):**
- Practice: Body scan, mindful breathing
- Prompt: "What does peace feel like in your body?"

**Anxious (😰):**
- Practice: 4-7-8 breathing, grounding techniques
- Prompt: "What do you need to feel safe right now?"

**Sad (😔):**
- Practice: Compassionate self-talk, gentle stretching
- Prompt: "What would you say to comfort a friend feeling this way?"

---

## 🛠️ Technical Implementation

### File Structure
```
app/
├── __init__.py
├── models.py           # Add Practice & JournalPrompt models
├── ai_service.py       # NEW: AI integration module
├── mindfulness_tracker_app.py  # Update /practice route
└── templates/
    └── practice.html   # Update with AI content display
```

### Dependencies to Install
```bash
pip install openai
pip freeze > requirements.txt
```

### Migration Command
```bash
flask db migrate -m "add practice and journal prompt models"
flask db upgrade
```

---

## 🎨 UI Design for Practice Page

### Layout Ideas
```
┌─────────────────────────────────────┐
│  🧘 Your Personalized Practice      │
├─────────────────────────────────────┤
│                                     │
│  [Practice Title]                   │
│  Type: Breathing Exercise           │
│                                     │
│  [Step-by-step description with     │
│   calming formatting]               │
│                                     │
├─────────────────────────────────────┤
│  💭 Journal Prompt                  │
│                                     │
│  "What does peace feel like         │
│   in your body right now?"          │
│                                     │
├─────────────────────────────────────┤
│  [Continue to Journal] button       │
└─────────────────────────────────────┘
```

---

## 💡 OpenAI API Tips

### Rate Limits (Free Tier)
- ~3 requests per minute
- Monitor usage at https://platform.openai.com/usage

### Best Practices
1. **Use GPT-3.5-turbo** for cost-effective responses
2. **Set max_tokens** to limit response length (e.g., 300)
3. **Cache responses** to avoid duplicate API calls
4. **Handle errors gracefully** (network issues, rate limits)

### Example API Call
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a mindful wellness coach..."},
        {"role": "user", "content": f"User is feeling {mood}"}
    ],
    max_tokens=300,
    temperature=0.7
)
```

---

## 🧪 Testing Sprint 3

### Test Cases
1. **Happy mood check-in** → Should get uplifting practice
2. **Anxious mood check-in** → Should get calming practice
3. **API failure** → Should show graceful error message
4. **No check-in today** → Should redirect to check-in page

### Manual Testing Flow
1. Log in
2. Complete daily check-in with mood
3. Get redirected to `/practice`
4. See AI-generated practice + prompt
5. Click "Continue to Journal"

---

## 📚 Resources

**OpenAI Documentation:**
- API Quickstart: https://platform.openai.com/docs/quickstart
- Chat Completions: https://platform.openai.com/docs/guides/chat

**Mindfulness Practices Reference:**
- 4-7-8 Breathing
- Body Scan Meditation
- 5-4-3-2-1 Grounding
- Loving-Kindness Meditation

**Journal Prompt Ideas:**
- Self-reflection questions
- Gratitude prompts
- Emotional exploration
- Body awareness

---

## 🚨 Potential Challenges

### 1. API Key Management
- **Issue:** Exposing API key in code
- **Solution:** Use `.env` file, never commit keys

### 2. Rate Limiting
- **Issue:** Too many requests
- **Solution:** Cache responses, implement request throttling

### 3. Response Parsing
- **Issue:** AI response not in expected format
- **Solution:** Request JSON format, validate structure

### 4. Cost Management
- **Issue:** Unexpected API costs
- **Solution:** Set usage limits in OpenAI dashboard

---

## ✅ Definition of Done (Sprint 3)

Sprint 3 is complete when:
- [ ] OpenAI API is integrated and working
- [ ] Users receive personalized practices based on mood
- [ ] Practice and journal prompt are displayed beautifully
- [ ] AI responses are stored in database
- [ ] Error handling is in place
- [ ] "Continue to Journal" button works (can redirect to placeholder)
- [ ] All routes tested manually
- [ ] Database migrations applied

---

## 🎯 Success Metrics

**Technical:**
- API calls succeed > 95% of the time
- Response time < 3 seconds
- No API key exposure

**User Experience:**
- Practices feel relevant to mood
- Instructions are clear and actionable
- UI is calming and intuitive

---

**Ready to start? Tomorrow we'll build something amazing! 🌿**
