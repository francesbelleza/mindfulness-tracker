# Quick Reference Guide 📚

**Last Updated:** December 27, 2025
**Current Sprint:** Sprints 0-4 Complete ✅ | Sprint 5 In Progress

---

## 🚀 Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
python run.py

# Visit in browser
http://127.0.0.1:5000
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `run.py` | Application entry point |
| `app/__init__.py` | App factory, Flask extensions |
| `app/models.py` | Database models (User, CheckIn, Practice, etc.) |
| `app/mindfulness_tracker_app.py` | All routes and logic |
| `app/ai_service.py` | OpenAI & ElevenLabs TTS integration |
| `app/config.py` | Configuration from .env |
| `.env` | Environment variables (API keys, database) |
| `PLANNING.md` | Sprint planning and features |
| `docs/UI_DESIGN.md` | Complete UI design system |

---

## 🗄️ Database Commands

```bash
# Create a new migration
flask db migrate -m "description"

# Apply migrations
flask db upgrade

# Check current migration
flask db current

# Rollback last migration
flask db downgrade
```

---

## 🌐 Routes

| Route | Method | Auth | Description |
|-------|--------|------|-------------|
| `/` | GET | No | Home page |
| `/signup` | GET/POST | No | User registration |
| `/login` | GET/POST | No | User login |
| `/logout` | GET | Yes | User logout |
| `/check-in` | GET/POST | Yes | Daily mood check-in (morning/night) |
| `/already-checked-in` | GET | Yes | Already checked in message |
| `/practice` | GET | Yes | AI-generated practice with audio |
| `/reflect` | GET/POST | Yes | Journal entry with voice input |
| `/feedback` | GET/POST | Yes | Practice feedback (rating, pacing) |
| `/thank` | GET | Yes | Thank you page |
| `/app-feedback` | GET | No | App feedback form (Formspree) |
| `/thank-you-feedback` | GET | No | App feedback thank you |

---

## 💾 Database Models

### User
- `id`: Integer (PK)
- `username`: String(20), unique
- `email`: String(120), unique
- `password_hash`: String(256)
- `created_at`: DateTime

### CheckIn
- `id`: Integer (PK)
- `user_id`: Integer (FK to User)
- `mood`: String(20) - Happy, Calm, Anxious, Angry, Sad
- `body_feeling`: String(200), optional
- `time_of_day`: String(10) - Morning or Night
- `created_at`: DateTime

### Practice
- `id`: Integer (PK)
- `checkin_id`: Integer (FK to CheckIn)
- `title`: String(200)
- `description`: Text (AI-generated guided meditation)
- `practice_type`: String(50) - breathing, meditation, movement, grounding
- `journal_prompt`: Text (AI-generated)
- `audio_file`: String(255) - Supabase Storage URL (ElevenLabs TTS)
- `created_at`: DateTime

### JournalEntry
- `id`: Integer (PK)
- `checkin_id`: Integer (FK to CheckIn)
- `user_id`: Integer (FK to User)
- `entry_text`: Text - Response to journal prompt
- `intention_for_day`: String(500) - Morning only
- `self_care_today`: String(500) - Night only
- `goal_for_tomorrow`: String(500) - Night only
- `created_at`: DateTime

### PracticeFeedback
- `id`: Integer (PK)
- `practice_id`: Integer (FK to Practice)
- `user_id`: Integer (FK to User)
- `rating`: Integer - 1-5 scale
- `helped`: Boolean - Did this help?
- `pacing`: String(20) - Too fast, Just right, Too slow
- `created_at`: DateTime

---

## 🎨 UI Design System

**Theme:** Dark Sunset

