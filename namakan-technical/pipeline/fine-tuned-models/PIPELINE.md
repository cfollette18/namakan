# Fine-Tuned Models Pipeline

*Namakan AI Engineering — Service Offering #1*

---

## The Offering

We train private AI models on a client's proprietary data. The result: an AI that understands THEIR domain, not just language in general.

**What they get:**
- A private AI model they own and control
- Deployed on their infrastructure or ours
- Continuously improved as more data becomes available

---

## Engagement Pipeline

```
Discovery → Data Assessment → Proposal → Contract → Data Intake →
Training → Evaluation → Deployment → Training → Handoff
```

---

## Phase 1: Discovery

### Discovery Call (45-60 min)


### Client-Specific Decisions Locked
- **Data Ingestion**: Signed URLs via Azure Blob / AWS S3 — clients upload directly to Namakan private cloud bucket. No third-party file-sharing services.
- **Base Model**: Per-client — determine based on size needs, reasoning requirements, and budget (Qwen/Llama/Mistral options)
- **Deployment**: Either client infrastructure OR Namakan-hosted on cloud with monthly subscription model
- **Training**: Google Colab (all training done in Colab — no local GPU needed)

- [ ] Understand their business, industry, products
- [ ] Identify what they want the model to do
- [ ] Assess data availability and quality
- [ ] Preliminary scope and timeline estimate
- [ ] Budget qualification

### Discovery Output
- Summary of understanding
- Preliminary scope document
- Ballpark estimate: $10K-50K based on complexity

---

## Phase 2: Data Assessment

### Data Audit (1-2 weeks)
- Inventory available data sources
- Estimate volume and format
- Assess labeling requirements
- Identify PII/sensitive data
- Data quality scoring

### Assessment Deliverable
- Data audit report
- Recommended data preparation approach
- Final scope and timeline
- Fixed-price proposal

---

## Phase 3: Data Intake & Preparation

### Secure Data Transfer
- Encrypted upload via SFTP
- SHA-256 hash verification
- Virus/malware scan
- Data manifest generation

### Data Cleaning
```python
# Standard cleaning pipeline
def clean_training_data(raw_dir, clean_dir):
    for filename in os.listdir(raw_dir):
        text = read(filename)
        text = normalize_whitespace(text)
        text = remove_control_characters(text)
        text = redact_pii(text)          # SSN, email, phone
        text = anonymize_entities(text)  # Names, addresses
        text = filter_quality(text)      # Length, duplicates
        save(clean_dir, filename, text)
```

### Format as Instruction Data
```json
{
  "instruction": "What is the return policy for widget X?",
  "input": "",
  "output": "Widget X can be returned within 30 days..."
}
```

### Data Volume Guidelines

| Model Size | Min Examples | Recommended | Max Context |
|-----------|-------------|-------------|-------------|
| 3B | 1,000 | 5,000 | 8K |
| 7B | 2,000 | 10,000 | 16K |
| 13B | 5,000 | 20,000 | 32K |
| 70B | 10,000 | 50,000 | 128K |

---

## Phase 4: Model Selection

### Base Model Recommendation

| Use Case | Recommended Base | Size | Hardware |
|----------|-----------------|------|----------|
| General domain | Llama 3.1/3.2 | 8B, 13B | 1x A100 or 4x 3090 |
| Code generation | Qwen2.5-Coder | 7B, 13B | 1x A100 |
| Reasoning | DeepSeek R1 | 7B, 14B | 1x A100 |
| Multimodal | Qwen2-VL | 11B, 90B | 2x A100 |
| Domain expert | Llama 3.1 + corpus | 8B-70B | Varies |
| Edge/deployment | Qwen2.5-3B, Mistral | 3B-7B | Consumer GPU |

### Client Presentation
- Explain recommendation
- Discuss tradeoffs (quality vs cost vs speed)
- Get written approval on base model selection

---

## Phase 5: Training

### LoRA Configuration
```yaml
base_model: Qwen/Qwen2.5-14B-Instruct
adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj
  - k_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj

training:
  num_epochs: 3
  micro_batch_size: 2
  gradient_accumulation_steps: 8
  learning_rate: 0.0002
  warmup_steps: 10
  optimizer: adamw_torch
  torch_dtype: float16
  bf16: full
  gradient_checkpointing: true
```

### Training Process
```
1. Load base model (quantized if large)
2. Tokenize dataset
3. Initialize LoRA adapters
4. Run training with gradient checkpointing
5. Save checkpoints at intervals
6. Evaluate at each checkpoint
7. Select best checkpoint
```

### Training: Google Colab (Primary)
We use Google Colab for all model training — no local GPU required.

