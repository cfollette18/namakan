# Namakan Backend

FastAPI backend for the Namakan multi-agent AI platform.

## Stack

- **Framework:** FastAPI + Pydantic v2
- **Database:** PostgreSQL + Prisma ORM
- **Cache/Queue:** Redis
- **AI Runtime:** LangGraph (multi-agent orchestration)
- **Container:** Docker + Docker Compose

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL + Redis via Docker Compose
docker-compose up -d

# Run database migrations
prisma migrate dev

# Start the server
python -m uvicorn app.main:app --reload --port 8000
```

## API Docs

Once running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI schema: http://localhost:8000/openapi.json

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── agents/              # Agent base classes + LangGraph workflows
│   │   ├── base_agent.py        # Abstract agent base class
│   │   ├── orchestrator_agent.py # Top-level task orchestrator
│   │   ├── supervisor_agent.py   # Supervisor for sub-agents
│   │   ├── worker_agent.py       # Worker agent implementation
│   │   ├── langgraph_workflow.py # LangGraph state machine
│   │   └── tool_registry.py      # Agent tool registry
│   ├── collaboration/       # Multi-agent collaboration primitives
│   ├── core/               # Config, database, Redis
│   ├── db/                 # Database utilities + Prisma client
│   ├── learning/            # Agent learning + feedback systems
│   ├── marketplace/        # Agent/template marketplace
│   ├── models/             # Pydantic request/response models
│   ├── routers/            # API route handlers
│   ├── services/           # Business logic
│   └── tools/              # Agent tools (web, data, docs)
├── prisma/
│   └── schema.prisma       # Database schema
├── tests/
│   ├── test_event_store.py
│   └── test_circuit_breaker.py
├── docker-compose.yml      # PostgreSQL + Redis
├── requirements.txt
└── pytest.ini
```

## Agent Architecture

Namakan uses a **supervisor/worker** hierarchy:

```
Orchestrator Agent
└── Supervisor Agent
    ├── Worker Agent (Task A)
    ├── Worker Agent (Task B)
    └── Worker Agent (Task C)
```

- **Orchestrator:** Receives user tasks, decomposes into sub-tasks, routes to supervisors
- **Supervisor:** Manages a team of workers, handles escalation, ensures coherence
- **Worker:** Executes specific domain tasks using available tools

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/agent/run` | Run a task against the agentic system |
| POST | `/api/v1/agent/stream` | Stream agent execution |
| GET | `/api/v1/agent/status/{run_id}` | Check task status |
| POST | `/api/v1/tools/execute` | Execute a specific tool |
| GET | `/api/v1/health` | Health check |

## Environment Variables

Copy `.env-template.txt` to `.env` and configure:

```
DATABASE_URL=postgresql://namakan:namakan@localhost:5432/namakan
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=sk-...
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_event_store.py
```

## Deployment

See `DEPLOYMENT.md` in the repo root for Azure AKS deployment instructions.
