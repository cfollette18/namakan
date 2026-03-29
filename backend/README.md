# Namakan Backend

FastAPI backend for the Namakan platform.

## Stack

- **Framework:** FastAPI + Pydantic v2
- **Database:** PostgreSQL + Prisma ORM
- **Cache:** Redis
- **Container:** Docker + Docker Compose

## Structure

```
backend/
├── app/
│   ├── agents/         # Agent implementations
│   ├── collaboration/  # Multi-agent collaboration
│   ├── core/           # Config, database, redis
│   ├── db/             # Database utilities
│   ├── learning/       # Learning/feedback systems
│   ├── marketplace/    # Marketplace functionality
│   ├── models/         # Pydantic models
│   ├── routers/        # API routes
│   ├── services/       # Business logic
│   └── tools/          # Agent tools
├── prisma/            # Database schema
├── tests/             # Test suite
└── main.py            # FastAPI entry point
```

## Setup

```bash
cd backend
cp env-template.txt .env
# Configure .env with database credentials
docker-compose up -d
python3 -m prisma migrate dev
uvicorn app.main:app --reload
```

## Development

```bash
pytest backend/        # Run tests
pytest backend/tests/  # Specific test dir
```

## API

See `app/main.py` for routes. API docs at `/docs` when running.
