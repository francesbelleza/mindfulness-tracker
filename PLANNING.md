# planning

## Current Progress: Sprint 4 Complete

**Completed:** Sprint 0, Sprint 1, Sprint 2, Sprint 3, Sprint 4
**Next Up:** Sprint 5 - Journal History & Dashboard
**Overall MVP Progress:** ~80% complete

---

## overview
This project is a mindfulness-based web application that invites
users to check in with themselves twice a day (morning and night). Through mood selection,
AI-powered suggestions with natural voice narration, and reflective journaling with voice-to-text,
the app fosters emotional awareness and grounding. The goal is to provide practices
and prompts that meet users where they are, using thoughtful design
and intentional flow.

---

## High-Level MVP Goals

[✅] **User Authentication System**
  - Users can sign up, log in, and log out securely. Only logged-in users can access core features.

[✅] **2x Daily Mood Check-In (Morning + Night)**
  - Users can check in twice per day (morning and night) with time-of-day selection, mood emoji, and body feeling. AI generates context-appropriate practices based on time of day.

[✅] **AI-Powered Practice Suggestions with Natural Voice**
  - After checking in, the app uses OpenAI API to suggest personalized mindfulness practices and journal prompts. ElevenLabs TTS generates natural meditation audio with optimized pacing.

[✅] **Practice Display Page with Audio Player**
  - The AI-generated mindfulness practice is shown with title, description, practice type badge, and custom HTML5 audio player with play/pause controls and progress bar.

[✅] **Journal Reflection Page with Voice-to-Text**
  - Users can type or speak their journal reflections using Web Speech API. Entries are saved securely and linked to check-ins.

[✅] **Feedback System with Emoji Ratings**
  - After journaling, users rate practices with emoji scale (1-5) and answer detailed questions about helpfulness and pacing. Data saved for future AI personalization.

[✅] **Thank You / Closing Page**
  - The app ends each session with time-of-day appropriate affirmations and closure messages, creating a complete mindfulness experience.

[✅] **Basic UI & Styling**
  - A clean, mobile-friendly interface using a burnt orange/white/black color palette with emoji-based interactions.

[✅] **Cloud-Based Data Storage**
  - User check-ins, AI-generated practices, and journal prompts are stored in PostgreSQL via Supabase, making the app scalable and persistent beyond local development.

---

## tech stack

**frontend**
- HTML5
- CSS3
- JavaScript (audio player, Web Speech API)
- Jinja2 Templates

**backend**
- Python 3
- Flask
- Flask-Login
- SQLAlchemy ORM

**database**
- PostgreSQL (via Supabase)
- SQLite for local testing (optional)

**AI/nlp**
- OpenAI API (GPT-3.5-turbo)
- ElevenLabs Text-to-Speech API (eleven_multilingual_v2)
- Custom prompt engineering with mood-based practice generation
- Natural voice meditation narration with pause optimization
- Fallback content system for API failures

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
- [x] Build `/check-in` route + form (emoji mood + body input)
- [x] Add logic to allow one check-in per day (later updated to 2x in Sprint 4)
  - [x] If already checked in → redirect to `/already-checked-in`
  - [x] Else → save and redirect to `/practice`
- [x] Beautiful UI with emoji mood selector (😊 😌 😰 😔)
- [x] Smooth animations and transitions
- [x] Mobile-responsive design
- [x] Practice page placeholder created

**Note:** Sprint 4 enhanced this with morning/night check-ins and time-of-day field.

---

### ✅ Sprint 3: AI Suggestion Logic + Practice Page + Natural Voice (COMPLETED)
**Goal:** Integrate OpenAI API to generate personalized mindfulness practices and journal prompts based on user's mood, with natural AI-generated voice narration.

**Tasks:**
- [x] Set up OpenAI API integration
  - [x] Add OpenAI API key to `.env`
  - [x] Install `openai` Python package
  - [x] Create AI service module for API calls
  - [x] Design meditation-style prompt with pause notation
- [x] Set up ElevenLabs TTS integration
  - [x] Add ElevenLabs API key to `.env`
  - [x] Install `elevenlabs` Python package
  - [x] Test and select optimal voice (Lily - Velvety Actress)
  - [x] Optimize voice settings (stability, speed, similarity)
- [x] Create database models:
  - [x] `Practice` model (exercise suggestions + audio file)
  - [x] `JournalPrompt` model (reflection prompts)
  - [x] Add audio file migration
- [x] Update `/practice` route:
  - [x] Fetch user's latest check-in (mood + body feeling)
  - [x] Call OpenAI API with mood-based prompt
  - [x] Parse AI response to extract practice + journal prompt
  - [x] Generate natural AI voice audio via ElevenLabs
  - [x] Store practice, prompt, and audio filename in database
  - [x] Display on practice page
