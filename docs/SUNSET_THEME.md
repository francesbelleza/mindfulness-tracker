# Dark Sunset Meditation Theme

## Design Philosophy
Inspired by o-p-e-n.com - creating a calming, meditative experience with a soft dark sunset aesthetic.

## Color Palette

### Backgrounds
- `--bg-primary: #143642` - Deep ocean blue (main background)
- `--bg-secondary: #1f4451` - Slightly lighter blue
- `--bg-card: #263c41` - Card backgrounds
- `--bg-card-hover: #2d4a50` - Hover states

### Sunset Accents
- `--sunset-peach: #e8a87c` - Soft peach (primary CTAs, highlights)
- `--sunset-coral: #d4917e` - Coral accents
- `--sunset-warm: #bf7d6a` - Warm brown-coral
- `--sunset-deep: #a56b5c` - Deep sunset tone

### Text
- `--text-light: rgba(255, 255, 255, 0.95)` - Primary text
- `--text-medium: rgba(255, 255, 255, 0.75)` - Secondary text
- `--text-subtle: rgba(255, 255, 255, 0.5)` - Subtle text
- `--text-accent: #e8a87c` - Accent text

## Typography
- **Font Family**: 'Georgia', 'Palatino', 'Times New Roman', serif
- **Font Weight**: 200-300 (very light, soft)
- **Letter Spacing**: 0.3px - 2px (increased for elegance)
- **Line Height**: 1.8 - 2 (generous breathing room)

## Spacing
Very generous spacing for calm, uncluttered feel:
- `--space-xs: 0.5rem`
- `--space-sm: 1rem`
- `--space-md: 1.5rem`
- `--space-lg: 2.5rem`
- `--space-xl: 3.5rem`
- `--space-2xl: 5rem`

## Visual Effects
- **Soft Glows** instead of hard shadows:
  - `--glow-subtle: 0 0 20px rgba(232, 168, 124, 0.1)`
  - `--glow-medium: 0 0 30px rgba(232, 168, 124, 0.15)`
  - `--glow-strong: 0 0 40px rgba(232, 168, 124, 0.25)`
- **Backdrop Blur**: `backdrop-filter: blur(10px-20px)`
- **Glassmorphism**: Semi-transparent cards with blur

## Component Patterns

### Cards
```css
background: rgba(38, 60, 65, 0.4);
backdrop-filter: blur(20px);
border: 1px solid rgba(232, 168, 124, 0.2);
border-radius: var(--radius-xl);
box-shadow: var(--shadow-card), var(--glow-subtle);
```

### Buttons (Primary)
```css
background: linear-gradient(135deg, var(--sunset-peach) 0%, var(--sunset-coral) 100%);
color: var(--bg-primary);
border-radius: var(--radius-lg);
box-shadow: var(--glow-subtle);
```

### Form Inputs
```css
background: rgba(255, 255, 255, 0.05);
border: 1px solid rgba(232, 168, 124, 0.2);
color: var(--text-light);
```

### Hover States
- Subtle `translateY(-2px to -3px)`
- Increased glow
- Never harsh shadows

## Key Changes from Previous Design
1. Dark background instead of light
2. Serif font (Georgia) instead of sans-serif
3. Lighter font weights (200-300)
4. Soft glows instead of hard shadows
5. Generous spacing everywhere
6. Glassmorphism cards
7. Sunset gradient accents
8. No emojis (except feedback page)
9. Minimal borders, soft glows
10. Letter-spacing for elegance
