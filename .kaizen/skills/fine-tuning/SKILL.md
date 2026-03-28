# Fine-Tuning Pipeline Skill

**Purpose**: Deliver fine-tuned models to clients using Google Colab + LoRA/QLoRA

## Pipeline Overview

```
Discovery → Data Ingestion → Colab Training → Evaluation → Deployment
```

## The 4 Service Offerings

1. **Fine-Tuned Models** ($10K–$50K)
   - LoRA/QLoRA fine-tuning via Google Colab
   - Any base model (Qwen, Llama, Mistral)
   - Data-constrained or compute-constrained approaches

## Data Ingestion (SECURE)

**ONLY** signed URLs via Azure Blob or AWS S3:
1. Generate a temporary signed URL for client's private bucket
2. Client uploads data directly to their bucket
3. Trainer downloads from signed URL → Colab → processes
4. Delete data from Colab after processing

**NEVER**: Email, Google Drive shares, third-party file hosts

## Colab Workflow

```bash
# 1. Generate client-specific notebook
python3 namakan-technical/pipeline/fine-tuned-models/colab/generate_colab.py \
  --client "Client Name" \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --train "data/train.jsonl" \
  --bucket "namakan-clients"
```

```bash
# 2. Fill in Section 0 of the generated notebook:
CLIENT_NAME = "Client Name"
BASE_MODEL = "Qwen/Qwen2.5-7B-Instruct"
HF_TOKEN = "hf_..."       # From huggingface.co
DATA_URL = "https://storage.googleapis.com/..."  # Signed URL
SYSTEM_PROMPT = "You are a helpful assistant..."
EPOCHS = 3
LORA_R = 16
```

```bash
# 3. Run all cells in Colab
# 4. Download adapter from /content/adapters/
```

## Reusable Notebook Location

```
namakan-technical/pipeline/fine-tuned-models/colab/
├── namakan-reusable-finetune.ipynb  # Main template
├── namakan-lora-training-template.ipynb
├── generate_colab.py                 # Client-specific notebook generator
├── REUSABLE.md                       # Usage docs
└── LEARNINGS.md                      # Battle-tested learnings
```

## Key Learnings (from Vermicelli)

- Use `display.clear_output(wait=True)` + `display.display()` for live charts (NOT `plt.show()`)
- Guard all log values against None/NaN
- Track train_loss and eval_loss SEPARATELY (eval only at intervals)
- Use `paged_adamw_8bit` optimizer (not `adamw_torch`)
- Use `cosine` LR scheduler
- Set `max_grad_norm=0.3`
- Set `remove_unused_columns=False`
- Evaluate every 50 steps, not just at epoch end
- `eval_strategy="steps"` not `"epoch"`
- T4 GPU: ~16GB VRAM, up to 7B model at 4-bit

## Data Format

JSONL with instruction/output pairs:
```jsonl
{"instruction": "What is the warranty?", "output": "The warranty covers 12 months..."}
{"instruction": "How do I file a claim?", "output": "To file a claim, visit..."}
```

## Deployment

After training:
1. Download adapter weights from Colab
2. Merge with base model (optional) or use LoRA inference
3. Deploy via `deployment_pipeline.py` (Ollama, vLLM, or FastAPI)
4. Client pays monthly hosting fee ($500–$2K/mo)

## Evaluation

- Perplexity (lower = better)
- Task accuracy on held-out test set
- ROUGE-L against reference responses
- Red teaming: check for hallucinations, off-topic responses
