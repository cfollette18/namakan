# Codebase Skill

**Purpose**: Navigate, understand, and modify the Namakan codebase efficiently.

## Repo Structure

```
namakan/
├── frontend/              # Next.js 14 (App Router)
│   ├── app/
│   │   ├── page.tsx         # Home/landing
│   │   ├── layout.tsx        # Root layout
│   │   ├── (authenticated)/ # Protected routes
│   │   └── api/             # Route handlers
│   ├── components/          # UI components
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/               # FastAPI
│   ├── app/
│   │   ├── main.py           # FastAPI entry
│   │   ├── agents/           # LangGraph agents
│   │   ├── routers/          # /agents, /projects, /users
│   │   ├── services/         # Business logic
│   │   ├── models/           # Pydantic models
│   │   ├── tools/            # Agent tools (web, code, file)
│   │   └── core/             # config, database, redis
│   ├── requirements.txt
│   ├── pytest.ini
│   └── prisma/schema.prisma
│
├── namakan-technical/        # 4 service pipelines
│   ├── fine-tuned-models/
│   ├── rag-pipelines/
│   ├── agentic-workflows/
│   └── custom-ai-employees/
│
├── docker-compose.yml     # PostgreSQL + Redis
└── init.sql             # DB schema + pgvector
```

## How to Navigate

### Find a backend endpoint:
```bash
grep -r "router\|@app\|APIRouter" backend/app/routers/
```

### Find a frontend page:
```bash
ls frontend/app/
```

### Find an agent definition:
```bash
ls backend/app/agents/
```

### Find pipeline workflows:
```bash
ls namakan-technical/*/workflows/
```

## Common Tasks

### Add a new API route:
1. Create `backend/app/routers/my_feature.py`
2. Import into `backend/app/main.py`
3. Add to FastAPI app: `app.include_router(my_feature.router)`

### Add a new frontend page:
1. Create `frontend/app/my-page/page.tsx`
2. Use App Router conventions (server component by default)

### Add a new agent tool:
1. Create tool in `backend/app/tools/my_tool.py`
2. Register in `backend/app/agents/tool_registry.py`

### Update a pipeline:
1. Read `namakan-technical/{service}/PIPELINE.md`
2. Update the relevant workflow script
3. Update `namakan-technical/{service}/workflows/`
4. Commit and push

## Code Conventions

- **Python**: `ruff` for linting/formatting, `pytest` for tests
- **TypeScript**: `eslint` + `prettier`, `npm test` for tests
- **Commits**: conventional format (`feat:`, `fix:`, `docs:`)
