# Quick Reference Guide 📚

**Last Updated:** December 22, 2025
**Current Sprint:** Sprint 3 Complete ✅

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
| `app/models.py` | Database models (User, CheckIn) |
| `app/mindfulness_tracker_app.py` | All routes and logic |
| `app/config.py` | Configuration from .env |
| `.env` | Environment variables (SECRET_KEY, DATABASE_URL) |
| `PLANNING.md` | Sprint planning and progress |
| `CODE_WALKTHROUGH.md` | Detailed code documentation |

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
| `/check-in` | GET/POST | Yes | Daily mood check-in |
| `/already-checked-in` | GET | Yes | Duplicate check-in message |
| `/practice` | GET | Yes | Practice page (Sprint 3) |

---

## 💾 Database Models

### User
- `id`: Integer (PK)
- `username`: String(20), unique
- `email`: String(120), unique
- `password_hash`: String(128)
- `created_at`: DateTime
- `checkins`: Relationship to CheckIn

### CheckIn
- `id`: Integer (PK)
- `user_id`: Integer (FK to User)
- `mood`: String(20) - Happy, Calm, Anxious, Sad
- `body_feeling`: String(200), optional
- `created_at`: DateTime

---

## 🎨 UI Components

**Mood Emojis:**
- 😊 Happy
- 😌 Calm
- 😰 Anxious
- 😔 Sad

**Color Palette:**
- Primary: `#C3521A` (burnt orange)
- Secondary: `#E67E3C` (lighter orange)
- Neutral: `#6c757d`

**Animations:**
- Button hover: `translateY(-2px)`
- Leaf sway: `rotate(-5deg to 5deg)`
- Meditation float: `translateY(-10px)`

---

## 📊 Sprint Progress

| Sprint | Status | Features |
|--------|--------|----------|
| 0 | ✅ Complete | Setup, database, git |
| 1 | ✅ Complete | Auth system, signup/login |
| 2 | ✅ Complete | Check-in, mood tracking, UI |
| 3 | ⏳ Next | AI integration, practices |
| 4 | 📋 Planned | Journal, feedback |
| 5 | 📋 Planned | Styling polish |
| 6 | 📋 Planned | Dashboard, history |

---

## 🔧 Environment Variables

```bash
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=sqlite:///mindfulness_tracker.db
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-api-key  # For Sprint 3
```

---

## 🧪 Testing Checklist

**Before Each Commit:**
- [ ] Test signup flow
- [ ] Test login/logout
- [ ] Test check-in (happy path)
- [ ] Test duplicate check-in validation
- [ ] Test mobile responsiveness
- [ ] Check browser console for errors
- [ ] Verify database updates

---

## 🐛 Common Issues

### "Login form not working"
- **Fix:** Restart Flask server (Ctrl+C, then `python run.py`)

### "Database connection error"
- **Fix:** Check `.env` has `DATABASE_URL=sqlite:///mindfulness_tracker.db`

### "flask command not found"
- **Fix:** Run `source venv/bin/activate` first

### "Module not found"
- **Fix:** Run `pip install -r requirements.txt`

---

## 📦 Dependencies

**Core:**
- Flask 3.1.0
- Flask-Login 0.6.3
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.1.0

**Database:**
- psycopg2-binary 2.9.10 (PostgreSQL)
- SQLite (built-in)

**Utilities:**
- python-dotenv
- Werkzeug (password hashing)

---

## 🎯 MVP Features Status

| Feature | Status |
|---------|--------|
| User Authentication | ✅ Done |
| Daily Mood Check-In | ✅ Done |
| One-Per-Day Validation | ✅ Done |
| Beautiful UI | ✅ Done |
| Mobile Responsive | ✅ Done |
| AI Practices | ⏳ Sprint 3 |
| Journal Prompts | ⏳ Sprint 3 |
| Journal Entry | 📋 Sprint 4 |
| Feedback System | 📋 Sprint 4 |
| Dashboard | 📋 Sprint 6 |

---

## 📖 Documentation

**Read These:**
- [PLANNING.md](PLANNING.md) - Sprint breakdown
- [CODE_WALKTHROUGH.md](CODE_WALKTHROUGH.md) - Detailed code docs
- [SPRINT_3_PREP.md](SPRINT_3_PREP.md) - Next sprint guide
- [SPRINT_2_SUMMARY.md](SPRINT_2_SUMMARY.md) - What we built

---

## 🔗 Useful Links

**Documentation:**
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Bootstrap: https://getbootstrap.com/docs/5.3/

**Tools:**
- OpenAI Platform: https://platform.openai.com/
- Render Dashboard: https://dashboard.render.com/

---

## 💡 Tips

1. **Always activate venv first:** `source venv/bin/activate`
2. **Restart Flask after .env changes:** Ctrl+C, then run again
3. **Check migrations before coding:** `flask db current`
4. **Test in incognito:** Avoid session caching issues
5. **Use git branches:** Create feature branches for new work
6. **Commit often:** Small, focused commits are better

---

## 🎓 Learning Resources

**Next Topics to Study:**
- OpenAI API integration
- Prompt engineering for AI
- JSON parsing in Python
- Error handling best practices
- Database query optimization

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
flask db downgrade

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

**Happy coding! 🌿**
