# UI Design System - Recalibrate

**Status:** Sprint 1 Complete ✅
**Last Updated:** December 27, 2025

---

## Design Philosophy

**Core Principles:**
- **Dark sunset aesthetic** - Calming, meditative experience inspired by twilight
- **Minimalist & clean** - No visual clutter, generous spacing
- **Simple sans-serif** - ui-sans-serif (General Sans) for personality with simplicity
- **Soft glows over harsh shadows** - Gentle, welcoming feel
- **Compact interactive elements** - Smaller buttons for cleaner interface

---

## Color Palette

### Backgrounds
```css
/* Ombre Gradient Background (6-stop linear gradient) */
background: linear-gradient(
  180deg,
  #e8a87c 0%,      /* Soft peach (top) */
  #d89b76 16.67%,  /* Peachy orange */
  #c08d6f 33.33%,  /* Warm coral */
  #a07f69 50%,     /* Muted brown-coral */
  #6f7266 66.67%,  /* Cool gray-blue */
  #143642 100%     /* Deep ocean blue (bottom) */
);

--bg-primary: #143642;     /* Deep ocean blue - main theme color */
--bg-card: #1e3a45;        /* Dark teal - all cards (solid, not glassmorphic) */
```

### Sunset Accents
```css
--sunset-peach: #e8a87c;   /* Primary CTA, highlights */
--sunset-coral: #d4917e;   /* Secondary accent */

/* Gradient for buttons and selected states */
linear-gradient(135deg, var(--sunset-peach) 0%, var(--sunset-coral) 100%)
```

### Text
```css
--text-light: rgba(255, 255, 255, 0.95);   /* Headings, important text */
--text-medium: rgba(255, 255, 255, 0.75);  /* Body text, labels */
--text-subtle: rgba(255, 255, 255, 0.5);   /* Placeholder text */
```

---

## Typography

### Font Family
```css
font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont,
             'Segoe UI', 'Roboto', sans-serif;
```

**Rationale:** ui-sans-serif provides General Sans-like feel with personality while maintaining simplicity.

### Font Weights & Spacing
```css
/* Logo "recalibrate" */
font-weight: 500;
letter-spacing: 4px;

/* Buttons */
font-weight: 500;

/* Headings */
font-weight: 200-400;  /* Light to normal */

/* Body text */
font-weight: 300;
letter-spacing: 0.5px;
```

---

## Component Styles

### Navbar
```css
background: transparent !important;  /* Continuation of ombre */
border-bottom: none;

/* Logo */
.navbar-brand {
  color: var(--bg-primary) !important;  /* Dark blue */
  font-size: 1.5rem;
  font-weight: 500;
  letter-spacing: 4px;
}

/* Logout button */
.logout-btn {
  background: var(--bg-primary);
  color: var(--text-light);
  border-radius: var(--radius-md);
  padding: 10px 24px;
  font-weight: 500;
}
```

### Cards
```css
background: #1e3a45;  /* Solid dark teal, NOT glassmorphic */
border: 1px solid rgba(232, 168, 124, 0.3);
border-radius: var(--radius-xl);
padding: var(--space-2xl);
box-shadow: var(--shadow-card), var(--glow-subtle);

/* Hover */
box-shadow: var(--shadow-card), var(--glow-medium);
transform: translateY(-3px);
```

### Buttons
```css
/* Primary */
background: linear-gradient(135deg, var(--sunset-peach) 0%, var(--sunset-coral) 100%);
color: var(--bg-primary);
padding: 14px 32px;
border-radius: 12px;
font-weight: 500;

/* Secondary */
background: var(--bg-primary);
color: var(--text-light);
border-radius: 12px;
padding: 12px 24px;
font-weight: 500;
```

### Interactive Cards (Compact)

**Time Cards:**
- Width: 350px (down from 450px)
- Padding: var(--space-lg) (down from var(--space-xl))

**Mood Cards:**
- Width: 110px (down from 140px)
- Padding: var(--space-md) (down from var(--space-lg))
- Indicators: 40px (down from 50px)
- **Selected state:** Dark blue (#143642) instead of white

**Mood Colors:**
- Happy: #f4d03f (yellow)
- Calm: #85c1e2 (light blue)
- Anxious: #e17055 (orange)
- Angry: #d63031 (red)
- Sad: #74b9ff (soft blue)

**Feedback Cards:**
- Emoji cards: Reduced padding, 2rem font-size
- Toggle cards: 320px max-width (down from 400px)
- Pacing cards: 450px max-width (down from 550px)

### Audio Player
```css
/* SVG icons instead of emoji */
.play-pause-btn {
  background: linear-gradient(135deg, var(--sunset-peach), var(--sunset-coral));
  width: 56px;
  height: 56px;
  border-radius: 50%;
  color: var(--bg-primary);
}

/* Vertically centered with progress bar */
.audio-player {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
}
```

---

## Features Implemented

### Time-Based Restrictions
- Morning: 3am - 1pm
- Evening: 1pm - 3am
- Warning messages for wrong time selection

### Twice-Daily Check-Ins
- Separate morning and night practices
- Prevents duplicates per time period
- Time-specific messaging when already checked in

### App Feedback System
- Formspree integration via AJAX
- Custom thank you page
- Types: Bug Report, Feature Request, General

### Minimum Practice Duration
- All practices ≥ 1 minute when spoken
- AI prompt enforces minimum
- TTS speed: 0.85 for meditative pacing

---

## Design Tokens

```css
:root {
  /* Colors */
  --bg-primary: #143642;
  --sunset-peach: #e8a87c;
  --sunset-coral: #d4917e;
  --text-light: rgba(255, 255, 255, 0.95);
  --text-medium: rgba(255, 255, 255, 0.75);
  --text-subtle: rgba(255, 255, 255, 0.5);

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;

  /* Border Radius */
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* Effects */
  --shadow-soft: 0 2px 8px rgba(0, 0, 0, 0.15);
  --shadow-card: 0 4px 16px rgba(0, 0, 0, 0.2);
  --glow-subtle: 0 0 20px rgba(232, 168, 124, 0.1);
  --glow-medium: 0 0 30px rgba(232, 168, 124, 0.15);
  --transition-smooth: 0.3s ease;
}
```

---

**End of UI Design Document**
