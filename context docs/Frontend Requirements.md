# Frontend Requirements - Namakan AI Platform

## Typography

### Primary Font: Satoshi
**All text elements must use the Satoshi font family**

- **Headings**: Satoshi Bold (700-900 weight)
- **Body Text**: Satoshi Regular (400-500 weight)
- **UI Elements**: Satoshi Medium (500-600 weight)
- **Code/Monospace**: Use Satoshi if available, fallback to system monospace

**Font Sizes:**
- Hero Headings: 72-96px (6xl-8xl)
- Section Headings: 36-48px (4xl-5xl)
- Subsections: 24-30px (2xl-3xl)
- Body Large: 18-20px (lg-xl)
- Body Regular: 16px (base)
- Body Small: 14px (sm)
- Caption: 12px (xs)

## Color Palette

### Primary Color
**Hot Pink** - The ONLY color accent allowed
- Primary 500: `#f43f5e` (Main brand color)
- Primary 400: `#fb7185` (Lighter variant)
- Primary 600: `#e11d48` (Darker variant)
- Primary 700: `#be123c` (Deep variant)

**Usage:**
- CTAs and buttons
- Links and interactive elements
- Gradients (hot pink to slightly deeper pink)
- Accent highlights
- Brand elements

### Accent Colors (Neutrals Only)
**Slate Tones:**
- Slate 50: `#f8fafc` (Lightest background - light mode)
- Slate 100: `#f1f5f9`
- Slate 200: `#e2e8f0` (Borders - light mode)
- Slate 300: `#cbd5e1`
- Slate 400: `#94a3b8` (Muted text)
- Slate 500: `#64748b`
- Slate 600: `#475569`
- Slate 700: `#334155` (Borders - dark mode)
- Slate 800: `#1e293b` (Secondary background - dark mode)
- Slate 900: `#0f172a` (Primary background - dark mode)
- Slate 950: `#020617` (Deepest background)

**Grey Tones:**
- Use sparingly, primarily for UI elements that need true neutral
- Grey 100-900 available for borders, dividers, shadows

**Black:**
- Pure Black: `#000000` (Text on light backgrounds only)
- Rich Black: `#0a0a0a` (Deep UI elements)

**White:**
- Pure White: `#ffffff` (Text on dark backgrounds, cards)
- Off-White: `#fafafa` (Subtle backgrounds)

### Prohibited Colors
**NO other colors are permitted except:**
- Hot Pink (primary)
- Slate/Grey tones
- Black
- White

**Specifically FORBIDDEN:**
- Blue (any shade)
- Purple (except as gradient FROM hot pink)
- Green (including success states)
- Yellow/Orange (including warning states)
- Red (except as part of hot pink)

**System States Must Use:**
- Success: Hot Pink with checkmark icon
- Warning: Slate 400 with alert icon
- Error: Slate 600/700 with X icon
- Info: Slate 500 with info icon

## Layout & Spacing

### Container Widths
- Max Width: 1280px (max-w-6xl)
- Hero Sections: 1536px (max-w-7xl)
- Content Sections: 1024px (max-w-5xl)

### Spacing Scale (Tailwind)
- xs: 4px (gap-1)
- sm: 8px (gap-2)
- md: 16px (gap-4)
- lg: 24px (gap-6)
- xl: 32px (gap-8)
- 2xl: 48px (gap-12)
- 3xl: 64px (gap-16)
- 4xl: 80px (gap-20)
- 5xl: 96px (gap-24)

### Section Padding
- Vertical: 80px (py-20) - Desktop
- Vertical: 48px (py-12) - Mobile
- Horizontal: 24px (px-6) - All screens

## Component Specifications

### Buttons
**Primary CTA:**
- Background: `gradient from-pink-500 to-pink-600`
- Padding: `px-8 py-4`
- Font: Satoshi Bold
- Border Radius: `rounded-xl` (12px)
- Shadow: `shadow-lg shadow-pink-500/30`
- Hover: Scale 1.05, increased shadow

