# UI Design System - Recalibrate App

**Status:** In Progress (Sprint 4.5 - UI Polish)
**Last Updated:** December 26, 2025

---

## Design Philosophy

**Core Principles:**
- Sleek, simple, and calming
- Minimal visual noise
- Earthy, grounding aesthetic
- Mobile-first responsive design
- Clean typography hierarchy

---

## Color Palette

### Primary Colors
```css
--primary-warm: #b76935;      /* Main CTA buttons, primary actions */
--primary-warm-hover: #a56336; /* Hover states for primary elements */
--primary-medium: #935e38;     /* Borders, dividers, accents */
```

### Text Colors
```css
--text-dark: #4a473e;          /* Headings, important text */
--text-medium: #5c4d3c;        /* Body text, labels */
--text-warm: #815839;          /* Secondary text, emphasis */
```

### Background Colors
```css
--bg-light: #f8f6f4;           /* Page backgrounds */
--bg-card: #ffffff;            /* Card backgrounds */
--bg-subtle: #38413f;          /* Subtle dark backgrounds */
--bg-dark: #263c41;            /* Footer, dark sections */
--bg-darkest: #143642;         /* Contrast elements, header */
```

### Neutral Shades
```css
--neutral-light: #6f523b;      /* Light brown accents */
--neutral-dark: #5c4d3c;       /* Dark brown elements */
```