- [x] Enhance `/practice` template:
  - [x] Show AI-generated mindfulness practice
  - [x] Display journal prompt
  - [x] Add custom HTML5 audio player
  - [x] Implement play/pause controls
  - [x] Add progress bar with seek functionality
  - [x] Add "Continue to Journal" button → `/reflect`
  - [x] Add practice category icons/tags (emoji-based)
- [x] Create AI prompt engineering:
  - [x] Design system prompt for mindfulness practices
  - [x] Map moods to practice types (breathing, meditation, movement, grounding)
  - [x] Implement three-tier pause system (ellipses)
  - [x] Ensure responses are calming, supportive, and actionable
  - [x] Add fallback content for each mood if API fails
- [x] Voice optimization:
  - [x] Test OpenAI TTS (rejected - robotic)
  - [x] Test ElevenLabs with multiple voices
  - [x] Optimize for meditation pacing (0.85x speed)
  - [x] Tune stability and similarity settings

---

### ✅ Sprint 4: Journal & Feedback System (COMPLETED)
**Goal:** Complete the user session flow with journal reflection, practice feedback, and session closure. Add morning/night check-ins with context-aware AI practices. Implement structured journal data collection.

**Tasks:**
- [x] Add time-of-day selection to check-in (Morning ☀️ / Night 🌙)
- [x] Update CheckIn model with `time_of_day` field
- [x] Allow 2 check-ins per day (one morning, one night)
- [x] Enhance AI service with time-of-day context
  - [x] Morning practices: Energizing, grounding, intention-setting
  - [x] Night practices: Calming, reflective, restorative
  - [x] AI generates complementary prompts (not duplicating structured questions)
- [x] Create JournalEntry model with structured fields
  - [x] `entry_text` - Response to AI-generated prompt
  - [x] `intention_for_day` - Morning only: daily intention
  - [x] `self_care_today` - Night only: self-care activity
  - [x] `goal_for_tomorrow` - Night only: tomorrow's goal
- [x] Create `/reflect` route + template with Web Speech API
  - [x] Voice-to-text transcription (Speak button)
  - [x] Editable textarea for AI prompt response
  - [x] Separate input fields for time-specific questions
  - [x] Character counter
  - [x] Save structured journal entries to database
- [x] Refactor journal prompt storage
  - [x] Move `journal_prompt` field to Practice model
  - [x] Remove redundant JournalPrompt table
  - [x] Database migration for refactoring
- [x] Create PracticeFeedback model
- [x] Create `/feedback` route + template with emoji ratings
  - [x] Emoji rating scale (😞 😐 🙂 😊 🤩 = 1-5)
  - [x] "Did this help?" Yes/No question
  - [x] Pacing feedback (Too fast, Just right, Too slow)
  - [x] Save feedback to database
- [x] Create `/thank` route + template
  - [x] Time-of-day specific affirmations (no fake quotes)
  - [x] Session completion stats
  - [x] Simple "Return Home" navigation
- [x] Update navigation flow (practice → reflect → feedback → thank)
- [x] Database migrations for all new models and schema changes

---

### Sprint 5: Journal History & Dashboard
- [ ] Create `/journal-history` route to view past entries
- [ ] Add filtering by date, mood, time of day
- [ ] Add search functionality for journal entries
- [ ] Create `/dashboard` route for user overview
  - [ ] Mood trends visualization
  - [ ] Check-in streak tracking
  - [ ] Practice completion stats
- [ ] Styling & flow polish
  - [ ] Refine mobile experience
  - [ ] Add loading states
  - [ ] Improve error messages

---

### Sprint 6: AI Personalization & Advanced Features
- [ ] Use PracticeFeedback data to improve AI suggestions
- [ ] Personalized practice recommendations based on history
- [ ] Favorite/save practices feature
- [ ] Email reminders for daily check-ins (optional)
- [ ] Sentiment analysis on journal entries (optional, opt-in)

---

## HTML Templates

**Completed:**
- ✅ `index.html` – Home page (public welcome screen)
- ✅ `signup.html` – User registration form
- ✅ `login.html` – User login form
- ✅ `check_in.html` – Morning/Night check-in form with mood + body feeling
- ✅ `already_checked_in.html` – Message for users who already checked in
- ✅ `practice.html` – AI practice display with audio player
- ✅ `reflect.html` – Journal entry with voice-to-text
- ✅ `feedback.html` – Emoji rating + detailed feedback form
- ✅ `thank.html` – Session closure with affirmations

**Planned (Sprint 5+):**
- `journal_history.html` – View past journal entries
- `dashboard.html` – User overview with stats and trends
- `error.html` – Custom 404 or access denied pages

---

This planning document reflects my intention to build a mindful, 
scalable MVP rooted in purpose and simplicity. Each sprint is 
designed to help me learn, create, and grow as a developer while 
staying grounded in the heart of the app.
