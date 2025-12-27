# Mindfulness Tracker App

### About the Project
Mindfulness Tracker is a compassionate, AI-powered web app designed to help users check in with themselves twice daily (morning and night). Through time-aware mood tracking, personalized mindfulness practices with natural AI voice narration, voice-to-text journaling, and practice feedback, the app fosters emotional awareness and grounding.

It provides:
- **Morning and night check-ins** with time-of-day awareness
- **AI-generated mindfulness practices** tailored to your mood and time of day
- **Natural voice-guided meditation** with calm, meditative pacing
- **Voice-to-text journaling** for easy reflection
- **Practice feedback system** to improve future recommendations
- **Session closure** with personalized affirmations

> Read more about the vision:
> **[My Blog Post](https://medium.com/@belleza.frances/my-app-development-journey-high-level-vision-from-ideation-to-planning-d6b0bbc3fc66)**

---

## Current Features (Sprint 0-4 Complete)

### User Authentication
- Secure sign up and login system
- Password hashing with Flask-Login
- Session management

### Morning and Night Check-Ins
- Time-of-day selection (Morning or Night)
- Two check-ins per day (one morning, one night)
- Four mood options: Happy, Calm, Anxious, Sad
- Required body feeling input for holistic awareness
- AI generates context-appropriate practices based on time of day

### AI-Powered Mindfulness Practices
- **OpenAI GPT-3.5-turbo** generates personalized practices based on:
  - Current mood
  - Body sensations
  - Time of day (morning practices are energizing, night practices are calming)
- Practice types: Breathing, Meditation, Movement, Grounding
- Fallback content system if API fails

### Natural Voice Meditation
- **ElevenLabs Text-to-Speech** generates natural-sounding audio
- Lily voice (Velvety Actress) - calm, meditative tone
- Optimized settings:
  - Slower pacing (0.85x speed) for meditation
  - Three-tier pause system for natural breathing pauses
  - Stability tuned for consistent delivery
- Custom HTML5 audio player with:
  - Play/Pause controls
  - Progress bar with seek functionality
  - Time display

### Personalized Journal Prompts
- AI-generated prompts tailored to mood, body sensations, and time of day
- Prompts complement (don't duplicate) structured questions
- Thought-provoking emotional reflection questions
- Stored with each practice for easy access

### Structured Journal Data Collection
- **Voice-to-Text Journaling** via Web Speech API
- Type or speak journal reflections with real-time transcription
- Separate input fields for structured data:
  - **Morning:** Daily intention ("What is your intention for the day?")
  - **Night:** Self-care reflection ("What did you do for yourself today?")
  - **Night:** Tomorrow's goal ("What do you want to accomplish tomorrow?")
- AI prompt response captured in main textarea
- Character counter and editable transcriptions
- Enables future analytics and trend visualization

### Practice Feedback System
- Emoji rating scale (1-5) for practice effectiveness
- "Did this help?" Yes/No question
- Pacing feedback (Too fast, Just right, Too slow)
- Data stored for future AI personalization

### Session Closure
- Time-of-day specific affirmations (morning/night)
- Authentic affirmations without fake quote attributions
- Session completion stats (check, journal, feedback icons)
- Simple "Return Home" navigation
- Encouraging footer message
- Sense of completion and closure

---

## Tech Stack

**Frontend:**
- HTML5
- CSS3 (responsive design, mobile-first)
- JavaScript (audio player controls, Web Speech API)

**Backend:**
- Python 3.11
- Flask (web framework)
- Flask-Login (authentication)
- SQLAlchemy ORM (database management)

**Database:**
- PostgreSQL (via Supabase) - Production
- SQLite - Local development/testing

**AI & Voice:**
- OpenAI API (GPT-3.5-turbo) - Text generation
- ElevenLabs API (eleven_multilingual_v2) - Voice synthesis
- Custom prompt engineering with pause notation
- Natural voice meditation narration

**Hosting:**
- Flask development server (local)
- Deployment: TBD (Render.com planned)

---

## Project Structure

```
mindfulness-tracker/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models (User, CheckIn, Practice, JournalEntry, PracticeFeedback)
│   ├── mindfulness_tracker_app.py  # Routes and logic
│   ├── ai_service.py            # OpenAI + ElevenLabs integration
│   ├── static/
│   │   └── audio/               # Generated meditation audio files
│   └── templates/
│       ├── base.html            # Base template
│       ├── index.html           # Landing page
│       ├── signup.html          # User registration
│       ├── login.html           # User login
│       ├── check_in.html        # Morning/night mood check-in
│       ├── practice.html        # AI practice + audio player + journal prompt
│       ├── reflect.html         # Voice-to-text journal with structured inputs
│       ├── feedback.html        # Emoji rating + detailed feedback
│       ├── thank.html           # Session closure with affirmations
│       └── already_checked_in.html
├── migrations/                  # Database migrations (3 migrations in Sprint 4)
├── docs/                        # Documentation
│   ├── SPRINT_2_SUMMARY.md
│   ├── SPRINT_3_SUMMARY.md
│   ├── SPRINT_4_SUMMARY.md
│   ├── ai-flow.md
│   ├── database-schema.md
│   └── user-flow.md
├── .env                         # API keys (not in repo)
├── requirements.txt             # Python dependencies
├── PLANNING.md                  # Sprint planning
└── README.md                    # This file
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- pip
- PostgreSQL (or use Supabase)
- OpenAI API key
- ElevenLabs API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/francesbelleza/mindfulness-tracker.git
   cd mindfulness-tracker
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   OPENAI_API_KEY=your_openai_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```

5. **Initialize database:**
   ```bash
   flask db upgrade
   ```

6. **Run the app:**
   ```bash
   flask run
   ```

7. **Open in browser:**
   Navigate to `http://127.0.0.1:5000`

---

## Usage

1. **Sign up** for an account
2. **Log in** with your credentials
3. **Complete check-in:**
   - Select time of day (Morning ☀️ or Night 🌙)
   - Select your mood (Happy, Calm, Anxious, Sad)
   - Describe how your body feels
4. **Receive personalized practice:**
   - View AI-generated mindfulness practice (tailored to time of day)
   - Play audio to hear guided meditation with calm voice narration
   - Preview your journal prompt
5. **Reflect on your experience:**
   - Respond to AI-generated journal prompt (type or speak)
   - Voice-to-text transcription with Speak button
   - Answer time-specific structured questions:
     - **Morning:** "What is your intention for the day?"
     - **Night:** "What did you do for yourself today?" + "What do you want to accomplish tomorrow?"
6. **Provide feedback:**
   - Rate the practice with emoji scale (😞 😐 🙂 😊 🤩)
   - Answer helpfulness and pacing questions
7. **Session closure:**
   - Receive personalized affirmation
   - See session completion stats
   - Return home when ready

---

## Development Progress

**Completed Sprints:**
- **Sprint 0:** Dev Environment + Cloud Setup
- **Sprint 1:** Authentication System
- **Sprint 2:** Daily Check-In Flow
- **Sprint 3:** AI Practices + Natural Voice
- **Sprint 4:** Journal & Feedback System + Structured Data Collection
  - Morning/Night check-ins with time-aware AI
  - Voice-to-text journaling with structured questions
  - Journal prompt refactoring (removed redundant table)
  - Practice feedback with emoji ratings
  - Session closure improvements

**Next Sprint:** Sprint 5 - Journal History & Dashboard

**Overall MVP Progress:** ~80% complete

See [PLANNING.md](PLANNING.md) for detailed sprint breakdown and [docs/SPRINT_4_SUMMARY.md](docs/SPRINT_4_SUMMARY.md) for Sprint 4 details.

---

## Design Philosophy

### Color Palette:
- Primary: `#C3521A` (burnt orange) - warmth, grounding
- Accent: Purple gradients - calm, meditation
- Neutrals: Whites and light grays - simplicity, clarity

### UI Principles:
- Clean, minimal interface
- Emoji-based interactions for accessibility
- Mobile-first responsive design
- Calm, spacious layouts
- Smooth animations and transitions

---

## Security & Privacy

- Passwords hashed with Werkzeug security
- API keys stored in environment variables (never committed)
- Session-based authentication with Flask-Login
- Foreign key constraints ensure data integrity
- HTTPS required for production (planned)

---

## Future Features

### Sprint 5 (Next):
- **Journal history dashboard** to view past entries
- **Filter journal entries** by date, mood, time of day
- **Search functionality** for journal entries
- **User dashboard** with:
  - Mood trends visualization
  - Check-in streak tracking
  - Practice completion stats
  - Intention, self-care, and goal tracking over time

### Sprint 6 & Beyond:
- **AI personalization** using practice feedback data
- Personalized practice recommendations based on history
- **Structured data analytics:**
  - Track all daily intentions
  - Self-care patterns and trends
  - Goal achievement tracking
- Calendar view of check-ins
- Daily reminder notifications
- Favorite/save practices feature
- Mood history visualization with charts
- Mobile app (iOS/Android)
- Breathing exercise animations

---

## License

This project is currently unlicensed. All rights reserved.

---

**Built with care, purpose, and mindfulness**
**Status:** In Active Development
**Last Updated:** December 26, 2025