### Usage Guidelines
- **Primary warm** (#b76935) for all CTAs and important actions
- **Text dark** (#4a473e) for all headings
- **Text medium** (#5c4d3c) for body text
- **Background light** (#f8f6f4) for page backgrounds
- White (#ffffff) for card backgrounds
- Avoid using too many colors in one section

---

## Typography

### Font Family
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
             'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans',
             'Helvetica Neue', sans-serif;
```

**Rationale:** System font stack provides native feel, fast loading, and accessibility across all platforms.

### Type Scale
```css
/* Display (Hero headings) */
--font-display: 2.5rem;        /* 40px */
--font-display-weight: 700;

/* H1 (Page titles) */
--font-h1: 2rem;               /* 32px */
--font-h1-weight: 600;

/* H2 (Section headings) */
--font-h2: 1.5rem;             /* 24px */
--font-h2-weight: 600;

/* H3 (Card titles) */
--font-h3: 1.25rem;            /* 20px */
--font-h3-weight: 600;

/* Body (Regular text) */
--font-body: 1rem;             /* 16px */
--font-body-weight: 400;

/* Small (Helper text) */
--font-small: 0.875rem;        /* 14px */
--font-small-weight: 400;
```

### Line Height
```css
--line-height-tight: 1.2;      /* Headings */
--line-height-normal: 1.5;     /* Body text */
--line-height-relaxed: 1.8;    /* Reading content */
```

---

## Spacing System

```css
--space-xs: 0.25rem;    /* 4px */
--space-sm: 0.5rem;     /* 8px */
--space-md: 1rem;       /* 16px */
--space-lg: 1.5rem;     /* 24px */
--space-xl: 2rem;       /* 32px */
--space-2xl: 3rem;      /* 48px */
--space-3xl: 4rem;      /* 64px */
```

**Usage:**
- Cards: `padding: var(--space-xl);`
- Sections: `margin-bottom: var(--space-2xl);`
- Elements: `gap: var(--space-md);`

---

## Component Styles

### Buttons

**Primary Button**
```css
background: linear-gradient(135deg, #b76935 0%, #a56336 100%);
color: white;
padding: 12px 32px;
border-radius: 8px;
font-weight: 600;
border: none;
transition: all 0.3s ease;

/* Hover */
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(183, 105, 53, 0.3);
```

**Secondary Button**
```css
background: transparent;
color: #5c4d3c;
border: 2px solid #935e38;
padding: 10px 30px;
border-radius: 8px;
font-weight: 600;
transition: all 0.3s ease;

/* Hover */
background: #935e38;
color: white;
```

### Cards

**Standard Card**
```css
background: white;
border: 1px solid #935e38;
border-radius: 12px;
padding: 32px;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
transition: all 0.3s ease;

/* Hover */
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
transform: translateY(-2px);
```

### Form Inputs

**Text Input**
```css
border: 2px solid #935e38;
border-radius: 8px;
padding: 12px 16px;
font-size: 1rem;
color: #5c4d3c;
background: white;
transition: all 0.3s ease;

/* Focus */
border-color: #b76935;
box-shadow: 0 0 0 3px rgba(183, 105, 53, 0.1);
outline: none;
```

### Mood/Rating Indicators

**Circular Indicator (Replaces emoji)**
```css
width: 60px;
height: 60px;
border-radius: 50%;
border: 3px solid #935e38;
background: white;
display: flex;
align-items: center;
justify-content: center;
font-weight: 600;
font-size: 0.9rem;
color: #5c4d3c;
cursor: pointer;
transition: all 0.3s ease;

/* Selected */
background: linear-gradient(135deg, #b76935 0%, #a56336 100%);
border-color: #b76935;
color: white;
box-shadow: 0 4px 12px rgba(183, 105, 53, 0.3);
```

---

## Navbar Design

```css
background: white;
border-bottom: 1px solid #935e38;
padding: 16px 0;
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

/* Logo */
font-size: 1.5rem;
font-weight: 700;
color: #b76935;
letter-spacing: -0.5px;

/* Nav links */
color: #5c4d3c;
font-weight: 500;
padding: 8px 16px;
border-radius: 6px;
transition: all 0.3s ease;

/* Nav link hover */
background: rgba(183, 105, 53, 0.1);
color: #b76935;
```

---

## Icon Replacements

### Mood Indicators
**Before:** 😊 😌 😰 😔
**After:** Circular buttons with mood names (Happy, Calm, Anxious, Sad)

### Time of Day
**Before:** ☀️ 🌙
**After:** Text buttons with "Morning" / "Night" labels

### Practice Types
**Before:** 🌬️ 🧘‍♀️ 🤸‍♀️ 🌿
**After:** Text badges (Breathing, Meditation, Movement, Grounding)

### Rating Scale
**Before:** 😞 😐 🙂 😊 🤩
**After:** Number circles (1-5) or stars

### Decorative Icons
**Before:** ✨ 💭 📝 ⭐
**After:** Simple CSS shapes, text, or minimal SVG icons

---

## Shadow System

```css
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);
--shadow-xl: 0 8px 24px rgba(0, 0, 0, 0.15);

/* Colored shadow for primary actions */
--shadow-primary: 0 4px 12px rgba(183, 105, 53, 0.3);
```

---

## Border Radius

```css
--radius-sm: 6px;     /* Small elements */
--radius-md: 8px;     /* Buttons, inputs */
--radius-lg: 12px;    /* Cards */
--radius-xl: 16px;    /* Large cards */
--radius-full: 9999px; /* Circular elements */
```

---

## Transitions

```css
--transition-fast: 0.15s ease;
--transition-normal: 0.3s ease;
--transition-slow: 0.5s ease;
```

**Usage:**
- Hover effects: `transition: all var(--transition-normal);`
- Transforms: `transition: transform var(--transition-fast);`
- Color changes: `transition: color var(--transition-normal);`

---

## Responsive Breakpoints

```css
/* Mobile first approach */
--breakpoint-sm: 576px;   /* Small devices (landscape phones) */
--breakpoint-md: 768px;   /* Medium devices (tablets) */
--breakpoint-lg: 992px;   /* Large devices (desktops) */
--breakpoint-xl: 1200px;  /* Extra large devices (large desktops) */
```

---

## Page-Specific Guidelines

### Landing Page (index.html)
- Hero section with clean heading
- Single CTA button
- Remove features section
- Minimal, welcoming design

### Check-In Page (check_in.html)
- Grid of mood buttons (circular indicators with text)
- Time-of-day selection (Morning/Night text buttons)
- Clean form layout
- No emojis

### Practice Page (practice.html)
- Audio player styled with warm colors (not purple)
- Practice type badge (text only)
- Journal prompt card with clean typography
- Minimal decorations

### Reflect Page (reflect.html)
- Voice button styled with warm colors (not purple)
- Clean textarea styling
- Structured questions with clear labels
- Simple, focused layout

### Feedback Page (feedback.html)
- Rating scale as numbered circles (1-5)
- Yes/No toggle buttons
- Clean radio buttons for pacing
- No emoji reactions

### Thank You Page (thank.html)
- Centered message card
- Completion stats with text/symbols
- Single "Return Home" button
- Minimal decorations

---

## Implementation Checklist

- [ ] Update base.html with new color variables and font
- [ ] Redesign navbar with new styling
- [ ] Remove features section from landing page
- [ ] Replace all emojis in check-in page with circular indicators
- [ ] Update practice page audio player colors (purple → orange)
- [ ] Replace emojis in practice type badges
- [ ] Update reflect page voice button colors (purple → orange)
- [ ] Replace emoji ratings in feedback page with numbers
- [ ] Remove decorative emojis from thank you page
- [ ] Update login/signup pages with new colors
- [ ] Test responsive design on mobile
- [ ] Test all interactions and hover states

---

## Design Tokens (CSS Variables)

All colors, spacing, and typography will be defined as CSS custom properties in base.html for consistency and easy maintenance.

```css
:root {
  /* Colors */
  --primary-warm: #b76935;
  --primary-warm-hover: #a56336;
  --primary-medium: #935e38;
  --text-dark: #4a473e;
  --text-medium: #5c4d3c;
  --text-warm: #815839;
  --bg-light: #f8f6f4;
  --bg-card: #ffffff;
  --bg-subtle: #38413f;
  --bg-dark: #263c41;
  --bg-darkest: #143642;

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;

  /* Border Radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);
  --shadow-primary: 0 4px 12px rgba(183, 105, 53, 0.3);

  /* Transitions */
  --transition-normal: 0.3s ease;
}
```

---

**End of UI Design Document**
