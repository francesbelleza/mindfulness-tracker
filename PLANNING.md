# planning

## 📊 Current Progress: Sprint 3 Complete! 🎉

**Completed:** Sprint 0, Sprint 1, Sprint 2, Sprint 3
**Next Up:** Sprint 4 - Journal & Feedback System
**Overall MVP Progress:** ~60% complete

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

[✅] **AI-Powered Practice Suggestions (via Wrapper)**
  - After checking in, the app uses OpenAI API to suggest one mindfulness practice and one journal prompt based on the user's mood and body feelings. Includes fallback content if API fails.

[✅] **Practice Display Page**
  - The AI-generated mindfulness practice is shown on a beautifully designed page with title, description, practice type badge, and journal prompt. Includes "Continue to Journal" button.

[] **Journal Reflection Page** ← Sprint 4
  - Users are given a journal prompt and can respond in a text box. Their reflections are saved securely.

[] **Feedback System** ← Sprint 4
  - After journaling, users are asked to rate how the practice felt using emojis or a simple rating. This will help future personalization.

[] **Thank You / Closing Page** ← Sprint 4
  - The app ends each session with a calming "Thank you" message or affirmation, creating closure for the user.

[✅] **Basic UI & Styling**
  - A clean, mobile-friendly interface using a burnt orange/white/black color palette with emoji-based interactions.

[✅] **Cloud-Based Data Storage**
  - User check-ins, AI-generated practices, and journal prompts are stored in PostgreSQL via Supabase, making the app scalable and persistent beyond local development.

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
- PostgreSQL (via Supabase)
- SQLite for local testing (optional)

**AI/nlp**
- OpenAI API (GPT-3.5-turbo)
- Custom prompt engineering with mood-based practice generation
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
- [x] Build `/check-in` route + form (emoji mood + optional body input)
- [x] Add logic to allow one check-in per day
  - [x] If already checked in → redirect to `/already-checked-in`
  - [x] Else → save and redirect to `/practice`
- [x] Beautiful UI with emoji mood selector (😊 😌 😰 😔)
- [x] Smooth animations and transitions
- [x] Mobile-responsive design
- [x] Practice page placeholder created

---

### ✅ Sprint 3: AI Suggestion Logic + Practice Page (COMPLETED)
**Goal:** Integrate OpenAI API to generate personalized mindfulness practices and journal prompts based on user's mood.

**Tasks:**
- [x] Set up OpenAI API integration
  - [x] Add OpenAI API key to `.env`
  - [x] Install `openai` Python package
  - [x] Create AI service module for API calls
- [x] Create database models:
  - [x] `Practice` model (exercise suggestions)
  - [x] `JournalPrompt` model (reflection prompts)
- [x] Update `/practice` route:
  - [x] Fetch user's latest check-in (mood + body feeling)
  - [x] Call OpenAI API with mood-based prompt
  - [x] Parse AI response to extract practice + journal prompt
  - [x] Store practice and prompt in database
  - [x] Display on practice page
- [x] Enhance `/practice` template:
  - [x] Show AI-generated mindfulness practice
  - [x] Display journal prompt
  - [x] Add "Continue to Journal" button → `/reflect`
  - [x] Add practice category icons/tags (emoji-based)
- [x] Create AI prompt engineering:
  - [x] Design system prompt for mindfulness practices
  - [x] Map moods to practice types (breathing, meditation, movement, grounding)
  - [x] Ensure responses are calming, supportive, and actionable
  - [x] Add fallback content for each mood if API fails

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
