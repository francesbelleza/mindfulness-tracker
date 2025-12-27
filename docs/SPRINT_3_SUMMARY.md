# Sprint 3 Summary: AI-Powered Mindfulness Practices with Natural Voice
**Completed: December 26, 2025**

---

## 🎯 Sprint Goal
Integrate OpenAI API to generate personalized mindfulness practices and journal prompts based on user's daily mood check-ins, with natural AI-generated voice narration for guided meditation experiences.

---

## ✅ What Was Built

### 1. Database Models
Created two new models to store AI-generated content with audio support:

**Practice Model** ([app/models.py:40-53](app/models.py))
```python
class Practice(db.Model):
    """AI-generated mindfulness practice"""
    id = db.Column(db.Integer, primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('user_checkins.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    practice_type = db.Column(db.String(50), nullable=False)  # breathing, meditation, movement, grounding
    audio_file = db.Column(db.String(255), nullable=True)  # ElevenLabs TTS audio filename
    created_at = db.Column(db.DateTime, default=datetime.now)
```

**JournalPrompt Model** ([app/models.py:56-66](app/models.py))
```python
class JournalPrompt(db.Model):
    """AI-generated journal prompt"""
    id = db.Column(db.Integer, primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('user_checkins.id'))
    prompt_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
```

**Relationships:**
- Each CheckIn can have ONE Practice and ONE JournalPrompt (one-to-one)
- Implemented using `uselist=False` in relationship definitions

### 2. AI Service Module
Created comprehensive AI integration module: [app/ai_service.py](app/ai_service.py)

**Key Functions:**

#### 1. `generate_practice_and_prompt(mood, body_feeling)`
- Calls OpenAI API (GPT-3.5-turbo)
- Uses advanced prompt engineering for mindfulness practices
- Generates meditation-style spoken instructions with natural pauses
- Returns JSON with practice (title, description, type) and journal prompt
- Handles errors gracefully

**Advanced Pause System:**
```
- THREE ellipses (...  ...  ...) = 3-5 second meditative pauses for breathing
- TWO ellipses (...  ...) = 2-3 second pauses between instructions
- ONE ellipsis (...) = 1-2 second brief pauses
```

Example output:
```
"Find a comfortable position... ... ... When you're ready... ... gently close your eyes... ... ...
Take a deep, slow breath in... ... ... and exhale fully... ... ..."
```

#### 2. `generate_audio(practice_text, practice_id, mood)`
- Generates natural-sounding AI voice using **ElevenLabs Text-to-Speech API**
- Uses Lily voice (Velvety Actress) - calm, meditative voice for all moods
- Saves MP3 files to `app/static/audio/`
- Returns filename for database storage

**Voice Optimization Settings:**
```python
voice_settings={
    "stability": 0.75,         # Higher = more consistent, calmer delivery
    "similarity_boost": 0.5,   # Lower = softer, less harsh voice
    "speed": 0.85              # Slower speed for meditative pacing
}
```

**Technology Evolution:**
- ❌ Started with OpenAI TTS (sounded robotic and monotone)
- ✅ Switched to ElevenLabs API for natural, human-like voice
- ✅ Tested multiple voices (Jessica, Sarah, Matilda)
- ✅ Settled on Lily as single calm meditative voice
- ✅ Optimized stability, similarity, and speed settings
- ✅ Enhanced AI prompt with three-tier pause system

#### 3. `_validate_response(result)`
- Validates AI response structure
- Ensures all required fields are present
- Checks practice type is valid (breathing, meditation, movement, grounding)

#### 4. `get_fallback_content(mood)`
- Provides high-quality fallback practices if API fails
- Mood-specific content for: Happy, Calm, Anxious, Sad
- Ensures user always gets meaningful content
- All fallback practices include natural pause notation

### 3. Enhanced Practice Route
Updated `/practice` route ([app/mindfulness_tracker_app.py:87-153](app/mindfulness_tracker_app.py))

**New Functionality:**
1. Fetches user's latest check-in from today
2. Redirects to check-in if none exists
3. Checks if practice already generated (prevents duplicate API calls)
4. Calls AI service to generate new content
5. Falls back to pre-written content if API fails
6. Saves Practice and JournalPrompt to database
7. **Generates natural AI audio using ElevenLabs**
8. Updates practice with audio filename
9. Passes content to template for display

**Audio Generation Flow:**
```python
# Generate natural AI audio for the practice
audio_filename = generate_audio(
    ai_result['practice']['description'],
    practice_obj.id,
    latest_checkin.mood
)
if audio_filename:
    practice_obj.audio_file = audio_filename
    db.session.commit()
```

