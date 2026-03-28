# Backend Skill

**Stack**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy, PostgreSQL, Redis, LangGraph

## Project Layout

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── agents/              # LangGraph agent definitions
│   │   ├── base_agent.py
│   │   ├── orchestrator_agent.py
│   │   ├── supervisor_agent.py
│   │   ├── worker_agent.py
│   │   ├── tool_registry.py
│   │   ├── circuit_breaker.py
│   │   └── langgraph_workflow.py
│   ├── routers/            # API endpoints
│   │   ├── agents.py
│   │   ├── projects.py
│   │   ├── users.py
│   │   └── marketplace.py
│   ├── services/            # Business logic
│   │   ├── agent_service.py
│   │   ├── ai_service.py
│   │   └── project_service.py
│   ├── models/              # Pydantic models
│   ├── tools/               # Agent tools
│   │   ├── web_browser.py
│   │   ├── document_writer.py
│   │   └── data_analyzer.py
│   ├── core/                # Config, DB, Redis
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── redis.py
│   │   └── event_store.py
│   └── db/
│       └── models.py        # SQLAlchemy ORM models
├── prisma/schema.prisma   # DB schema (Prisma)
├── requirements.txt
└── pytest.ini
```

## Rules

1. **Async everywhere** — `async def` for all route handlers and DB operations
2. **Pydantic for validation** — all request/response models use Pydantic
3. **SQLAlchemy ORM** — no raw SQL strings
4. **Dependency injection** — use FastAPI's `Depends()` for shared resources
5. **Never commit secrets** — use `.env` files, `python-dotenv`

## Development

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
pytest                    # Run tests
pytest -v                 # Verbose
pytest tests/test_*.py    # Specific test file
```

## Key Patterns

### API Route:
```python
# backend/app/routers/agents.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.pydantic import AgentCreate

router = APIRouter(prefix="/agents", tags=["agents"])

@router.post("/")
async def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    return {"id": agent.id, "name": agent.name}
```

### Database Session:
```python
from ..core.database import get_db

@router.get("/items")
async def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### Agent Tool:
```python
# backend/app/tools/web_browser.py
class WebBrowserTool:
    name = "web_search"
    description = "Search the web for information"

    def run(self, query: str) -> str:
        # implementation
        return result
```

## Adding a New Router

1. Create `backend/app/routers/my_feature.py`
2. Import: `from .my_feature import router as my_feature_router`
3. Register in `main.py`: `app.include_router(my_feature_router, prefix="/api/v1")`

## Testing

```bash
cd backend
pytest tests/ -v --tb=short
```
