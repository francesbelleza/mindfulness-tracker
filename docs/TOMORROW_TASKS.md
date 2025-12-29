# Tomorrow's Task List

**Date:** December 28, 2025
**Sprint:** Sprint 5 - Journal History & Dashboard

---

## 🎯 Priority Tasks (in order)

### 1. ⭐ #1 PRIORITY: Research & Find Better Voice
- Explore ElevenLabs quality vs cost
- Test different Google Cloud TTS voices (WaveNet-D, WaveNet-G, Journey-D, Journey-F, Neural2 variants)
- Research alternatives: Amazon Polly Neural, Microsoft Azure Speech, Play.ht, Murf.ai
- Compare quality vs cost vs naturalness
- Make final decision on voice provider

### 2. Test New GPT Meditation Pacing
- Restart Flask app
- Run `python3 clear_data.py` to clear old practices
- Create new check-in and test meditation
- Verify:
  - Duration is 1-2.5 minutes (not 6+ minutes)
  - Natural comma pauses (not excessive)
  - Strategic pause locations (transitions, breathing cues only)
  - Speaking rate 0.80 sounds calm and meditative

### 3. Fix Spacing if Still Not Right
- Adjust pause timings in `_convert_pauses_to_ssml()` if needed
- Adjust speaking rate in `generate_audio()` if needed
- Update GPT prompt for better comma/ellipsis usage

---

## 📋 Sprint 5 Remaining Phases

### Phase 1: Reflection Space (Journal History)
- [ ] Create `/journal-history` route
- [ ] Build journal timeline view with past entries
- [ ] Add date filtering (by date range, mood, time of day)
- [ ] Add search functionality for journal text
- [ ] Display check-in streak counter
- [ ] Show mood visualization/trends over time

### Phase 2: Profile & Settings
- [ ] Create `/profile` route
- [ ] Display user info (username, email, join date)
- [ ] Add "Edit Profile" functionality (change username/email)
- [ ] Add "Change Password" feature
- [ ] Create "Account Deletion" with CASCADE (delete all user data)

### Phase 3: Settings & Preferences
- [ ] Create `/settings` route
- [ ] Add notification preferences (if implementing reminders)
- [ ] Add privacy settings toggles
- [ ] Add data export option (download journal entries as JSON/CSV)

### Phase 4: Privacy & Legal
- [ ] Create `/privacy-policy` page
- [ ] Create `/terms-of-service` page
- [ ] Add consent checkbox to signup
- [ ] Add cookie notice (if applicable)

### Phase 5: Navigation & Polish
- [ ] Implement hamburger menu for mobile
- [ ] Add navigation links to all new pages
- [ ] Refine mobile experience across all Sprint 5 pages
- [ ] Add loading states for async operations
- [ ] Improve error messages and user feedback


### Phase 6: Think about RLS 
- [] research how to protect user data before shipping on supabase
---

## 🚀 Sprint 6 Features (Quick Refresher)
- **AI Personalization**: Use PracticeFeedback data to improve recommendations
- **Practice History**: Personalized recommendations based on past patterns
- **Favorites**: Save/bookmark favorite practices
- **Email Reminders**: Optional daily check-in emails
- **Sentiment Analysis**: Optional journal sentiment tracking
- **Analytics Dashboard**: Mood trends, streaks, completion stats
- **Structured Data Insights**: Track intentions, self-care patterns, goals