**Why Colab:**
- Free tier: T4 GPU available
- Colab Pro ($10/mo): L4/A100 available
- No setup, fully managed environment
- Data stays in Google Cloud (secure)
- Easy to share notebooks with client for review

**Colab Workflow:**
```
1. Client uploads data via S3 signed URL → Google Cloud Storage bucket
2. Trainer creates Colab notebook with:
   - Mount GCS bucket
   - Load base model (Qwen/Llama/Mistral)
   - Load training data from GCS
   - Configure LoRA/QLoRA training (PEFT)
   - Train with GPU acceleration
   - Save adapter weights to GCS
3. Download trained adapters → deploy to inference stack
4. Share Colab notebook with client for reproducibility
```

**Colab Notebooks:**
- Use `transformers` + `peft` + `trl` libraries
- T4 GPU: up to 7B models in 4-bit
- A100: up to 70B models
- Always use `torch.float16` for GPU efficiency
- Save checkpoints to Google Drive or GCS

**Training Libraries (in Colab):**
```bash
!pip install transformers peft trl accelerate bitsandbytes
```

### Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Loss NaN | LR too high, bad data | Reduce LR, clean data |
| Catastrophic forgetting | Too many epochs | Early stopping, more diverse data |
| Bad output format | Instruction format mismatch | Fix template |
| Overfitting | Too few examples | Add regularization |

---

## Phase 6: Evaluation

### Evaluation Metrics
- **Perplexity** — Model confidence
- **Task accuracy** — Did it complete the task?
- **ROUGE/BLEU** — N-gram overlap
- **BERTScore** — Semantic similarity
- **Human evaluation** — Gold standard

### Evaluation Framework
```python
def evaluate_model(model, test_data, tokenizer):
    perplexity = compute_perplexity(model, test_data)
    accuracy = compute_task_accuracy(model, test_data)
    
    predictions = [generate(prompt) for prompt in test_data["prompt"]]
    references = test_data["reference"]
    
    return {
        "perplexity": perplexity,
        "accuracy": accuracy,
        "rouge": rouge.compute(predictions=predictions, references=references),
        "human_sample": human_evaluate(predictions[:20])
    }
```

### Red Teaming
- Adversarial prompts
- PII extraction attempts
- Hallucination tests
- Out-of-domain queries

---

## Phase 7: Deployment

### Deployment Options

**Option A: Our Infrastructure**
- Deploy on our GPU servers
- API access for client
- Monthly fee: $500-2K/mo

**Option B: Client's Cloud**
- AWS, GCP, or Azure
- We set up, client manages
- One-time setup: $2K-5K

**Option C: On-Premise**
- Deploy on client's hardware
- Full privacy
- Setup time longer

### Inference Stack
```python
# llama.cpp (CPU/GPU, fast)
from llama_cpp import Llama
llm = Llama(model_path="./model.gguf", n_ctx=4096)

# vLLM (higher throughput, needs GPU)
from vllm import LLM
llm = LLM(model="./model/", tensor_parallel_size=1)
```

### API Layer
```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/generate")
async def generate(prompt: str, max_tokens: int = 512):
    output = llm.generate(prompt, max_tokens=max_tokens)
    return {"output": output}
```

---

## Phase 8: Monitoring & Iteration

### Production Monitoring
- Request latency
- Token usage
- Error rates
- Output quality sampling
- Drift detection

### Retraining Triggers
- Performance drops below threshold
- New data available (>1K new examples)
- Quarterly refresh cycle
- Client feedback

---

## Deliverables

1. **Trained model weights** (LoRA adapters or full model)
2. **Inference API** (FastAPI + Docker)
3. **Deployment documentation**
4. **Evaluation report** (pre/post metrics)
5. **User guide** for API integration
6. **3-month support** included

---

## Pricing

| Tier | Data Size | Model Size | Timeline | Price |
|------|-----------|------------|----------|-------|
| **Starter** | 1-5K examples | 3B-7B | 2-3 weeks | $10K-20K |
| **Professional** | 5-15K examples | 8B-14B | 3-5 weeks | $20K-35K |
| **Enterprise** | 15K+ examples | 30B-70B | 6-10 weeks | $35K-50K |
| **Annual Retainer** | Ongoing | Any | Continuous | $3K-8K/mo |

---

## Timeline

```
Week 1-2:    Discovery + Data Assessment
Week 2-3:    Data Intake + Preparation
Week 3-6:    Training (depending on size)
Week 6-7:    Evaluation + Iteration
Week 7-8:    Deployment + Testing
Week 8-9:    Handoff + Training
```

Total: 8-10 weeks typical
