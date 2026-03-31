# Namakan Technical Reference

Complete technical documentation for all 4 Namakan AI Engineering service pipelines.

---

## The 4 Pipelines

```
namakan-technical/
├── fine-tuned-models/       → LoRA/QLoRA fine-tuning via Google Colab
├── rag-pipelines/          → ChromaDB document retrieval
├── agentic-workflows/       → ReAct autonomous agents (primary active pipeline)
└── custom-ai-employees/    → Role-specific AI workers
```

---

## Each Pipeline Contains

| Directory | Contents |
|-----------|----------|
| `PIPELINE.md` | Complete engagement guide — discovery questions, phases, deliverables, pricing |
| `workflows/` | Runnable Python scripts for each phase of the pipeline |
| `SECURE-DATA-PIPELINE.md` | Data handling, classification, encryption, compliance |
| `requirements.txt` | Python dependencies |
| `colab/` | Google Colab notebooks and training tools *(fine-tuned-models only)* |

---

## Pipeline Summary

### 1. Fine-Tuned Models ($5K–$15K)
**LoRA/QLoRA fine-tuning via Google Colab**

- Discovery → Data Assessment → Secure Intake → Training → Evaluation → Deployment → Monitoring
- Base models: Qwen, Llama, Mistral
- Colab notebooks with live loss charts
- Deployment: client infra OR Namakan cloud subscription

**Key files:**
- `PIPELINE.md` (17K chars) — full engagement guide
- `workflows/data_pipeline.py` — PII redaction, cleaning, formatting
- `workflows/training_pipeline.py` — LoRA/QLoRA training
- `workflows/evaluation_pipeline.py` — perplexity, accuracy, red teaming
- `workflows/deployment_pipeline.py` — Ollama, vLLM, FastAPI
- `colab/namakan-reusable-finetune.ipynb` — universal training notebook

### 2. RAG Pipelines ($5K–$15K build + $500/mo)
**ChromaDB vector store + document retrieval**

- Discovery → Document Audit → Architecture → Build → Evaluation → Deploy → Handoff
- Vector DB: ChromaDB (client-confirmed preference)
- Data ingestion: S3/Azure signed URLs only
- Chunking: 512 tokens, 50-token overlap
- Retrieval: hybrid search + cross-encoder re-ranking

**Key files:**
- `PIPELINE.md` (10K chars) — full engagement guide
- `workflows/ingestion_pipeline.py` — extract, chunk, embed, index
- `workflows/retrieval_pipeline.py` — query, retrieve, re-rank, generate

### 3. Agentic Workflows ($5K–$15K)
**ReAct autonomous agents with custom tools**

- Discovery → Process Mapping → Architecture → Build → Testing → Eval → Monitor → Deploy
- Runtime: LangGraph (stateful multi-agent orchestration)
- Pattern: ReAct loop (Reason + Act + Observe)
- Tools: web_search, file_read, file_write, run_command, human_escalate
- Confidence thresholds: >0.8 execute, 0.5-0.8 explain, <0.5 escalate

**Key files:**
- `PIPELINE.md` (modular — split into docs/01-07-*.md)
- `docs/` — modular docs: Engagement Pipeline, Process Mapping, Architecture, Build, Testing, Deployment, Monitoring
- `workflows/agent_engine.py` — ReAct agent + tool registry (v2.0: multi-LLM, streaming, self-correction)
- `workflows/eval_pipeline.py` — pytest test suite (happy path, error injection, escalation, concurrency)
- `workflows/monitoring.py` — Prometheus metrics + Loki structured logging

### 4. Custom AI Employees ($2K/mo)
**Role-specific AI workers with permanent deployment**

- Discovery → Persona Design → Training → Onboarding → Full Deployment → Monitoring
- Onboarding phases: Shadow → Assist → Partial → Full autonomy
- Monthly performance monitoring + retraining triggers
- Supervisor assigned per AI Employee

**Key files:**
- `PIPELINE.md` (14K chars) — full engagement guide

---

## Shared: SECURE-DATA-PIPELINE.md

Every pipeline includes `SECURE-DATA-PIPELINE.md` — mandatory data handling rules:
- S3/Azure signed URLs only for ingestion
- AES-256 encryption at rest, TLS 1.2+ in transit
- No third-party file-sharing services
- Client data deleted within 30 days of project completion
- HIPAA/GDPR/SOC 2 compliance frameworks

---

## Workflow Execution

Run any pipeline phase directly:

```bash
# Fine-tuned models
./run_pipeline.sh fine-tuned-models data --input ./raw-data
./run_pipeline.sh fine-tuned-models train --client "Acme Corp"
./run_pipeline.sh fine-tuned-models eval --model ./outputs/final
./run_pipeline.sh fine-tuned-models deploy --adapter ./adapters/acme

# RAG pipelines
./run_pipeline.sh rag-pipelines ingest --input ./documents
./run_pipeline.sh rag-pipelines query --question "What is the warranty policy?"

# Agentic workflows
python3 agentic-workflows/workflows/agent_engine.py --task "Process incoming email"
```
