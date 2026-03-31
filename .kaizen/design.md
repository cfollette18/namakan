# Namakan Frontend Design Specification

*Inspired by: Shopify, Spotify, Linear — clean, professional, trustworthy*

---

## Brand Direction

**The feeling:** Calm confidence. Not flashy startup. Not boring enterprise. Something in between — a company that knows what it's doing.

**The vibe:** Think Linear.app meets Shopify. Clean lines, purposeful whitespace, colors that don't shout.

---

## Color Palette

### Primary: Deep Teal (#0D9488)
Trustworthy, professional, modern tech without being cold.

```css
primary-50: #f0fdfa
primary-100: #ccfbf1
primary-500: #0D9488    /* MAIN BRAND COLOR */
primary-600: #0f766e
primary-700: #115e59
```

### Secondary: Slate
For backgrounds, text, borders — the backbone of the interface.

```css
slate-50: #f8fafc    /* Light backgrounds */
slate-100: #f1f5f9
slate-200: #e2e8f0
slate-400: #94a3b8    /* Muted text */
slate-600: #475569    /* Secondary text */
slate-800: #1e293b    /* Dark text/headings */
slate-900: #0f172a    /* Darkest */
```

### Accent: Emerald (#10B981)
Success states, checkmarks, positive indicators.

```css
emerald-500: #10B981
emerald-600: #059669
```

### Error: Red (#EF4444)
Errors, warnings, destructive actions.

```css
red-500: #EF4444
red-600: #DC2626
```

### Background
```css
bg-primary: #FFFFFF      /* Light mode - clean white */
bg-secondary: #F8FAFC    /* Subtle gray sections */
bg-card: #FFFFFF         /* Cards on white */
```

### Text
```css
text-primary: #0F172A    /* Headlines, body */
text-secondary: #475569  /* Supporting text */
text-muted: #94A3B8     /* Captions, placeholders */
```

---

## Typography

### Font: Inter
The standard for professional SaaS. Clean, readable, trustworthy.

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
```

### Scale
```
Hero H1:     3.5rem / 700 weight / -0.02em tracking
H2:          2rem / 600 weight
H3:          1.25rem / 600 weight
Body:        1rem / 400 weight / 1.6 line-height
Small:       0.875rem / 500 weight
Caption:     0.75rem / 400 weight
```

---

## Layout & Spacing

### Grid
- **Max width**: 1200px (container)
- **Gutters**: 24px mobile, 32px desktop
- **Sections**: 80-120px vertical padding
- **Card radius**: 12px
- **Button radius**: 8px

### Rhythm
```
Section → Card → Element
80px → 24px → 12px
```

### Breakpoints
```
Mobile:  < 640px
Tablet:  640px - 1024px
Desktop: > 1024px
```

---

## Components

### Buttons

**Primary Button**
```css
background: #0D9488;       /* Teal */
color: white;
padding: 12px 24px;
border-radius: 8px;
font-weight: 600;
```
- Hover: darken to #0f766e, subtle shadow
- Active: darken further
- Disabled: 50% opacity

**Secondary Button**
```css
background: transparent;
border: 1px solid #e2e8f0;
color: #0f172a;
padding: 12px 24px;
border-radius: 8px;
```
- Hover: background #f8fafc, border darkens

**Text Button**
```css
color: #0D9488;
font-weight: 500;
```
- Hover: underline

### Cards
```css
background: white;
border: 1px solid #e2e8f0;
border-radius: 12px;
padding: 24px;
box-shadow: 0 1px 3px rgba(0,0,0,0.05);
```
- Hover: subtle shadow increase, border darkens

### Forms
```css
background: white;
border: 1px solid #e2e8f0;
border-radius: 8px;
padding: 12px 16px;
```
- Focus: border #0D9488, ring shadow
- Placeholder: #94a3b8

### Navigation
```css
background: white;
border-bottom: 1px solid #e2e8f0;
height: 64px;
```
- Logo left, links center, CTA right
- Mobile: hamburger menu

### Badges
```css
background: #ccfbf1;       /* primary-100 */
color: #0D9488;
padding: 4px 12px;
border-radius: 999px;
font-size: 0.75rem;
font-weight: 600;
```

---

## Page Structure

### Homepage Flow

```
1. NAV
       ↓
2. HERO — Split comparison (Generic vs Namakan)
       ↓
3. SOCIAL PROOF — Logos, stats
       ↓
