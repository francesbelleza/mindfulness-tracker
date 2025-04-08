# planning

## overview
This project is a mindfulness-based web application that invites 
users to check in with themselves once a day. Through mood selection, 
AI-powered suggestions, and reflective journaling, the app fosters 
emotional awareness and grounding. The goal is to provide practices 
and prompts that meet users where they are, using thoughtful design 
and intentional flow.

---

## High-Level MVP Goals

[] **User Authentication System**  
  - Users can sign up, log in, and log out securely. Only logged-in users can access core features.

[]**1x Daily Mood Check-In**  
  - Users can check in once per day with a mood emoji and an optional body feeling. Repeat check-ins are gently blocked until the next day.

[] **AI-Powered Practice Suggestions (via Wrapper)**  
  - After checking in, the app uses an AI wrapper (like OpenAI or Claude) to suggest one mindfulness practice and one journal prompt based on the user's mood and internal research mappings.

[] **Practice Display Page**  
  - The selected mindfulness practice is shown on a dedicated page with a written description and (optionally) an image, audio, or video link to guide the user through the practice.

[] **Journal Reflection Page**  
  - Users are given a journal prompt and can respond in a text box. Their reflections are saved securely.

[] **Feedback System**  
  - After journaling, users are asked to rate how the practice felt using emojis or a simple rating. This will help future personalization.

[] **Thank You / Closing Page**  
  - The app ends each session with a calming “Thank you” message or affirmation, creating closure for the user.

[] **Basic UI & Styling**  
  - A clean, mobile-friendly interface using a burnt orange/white/black color palette with emoji-based interactions.

[] **Cloud-Based Data Storage**  
  - User check-ins, reflections, and feedback are stored in a cloud-hosted PostgreSQL database (via Render), making the app scalable and persistent beyond local development.

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
- [ ] Set up free PostgreSQL instance on Render (or Railway)
- [ ] Replace SQLite URI with cloud PostgreSQL URI in `config.py`
- [ ] Run a test to confirm cloud DB connection is working
- [ ] Add `.env` to `.gitignore` so credentials stay private

---

### Sprint 1: User Authentication System
- [ ] Create `User` model (username, email, hashed password)
- [ ] Implement Flask-Login for session management
- [ ] Build `/signup`, `/login`, and `/logout` routes
- [ ] Add redirects after login/logout
- [ ] Protect routes with `@login_required`

---

### Sprint 2: Daily Mood Check-In
- [ ] Create `CheckIn` model (mood, body_feeling, created_at, user_id)
- [ ] Build `/check-in` route + form (emoji mood + optional body input)
- [ ] Add logic to allow one check-in per day
  - [ ] If already checked in → redirect to `/already-checked-in`
  - [ ] Else → save and redirect to `/practice`

---

### Sprint 3: AI Suggestion Logic + Practice Page
- [ ] Create `practices`, `journal_prompts`, and `research_data` tables
- [ ] Add AI wrapper
- [ ] Create prompt logic using mood, tags, and research data
- [ ] Parse AI response to extract one practice and one prompt
- [ ] Create `/practice` route and template:
  - Show title, description
  - Optional image or video link
  - “Continue to Journal” button

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
