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


---

# Custom LLM / Fine-Tuning Pipeline

*Namakan AI Engineering — Technical Reference*

---

## The Offering

We build **private, domain-specific AI models** trained on a client's proprietary data. Unlike generic AI, their model understands their industry, their products, their customers — and nothing else.

**What you get:**
- A private AI model they own and control
- Deployed on their infrastructure or ours
- Continuously improved as more data becomes available

---

## Pipeline Overview

```
Client Data → Assessment → Data Prep → Training → Evaluation → Deployment → Monitoring
```

---

## Phase 1: Discovery & Assessment

### 1.1 Data Audit
- Inventory all available data sources
- Estimate data volume and quality
- Identify PII and sensitive data
- Assess labeling requirements

### 1.2 Use Case Definition
- What should the model do?
- How will it be used?
- What does success look like?

### 1.3 Base Model Selection

| Use Case | Recommended Base | Size | Hardware |
|----------|-----------------|------|----------|
| General chat | Llama 3.1/3.2 | 8B, 13B | 1x A100 or 4x 3090 |
| Code generation | CodeLlama, Qwen2.5-Coder | 7B, 13B | 1x A100 |
| Reasoning | DeepSeek R1 | 7B, 14B | 1x A100 |
| Multimodal | Qwen2-VL, Llama 3.2-Vision | 11B, 90B | 2x A100 |
| Domain expert | Llama 3.1 + domain corpus | 8B-70B | Varies |
| Edge/deployment | Qwen2.5-3B, Mistral-3B | 3B-7B | Consumer GPU |

### 1.4 Scope & Proposal
- Data prep timeline
- Training timeline
- Evaluation criteria
- Deployment approach
- Pricing

---

## Phase 2: Data Collection & Preparation

### 2.1 Data Sources
- Internal documents (PDF, Markdown, HTML)
- CRM data
- Support tickets and chat logs
- Email archives
- Product databases
- Public datasets (industry-specific)
- Synthetic data generation

### 2.2 Data Cleaning
```python
# Example: cleaning text data
import re
from datasets import load_dataset

def clean_text(text):
    # Remove PII
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)  # SSN
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b', '[EMAIL]', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def filter_quality(texts, min_length=50, max_length=8192):
    return [t for t in texts if min_length <= len(t) <= max_length]
```

### 2.3 Data Formats

**Instruction Tuning (recommended for task completion):**
```json
{
  "instruction": "What is the return policy for widget X?",
  "input": "",
  "output": "Widget X can be returned within 30 days of purchase with receipt..."
}
```

**Chat Format (for conversational AI):**
```json
{
  "messages": [
    {"role": "system", "content": "You are AcmeBot, a customer service AI."},
    {"role": "user", "content": "How do I reset my password?"},
    {"role": "assistant", "content": "To reset your password, go to acme.com/reset..."}
  ]
}
```

**Completion Format (for text generation):**
```json
{"text": "Customer: I need to return my order.\nAgent: I'm sorry to hear that..."}
```

### 2.4 Data Volume Guidelines

| Model Size | Min Examples | Recommended | Max Context |
|-----------|-------------|-------------|-------------|
| 3B | 1,000 | 5,000 | 8K |
| 7B | 2,000 | 10,000 | 16K |
| 13B | 5,000 | 20,000 | 32K |
| 70B | 10,000 | 50,000 | 128K |

### 2.5 Synthetic Data Generation
For clients with limited data, generate synthetic examples:
```python
# Use a stronger model to generate training examples
from openai import OpenAI
client = OpenAI()

def generate_synthetic_examples(domain, n=100):
    prompt = f"""Generate {n} question-answer pairs about {domain}.
    Format as JSON array of {{"instruction": "...", "output": "..."}}
    Make questions diverse and realistic."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)
```

---

## Phase 3: Training

### 3.1 Training Stack
- **Framework**: Axolotl, Unsloth, or PEFT + Transformers
- **Method**: LoRA (default), QLoRA (for large models on limited hardware), DPO (for preference alignment)
- **Hardware**: Our GPU cluster or client infrastructure

### 3.2 LoRA Configuration
```yaml
# axolotl config for LoRA fine-tuning
base_model: Qwen/Qwen2.5-14B-Instruct
model_type: AutoAutoModelForCausalLM

dataset_prepared_path: ./data/prepared
output_dir: ./outputs
sequence_len: 2048

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

dataset:
  type: instruction
  train_file: ./data/train.jsonl
  val_file: ./data/val.jsonl

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
  logging_steps: 10
  save_steps: 100
  eval_steps: 100
  save_total_limit: 3
```

