# Namakan Frontend Design Specification

## Overview

Namakan's frontend should feel like a **premium B2B SaaS product** — clean, confident, slightly technical. Not flashy startup energy. Not corporate dinosaur. Something in between: modern engineering firm that takes your money seriously.

---

## Brand Identity

### Brand Personality
- **Confident but not arrogant**
- **Technical but not intimidating**
- **Premium but not flashy**
- **Direct, no fluff in copy**

### Voice & Tone
- Speak in specifics, not vague promises
- Use numbers: "40% faster", "3-day setup", "$10K-50K"
- Acknowledge pain points directly
- No exclamation points (except CTAs)
- Short sentences. Impactful copy.

---

## Color Palette

### Primary: Hot Pink (#f43f5e)
The **only** color accent allowed. Used sparingly for maximum impact.

```css
primary-500: #f43f5e   /* Hot Pink — brand color, CTAs, accents */
primary-600: #e11d48   /* Darker pink — hover states */
primary-700: #be123c   /* Even darker — active states */
```

### Neutrals: Slate
Used for backgrounds, text, borders. **No blue, no purple gradients.**

```css
slate-950: #020617   /* Darkest — primary background */
slate-900: #0f172a   /* Cards, elevated surfaces */
slate-800: #1e293b   /* Secondary backgrounds */
slate-700: #334155   /* Borders */
slate-400: #94a3b8   /* Muted text */
slate-50: #f8fafc    /* Light backgrounds (if needed) */
```

### Semantic Colors (Use Sparingly)
```css
green-500: #22c55e    /* Success, checkmarks */
red-500: #ef4444     /* Errors, warnings */
yellow-500: #eab308   /* Alerts (rare) */
```

### What NOT To Use
- ❌ Blue anywhere (too generic SaaS)
- ❌ Purple gradients
- ❌ Rainbow accents
- ❌ More than 2 colors on a page

---

## Typography

### Primary Font: Satoshi
The **only** font for everything — headlines, body, UI elements.

```css
font-family: var(--font-satoshi), system-ui, sans-serif;
```

Fallback stack:
```css
system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
```

### Scale
```
Hero H1:     4rem / 700 weight / -0.02em tracking
H2:          2.5rem / 700 weight / tight
H3:          1.5rem / 600 weight
Body:        1rem / 400 weight / 1.6 line-height
Small:       0.875rem / 500 weight
Caption:     0.75rem / 400 weight
```

### Code/Mono
Use **Satoshi** with `font-feature-settings: 'ss01'` for code blocks if available. Fall back to system monospace.

---

## Layout & Spacing

### Grid System
- **Max width**: 1200px (container)
- **Gutters**: 24px on mobile, 32px on desktop
- **Sections**: 80px vertical padding on desktop, 48px on mobile

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

### Visual Pacing
- Hero section: Full viewport height or close to it
- Alternating section density: Dense → Spacious → Dense
- White space is a feature, not waste

---

## Components

### Buttons

**Primary Button** (Hot Pink CTA)
```css
background: primary-500;
color: white;
padding: 12px 24px;
border-radius: 8px;
font-weight: 600;
transition: all 0.2s;
```
- Hover: darken 10%, slight lift (translateY -1px)
- Active: darken 15%
- Disabled: 50% opacity, no pointer

**Secondary Button** (Outline)
```css
background: transparent;
border: 2px solid slate-700;
color: slate-50;
padding: 10px 22px;
border-radius: 8px;
```
- Hover: border brightens, subtle glow

**Text Button** (Links)
```css
color: primary-500;
underline on hover;
```

### Cards
```css
background: slate-900;
border: 1px solid slate-800;
border-radius: 12px;
padding: 24px;
```
- Hover: border brightens slightly
- No heavy shadows — use borders instead

### Forms
- Inputs: slate-800 background, slate-700 border, slate-400 placeholder
- Focus: primary-500 border with subtle glow
- Labels: slate-400, uppercase, small