**Secondary:**
- Background: `slate-800` (dark) / `slate-100` (light)
- Padding: `px-8 py-4`
- Font: Satoshi Medium
- Border: `border border-slate-700`
- Border Radius: `rounded-xl`
- Hover: Background darkens/lightens

### Cards
- Background: `white` (light) / `slate-900` (dark)
- Border: `border border-slate-200/slate-800`
- Border Radius: `rounded-2xl` (16px)
- Padding: `p-6` to `p-8`
- Shadow: `shadow-sm`
- Hover: `border-pink-500/50`, slight scale

### Navigation
- Height: 72px
- Background: `white/80` or `slate-950/80` with backdrop blur
- Sticky positioned at top
- Border bottom: `border-slate-200/slate-800`
- Links: Satoshi Medium

### Forms
**Input Fields:**
- Background: `white` (light) / `slate-800` (dark)
- Border: `border border-slate-300/slate-700`
- Border Radius: `rounded-lg` (8px)
- Padding: `px-4 py-3`
- Font: Satoshi Regular
- Focus: `border-pink-500`, `ring-2 ring-pink-500/20`

**Labels:**
- Font: Satoshi Medium
- Size: 14px (text-sm)
- Color: `slate-700` (light) / `slate-300` (dark)

## Animation Guidelines

### Transitions
- Duration: 200-300ms for most interactions
- Easing: ease-out for entrances, ease-in for exits
- Properties: transform, opacity, colors

### Hover Effects
- Buttons: Scale 1.05, shadow increase
- Cards: Border color change, subtle lift
- Links: Color change to pink-500

### Page Load
- Stagger animations: 0.1s delay between elements
- Fade in + slide up pattern
- Initial opacity: 0, translate: 20px

### Framer Motion
- Use for complex animations
- Hero text rotation: 2.5s interval
- Section reveals: scroll-triggered, once only

## Accessibility

### Contrast Ratios
- Body text: Minimum 7:1 (AAA)
- UI text: Minimum 4.5:1 (AA)
- Large text: Minimum 3:1 (AA)

### Focus States
- All interactive elements must have visible focus
- Focus ring: `ring-2 ring-pink-500/50`
- Never remove outline without replacement

### Semantic HTML
- Use proper heading hierarchy (h1 → h2 → h3)
- Use semantic tags: nav, main, section, article, footer
- Include ARIA labels where needed

## Responsive Design

### Breakpoints
- Mobile: < 768px (default)
- Tablet: 768px - 1023px (md:)
- Desktop: 1024px - 1279px (lg:)
- Large Desktop: 1280px+ (xl:)

### Mobile-First Approach
- Design for mobile first
- Progressively enhance for larger screens
- Test on actual devices

### Typography Scaling
- Hero: 3xl → 6xl → 8xl
- Headings: 2xl → 3xl → 5xl
- Body: base → lg
- Reduce line height on smaller screens

## Dark Mode

### Implementation
- Default to dark mode
- Support system preference
- Class-based toggling (Tailwind dark:)

### Color Adjustments
- Reduce contrast slightly in dark mode
- Soften hot pink intensity (use opacity)
- Ensure readability in both modes

## Performance

### Font Loading
- Use `next/font` for Satoshi
- Include font-display: swap
- Preload font files
- Subset fonts if possible

### Image Optimization
- Use Next.js Image component
- Lazy load below fold
- Appropriate formats (WebP, AVIF)
- Responsive sizing

### Code Splitting
- Lazy load heavy components
- Split routes automatically
- Minimize bundle size

## File Organization

### Component Structure
```
components/
├── ui/
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Input.tsx
│   └── ...
├── sections/
│   ├── Hero.tsx
│   ├── Features.tsx
│   └── ...
└── layout/
    ├── Navigation.tsx
    ├── Footer.tsx
    └── ...
```

### Naming Conventions
- Components: PascalCase
- Utilities: camelCase
- CSS classes: kebab-case (Tailwind handles this)
- Files: PascalCase for components, lowercase for configs

