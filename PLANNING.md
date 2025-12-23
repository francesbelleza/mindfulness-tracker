# planning

## 📊 Current Progress: Sprint 2 Complete! 🎉

**Completed:** Sprint 0, Sprint 1, Sprint 2
**Next Up:** Sprint 3 - AI Integration
**Overall MVP Progress:** ~40% complete

---

## overview
This project is a mindfulness-based web application that invites
users to check in with themselves once a day. Through mood selection,
AI-powered suggestions, and reflective journaling, the app fosters
emotional awareness and grounding. The goal is to provide practices
and prompts that meet users where they are, using thoughtful design
and intentional flow.

---

## High-Level MVP Goals

[✅] **User Authentication System**
  - Users can sign up, log in, and log out securely. Only logged-in users can access core features.

[✅] **1x Daily Mood Check-In**
  - Users can check in once per day with a mood emoji and an optional body feeling. Repeat check-ins are gently blocked until the next day.

[⏳] **AI-Powered Practice Suggestions (via Wrapper)** ← NEXT (Sprint 3)
  - After checking in, the app uses an AI wrapper (like OpenAI or Claude) to suggest one mindfulness practice and one journal prompt based on the user's mood and internal research mappings.

[⏳] **Practice Display Page** ← Sprint 3
  - The selected mindfulness practice is shown on a dedicated page with a written description and (optionally) an image, audio, or video link to guide the user through the practice.

[] **Journal Reflection Page** ← Sprint 4
  - Users are given a journal prompt and can respond in a text box. Their reflections are saved securely.

[] **Feedback System** ← Sprint 4
  - After journaling, users are asked to rate how the practice felt using emojis or a simple rating. This will help future personalization.

[] **Thank You / Closing Page** ← Sprint 4
  - The app ends each session with a calming "Thank you" message or affirmation, creating closure for the user.

[✅] **Basic UI & Styling**
  - A clean, mobile-friendly interface using a burnt orange/white/black color palette with emoji-based interactions.

[✅] **Cloud-Based Data Storage**
  - User check-ins, reflections, and feedback are stored in SQLite locally (PostgreSQL available for deployment via Render), making the app scalable and persistent beyond local development.

---

## tech stack

**fronend**
- HTML5
- CSS3
- Jinja2 Templates

**backend**
- Python 3
- Flask
- Flask-Login
- SQLAlchemy ORM

**database**
- PostgreSQL (via Render.com)
- SQLite for local testing only (optional)

**AI/nlp**
- AI Wrapper (OpenAI or Claude)
- Custom prompt logic using internal research mappings

---

## sprint breakdown

### Sprint 0: Dev Environment + Cloud Setup
- [x] Set up local virtual environment (venv)
- [x] Install dependencies: Flask, Flask-Login, SQLAlchemy
- [x] Initialize Git repo & connect to GitHub
- [x] Create `requirements.txt` for version tracking
- [x] Create `.env` file and `config.py` to store DB credentials
- [x] Set up free PostgreSQL instance on Render (or Railway)
- [x] Replace SQLite URI with cloud PostgreSQL URI in `config.py`
- [x] Run a test to confirm cloud DB connection is working
- [x] Add `.env` to `.gitignore` so credentials stay private

---

### Sprint 1: User Authentication System
- [x] Create `User` model (username, email, hashed password)
- [x] Implement Flask-Login for session management
- [x] Build `/signup`, `/login`, and `/logout` routes
- [x] Add redirects after login/logout
- [x] Protect routes with `@login_required`

---

### ✅ Sprint 2: Daily Mood Check-In (COMPLETED)
- [x] Create `CheckIn` model (mood, body_feeling, created_at, user_id)
- [x] Build `/check-in` route + form (emoji mood + optional body input)
- [x] Add logic to allow one check-in per day
  - [x] If already checked in → redirect to `/already-checked-in`
  - [x] Else → save and redirect to `/practice`
- [x] Beautiful UI with emoji mood selector (😊 😌 😰 😔)
- [x] Smooth animations and transitions
- [x] Mobile-responsive design
- [x] Practice page placeholder created

---

### ⏳ Sprint 3: AI Suggestion Logic + Practice Page (NEXT)
**Goal:** Integrate OpenAI API to generate personalized mindfulness practices and journal prompts based on user's mood.

**Tasks:**
- [ ] Set up OpenAI API integration
  - [ ] Add OpenAI API key to `.env`
  - [ ] Install `openai` Python package
  - [ ] Create AI service module for API calls
- [ ] Create database models:
  - [ ] `Practice` model (exercise suggestions)
  - [ ] `JournalPrompt` model (reflection prompts)
- [ ] Update `/practice` route:
  - [ ] Fetch user's latest check-in (mood + body feeling)
  - [ ] Call OpenAI API with mood-based prompt
  - [ ] Parse AI response to extract practice + journal prompt
  - [ ] Store practice and prompt in database
  - [ ] Display on practice page
- [ ] Enhance `/practice` template:
  - [ ] Show AI-generated mindfulness practice
  - [ ] Display journal prompt
  - [ ] Add "Continue to Journal" button → `/reflect`
  - [ ] Optional: Add practice category icons/tags
- [ ] Create AI prompt engineering:
  - [ ] Design system prompt for mindfulness practices
  - [ ] Map moods to practice types (breathing, meditation, movement, etc.)
  - [ ] Ensure responses are calming, supportive, and actionable

---

### Sprint 4: Journal & Feedback
- [ ] Create `/reflect` route + form for journal entry
- [ ] Save journal entry to DB (linked to check-in)
- [ ] Create `/feedback` route with emoji/rating form
- [ ] Save feedback to DB
- [ ] Redirect to `/thank`

---

### 🚀 Sprint 5: Styling & Flow Polish
- [ ] Apply color theme
- [ ] Style emoji buttons, forms, spacing
- [ ] Clean up templates for readability and mobile
- [ ] Refine copy for tone and flow

---

###  ~ Sprint 6: Optional Features (Post-MVP) ~
- [ ] Build `/dashboard` for mood and journal history
  - [ ] Add mood trends (emoji log or graphs)
- [ ] Let users favorite/save practices
- [ ] Add email reminders for daily check-ins
- [ ] Enable AI to adapt based on user feedback and history
- [ ] Sentiment analysis on journal entries (optional, opt-in)

---

## req HTML templates

- `index.html` – Home page (public welcome screen)
- `signup.html` – Form for new users to sign up
- `login.html` – Form to log in
- `check_in.html` – Daily mood check-in form (emoji + body)
- `already_checked_in.html` – Message for users who already checked in
- `practice.html` – Display selected practice and journal prompt
- `reflect.html` – Journal entry textbox
- `feedback.html` – Emoji or rating form
- `thank_you.html` – Gratitude message / end screen

**optional**
- 'dashboard.html' - (Sprint 6 / future)
-  'error.html' - (custom 404 or access denied)

---

This planning document reflects my intention to build a mindful, 
scalable MVP rooted in purpose and simplicity. Each sprint is 
designed to help me learn, create, and grow as a developer while 
staying grounded in the heart of the app.
