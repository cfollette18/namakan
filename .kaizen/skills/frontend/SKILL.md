# Frontend Skill

**Stack**: Next.js 14, React 18, TypeScript, TailwindCSS, App Router

## Project Layout

```
frontend/
├── app/
│   ├── page.tsx              # Home page (server component)
│   ├── layout.tsx            # Root layout
│   ├── globals.css           # Tailwind imports
│   ├── (authenticated)/      # Protected routes (need auth)
│   │   ├── dashboard/page.tsx
│   │   ├── project/[id]/page.tsx
│   │   └── settings/page.tsx
│   └── api/                  # Route handlers (server-side)
│       └── hello/route.ts
├── components/
│   ├── ui/                   # Reusable primitives
│   └── ...                   # Feature components
├── next.config.js
├── tailwind.config.js
└── package.json
```

## Rules

1. **Server components by default** — `"use client"` only when needed (useState, useEffect, event handlers)
2. **Tailwind only** — no inline styles, no CSS modules unless necessary
3. **TypeScript strict** — no `any`, define interfaces for all props
4. **API calls in server components or route handlers** — never in client components directly
5. **Environment variables** — `NEXT_PUBLIC_` prefix for client-exposed vars

## Development

```bash
cd frontend
npm install
npm run dev      # http://localhost:3000
npm run build    # production build
npm test         # Jest tests
```

## Key Patterns

### Server Component (default):
```typescript
// app/dashboard/page.tsx
export default async function Dashboard() {
  const data = await fetchData() // direct DB call
  return <div>{data.map(item => <Card key={item.id} item={item} />)}</div>
}
```

### Client Component:
```typescript
'use client'
// components/Counter.tsx
export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

### API Route Handler:
```typescript
// app/api/projects/route.ts
export async function GET() {
  const projects = await db.projects.findMany()
  return Response.json(projects)
}
```

## Testing

```bash
npm test                  # Run all tests
npm test -- --watch      # Watch mode
```

## Adding a New Page

1. `frontend/app/my-page/page.tsx` — create the page
2. `frontend/components/my-page/` — add any components
3. Add to navigation if applicable
4. Test: `npm run dev` → `localhost:3000/my-page`