**Smart Caching:**
- Only generates AI content once per check-in
- Prevents duplicate API calls on page refresh
- Reduces OpenAI and ElevenLabs API costs
- Stores audio files permanently in static directory

### 4. Beautiful Practice Page with Audio Player
Completely redesigned [practice.html](app/templates/practice.html) with:

**Audio Player Features:**
- Custom HTML5 audio player with elegant UI
- Play/Pause button with emoji icons (▶️/⏸️)
- Progress bar with click-to-seek functionality
- Current time and total duration display
- Smooth animations and hover effects
- Purple gradient styling to complement burnt orange theme

**Audio Player UI:**
```
┌─────────────────────────────────────┐
│  ▶️  ████████░░░░░░  2:15 / 3:42   │
└─────────────────────────────────────┘
```

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
- Natural meditation-style description with pauses
- Audio player for guided practice (if audio generated)
- Dedicated journal prompt card
- Clear typography with good line spacing
- Mobile-responsive layout

**Navigation:**
- "Back to Home" button
- "Continue to Journal" button (placeholder for Sprint 4)

### 5. Database Migrations
Created three migrations:

1. **`83595024615d_add_practice_and_journal_prompt_models.py`**
   - Added `practices` table
   - Added `journal_prompts` table

2. **`ac508cdd8438_add_audio_file_to_practice_model.py`**
   - Added `audio_file` column to Practice model

3. **`ce9e059f4c6c_increase_password_hash_length_to_256.py`**
   - Updated password hash field to support longer hashes

All successfully applied to Supabase PostgreSQL database.

### 6. Additional UI Improvements
- Changed signup form label from "Username" to "Full Name" ([signup.html:15](app/templates/signup.html))
- Made body feeling field **required** in check-in form ([check_in.html:61](app/templates/check_in.html))

---

## 📁 Files Created/Modified

### Created:
- `app/ai_service.py` - OpenAI + ElevenLabs API integration module
- `app/static/audio/` - Directory for storing generated MP3 files
- `migrations/versions/83595024615d_add_practice_and_journal_prompt_models.py`
- `migrations/versions/ac508cdd8438_add_audio_file_to_practice_model.py`
- `migrations/versions/ce9e059f4c6c_increase_password_hash_length_to_256.py`
- `SPRINT_3_SUMMARY.md` (this file)

### Modified:
- `app/models.py` - Added Practice and JournalPrompt models with audio support
- `app/mindfulness_tracker_app.py` - Enhanced /practice route with AI + audio
- `app/templates/practice.html` - Complete redesign with audio player
- `app/templates/signup.html` - Changed "Username" to "Full Name"
- `app/templates/check_in.html` - Made body feeling required
- `PLANNING.md` - Marked Sprint 3 complete, updated to 60% MVP progress
- `.env` - Added ELEVENLABS_API_KEY
- `requirements.txt` - Added `openai` and `elevenlabs` packages

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
   - **Enter body feeling (required)**
   - Submit form

4. **View AI-generated practice with audio:**
   - Should automatically redirect to `/practice`
   - See AI-generated practice title, description, and type badge
   - **See audio player with play button**
   - **Click play to hear natural AI voice narration**
   - Test progress bar seeking
   - See personalized journal prompt
   - Verify emoji icon matches practice type
   - Check that content is relevant to selected mood

5. **Test audio player:**
   - Click play button (▶️ → ⏸️)
   - Verify audio plays with natural voice and pauses
   - Click on progress bar to seek
   - Verify time display updates
   - Listen for meditative pacing and natural pauses

6. **Test error handling:**
   - If OpenAI API fails, should see fallback content
   - Flash message: "Using fallback practice (AI service unavailable)"
   - Audio still generated for fallback content

7. **Test caching:**
   - Refresh `/practice` page multiple times
   - Should see same practice and audio (not regenerated)
   - Confirms caching works

8. **Test navigation:**
   - "Back to Home" → redirects to `/`
   - "Continue to Journal" → redirects to `/` (placeholder for Sprint 4)

### Test Different Moods:

**Happy (😊):**
- Expect: Gratitude practices, energizing exercises
- Journal prompt about joy and appreciation
- Voice should sound warm and appreciative

**Calm (😌):**
- Expect: Body scan, mindfulness meditation
- Journal prompt about peace and awareness
- Voice should sound very calm with spacious pauses

**Anxious (😰):**
- Expect: Breathing exercises (4-7-8), grounding techniques
- Journal prompt about safety and grounding
- Voice should sound reassuring with longer pauses

**Sad (😔):**
- Expect: Self-compassion practices, gentle movement
- Journal prompt about self-kindness
- Voice should sound compassionate and nurturing