### Navigation
- Fixed top, 60px height
- Background: `rgba(2, 6, 23, 0.85)` with backdrop blur
- Logo left, nav links center/right
- Mobile: hamburger menu

### Badges/Tags
```css
background: rgba(244, 63, 94, 0.15); /* Primary dim */
color: primary-500;
padding: 4px 12px;
border-radius: 999px;
font-size: 0.75rem;
font-weight: 600;
```

---

## Page Structure

### Homepage Flow

```
1. NAV (fixed)
       ↓
2. HERO — Split comparison (see Hero section spec below)
       ↓
3. PROBLEM AGITATION
   - 3 pain points, icon + short text
   - No fluff — just real problems
       ↓
4. SERVICES/PRODUCTS
   - 4 cards (our offerings)
   - Each: Icon, title, brief desc, starting price
   - Clear CTA per card
       ↓
5. SOCIAL PROOF
   - Testimonial or case study hook
   - "See how [similar company] did it"
       ↓
6. PROCESS (optional)
   - 3-4 step overview
   - Keep it brief
       ↓
7. FINAL CTA
   - Strong close
   - "Ready to start?"
       ↓
8. FOOTER
   - Minimal: Logo, links, copyright
```

### Hero Section — Split Comparison

The hero is the **centerpiece of the homepage**. It shows a side-by-side comparison of two chat interfaces: a generic LLM vs Namakan's fine-tuned chat. The goal: make the difference obvious in 3 seconds.

**Layout:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        [NAMAKAN LOGO]        [NAV]                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Headline: "Your AI has no idea who your customers are."               │
│   Subtext: "We fix that."                                              │
│                                                                         │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐    │
│   │  GENERIC LLM                │  │  NAMAKAN                   │    │
│   │  (slightly dimmed/faded)    │  │  (vibrant, highlighted)    │    │
│   │                             │  │                             │    │
│   │  [Chat bubbles]             │  │  [Chat bubbles + context]  │    │
│   │  - Hallucinating            │  │  - Citing your docs        │    │
│   │  - Generic answers          │  │  - Specific answers        │    │
│   │  - No domain knowledge      │  │  - Trained on your data    │    │
│   │                             │  │                             │    │
│   │  ❌ Wrong product specs     │  │  ✅ Correct from your DB  │    │
│   │  ❌ Generic support tone    │  │  ✅ Your brand voice      │    │
│   │  ❌ Made-up policies       │  │  ✅ Your actual policies   │    │
│   └─────────────────────────────┘  └─────────────────────────────┘    │
│                                                                         │
│              [Talk to Us →]                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Visual Treatment:**

**Generic LLM Side (Left)**
```css
opacity: 0.5;                      /* Visually dimmed */
filter: grayscale(20%);           /* Slightly desaturated */
border: 1px solid slate-700;    /* Subtle border */
```

**Namakan Side (Right)**
```css
opacity: 1;                        /* Full vibrancy */
border: 1px solid primary-500;  /* Hot pink border accent */
box-shadow: 0 0 40px rgba(244, 63, 94, 0.2);  /* Subtle glow */
```

**Chat Interface Elements to Show:**

**Generic LLM:**
- Response with wrong technical specs
- Hallucinated policy references
- Generic corporate tone
- "I'm not sure" hedging language
- Source: "Internet (unreliable)"

**Namakan (Fine-tuned):**
- Response with correct specs from client's database
- Citing actual documents (show doc name/path)
- Client's brand voice (formal/casual/technical)
- Confident, specific answers
- Source: "Your Knowledge Base"

**Labels:**

Above each chat window:
- Left: `GENERIC LLM` in slate-400, small caps
- Right: `NAMAKAN` in primary-500, small caps

**Animation:**

On load, left side fades in first (300ms), right side follows with subtle glow pulse to draw attention.

