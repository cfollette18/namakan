# Agentic Coding Team – Shared Workspace

**GitHub Repository**: https://github.com/cfollette18/agentic-coding-team

This workspace is used by a team of seven specialized AI agents:

1. **Team Lead** – orchestrator, task decomposition, coordination
2. **Frontend Architect** – React/TypeScript, UI/UX, component libraries
3. **Backend Engineer** – Node.js, REST/GraphQL APIs, authentication, Prisma ORM
4. **Database Specialist** – PostgreSQL, Prisma Schema, migrations, query optimization
5. **AI Workflow Designer** – LLM‑based automation, agentic workflows, tool integration
6. **Steve Jobs Ideation Engineer** – visionary product thinking, simplicity, user‑centric design
7. **GitHub Agent** – Git, repository management, version control, PRs, CI/CD

## Tech Stack

- **Database**: PostgreSQL (local via Docker, or cloud provider)
- **ORM**: Prisma
- **Backend**: Node.js + TypeScript, Express/Fastify
- **Frontend**: React + TypeScript, Vite, Tailwind CSS
- **Tooling**: Git, Docker, ESLint, Prettier, Playwright

## Project Structure

```
team‑coding/
├── backend/          # Node.js + Prisma backend
│   ├── prisma/
│   │   └── schema.prisma
│   ├── src/
│   └── package.json
├── frontend/         # React frontend
│   ├── src/
│   └── package.json
├── docs/             # Design decisions, API specs
├── task‑board.md     # Team task tracking
└── docker‑compose.yml (optional)
```

## Getting Started

1. **Database**: Run `docker‑compose up -d` to start PostgreSQL.
2. **Backend**: `cd backend && npm install && npx prisma migrate dev`
3. **Frontend**: `cd frontend && npm install && npm run dev`

## Communication

- Agents communicate via OpenClaw `sessions_send` and update the task‑board.md.
- All code changes are committed to this workspace (simulated Git).
- Cross‑agent dependencies should be flagged early in the task board.

## First Project

**Goal**: Build a secure note‑taking web app with user authentication, a PostgreSQL backend, and a React frontend.

**Subtasks**:
1. Database Specialist: design user and note tables in Prisma Schema.
2. Backend Engineer: implement auth endpoints (register, login, JWT) and CRUD for notes.
3. Frontend Architect: create login/register UI and a note‑management interface.
4. AI Workflow Designer: propose an automated code‑review or test‑generation workflow.
5. Team Lead: coordinate, review, and integrate.