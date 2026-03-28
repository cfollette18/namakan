# Namakan — Service Pipelines

Automated, production-ready pipelines for each of Namakan's four service offerings.

## Directory Structure

```
pipeline/
├── fine-tuned-models/
│   ├── PIPELINE.md          — Process documentation
│   ├── workflows/
│   │   ├── data_pipeline.py       — Data collection, cleaning, PII redaction
│   │   ├── training_pipeline.py    — LoRA/QLoRA training (PEFT or Axolotl)
│   │   ├── evaluation_pipeline.py  — Perplexity, accuracy, red teaming
│   │   └── deployment_pipeline.py  — Ollama, vLLM, FastAPI, GGUF export
│   └── requirements.txt
│
├── rag-pipelines/
│   ├── PIPELINE.md
│   ├── workflows/
│   │   ├── ingestion_pipeline.py  — PDF/DOCX/HTML extraction, chunking, embedding, indexing
│   │   └── retrieval_pipeline.py   — FAISS/Chroma retrieval, re-ranking, generation
│   └── requirements.txt
│
├── agentic-workflows/
│   ├── PIPELINE.md
│   ├── workflows/
│   │   ├── agent_engine.py         — ReAct agent with tool definitions, state management
│   │   └── test_workflows.py       — Workflow testing suite
│   └── requirements.txt
│
└── custom-ai-employees/
    ├── PIPELINE.md
    ├── workflows/
    │   ├── persona_training.py     — Role-specific fine-tuning
    │   ├── onboarding.py           — AI employee onboarding automation
    │   └── monitoring.py            — Performance tracking + retraining triggers
    └── requirements.txt
```

## Quick Start

```bash
# Fine-tuned model pipeline
./run_pipeline.sh fine-tuned-models data --input ./raw-data --output ./data/prepared
./run_pipeline.sh fine-tuned-models train --base-model Qwen/Qwen2.5-7B --adapter ./adapters/client-a
./run_pipeline.sh fine-tuned-models eval --model ./outputs/final --test-data ./data/val.jsonl
./run_pipeline.sh fine-tuned-models deploy --base-model Qwen/Qwen2.5-7B --adapter ./adapters/client-a --method ollama

# RAG pipeline
./run_pipeline.sh rag-pipelines ingest --input ./documents --output ./vector-store
python3 rag-pipelines/workflows/retrieval_pipeline.py --index-dir ./vector-store --query "What is the warranty policy?"

# Agentic workflow
python3 agentic-workflows/workflows/agent_engine.py --task "Process the incoming customer email" --role "Customer Service Agent"
```

## Each Pipeline Covers

| Pipeline | Input | Output | Key Tools |
|---------|-------|--------|-----------|
| Fine-Tuned Models | Raw documents | Deployed model (Ollama/vLLM/API) | PEFT, Axolotl, llama.cpp |
| RAG Pipelines | Documents | Queryable vector store | ChromaDB, FAISS, sentence-transformers |
| Agentic Workflows | Task definition | Running agent with tools | ReAct, tool definitions |
| Custom AI Employees | Role + data | Trained agent + onboarding | Fine-tuning + workflows |