```tsx
// Hero entrance animation
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3, delay: 0.2 }}
>
  {/* Generic side */}
  <motion.div
    initial={{ opacity: 0, x: -20 }}
    animate={{ opacity: 0.5, x: 0 }}
    transition={{ duration: 0.5, delay: 0.3 }}
  />
  
  {/* Namakan side */}
  <motion.div
    initial={{ opacity: 0, x: 20 }}
    animate={{ opacity: 1, x: 0, boxShadow: '0 0 40px rgba(244, 63, 94, 0.2)' }}
    transition={{ duration: 0.5, delay: 0.5 }}
  />
</motion.div>
```

**Responsive:**

- **Desktop (>1024px):** Side by side
- **Tablet (640-1024px):** Stacked vertically, generic on top, Namakan on bottom
- **Mobile (<640px):** Stacked, Namakan first (most important)

**CTA Below Comparison:**

```tsx
<motion.button
  whileHover={{ scale: 1.02, backgroundColor: 'var(--primary-600)' }}
  whileTap={{ scale: 0.98 }}
  className="bg-primary-500 text-white px-8 py-4 rounded-lg font-semibold text-lg"
>
  Talk to Us →
</motion.button>
```

### Services Pages (Future)
```
1. NAV
       ↓
2. HERO (service name + brief)
       ↓
3. WHAT IT IS
   - Plain English explanation
   - Who it's for
       ↓
4. WHAT YOU GET
   - Deliverables list
   - Process overview
       ↓
5. PRICING
   - Clear starting price
   - What's included
   - What's not
       ↓
6. FAQ
   - 4-6 common questions
       ↓
7. CTA
```

### Contact Page
- Simple form: Name, Email, Company, Message
- No lengthy contact info list
- Response time promise: "We respond within 24 hours"

---

## Video Ad / Product Demo Spec

Inspired by "Cowork: Claude Code for the rest of your work" — clean, fast, professional SaaS product demo.

### Style
- **Length**: 30-60 seconds
- **Tone**: Confident, direct, technical but accessible
- **Editing**: Fast cuts, modern pacing, no fluff
- **Visuals**: Screen recording + UI overlays + subtle animations

### Structure

```
[0:00-0:03] HOOK
- Problem statement: "Your AI doesn't know your business"
- Fast cut to contrast

[0:03-0:15] DEMO - Generic LLM
- Show chat interface making mistakes
- Highlight errors with red annotations
- Quick, punchy

[0:15-0:27] DEMO - Namakan
- Show our fine-tuned interface
- Highlight correct answers with green/checkmarks
- Subtle UI animations (Framer Motion)
- Show "citing your docs" in real-time

[0:27-0:35] VALUE PROP
- Quick benefits: "Trained on your data. Knows your business."
- Show logos of things it integrates with

[0:35-0:45] SOCIAL PROOF (if available)
- "Used by X companies"
- Or: "Starting at $X"

[0:45-0:50] CTA
- "Talk to Us"
- namakan.ai
```

