# DevOps Skill

**Stack**: Docker, Docker Compose, GitHub Actions, nginx

## Local Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all
docker-compose down

# Reset database
docker-compose down -v && docker-compose up -d
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| postgres | 5432 | PostgreSQL 16 + pgvector |
| redis | 6379 | Redis 7 |
| backend | 8000 | FastAPI |
| frontend | 3000 | Next.js |

## Backend Deployment

```bash
cd backend
docker build -t namakan-backend .
docker run -p 8000:8000 namakan-backend
```

## Frontend Deployment

```bash
cd frontend
npm run build
# Deploy .next/ to Vercel, Netlify, or self-hosted
```

## Environment Variables

Create `backend/.env`:
```
DATABASE_URL=postgresql://admin:admin@postgres:5432/namakan_dev
REDIS_URL=redis://redis:6379
HF_TOKEN=hf_...
OPENAI_API_KEY=sk-...
```

## GitHub Actions (CI/CD)

```yaml
# .github/workflows/ci.yml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run backend tests
        run: docker-compose run backend pytest
      - name: Run frontend tests
        run: docker-compose run frontend npm test
```

## Health Checks

```yaml
# docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```