---

## 🎨 Design Features

### Color Palette:
- Primary: `#C3521A` (burnt orange)
- Gradient: `#C3521A` → `#E67E3C`
- Audio Player: `#5a67d8` → `#7c3aed` (purple gradient)
- Neutrals: White, light grays
- Text: Dark grays for readability

### UI Elements:
- **Practice Card:**
  - Gradient background: `#ffffff` → `#fef9f7`
  - 2px border: `#f1e8e3`
  - Rounded corners: 20px
  - Hover effect: Lifts up 2px with shadow

- **Audio Player:**
  - Gradient container: `#f8f9fa` → `#fff`
  - Purple gradient play button
  - 60px circular button with hover scale
  - 6px progress bar with smooth fill animation
  - Time display in gray (current / total)

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
- Audio button scale on hover (1.1x)
- Smooth progress bar fill transitions

### Responsive Design:
- Mobile breakpoint: 576px
- Full-width buttons on mobile
- Reduced padding on small screens
- Smaller font sizes for mobile
- Audio player stacks vertically on mobile

---

## 🔐 Security & Best Practices

### API Key Management:
- ✅ OpenAI API key stored in `.env` file
- ✅ ElevenLabs API key stored in `.env` file
- ✅ `.env` file in `.gitignore` (never committed)
- ✅ API keys loaded via `os.getenv()`

### Error Handling:
- ✅ Try/except blocks around API calls
- ✅ JSON parsing validation
- ✅ Fallback content if AI fails
- ✅ Graceful audio generation failure (app works without audio)
- ✅ Console error logging for debugging

### Database:
- ✅ Foreign key relationships properly defined
- ✅ Nullable constraints on required fields
- ✅ One-to-one relationships enforced
- ✅ Audio files stored separately from database

### Performance:
- ✅ Practice caching (no duplicate API calls)
- ✅ Max tokens limit (400) to control costs
- ✅ Single database query to check existing practice
- ✅ Audio files served as static assets (fast delivery)
- ✅ Audio preload="metadata" for faster loading

### File Management:
- ✅ Audio directory created automatically if missing
- ✅ Unique filenames based on practice ID
- ✅ MP3 format for broad browser compatibility
- ✅ Audio files persist across sessions

---

## 💡 AI Prompt Engineering Insights

### System Prompt Strategy:
1. **Persona:** "Compassionate mindfulness meditation teacher"
2. **Voice-First Instructions:** "Write as if speaking directly to user in calm, guiding voice"
3. **Pause Notation:** Three-tier ellipsis system for natural meditation pacing
4. **JSON Output:** Enforced structured response
5. **Guidelines:** Mood-specific practice recommendations

### Pause System (Critical for Natural Voice):
```
Example meditation script with pauses:

"Find a comfortable position... ... ...
When you're ready... ... gently close your eyes... ... ...
Take a deep, slow breath in... ... ...
and exhale fully... ... ...
Notice the sensation of your breath... ... ...
Continue breathing naturally... ... ..."
```

**Why this matters:**
- TTS engines read ellipses as natural pauses
- Multiple ellipses create longer, more meditative pauses
- Creates spacious, calming meditation experience
- Prevents rushed, tutorial-like delivery

### Practice Types Mapping:
- **Breathing:** Quick, accessible, calming (4-7-8 breath, box breathing)
- **Meditation:** Introspective, mindful, present (body scan, loving-kindness)
- **Movement:** Gentle, embodied, energizing (mindful stretching, gentle flow)
- **Grounding:** Stabilizing, centering, safe (5-4-3-2-1 senses, earthing)

### Quality Control:
- Response validation ensures completeness
- Practice type must be one of 4 valid options
- Title limited to ~50 characters
- Description 150-250 words (spoken-style, with pauses)
- Journal prompt 1-2 sentences (thought-provoking)

---

## 🎙️ Voice Technology Deep Dive

### Why ElevenLabs Over OpenAI TTS?

**Initial Attempt: OpenAI TTS**
- ❌ Sounded robotic and monotone
- ❌ No natural pauses even with ellipses
- ❌ Fast, tutorial-like delivery
- ❌ Didn't feel like real guided meditation

**Final Solution: ElevenLabs**
- ✅ Natural, human-like voice quality
- ✅ Respects pause notation (ellipses)
- ✅ Customizable voice settings (stability, speed)
- ✅ Calm, meditative delivery
- ✅ Multiple voice options tested

### Voice Selection Process:
1. **Tested mood-specific voices:**
   - Happy → Jessica (Playful, Bright, Warm)
   - Calm → Lily (Velvety Actress)
   - Anxious → Sarah (Mature, Reassuring)
   - Sad → Matilda (Knowledgeable, Professional)

