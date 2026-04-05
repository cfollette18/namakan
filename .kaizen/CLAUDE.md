# Namakan — AI Engineering Firm

## What We Build

Custom AI systems for businesses with proprietary data:
1. **Fine-Tuned Models** — Train AI on your data (SMB: $5K–$15K, Mid-Market: $15K–$25K, Enterprise: $25K–$40K)
2. **Custom Agents** — AI workers on top of your fine-tuned model (Build/Growth/Enterprise: $5K–$30K)
3. **Custom AI Employees** — Full-time AI workers, ongoing retainer (Standard: $2K/mo, Senior: $4K/mo)
4. **RAG Pipelines** — Document retrieval, built into fine-tuning projects ($500–$2K/mo operations)

Every engagement starts with fine-tuning. Agents build on top of the model that knows your business.

## The Stack

```
Training:     Google Colab (LoRA/QLoRA via PEFT + transformers)
Agent Runtime: LangGraph (stateful multi-agent orchestration)
ReAct Pattern: Reason + Act + Observe loop
LLM:          Dynamic (OpenAI, Anthropic, or local Ollama)
Vector Store:  ChromaDB (client) / FAISS (local)
Observability: Prometheus metrics + Loki structured logging
Testing:       pytest with eval_pipeline.py
```

## Repo Structure

```
namakan/
├── namakan-technical/          # Engineering pipelines
│   ├── fine-tuned-models/      # LoRA/QLoRA training + workflows
│   ├── rag-pipelines/         # ChromaDB document retrieval
│   ├── agentic-workflows/      # ReAct autonomous agents (v2.0)
│   └── custom-ai-employees/   # Role-specific AI workers
├── namakan-business/           # Pricing, business plans, service offerings
├── namakan-sales/             # Cold outreach, objection handling, proposals
├── namakan-marketing/         # Content, advertising, strategy
├── namakan-legal/             # MSA, NDA, contracts
├── frontend/                   # Next.js website (namakanai.com)
└── .kaizen/                   # Kaizen agent config (this file)
```

## Key Files

| File | Purpose |
|------|---------|
| `namakan-business/service-offerings.md` | Current pricing and service descriptions |
| `namakan-business/pricing_section.md` | Detailed pricing breakdown |
| `namakan-technical/*/PIPELINE.md` | Phase-by-phase engagement guides |
| `namakan-sales/COLD-EMAIL-SEQUENCE.md` | 5-email outreach sequence |
| `namakan-sales/OBJECTION-HANDLING.md` | Top 10 objections + responses |
| `namakan-sales/PROPOSAL-TEMPLATE.md` | Proposal template |
| `namakan-technical/*/SECURE-DATA-PIPELINE.md` | Client data handling |

## Philosophy

- **No hallucinations** — AI must always ground responses in retrieved context
- **Human in the loop** — escalation paths for uncertain or high-stakes decisions
- **Production-first** — code that ships is better than code that's perfect
- **Data security** — client data is sacred, never exfiltrated
