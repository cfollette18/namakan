# Database Skill

**Stack**: PostgreSQL 16 + pgvector, Redis 7, SQLAlchemy ORM

## Services (via docker-compose)

```yaml
# docker-compose.yml
postgres:
  image: pgvector/pgvector:pg16
  ports: ["5432:5432"]
  environment:
    POSTGRES_DB: namakan_dev
    POSTGRES_USER: admin
    POSTGRES_PASSWORD: admin

redis:
  image: redis:7-alpine
  ports: ["6379:6379"]
```

## Init Schema

`init.sql` creates the schema with pgvector extension:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## ORM Models

All models in `backend/app/db/models.py` using SQLAlchemy:
```python
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from .base import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    embedding = Column(Vector(1536))  # pgvector
```

## Connection

```python
# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5432/namakan_dev")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## pgvector for RAG

```python
# Semantic search with pgvector
result = db.execute(text("""
    SELECT id, content, 1 - (embedding <=> :query_embedding) AS similarity
    FROM documents
    ORDER BY embedding <=> :query_embedding
    LIMIT 5
"""), {"query_embedding": query_embedding})
```

## Redis for Cache/Queue

```python
# backend/app/core/redis.py
import redis
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Cache agent responses
redis_client.setex(f"agent:{session_id}", ttl=3600, value=response)
```

## Never

- No raw SQL strings (use SQLAlchemy or raw text with proper escaping)
- No credentials in code (use `.env`)
- No `SELECT *` in production