2. **User feedback:** "Voice sounds too harsh like a tutorial lesson"

3. **Final decision:** Single meditative voice (Lily) for all moods
   - More consistent experience
   - Calm and soothing across all practices
   - Better for meditation context

### Voice Settings Optimization:

```python
{
    "stability": 0.75,          # Calm, consistent delivery
    "similarity_boost": 0.5,    # Softer, less harsh tone
    "speed": 0.85               # 15% slower for meditation pacing
}
```

**Impact:**
- Higher stability = More predictable, calmer voice
- Lower similarity = Softer, less harsh sound
- Slower speed = More spacious, meditative feel

### Audio Technical Specs:
- **Format:** MP3 (broad compatibility)
- **Model:** eleven_multilingual_v2 (high quality)
- **Voice:** Lily (pFZP5JQG7iQjIQuC4Bku)
- **Average file size:** ~600KB - 900KB (2-4 minutes)
- **Storage:** app/static/audio/practice_{id}.mp3

---

## 📊 Sprint 3 Metrics

### Code Added:
- **Lines of Code:** ~500+ lines
- **New Files:** 4
- **Modified Files:** 8
- **Database Tables:** 2
- **Database Migrations:** 3
- **Audio Files Generated:** Dynamic (one per practice)

### Features Delivered:
- ✅ OpenAI API integration for practice generation
- ✅ ElevenLabs API integration for voice synthesis
- ✅ AI practice generation (4 mood types)
- ✅ AI journal prompt generation
- ✅ Natural voice meditation narration
- ✅ Custom HTML5 audio player
- ✅ Advanced pause system for meditation pacing
- ✅ Voice optimization (stability, speed, tone)
- ✅ Fallback content system
- ✅ Practice caching mechanism
- ✅ Audio file management
- ✅ Beautiful practice display page
- ✅ Database persistence with audio support

### API Integration:

**OpenAI (Text Generation):**
- Model: GPT-3.5-turbo
- Max tokens: 400
- Temperature: 0.7
- Average response time: 2-4 seconds
- Cost per request: ~$0.0004

**ElevenLabs (Voice Synthesis):**
- Model: eleven_multilingual_v2
- Voice: Lily (Velvety Actress)
- Settings: stability=0.75, similarity=0.5, speed=0.85
- Average response time: 5-8 seconds
- Cost per request: ~$0.15 (based on character count)

### Total API Costs Per Check-In:
- Text generation: $0.0004
- Voice synthesis: $0.15
- **Total: ~$0.15 per user check-in**

---

## 🚀 What's Next: Sprint 4

Sprint 4 will focus on:
1. **Journal Reflection Page:**
   - Create `/reflect` route
   - Build journal entry form
   - Save entries to database
   - Link to practice and check-in

2. **Feedback System:**
   - Create `/feedback` route
   - Emoji/rating interface
   - Store user feedback
   - Track practice effectiveness

3. **Thank You Page:**
   - Create `/thank` route
   - Closing affirmation message
   - Summary of session

---

## 🎉 Sprint 3 Success Criteria

All criteria met and exceeded:
- [x] OpenAI API successfully integrated
- [x] Users receive personalized practices based on mood
- [x] Practice and journal prompt displayed beautifully
- [x] AI responses stored in database
- [x] Error handling and fallback content working
- [x] "Continue to Journal" button implemented
- [x] Database migrations applied successfully
- [x] **Natural AI voice generation implemented**
- [x] **Custom audio player with seek controls**
- [x] **Meditation-style pauses optimized**
- [x] **Voice settings tuned for calm delivery**
- [x] **Audio files stored and served efficiently**

**Sprint 3 Status: ✅ COMPLETE**

---

## 🏆 Key Achievements

### Technical Excellence:
- Successfully integrated two AI APIs (OpenAI + ElevenLabs)
- Built robust error handling with graceful fallbacks
- Implemented efficient caching to minimize API costs
- Created custom audio player with full controls
- Optimized voice settings through iterative testing

### User Experience:
- Natural, human-like meditation voice
- Calm pacing with strategic pauses
- Beautiful, accessible UI design
- Smooth audio playback experience
- Personalized content based on mood and body feelings

### Innovation:
- Three-tier pause system for meditation narration
- Dynamic voice settings optimization
- Spoken-style AI prompt engineering
- Seamless integration of text and audio generation

---

**Built with care and mindfulness by Frances Belleza**
**Date: December 26, 2025**
**Sprint Duration: 1 day**
**Iterations: Multiple rounds of voice optimization**
**Status: Production-ready ✨**
