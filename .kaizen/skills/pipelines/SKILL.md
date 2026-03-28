# Pipelines Skill

**Purpose**: Reference for all 4 Namakan service delivery pipelines.

## The 4 Pipelines

```
namakan-technical/pipeline/
├── fine-tuned-models/       # LoRA/QLoRA fine-tuning via Colab
├── rag-pipelines/           # ChromaDB document retrieval
├── agentic-workflows/       # ReAct autonomous agents
└── custom-ai-employees/     # Role-specific AI workers
```

## Each Pipeline Has

```
{pipeline}/
├── PIPELINE.md              # Full engagement guide
├── workflows/               # Python automation scripts
│   ├── data_pipeline.py     # (fine-tuned only)
│   ├── ingestion_pipeline.py # (RAG only)
│   └── ...
├── requirements.txt
└── colab/                   # Colab notebooks (fine-tuned only)
    ├── namakan-reusable-finetune.ipynb
    ├── LEARNINGS.md
    └── generate_colab.py
```

## Reading a Pipeline Doc

1. Start with the PIPELINE.md — engagement flow, discovery questions, deliverables
2. Check workflows/*.py for automation scripts
3. For fine-tuning: also check colab/REUSABLE.md + colab/LEARNINGS.md

## Fine-Tuning Pipeline

- Colab primary training environment
- Data: S3/Azure signed URL ingestion
- LoRA R=16, α=32, epochs=3, lr=2e-4
- ChromaDB for vector retrieval
- Deployment: client infra OR Namakan cloud subscription

## RAG Pipeline

- ChromaDB vector store (client preference)
- Documents: PDF, DOCX, HTML, TXT, CSV
- Chunking: 512 tokens, 50-token overlap
- Retrieval: hybrid search + cross-encoder reranking

## Agentic Workflows

- LangGraph ReAct loop
- Tools: web_search, file_read, file_write, run_command, human_escalate
- Confidence thresholds: >0.8 = execute, 0.5-0.8 = explain, <0.5 = escalate

## Custom AI Employees

- Role persona fine-tuning
- Onboarding: Shadow → Assist → Partial → Full autonomy
- Monthly performance monitoring + retraining triggers
- $2K-$5K/month subscription