4. PRODUCTS — 4 cards in 2x2 grid
       ↓
5. HOW IT WORKS — 3-step process
       ↓
6. TESTIMONIALS — 2-3 quotes
       ↓
7. CTA — Final push
       ↓
8. FOOTER
```

### Hero Section — Split Comparison

**The centerpiece.** Side-by-side showing generic AI vs Namakan.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Your AI has no idea who your customers are.                    │
│   We fix that.                                                  │
│                                                                 │
│   ┌───────────────────────┐    ┌───────────────────────┐      │
│   │  Generic AI          │    │  Namakan              │      │
│   │  (subtle gray bg)   │    │  (white, teal border) │      │
│   │                       │    │                       │      │
│   │  [Chat interface]     │    │  [Chat interface]     │      │
│   │  ❌ Wrong answers    │    │  ✓ Correct answers   │      │
│   │  ❌ Generic tone    │    │  ✓ Your brand voice │      │
│   │                       │    │                       │      │
│   │  Source: Internet     │    │  Source: Your Docs     │      │
│   └───────────────────────┘    └───────────────────────┘      │
│                                                                 │
│                    [Talk to Us →]                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Visual Treatment:**

**Generic AI Side (Left)**
```css
background: #f8fafc;        /* Subtle gray */
border: 1px solid #e2e8f0;
opacity: 0.8;
```

**Namakan Side (Right)**
```css
background: white;
border: 2px solid #0D9488;  /* Teal border */
box-shadow: 0 4px 20px rgba(13, 148, 136, 0.1);
```

### Products Grid

2x2 grid on desktop, stacked on mobile.

```
┌────────────────────┐  ┌────────────────────┐
│ Fine-Tuned Models  │  │ RAG Pipelines      │
│ [Icon]             │  │ [Icon]             │
│ Starting $5K       │  │ Starting $5K       │
└────────────────────┘  └────────────────────┘
┌────────────────────┐  ┌────────────────────┐
│ Agentic Workflows │  │ AI Employees       │
│ [Icon]             │  │ [Icon]             │
│ Starting $5K        │  │ Starting $2K/mo     │
└────────────────────┘  └────────────────────┘
```

### Process Section

3 steps, horizontal on desktop.

```
[1. Connect] → [2. Train] → [3. Deploy]
```

Each step: icon, title, brief description.

---

## Animations & Interactions

### Philosophy
Subtle. Purposeful. Fast.

### Allowed
- ✅ Fade-in on scroll (opacity 0→1, 300ms)
- ✅ Button hover: background shift, subtle lift
- ✅ Card hover: shadow increase
- ✅ Smooth page transitions
- ✅ Loading skeletons (not spinners)

### Forbidden
- ❌ Heavy animations
- ❌ Confetti, particles, etc.
- ❌ Parallax
- ❌ Bouncy springs

### Framer Motion (if needed)
```tsx
const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } }
}

const stagger = {
  show: { transition: { staggerChildren: 0.1 } }
}
```

---

## Responsive Behavior

### Mobile
- Single column
- Hamburger nav
- Full-width cards
- 48px section padding

### Tablet
- 2-column grids
- Condensed navigation

### Desktop
- Full layout
- Hover states active

---

## Accessibility

- Color contrast: WCAG AA minimum (4.5:1)
- Focus states on all interactive elements
- Alt text on images
- Semantic HTML
- Keyboard navigable

---

## Technical Stack

- **Framework**: Next.js (App Router)
- **Styling**: Tailwind CSS
- **Fonts**: Inter (Google Fonts)
- **Components**: Custom
- **Hosting**: Vercel

---

## File Structure

```
frontend/
├── app/
│   ├── page.tsx              # Homepage
│   ├── layout.tsx            # Root layout
│   ├── globals.css           # Tailwind + custom
│   └── services/
│       ├── fine-tuned/
│       ├── rag/
│       ├── workflows/
│       └── employees/
├── components/
│   ├── ui/                   # Button, Card, Input, Badge
│   ├── Nav.tsx
│   ├── Footer.tsx
│   ├── Hero.tsx
│   ├── ProductCard.tsx
│   ├── ComparisonCard.tsx
│   └── Process.tsx
├── public/
│   ├── images/
│   └── logo.svg
└── design.md
```

---

*Last updated: 2026-03-29*
*Direction: Shopify/Linear inspired — clean, professional, teal + white*
