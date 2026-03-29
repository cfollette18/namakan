# Agentic Workflows — Deployment

## Production Architecture

```yaml
services:
  workflow-orchestrator:
    image: namakan/workflow-orchestrator:latest
    environment:
      - REDIS_URL=redis://redis:6379
      - POSTGRES_URL=postgres://workflows:prod
      - LOKI_URL=http://loki:3100
      - PROMETHEUS_ENABLED=true
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure

  workflow-worker:
    image: namakan/workflow-worker:latest
    environment:
      - QUEUE_URL=redis://redis/workflows
      - LLM_PROVIDER=ollama
      - OLLAMA_BASE_URL=http://ollama:11434
    deploy:
      replicas: 4

  redis:
    image: redis:7-alpine
  
  postgres:
    image: postgres:15
  
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM backend | `ollama`, `openai`, `anthropic` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://ollama:11434` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-...` |
| `REDIS_URL` | Redis connection | `redis://redis:6379` |
| `POSTGRES_URL` | PostgreSQL connection | `postgres://user:pass@host/db` |
| `LOKI_URL` | Loki server URL | `http://loki:3100` |
| `PROMETHEUS_ENABLED` | Enable metrics | `true` |
| `SESSION_STORE` | Session backend | `redis`, `postgres`, `memory` |

## Docker Compose Quick Start

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f workflow-worker

# Scale workers
docker-compose up -d --scale workflow-worker=8
```

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: workflow-worker
spec:
  replicas: 4
  selector:
    matchLabels:
      app: workflow-worker
  template:
    metadata:
      labels:
        app: workflow-worker
    spec:
      containers:
      - name: worker
        image: namakan/workflow-worker:latest
        env:
        - name: LLM_PROVIDER
          value: "ollama"
        - name: OLLAMA_BASE_URL
          value: "http://ollama-service:11434"
        resources:
          limits:
            nvidia.com/gpu: 1
```
