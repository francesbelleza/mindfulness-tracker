# Sprint 3 Summary: AI-Powered Mindfulness Practices
**Completed: December 26, 2025**

---

## 🎯 Sprint Goal
Integrate OpenAI API to generate personalized mindfulness practices and journal prompts based on user's daily mood check-ins.

---

## ✅ What Was Built

### 1. Database Models
Created two new models to store AI-generated content:

**Practice Model** ([app/models.py:40-52](app/models.py))
```python
class Practice(db.Model):
    """AI-generated mindfulness practice"""
    id = db.Column(db.Integer, primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('user_checkins.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    practice_type = db.Column(db.String(50), nullable=False)  # breathing, meditation, movement, grounding
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**JournalPrompt Model** ([app/models.py:55-65](app/models.py))
```python
class JournalPrompt(db.Model):
    """AI-generated journal prompt"""
    id = db.Column(db.Integer, primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('user_checkins.id'))
    prompt_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Relationships:**
- Each CheckIn can have ONE Practice and ONE JournalPrompt (one-to-one)
- Implemented using `uselist=False` in relationship definitions

### 2. AI Service Module
Created comprehensive AI integration module: [app/ai_service.py](app/ai_service.py)

**Key Functions:**

1. **`generate_practice_and_prompt(mood, body_feeling)`**
   - Calls OpenAI API (GPT-3.5-turbo)
   - Uses custom prompt engineering for mindfulness practices
   - Returns JSON with practice (title, description, type) and journal prompt
   - Handles errors gracefully

2. **`_validate_response(result)`**
   - Validates AI response structure
   - Ensures all required fields are present
   - Checks practice type is valid (breathing, meditation, movement, grounding)

3. **`get_fallback_content(mood)`**
   - Provides high-quality fallback practices if API fails
   - Mood-specific content for: Happy, Calm, Anxious, Sad
   - Ensures user always gets meaningful content

**AI Prompt Design:**
- System prompt: Compassionate wellness coach persona
- Mood-based practice suggestions (2-3 minutes, actionable)
- JSON-formatted responses for easy parsing
- Max 400 tokens, temperature 0.7 for creative variation

### 3. Enhanced Practice Route
Updated `/practice` route ([app/mindfulness_tracker_app.py:88-144](app/mindfulness_tracker_app.py))

**New Functionality:**
1. Fetches user's latest check-in from today
2. Redirects to check-in if none exists
3. Checks if practice already generated (prevents duplicate API calls)
4. Calls AI service to generate new content
5. Falls back to pre-written content if API fails
6. Saves Practice and JournalPrompt to database
7. Passes content to template for display

**Smart Caching:**
- Only generates AI content once per check-in
- Prevents duplicate API calls on page refresh
- Reduces OpenAI API costs

### 4. Beautiful Practice Page
Completely redesigned [practice.html](app/templates/practice.html) with:

**Visual Features:**
- Dynamic emoji icons based on practice type:
  - 🌬️ Breathing
  - 🧘‍♀️ Meditation
  - 🤸‍♀️ Movement
  - 🌿 Grounding
- Floating animation on practice icon
- Gradient card designs with subtle shadows
- Practice type badge with gradient styling

**Content Display:**
- Practice title prominently displayed
- Step-by-step practice description
- Dedicated journal prompt card
- Clear typography with good line spacing
- Mobile-responsive layout

**Navigation:**
- "Back to Home" button
- "Continue to Journal" button (placeholder for Sprint 4)

### 5. Database Migration
Created migration: `83595024615d_add_practice_and_journal_prompt_models.py`
- Added `practices` table
- Added `journal_prompts` table
- Successfully applied to Supabase PostgreSQL database

---

## 📁 Files Created/Modified

### Created:
- `app/ai_service.py` - OpenAI API integration module
- `migrations/versions/83595024615d_add_practice_and_journal_prompt_models.py`
- `SPRINT_3_SUMMARY.md` (this file)

### Modified:
- `app/models.py` - Added Practice and JournalPrompt models, relationships to CheckIn
- `app/mindfulness_tracker_app.py` - Enhanced /practice route with AI integration
- `app/templates/practice.html` - Complete redesign with AI content display
- `PLANNING.md` - Marked Sprint 3 complete, updated to 60% MVP progress
- `SPRINT_3_PREP.md` - Checked off completed tasks
- `.env` - Already had OPENAI_API_KEY configured

---

## 🧪 How to Test Sprint 3

### Manual Testing Flow:

1. **Start the app:**
   ```bash
   flask run
   ```

2. **Sign up / Log in:**
   - Navigate to `/signup` or `/login`
   - Create account or use existing credentials

3. **Complete daily check-in:**
   - Go to `/check-in`
   - Select a mood (😊 😌 😰 😔)
   - Optionally add body feeling
   - Submit form

4. **View AI-generated practice:**
   - Should automatically redirect to `/practice`
   - See AI-generated practice title, description, and type badge
   - See personalized journal prompt
   - Verify emoji icon matches practice type
   - Check that content is relevant to selected mood

