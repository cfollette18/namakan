# Deploy Command

Deploy the full stack to production.

## Usage

```bash
/deploy
```

## What It Does

```bash
# 1. Run tests
cd backend && pytest tests/ -q
cd frontend && npm test

# 2. Build Docker images
docker build -t namakan-backend ./backend

# 3. Push to registry (if configured)
docker tag namakan-backend:latest registry.example.com/namakan-backend:latest
docker push registry.example.com/namakan-backend:latest

# 4. Deploy (kubernetes/docker-compose)
kubectl apply -f k8s/
# OR
docker-compose -f docker-compose.prod.yml up -d
```

## Prerequisites

- [ ] All tests passing
- [ ] `docker-compose.prod.yml` configured
- [ ] Registry credentials set
- [ ] Environment variables configured in production

## Rollback

```bash
docker-compose -f docker-compose.prod.yml rollback
```
