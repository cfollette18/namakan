# Namakan Frontend

Next.js 15 frontend for Namakan AI Engineering (future production site).

## Stack

- **Framework:** Next.js 15 (App Router)
- **UI:** Tailwind CSS, Radix UI components
- **Animations:** Framer Motion
- **State:** TanStack React Query
- **HTTP:** Axios

## Pages

| Route | File | Purpose |
|-------|------|---------|
| `/` | `app/page.tsx` | Landing page |
| `/about` | `app/about/` | About page |
| `/solutions` | `app/solutions/` | Service offerings |
| `/pricing` | `app/pricing/` | Pricing tiers |
| `/contact` | `app/contact/` | Contact form |
| `/auth` | `app/auth/` | Authentication |
| `/privacy` | `app/privacy/` | Privacy policy |
| `/terms` | `app/terms/` | Terms of service |

## Development

```bash
cd frontend
npm install
npm run dev
```

## Build

```bash
npm run build
npm start
```

## Note

The current live website is the static HTML/CSS version in `../namakan-website/`. This Next.js version is for future production deployment.
