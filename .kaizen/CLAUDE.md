# Namakan — AI Engineering Firm

## What We Build

Custom AI systems for businesses:
1. **Fine-Tuned Models** — LoRA/QLoRA fine-tuning via Google Colab (Build: $5K–$15K)
2. **RAG Pipelines** — ChromaDB + document retrieval (Build: $5K–$15K + $500/mo)
3. **Agentic Workflows** — ReAct agents with custom tools (Build: $5K–$15K)
4. **Custom AI Employees** — Role-specific AI workers (Retainer: $2K/mo)

## The Stack

```
Frontend:     Next.js 14 (App Router) + TailwindCSS + TypeScript
Backend:      FastAPI (Python) + Pydantic + LangGraph
Database:     PostgreSQL 16 + pgvector
Cache/Queue:  Redis 7
AI Runtime:   LangGraph multi-agent orchestration
Vector Store: ChromaDB (client) / FAISS (local)
Training:     Google Colab (LoRA/QLoRA via PEFT + transformers)
```

## Repo Structure

```
namakan/
├── frontend/              # Next.js 14 app
│   └── app/              # App Router pages
├── backend/              # FastAPI Python app
│   └── app/
│       ├── agents/       # Agent definitions
│       ├── routers/      # API endpoints
│       ├── services/     # Business logic
│       ├── models/       # Pydantic models
│       ├── tools/        # Agent tools
│       └── core/         # Config, DB, Redis
├── namakan-technical/
│   └── agentic-workflows/  # Workflows: intake, agent_engine, eval_pipeline, monitoring
│       └── workflows/    # Core workflow modules
├── namakan-business/     # Business plans, pricing
├── namakan-sales/        # Sales scripts, target list
├── namakan-marketing/    # Content, strategy
├── namakan-legal/        # MSA, NDA, contracts
├── teams/               # Pre-configured agent teams
└── docker-compose.yml    # PostgreSQL + Redis
```

## Key Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | PostgreSQL 16 + pgvector, Redis 7 |
| `init.sql` | Database schema + pgvector extension |
| `namakan-technical/SECURE-DATA-PIPELINE.md` | Client data handling |
| `namakan-technical/agentic-workflows/` | Core workflow modules |
| `teams/` | Pre-built agent teams |

## Philosophy

- **No hallucinations** — AI must always ground responses in retrieved context
- **Human in the loop** — escalation paths for uncertain or high-stakes decisions
- **Production-first** — code that ships is better than code that's perfect
- **Data security** — client data is sacred, never exfiltrated
