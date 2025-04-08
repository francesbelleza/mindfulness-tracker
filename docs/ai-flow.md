# ai-flow

## overview
The Mindfulness Tracker app uses a lightweight AI wrapper to recommend mindfulness 
practices and journal prompts based on the user's check-in mood. The AI system is 
designed to be simple, intention-driven, and grounded in emotional context.

This file documents how the AI system makes decisions, what inputs it receives, 
and how its responses are integrated into the user flow.

---

## ai decision logic (v1)

### input
The AI receives the following data:
- `mood` (selected by the user at check-in)
- (future integration) body or emotional note from the user
- matched `tags` (e.g., grounding, uplifting, gratitude) based on internal logic
- static research-backed examples or guidance

### prompt structure
A structured prompt is sent to the AI like:

> "The user is feeling anxious. Recommend one short grounding mindfulness practice 
> (yoga, breath, or meditation) and one reflective journal prompt to support emotional clarity. 
> Return them as two labeled sections: **Practice** and **Prompt**."

### output
The AI returns:
- FIRST -> `practice`: a mindfulness activity with a title and short description
- THEN -> `journal prompt`: a question or reflection statement

These are displayed on the `/practice` + '/reflect' route 
respectively and saved with the check-in data.

---

## current ai flow

1. User checks in with a mood
2. App uses mood-to-tag mapping:
   - sad → uplifting
   - anxious → grounding
   - happy → gratitude or reflection
   - angry → release
3. Prompt is sent to AI wrapper (Claude)
4. Practice from API
5. Displayed in `/practice.html`
6. Then prompt from API
7. Displayed in '/prompt.html'

---

## future ai roadmap (post-mvp)

- Allow AI to personalize suggestions based on:
  - Past moods
  - Feedback emoji ratings
  - Journal sentiment
- Generate closing affirmations based on mood or journal entry
- Automatically tag journal reflections with themes
- Incorporate research data dynamically into prompt context

---

## non-happy behavior (in development)
If the AI call fails:
- A random practice + journal prompt will be selected based on mood-tag matching using static data

---

## ai wrapper details
- Provider: Claude most likely or OpenAI