**Colors:**
- Background: Orange-blue ombre gradient (6 stops)
- Cards: Solid dark teal (#1e3a45)
- Primary accent: Sunset peach (#e8a87c)
- Text: White with varying opacity

**Typography:**
- Font: ui-sans-serif (General Sans-like)
- Logo: font-weight 500, letter-spacing 4px
- Body: font-weight 300, letter-spacing 0.5px

**Mood Colors:**
- Happy: #f4d03f (yellow)
- Calm: #85c1e2 (light blue)
- Anxious: #e17055 (orange)
- Angry: #d63031 (red)
- Sad: #74b9ff (soft blue)

**Components:**
- Navbar: Transparent with dark blue logo
- Cards: Compact sizing (reduced from previous versions)
- Buttons: Sunset gradient for primary actions
- Audio player: SVG icons, vertically aligned

See [docs/UI_DESIGN.md](docs/UI_DESIGN.md) for complete design system.

---

## 🔧 Environment Variables

```bash
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:pass@host/db  # Supabase PostgreSQL
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SECRET_KEY=your-secret-key-here

# API Keys
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=sk_...
```

---

## 🧪 Testing Checklist

**Core Flows:**
- [ ] Signup → Login → Check-in (Morning)
- [ ] Check-in → Practice (audio plays)
- [ ] Practice → Journal (voice input works)
- [ ] Journal → Feedback → Thank you
- [ ] Second check-in same day (Night)
- [ ] Third check-in attempt (blocked)

**UI Tests:**
- [ ] Ombre background displays correctly
- [ ] Navbar is transparent with dark blue logo
- [ ] Mood grid is centered (5 moods)
- [ ] Selected mood shows dark blue indicator
- [ ] Audio player buttons aligned vertically
- [ ] Footer shows on all pages
- [ ] Mobile responsive (576px, 768px)

**Feature Tests:**
- [ ] Time restrictions (morning 3am-1pm, night 1pm-3am)
- [ ] Already checked in shows correct time message
- [ ] Practice duration ≥ 1 minute
- [ ] App feedback redirects to custom thank you page

---

## 📊 Sprint Status

| Sprint | Status | Features |
|--------|--------|----------|
| 0 | ✅ Complete | Setup, database, git |
| 1 | ✅ Complete | User authentication |
| 2 | ✅ Complete | Daily check-in flow |
| 3 | ✅ Complete | AI practices + natural voice (ElevenLabs TTS) |
| 4 | ✅ Complete | Journal & feedback system + structured data |
| 5 | 🚧 In Progress | Reflection Space, Profile, Settings, Privacy |

---

## 🚀 Features Implemented

**Sprint 1 Complete:**
- [x] User authentication (signup, login, logout)
- [x] Twice-daily check-ins (morning & night)
- [x] 5 moods (Happy, Calm, Anxious, Angry, Sad)
- [x] Time-based practice restrictions
- [x] AI-generated practices (OpenAI GPT-4o)
- [x] Text-to-speech audio (ElevenLabs Lily voice)
- [x] Minimum 1-minute practice duration
- [x] Journal prompts with voice input
- [x] Time-specific reflection questions
- [x] Practice feedback (rating, helpfulness, pacing)
- [x] App feedback form (Formspree integration)
- [x] Dark sunset UI theme
- [x] Compact button card sizing
- [x] Transparent navbar
- [x] Mobile responsive design

---

## 🐛 Common Issues

### "Audio not playing"
- **Fix:** Check Supabase Storage bucket `meditation-audio` is accessible
- **Fix:** Verify ElevenLabs API key in `.env`
- **Fix:** Ensure SUPABASE_URL and SUPABASE_KEY are set correctly

### "Time restriction not working"
- **Fix:** Check server time matches expected timezone
- **Fix:** Morning: 3am-1pm, Night: 1pm-3am

### "Formspree redirect failing"
- **Fix:** Check `_next` parameter in form
- **Fix:** Verify AJAX submission in app_feedback.html

### "Migration error"
- **Fix:** Delete `migrations/` folder and `flask db init` again
- **Fix:** Check database connection in `.env`

---

## 📦 Dependencies

**Core:**
- Flask 3.1.0
- Flask-Login 0.6.3
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.1.0

**Database:**
- psycopg2-binary 2.9.10 (PostgreSQL)

**AI/Audio:**
- openai 2.x
- elevenlabs 2.x
- supabase 2.x

**Utilities:**
- python-dotenv
- Werkzeug

---

## 💡 Tips

1. **Always activate venv first:** `source venv/bin/activate`
2. **Restart Flask after .env changes:** Ctrl+C, then run again
3. **Test time restrictions:** Mock current_hour in check_in route
4. **Clear database for testing:** `python3 clear_data.py`
5. **Check AI costs:** Monitor OpenAI & ElevenLabs TTS usage
6. **Supabase Storage:** Audio files stored in `meditation-audio` bucket
7. **Use git branches:** Create feature branches for new work

---

## 📞 Quick Commands

```bash
# Virtual environment
source venv/bin/activate
deactivate

# Run app
python run.py
flask run

# Database
flask db migrate -m "message"
flask db upgrade
python3 clear_data.py  # Clear all data except users

# Dependencies
pip install package-name
pip freeze > requirements.txt

# Git
git status
git add .
git commit -m "message"
git push origin branch-name
```

---

## 🔗 Useful Links

**Documentation:**
- Flask: https://flask.palletsprojects.com/
- OpenAI: https://platform.openai.com/docs
- ElevenLabs: https://elevenlabs.io/docs
- Supabase: https://supabase.com/docs
- Formspree: https://formspree.io/forms

**Tools:**
- OpenAI Platform: https://platform.openai.com/
- ElevenLabs Dashboard: https://elevenlabs.io/app
- Supabase Dashboard: https://supabase.com/dashboard
- Formspree: https://formspree.io/f/mvzorgoz

---

**Happy coding! 🌅**