## Brand Guidelines

### Voice & Tone
- Bold and confident
- Future-focused
- Professional yet approachable
- Technical but accessible

### Imagery
- Use abstract/geometric backgrounds
- Gradient overlays with hot pink
- High contrast, modern aesthetic
- No stock photography with people

### Icons
- Use Hero Icons (outline style)
- Consistent 24px size for UI
- 48-64px for feature icons
- Hot pink color or slate for neutrals

## Icon System - Lucide Icons

### Primary Icon Library
**ONLY Lucide icons are permitted for all iconography**

- **Package**: `lucide-react` (already installed)
- **Source**: https://lucide.dev/
- **Usage**: Import specific icons from `lucide-react`
- **Size**: 24px default (w-6 h-6)
- **Style**: Outline icons only (no filled variants)

### Icon Guidelines
```typescript
// ✅ CORRECT - Import specific icons
import { CpuChipIcon, SparklesIcon, ArrowRightIcon } from 'lucide-react'

// ❌ WRONG - No Heroicons or other icon libraries
import { CpuChipIcon } from '@heroicons/react/24/outline'
```

### Common Icon Mappings
```typescript
// Navigation & Actions
SparklesIcon // For "Get Started", magic, AI
ArrowRightIcon // For CTAs, next steps
ChevronDownIcon // For dropdowns
MenuIcon // For mobile menu
XIcon // For close buttons

// AI & Technology
CpuChipIcon // For AI agents, processing
BotIcon // For automation, robots
ZapIcon // For speed, lightning fast
BrainIcon // For intelligence, learning

// Business & Features
BarChartIcon // For analytics, metrics
UsersIcon // For teams, collaboration
ShieldCheckIcon // For security, trust
CheckCircleIcon // For success states
ClockIcon // For time, scheduling

// UI Elements
SearchIcon // For search functionality
SettingsIcon // For configuration
StarIcon // For favorites, ratings
HeartIcon // For likes, favorites
```

### Icon Usage Rules
- **Consistent sizing**: Use w-6 h-6 (24px) for most icons
- **Color**: Use current text color or hot pink for accents
- **Hover states**: Icons should respond to parent hover states
- **Accessibility**: Icons should have proper ARIA labels when needed

### Prohibited Icon Libraries
❌ **DO NOT USE:**
- `@heroicons/react` (currently installed - will be removed)
- `@heroicons/react/24/outline`
- `@heroicons/react/24/solid`
- `react-icons`
- `react-feather`
- Any other icon library

### Icon Implementation
```typescript
// ✅ CORRECT - Lucide icon usage
<SparklesIcon className="w-6 h-6 text-pink-500" />

// ✅ CORRECT - With hover effects
<ArrowRightIcon className="w-5 h-5 transition-transform group-hover:translate-x-1" />

// ✅ CORRECT - In buttons
<button className="flex items-center gap-2">
  <PlayIcon className="w-5 h-5" />
  Watch Demo
</button>
```

## Development Standards

### Code Quality
- TypeScript strict mode
- ESLint configuration enforced
- Prettier for formatting
- Component testing required

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Performance Targets
- Lighthouse Score: 90+ (all metrics)
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s
- Cumulative Layout Shift: < 0.1

## Prohibited Practices

❌ **DO NOT:**
- Add colors beyond hot pink and neutrals
- Use multiple font families
- Create inconsistent spacing
- Ignore dark mode
- Skip accessibility features
- Use inline styles (use Tailwind)
- Create custom CSS unless absolutely necessary
- Use outdated Next.js patterns (use App Router)

✅ **DO:**
- Follow design system strictly
- Use Satoshi font exclusively
- Stick to hot pink for all color accents
- Test in both light and dark modes
- Verify accessibility
- Use Tailwind utilities
- Keep components modular
- Document any deviations

---

**Version:** 1.0.0  
**Last Updated:** January 19, 2026  
**Maintained By:** Namakan Frontend Team