### 3.3 Training Process
```
1. Load base model (quantized if large)
2. Tokenize dataset
3. Initialize LoRA adapters
4. Run training with gradient checkpointing
5. Save checkpoints
6. Evaluate at intervals
7. Select best checkpoint
```

### 3.4 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Loss NaN | Learning rate too high, bad data | Reduce LR, clean data |
| Catastrophic forgetting | Too many epochs, wrong data ratio | Early stopping, more diverse data |
| Mode collapse | Data too homogeneous | Increase data diversity |
| Bad output format | Instruction format mismatch | Fix template, validate data |
| Overfitting | Too few examples, too many epochs | Add regularization, early stopping |

---

## Phase 4: Evaluation

### 4.1 Metrics
- **Perplexity** — Model confidence (lower = better)
- **ROUGE/BLEU** — N-gram overlap with reference
- **BERTScore** — Semantic similarity
- **Task-specific accuracy** — Did it complete the task?
- **Human evaluation** — Gold standard

### 4.2 Evaluation Framework
```python
from transformers import LLMCharacterLevelCrossEntropy
import evaluate

def evaluate_model(model, test_data, tokenizer):
    perplexity = LLMCharacterLevelCrossEntropy.compute(
        model=model, data=test_data
    )
    
    rouge = evaluate.load("rouge")
    bleurt = evaluate.load("bleurt")
    
    predictions = [generate(prompt) for prompt in test_data["prompt"]]
    references = test_data["reference"]
    
    return {
        "perplexity": perplexity,
        "rouge": rouge.compute(predictions=predictions, references=references),
        "bleurt": bleurt.compute(predictions=predictions, references=references)
    }
```

### 4.3 Red Teaming
- Adversarial prompts
- PII extraction attempts
- Hallucination tests
- Out-of-domain queries
- Format injection attacks

---

## Phase 5: Deployment

### 5.1 Deployment Options

**Option A: Our Infrastructure (Fastest)**
- Deploy on our GPU servers
- API access for client
- We handle maintenance
- Monthly fee

**Option B: Client's Cloud**
- Deploy on AWS, GCP, or Azure
- We set up, client manages
- One-time setup + hourly consulting

**Option C: On-Premise**
- Deploy on client's hardware
- Full privacy, highest latency
- Longest setup time

**Option D: Hybrid**
- Sensitive data stays on-prem
- Inference in our cloud
- Custom architecture

### 5.2 Inference Stack

**For 3B-13B models:**
```python
# llama.cpp (CPU/GPU, fast, portable)
from llama_cpp import Llama
llm = Llama(model_path="./model.gguf", n_ctx=4096)

# or vLLM (higher throughput, needs GPU)
from vllm import LLM
llm = LLM(model="./model/", tensor_parallel_size=1)
```

**For 70B+ models:**
```python
# vLLM with tensor parallelism
from vllm import LLM
llm = LLM(
    model="./model/",
    tensor_parallel_size=4,  # 4x A100
    gpu_memory_utilization=0.9,
    max_model_len=8192
)
```

### 5.3 API Layer
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.3

@app.post("/generate")
async def generate(query: Query):
    output = llm.generate(
        query.prompt,
        max_tokens=query.max_tokens,
        temperature=query.temperature
    )
    return {"output": output}

@app.post("/batch")
async def batch_generate(queries: list[Query]):
    return [generate(q) for q in queries]
```

---

## Phase 6: Monitoring & Iteration

### 6.1 Production Monitoring
- Request latency
- Token usage
- Error rates
- Output quality sampling
- Drift detection

### 6.2 Retraining Triggers
- Performance drops below threshold
- New data available (>1K new examples)
- Quarterly refresh cycle
- Client feedback

### 6.3 Continuous Improvement
```
Monthly: Quality review → Flag issues
Quarterly: Retrain with accumulated data
On-demand: Hotfix for specific failures
```

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
| **Starter** | 1-5K examples | 3B-7B | 2-3 weeks | $15K-25K |
| **Professional** | 5-20K examples | 8B-14B | 3-5 weeks | $25K-40K |
| **Enterprise** | 20K+ examples | 30B-70B | 6-10 weeks | $40K-75K+ |
| **Annual Retainer** | Ongoing | Any | Continuous | $3K-10K/mo |

Add-ons:
- Custom training data generation: $2K-5K
- On-premise deployment: $5K-15K
- Priority support (4hr SLA): +$1K/mo
- Additional fine-tuning rounds: $5K-15K each