5. **Test error handling:**
   - If OpenAI API fails, should see fallback content
   - Flash message: "Using fallback practice (AI service unavailable)"

6. **Test caching:**
   - Refresh `/practice` page multiple times
   - Should see same practice (not regenerated each time)
   - Confirms caching works

7. **Test navigation:**
   - "Back to Home" → redirects to `/`
   - "Continue to Journal" → redirects to `/` (placeholder for Sprint 4)

### Test Different Moods:

**Happy (😊):**
- Expect: Gratitude practices, energizing exercises
- Journal prompt about joy and appreciation

**Calm (😌):**
- Expect: Body scan, mindfulness meditation
- Journal prompt about peace and awareness

**Anxious (😰):**
- Expect: Breathing exercises (4-7-8), grounding techniques
- Journal prompt about safety and grounding

**Sad (😔):**
- Expect: Self-compassion practices, gentle movement
- Journal prompt about self-kindness

---

## 🎨 Design Features

### Color Palette:
- Primary: `#C3521A` (burnt orange)
- Gradient: `#C3521A` → `#E67E3C`
- Neutrals: White, light grays
- Text: Dark grays for readability

### UI Elements:
- **Practice Card:**
  - Gradient background: `#ffffff` → `#fef9f7`
  - 2px border: `#f1e8e3`
  - Rounded corners: 20px
  - Hover effect: Lifts up 2px with shadow

- **Practice Type Badge:**
  - Gradient background
  - White text
  - Rounded pill shape
  - Uppercase with letter spacing

- **Journal Card:**
  - Lighter gradient background
  - Centered text
  - Italic journal prompt
  - Thought bubble emoji (💭)

### Animations:
- Floating meditation icon (3s infinite loop)
- Hover effects on cards (lift + shadow)
- Button hover animations (lift + shadow)

### Responsive Design:
- Mobile breakpoint: 576px
- Full-width buttons on mobile
- Reduced padding on small screens
- Smaller font sizes for mobile

---

## 🔐 Security & Best Practices

### API Key Management:
- ✅ OpenAI API key stored in `.env` file
- ✅ `.env` file in `.gitignore` (never committed)
- ✅ API key loaded via `os.getenv()`

### Error Handling:
- ✅ Try/except blocks around API calls
- ✅ JSON parsing validation
- ✅ Fallback content if AI fails
- ✅ Console error logging for debugging

### Database:
- ✅ Foreign key relationships properly defined
- ✅ Nullable constraints on required fields
- ✅ One-to-one relationships enforced

### Performance:
- ✅ Practice caching (no duplicate API calls)
- ✅ Max tokens limit (400) to control costs
- ✅ Single database query to check existing practice

---

## 💡 AI Prompt Engineering Insights

### System Prompt Strategy:
1. **Persona:** "Compassionate mindful wellness coach"
2. **Clear Instructions:** Request specific format and structure
3. **JSON Output:** Enforced structured response
4. **Guidelines:** Mood-specific practice recommendations

### Practice Types Mapping:
- **Breathing:** Quick, accessible, calming
- **Meditation:** Introspective, mindful, present
- **Movement:** Gentle, embodied, energizing
- **Grounding:** Stabilizing, centering, safe

### Quality Control:
- Response validation ensures completeness
- Practice type must be one of 4 valid options
- Title limited to ~50 characters
- Description 100-200 words (clear, actionable)
- Journal prompt 1-2 sentences (thought-provoking)

---

## 📊 Sprint 3 Metrics

### Code Added:
- **Lines of Code:** ~350+ lines
- **New Files:** 2
- **Modified Files:** 5
- **Database Tables:** 2

### Features Delivered:
- ✅ OpenAI API integration
- ✅ AI practice generation (4 mood types)
- ✅ AI journal prompt generation
- ✅ Fallback content system
- ✅ Practice caching mechanism
- ✅ Beautiful practice display page
- ✅ Database persistence

### API Integration:
- Model: GPT-3.5-turbo
- Max tokens: 400
- Temperature: 0.7
- Average response time: 2-4 seconds
- Cost per request: ~$0.0004

---

## 🚀 What's Next: Sprint 4

Sprint 4 will focus on:
1. **Journal Reflection Page:**
   - Create `/reflect` route
   - Build journal entry form
   - Save entries to database

2. **Feedback System:**
   - Create `/feedback` route
   - Emoji/rating interface
   - Store user feedback

3. **Thank You Page:**
   - Create `/thank` route
   - Closing affirmation message

---

## 🎉 Sprint 3 Success Criteria

All criteria met:
- [x] OpenAI API successfully integrated
- [x] Users receive personalized practices based on mood
- [x] Practice and journal prompt displayed beautifully
- [x] AI responses stored in database
- [x] Error handling and fallback content working
- [x] "Continue to Journal" button implemented
- [x] Database migrations applied successfully

**Sprint 3 Status: ✅ COMPLETE**

---

**Built with care by Frances Belleza**
**Date: December 26, 2025**