### Visual Elements
- Dark background (matches brand)
- Hot pink (#f43f5e) for highlights and accents
- Clean chat interface mockups
- Subtle glow effects on Namakan side
- Red for generic LLM problems, green for Namakan solutions

### Audio
- **Voice**: Confident, slightly technical male or female voice
- **Music**: Upbeat but professional, tech-forward
- **SFX**: Subtle UI sounds (typing, notifications)

### Tools to Create
- **Screen recording**: Loom, OBS, or Camtasia
- **Editing**: DaVinci Resolve (free), Premiere, or Final Cut
- **Motion graphics**: After Effects or Motion (Mac)
- **AI tools**: Runway, Pika, or HeyGen for AI-generated visuals (optional)

### Deliverable
- 16:9 landscape (YouTube/Twitter)
- 9:16 vertical (Instagram Reels/TikTok)
- 1:1 square (LinkedIn/Facebook)

### Hero Section Video Variant
For the homepage hero, a shorter loop (10-15s) works best:
```
[0:00-0:03] Problem: "Your AI doesn't know your business"
[0:03-0:07] Generic LLM making mistakes
[0:07-0:10] Namakan getting it right
[0:10-0:12] "We fix that."
```

Auto-loops. No audio needed for web hero.

### Animation Vocabulary

| Name | Use When | Feel |
|------|----------|------|
| `fadeUp` | Section enters viewport | Gentle lift + fade |
| `fadeIn` | Elements that don't need lift | Pure fade |
| `scaleUp` | Cards, images on hover | Subtle grow |
| `slideIn` | Modals, drawers, dropdowns | Directional entry |
| `stagger` | Lists, grids, card stacks | Orchestrated cascade |

### Core Animation Presets

```tsx
// shared/animations.ts
import { type Transition, type Variant } from 'framer-motion'

export const fadeUp: Transition = {
  duration: 0.5,
  ease: [0.25, 0.46, 0.45, 0.94],
}

export const staggerContainer = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1,
    },
  },
}

export const staggerItem: Variant = {
  hidden: { opacity: 0, y: 20 },
  show: {
    opacity: 1,
    y: 0,
    transition: fadeUp,
  },
}

export const fadeIn: Transition = {
  duration: 0.3,
  ease: 'easeOut',
}

export const scaleUp: Variant = {
  rest: { scale: 1, opacity: 1 },
  hover: { scale: 1.02, transition: { duration: 0.2 } },
  tap: { scale: 0.98 },
}

export const slideIn = (
  direction: 'left' | 'right' | 'up' | 'down' = 'up',
  distance: number = 20
): Variant => ({
  hidden: {
    opacity: 0,
    x: direction === 'left' ? -distance : direction === 'right' ? distance : 0,
    y: direction === 'up' ? distance : direction === 'down' ? -distance : 0,
  },
  show: {
    opacity: 1,
    x: 0,
    y: 0,
    transition: fadeUp,
  },
})
```

### Usage Examples

**Hero Section — Staggered entrance:**
```tsx
<motion.div
  variants={staggerContainer}
  initial="hidden"
  animate="show"
  className="flex flex-col gap-6"
>
  <motion.h1 variants={staggerItem}>Headline</motion.h1>
  <motion.p variants={staggerItem}>Subtext</motion.p>
  <motion.button variants={staggerItem}>CTA</motion.button>
</motion.div>
```

**Card hover — Subtle lift:**
```tsx
<motion.div whileHover={{ y: -4, borderColor: 'var(--primary-600)' }}>
  Card content
</motion.div>
```

**Button press:**
```tsx
<motion.button
  whileHover={{ scale: 1.02, backgroundColor: 'var(--primary-600)' }}
  whileTap={{ scale: 0.98 }}
>
  Press me
</motion.button>
```

**Section reveal on scroll:**
```tsx
'use client'
import { motion, useInView } from 'framer-motion'
import { useRef } from 'react'

export function FadeUpSection({ children }: { children: React.ReactNode }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: '-100px' })
  
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 40 }}
      transition={{ duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] }}
    >
      {children}
    </motion.div>
  )
}

// Usage
<FadeUpSection>
  <ServicesGrid />
</FadeUpSection>
```

**Modal/Drawer:**
```tsx
<AnimatePresence>
  {isOpen && (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={() => setIsOpen(false)}
    >
      <motion.div
        initial={{ x: '100%' }}
        animate={{ x: 0 }}
        exit={{ x: '100%' }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
      >
        Drawer content
      </motion.div>
    </motion.div>
  )}
</AnimatePresence>
```

### Allowed Animations

- ✅ Page load: staggered fade-up (100-200ms delay between elements)
- ✅ Scroll reveal: fade-up on viewport entry
- ✅ Button hover: scale 1.02, background shift
- ✅ Button tap: scale 0.98
- ✅ Card hover: y lift (-4px), border brightens
- ✅ Modal/drawer: slide + backdrop fade
- ✅ Navigation: smooth drawer for mobile
- ✅ Page transitions: crossfade 200ms
- ✅ Form focus: subtle border glow transition

### Forbidden Animations

- ❌ Bouncy/spring animations on load (feels unprofessional)
- ❌ Parallax scrolling
- ❌ Auto-playing videos or animations
- ❌ Confetti, snowflakes, falling elements
- ❌ Spin animations (except loading spinners)
- ❌ Shake animations except for errors
- ❌ Excessive motion (total animation time per section < 1s)
- ❌ Animations on text selection, scrollbar, or OS elements

### Loading States

```tsx
// Don't use spinners. Use skeletons or pulse animations.
export function LoadingSkeleton() {
  return (
    <motion.div
      className="bg-slate-800 rounded"
      initial={{ opacity: 0.6 }}
      animate={{ opacity: [0.6, 1, 0.6] }}
      transition={{ duration: 1.5, repeat: Infinity }}
    />
  )
}
```

### Performance Rules

- Use `will-change` sparingly
- Prefer `transform` and `opacity` (GPU-accelerated)
- Avoid animating layout properties (width, height, margin)
- Use `once: true` for scroll animations (don't re-trigger)
- Keep total animation duration under 600ms for micro-interactions
- Keep section reveals under 800ms

---

## Responsive Behavior

### Mobile
- Single column layout
- Hamburger nav (slide-in menu)
- Full-width cards
- Larger touch targets (min 44px)
- Reduced section padding (48px)

### Tablet
- 2-column grids where appropriate
- Condensed navigation

### Desktop
- Full layout
- Hover states active
- Multi-column grids

---

## Accessibility

- Color contrast: WCAG AA minimum (4.5:1 for text)
- Focus states: visible outline on all interactive elements
- Alt text: all images
- Semantic HTML: proper heading hierarchy (h1 → h2 → h3)
- No auto-play
- Keyboard navigable

---

## Technical Stack

### Current
- **Framework**: Next.js (App Router)
- **Styling**: Tailwind CSS
- **Fonts**: Satoshi (via Fontshare CDN or self-hosted)
- **Components**: Custom (no UI library)

### Future Considerations
- CMS: Simple, headless (Sanity or similar)
- Forms: Formspree or custom
- Analytics: Plausible (privacy-focused)
- Hosting: Vercel or Cloudflare Pages

---

## Content Guidelines

### Headlines
- Lead with the problem or outcome, not the solution
- Specific > Clever
- "Stop losing deals to slow research" not "Supercharge Your AI"

### Body Copy
- 3rd person for marketing, 1st person for testimonials
- Short paragraphs (2-3 sentences max)
- Use bullets for lists, not prose
- Numbers speak louder than words: "40% faster" not "much faster"

### CTAs
- Specific: "Start Your Project" not "Submit"
- Action-oriented: verbs
- One primary CTA per section

### Images
- Real screenshots > stock photos
- Dark theme imagery when possible
- Minimal faces (none preferred)
- Technical diagrams encouraged

---

## File Structure

```
frontend/
├── app/
│   ├── page.tsx              # Homepage
│   ├── layout.tsx            # Root layout + nav + footer
│   ├── services/
│   │   ├── page.tsx          # Services overview
│   │   ├── fine-tuned/page.tsx
│   │   ├── rag/page.tsx
│   │   ├── workflows/page.tsx
│   │   └── employees/page.tsx
│   ├── about/page.tsx
│   ├── contact/page.tsx
│   └── globals.css           # Tailwind imports + custom styles
├── components/
│   ├── ui/                   # Primitives (Button, Card, Input, etc.)
│   ├── Nav.tsx
│   ├── Footer.tsx
│   ├── Hero.tsx
│   ├── ServiceCard.tsx
│   └── Testimonial.tsx
├── public/
│   ├── logo.svg
│   └── images/
├── tailwind.config.js
├── next.config.js
└── design.md                 # This file
```

---

## Implementation Priority

1. **Phase 1**: Homepage (hero, services, CTA)
2. **Phase 2**: Navigation + Footer
3. **Phase 3**: Services subpages
4. **Phase 4**: Contact page
5. **Phase 5**: About page
6. **Phase 6**: Polish (animations, transitions)

---

*Last updated: 2026-03-29*
