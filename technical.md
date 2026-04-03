# Namakan Technical Guide

**Fine-Tuning Pipeline: n8n → Colab → QLoRA → Qwen2.5-8B**

---

## Overview

This document covers the technical implementation of Namakan's fine-tuning pipeline:

1. **n8n** — Data extraction, cleaning, and orchestration
2. **Google Colab** — Model training environment
3. **HuggingFace PEFT** — QLoRA fine-tuning technique
4. **Qwen2.5-8B** — Base model

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  n8n (heater.local:5678)                                  │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │Salesforce│  │PostgreSQL│  │Google   │  │Clean PII│      │
│  │         │  │         │  │Drive    │  │         │      │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘      │
│       └────────────┴────────────┴────┬───────┘            │
│                                      │                     │
│                              ┌───────▼───────┐             │
│                              │ Format to Q&A │             │
│                              └───────┬───────┘             │
│                                      │                     │
│                              ┌───────▼───────┐             │
│                              │ Upload to     │             │
│                              │ Google Drive  │             │
│                              └───────┬───────┘             │
│                                      │                     │
│                              ┌───────▼───────┐             │
│                              │ Trigger Colab │             │
│                              │ Webhook       │             │
│                              └───────────────┘             │
└─────────────────────────────────────────────────────────────┘
                                     │
                                     │ webhook
                                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Google Colab                                              │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Download    │  │ QLoRA       │  │ Upload      │        │
│  │ training    │→ │ Fine-tune   │→ │ model to    │        │
│  │ data        │  │ (PEFT)      │  │ Drive       │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  Model: Qwen2.5-8B-Instruct                                │
│  Technique: QLoRA (r=16, alpha=32)                          │
│  Training time: ~45 minutes                                 │
└─────────────────────────────────────────────────────────────┘
                                     │
                                     │ notification
                                     ▼
┌─────────────────────────────────────────────────────────────┐
│  n8n (continued)                                           │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │ Download    │→ │ Notify      │                          │
│  │ model       │  │ (Telegram)  │                          │
│  └─────────────┘  └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 1: n8n Data Pipeline

### Setup

**n8n URL:** http://heater.local:5678

**Required credentials:**
- Salesforce API
- PostgreSQL
- Google Drive OAuth2
- Telegram Bot

### Manual Trigger Node

```javascript
// Start workflow manually or via schedule
// Output: {} (empty, just triggers)
```

### Salesforce Node

```javascript
{
  "operation": "search",
  "objectType": "Case",
  "filterConditions": {
    "conditions": [
      {
        "field": "Status",
        "operator": "equals",
        "value": "Closed"
      },
      {
        "field": "CreatedDate",
        "operator": "greaterThan",
        "value": "2024-01-01"
      }
    ]
  },
  "returnAll": true,
  "outputFields": [
    "Id",
    "Subject",
    "Description",
    "Status",
    "Category",
    "Resolution",
    "EscalationLevel",
    "CreatedDate"
  ]
}
```

### PostgreSQL Node

```javascript
{
  "operation": "executeQuery",
  "query": `
    SELECT 
      order_id,
      customer_tier,
      product_line,
      defect_type,
      root_cause,
      resolution_code,
      created_at
    FROM quality_records
    WHERE created_at > '2024-01-01'
    LIMIT 5000
  `
}
```

### Google Drive Node (Read Files)

```javascript
{
  "operation": "list",
  "folder": "YOUR_FOLDER_ID",
  "options": {
    "fileTypes": ["document"],
    "recursive": true
  }
}
```

### PII Cleaning Node (Code)

```javascript
// Clean PII from text fields
const records = $input.all();

// PII patterns to remove
const piiPatterns = [
  // Names (First Last format)
  {
    pattern: /\b[A-Z][a-z]+ [A-Z][a-z]+\b/g,
    replacement: '[REDACTED]'
  },
  // Email addresses
  {
    pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
    replacement: '[REDACTED]'
  },
  // Phone numbers (various formats)
  {
    pattern: /\b(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/g,
    replacement: '[REDACTED]'
  },
  // SSN
  {
    pattern: /\b\d{3}-\d{2}-\d{4}\b/g,
    replacement: '[REDACTED]'
  },
  // Street addresses
  {
    pattern: /\b\d{1,5}\s+[\w\s]+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln|Way|Court|Ct|Circle|Cir)\b/gi,
    replacement: '[REDACTED]'
  },
  // Order numbers (pattern varies by system)
  {
    pattern: /\b(ORD-|ORDER-)?\d{4,6}\b/g,
    replacement: '[ORDER_ID]'
  },
  // Credit card numbers
  {
    pattern: /\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b/g,
    replacement: '[REDACTED]'
  }
];

function cleanRecord(record) {
  const cleaned = { ...record.json };
  
  // Clean all string fields
  for (const key of Object.keys(cleaned)) {
    if (typeof cleaned[key] === 'string') {
      let value = cleaned[key];
      piiPatterns.forEach(({ pattern, replacement }) => {
        value = value.replace(pattern, replacement);
      });
      cleaned[key] = value;
    }
  }
  
  return { json: cleaned };
}

return records.map(cleanRecord);
```

### Q&A Formatting Node (Code)

```javascript
// Convert cleaned records to training format
const records = $input.all();

function createTrainingPair(record) {
  const r = record.json;
  
  // Extract key information
  const subject = r.Subject || r.subject || '';
  const description = r.Description || r.description || '';
  const category = r.Category || r.category || r.product_line || '';
  const resolution = r.Resolution || r.resolution || r.root_cause || '';
  const escalation = r.EscalationLevel || r.escalation_level || 'L1';
  const customerTier = r.customer_tier || r.CustomerType || 'Standard';
  
  // Build instruction
  const instruction = description 
    ? `A customer reports: ${description.substring(0, 200)}`
    : `Handle: ${subject}`;
  
  // Build response based on category and escalation
  let response = '';
  
  if (category.toLowerCase().includes('quality') || category.toLowerCase().includes('warranty')) {
    response = `Category: Quality - Warranty Claim
Escalation Level: ${escalation}
Customer Tier: ${customerTier}
Response Protocol:
1. Verify purchase date and warranty status
2. Check lot trace for manufacturing date
3. If under warranty: Issue return auth, arrange replacement
4. Document in system: lot_number, warranty_status, resolution
5. If out of warranty: Quote repair/replacement options`;
  } else if (category.toLowerCase().includes('billing') || category.toLowerCase().includes('invoice')) {
    response = `Category: Billing Inquiry
Escalation Level: ${escalation}
Customer Tier: ${customerTier}
Response Protocol:
1. Review account and invoice in question
2. Verify charges against contract terms
3. If error found: Issue credit or adjustment
4. If correct: Explain charges clearly
5. Document in CRM`;
  } else {
    response = `Category: ${category}
Escalation Level: ${escalation}
Customer Tier: ${customerTier}
Response Protocol:
1. Acknowledge customer concern
2. Review relevant records
3. Provide resolution or escalation path
4. Document in system`;
  }
  
  // Add resolution context if available
  if (resolution) {
    response += `\n\nKnown Resolution: ${resolution}`;
  }
  
  return {
    instruction,
    input: '',
    output: response
  };
}

const trainingData = records.map(createTrainingPair);
return trainingData.map(d => ({ json: d }));
```

### CSV Conversion

```javascript
// Node: Convert to CSV
{
  "mode": "jsonToCsv",
  "options": {
    "properties": {
      "headerRow": true,
      "quoteAll": false
    }
  }
}
```

### Google Drive Upload

```javascript
{
  "operation": "upload",
  "fileName": "={{ $now.format('YYYY-MM-DD') }}/training-data.csv",
  "folderId": "YOUR_NAMAKAN_FOLDER_ID",
  "options": {
    "mimeType": "text/csv"
  }
}
```

### Colab Webhook Trigger

```javascript
{
  "url": "https://colab.research.google.com/github/YOUR_REPO/train.ipynb",
  "method": "POST",
  "bodyParameters": {
    "parameters": {
      "data_file_id": "={{ $json.id }}",
      "base_model": "qwen2.5-8b-instruct",
      "output_name": "={{ $vars.clientSlug }}-v1",
      "lora_rank": 16,
      "lora_alpha": 32,
      "epochs": 3
    }
  }
}
```

---

## Part 2: Google Colab Training

### Colab Notebook

```python
# Namakan Fine-Tuning Pipeline
# =============================
# Base Model: Qwen2.5-8B-Instruct
# Technique: QLoRA via HuggingFace PEFT
# Runtime: High-RAM GPU (T4 or A100)

# Install dependencies
!pip install -q transformers accelerate peft bitsandbytes \
  sqlalchemy pandas huggingface_hub

# Imports
import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
import pandas as pd
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Configuration
CONFIG = {
    "base_model": "Qwen/Qwen2.5-8B-Instruct",
    "data_file": None,  # Set by webhook
    "output_name": "namakan-model",
    "lora_rank": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "batch_size": 4,
    "epochs": 3,
    "learning_rate": 2e-4,
    "warmup_steps": 100,
    "max_seq_length": 2048,
}

# Download training data from Drive
def load_training_data(file_id):
    """Load CSV from Google Drive"""
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    from io import BytesIO
    
    # For simplicity, we'll use pandas to read directly
    # In production, use googleapiclient
    pass

# Load base model with QLoRA config
def load_model():
    """Load Qwen2.5-8B with 4-bit quantization"""
    
    # Compute dtype based on GPU
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        CONFIG["base_model"],
        trust_remote_code=True,
        padding_side="right"
    )
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with bitsandbytes 4-bit quantization
    model = AutoModelForCausalLM.from_pretrained(
        CONFIG["base_model"],
        device_map="auto",
        torch_dtype=dtype,
        load_in_4bit=True,
        bnb_4bit_compute_dtype=dtype,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        trust_remote_code=True,
    )
    
    # Prepare for k-bit training
    model = prepare_model_for_kbit_training(model)
    
    # Configure LoRA
    lora_config = LoraConfig(
        r=CONFIG["lora_rank"],
        lora_alpha=CONFIG["lora_alpha"],
        lora_dropout=CONFIG["lora_dropout"],
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ]
    )
    
    # Apply LoRA
    model = get_peft_model(model, lora_config)
    
    # Print trainable params
    model.print_trainable_parameters()
    
    return model, tokenizer

# Load and format training data
def prepare_dataset(tokenizer, file_path):
    """Load CSV and format for training"""
    
    # Read CSV
    df = pd.read_csv(file_path)
    
    # Format as instruction-following
    def format_example(row):
        instruction = row['instruction']
        input_text = row.get('input', '')
        output = row['output']
        
        # Qwen chat template format
        text = f"<|im_start|>user\n{instruction}<|im_end|>\n"
        text += f"<|im_start|>assistant\n{output}<|im_end|>"
        
        return text
    
    texts = df.apply(format_example, axis=1).tolist()
    
    # Tokenize
    def tokenize(examples):
        result = tokenizer(
            examples,
            truncation=True,
            max_length=CONFIG["max_seq_length"],
            padding="max_length"
        )
        result["labels"] = result["input_ids"].copy()
        return result
    
    # Create dataset
    dataset = Dataset.from_dict({"text": texts})
    dataset = dataset.map(
        lambda x: tokenizer(x["text"]),
        batched=True,
        remove_columns=dataset.column_names
    )
    
    return dataset

# Training function
def train_model(model, tokenizer, dataset):
    """Fine-tune with QLoRA"""
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # Causal LM, not masked
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=f"/content/drive/MyDrive/{CONFIG['output_name']}",
        num_train_epochs=CONFIG["epochs"],
        per_device_train_batch_size=CONFIG["batch_size"],
        gradient_accumulation_steps=4,
        learning_rate=CONFIG["learning_rate"],
        warmup_steps=CONFIG["warmup_steps"],
        logging_steps=10,
        save_steps=500,
        fp16=torch.cuda.is_available(),
        report_to="none",
        optim="paged_adamw_8bit",
        max_grad_norm=0.3,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Save
    print("Saving model...")
    trainer.save_model()
    
    return model

# Merge and export
def export_model(model, tokenizer, output_name):
    """Merge LoRA weights and save as GGUF"""
    
    # Save merged model
    merged_model = model.merge_and_unload()
    merged_model.save_pretrained(
        f"/content/drive/MyDrive/{output_name}_full"
    )
    tokenizer.save_pretrained(
        f"/content/drive/MyDrive/{output_name}_full"
    )
    
    # Note: GGUF export requires llama.cpp
    # In Colab: !git clone https://github.com/ggerganov/llama.cpp
    # Then convert using: python llama.cpp/convert.py
    
    print(f"Model saved to /content/drive/MyDrive/{output_name}_full")

# Main execution
if __name__ == "__main__":
    # Load data
    print(f"Loading training data...")
    
    # Load model
    print(f"Loading {CONFIG['base_model']}...")
    model, tokenizer = load_model()
    
    # Prepare dataset
    print("Preparing dataset...")
    dataset = prepare_dataset(tokenizer, CONFIG["data_file"])
    print(f"Training on {len(dataset)} examples")
    
    # Train
    model = train_model(model, tokenizer, dataset)
    
    # Export
    export_model(model, tokenizer, CONFIG["output_name"])
    
    # Notify via webhook
    import requests
    webhook_url = "YOUR_N8N_WEBHOOK_URL"
    requests.post(webhook_url, json={
        "status": "complete",
        "model": CONFIG["output_name"],
        "file": f"/content/drive/MyDrive/{CONFIG['output_name']}_full"
    })
    
    print("Done!")
```

### Running the Notebook

**Manual:**
1. Open notebook in Colab
2. Upload CSV or link to Google Drive file
3. Set `CONFIG["data_file"]` to file path
4. Set `CONFIG["output_name"]` to client name
5. Runtime → Run all

**Automated (via webhook):**
1. n8n triggers notebook execution
2. Notebook reads data from Google Drive
3. Training runs (~45 min on T4, ~20 min on A100)
4. Model saved to Drive
5. Webhook notifies n8n

---

## Part 3: HuggingFace PEFT + QLoRA

### What is QLoRA?

**QLoRA = Quantized Low-Rank Adaptation**

Combines two techniques:
1. **Quantization** — Reduce model precision (4-bit instead of 16-bit)
2. **LoRA** — Fine-tune only small adapter weights, not full model

### Why QLoRA?

| Approach | GPU Memory | Trainable Params | Speed |
|----------|-----------|------------------|-------|
| Full Fine-tune (16-bit) | ~48GB | 8B | Slow |
| LoRA (16-bit) | ~24GB | 8B | Medium |
| **QLoRA (4-bit)** | **~12GB** | **8B** | **Fast** |

**Qwen2.5-8B with QLoRA fits on:**
- Google Colab T4 (15GB) ✅
- Consumer GPU (RTX 3080+) ✅
- MacBook M1/M2 (with limitations) ✅

### LoRA Configuration

```python
LoraConfig(
    r=16,                    # Rank (higher = more capacity, more params)
    lora_alpha=32,           # Scaling factor (typically 2x rank)
    lora_dropout=0.05,      # Regularization
    bias="none",            # Don't train biases
    task_type="CAUSAL_LM",  # For text generation
    
    # Which layers to adapt
    target_modules=[
        "q_proj",   # Query projection
        "k_proj",   # Key projection
        "v_proj",   # Value projection
        "o_proj",   # Output projection
        "gate_proj", # FFN gate
        "up_proj",   # FFN up
        "down_proj", # FFN down
    ]
)
```

### PEFT Key Functions

```python
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 1. Prepare model for k-bit training
model = prepare_model_for_kbit_training(model)

# 2. Create LoRA config
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]
)

# 3. Apply LoRA to model
model = get_peft_model(model, lora_config)

# 4. Now only LoRA params are trainable
# Original model stays frozen in 4-bit

# 5. After training, merge weights
merged_model = model.merge_and_unload()
```

### Training Process

```
┌─────────────────────────────────────────────────────────────┐
│  Frozen 4-bit Base Model (Qwen2.5-8B)                       │
│                                                             │
│  Input → [Frozen] → [Frozen] → [Frozen] → Output           │
│              ↓              ↓              ↓                │
│           q_proj          k_proj          v_proj           │
│              ↓              ↓              ↓                │
│           LoRA-A         LoRA-A          LoRA-A            │
│              ↑              ↑              ↑                │
│           (trainable)    (trainable)    (trainable)         │
└─────────────────────────────────────────────────────────────┘

Only LoRA weights update during training.
Base model stays frozen.
```

### BitsAndBytes 4-bit Config

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,              # Enable 4-bit loading
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,  # Double quantization
    bnb_4bit_quant_type="nf4",       # Normal Float 4
)
```

### Hyperparameters

| Param | Value | Notes |
|-------|-------|-------|
| r (rank) | 16 | Good balance for 8B model |
| alpha | 32 | 2x rank typical |
| dropout | 0.05 | Light regularization |
| batch_size | 4 | Adjust for GPU memory |
| learning_rate | 2e-4 | Standard for LoRA |
| epochs | 3 | Usually enough for fine-tune |
| warmup_steps | 100 | Gradual learning rate ramp |
| max_seq_length | 2048 | Qwen context window |
| gradient_accumulation | 4 | Effective batch = 16 |

### Memory Calculation

```
Base model (8B params, 4-bit):  ~4GB
Optimizer states (AdamW 8-bit): ~1.5GB
Activations:                    ~6GB
Gradients (trainable only):     ~0.5GB
─────────────────────────────────────
Total:                          ~12GB

Fits on: T4 (15GB), RTX 3080 (10GB)
```

---

## Part 4: Model Deployment

### Option A: Ollama (Local)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Create Modelfile
echo '
FROM ./acme-support-v1.gguf
PARAMETER temperature 0.7
PARAMETER top_p 0.9
TEMPLATE """
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""
SYSTEM "You are an AI support agent for Acme Corp..."
' > Modelfile

# Create model
ollama create acme-support-v1 -f Modelfile

# Run
ollama run acme-support-v1
```

### Option B: FastAPI Server

```python
# inference_server.py
from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = FastAPI()

# Load model at startup
tokenizer = AutoTokenizer.from_pretrained("./acme-support-v1")
model = AutoModelForCausalLM.from_pretrained(
    "./acme-support-v1",
    torch_dtype=torch.float16,
    device_map="auto"
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.7
)

class Query(BaseModel):
    text: str
    max_tokens: int = 512

@app.post("/generate")
async def generate(query: Query):
    result = pipe(query.text, max_new_tokens=query.max_tokens)
    return {"result": result[0]["generated_text"]}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Option C: API as a Service

```python
# Namakan API endpoint structure
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Per-client model routing
MODEL_REGISTRY = {
    "acme": "./models/acme-support-v1",
    "client-b": "./models/client-b-v1",
}

@app.post("/generate/{client_id}")
async def generate(client_id: str, request: GenerateRequest):
    if client_id not in MODEL_REGISTRY:
        raise HTTPException(404, "Client not found")
    
    # Load client's model
    model = load_model(MODEL_REGISTRY[client_id])
    
    # Generate
    result = model.generate(request.text)
    
    return {
        "client": client_id,
        "result": result,
        "usage": calculate_tokens(result)
    }
```

---

## Part 5: Complete n8n Workflow JSON

```json
{
  "name": "Namakan Fine-Tuning Pipeline",
  "nodes": [
    {
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 300]
    },
    {
      "name": "Salesforce",
      "type": "n8n-nodes-base.salesforce",
      "position": [500, 200],
      "parameters": {
        "operation": "search",
        "objectType": "Case",
        "filterConditions": {
          "conditions": [
            { "field": "Status", "operator": "equals", "value": "Closed" }
          ]
        }
      }
    },
    {
      "name": "PostgreSQL",
      "type": "n8n-nodes-base.postgres",
      "position": [500, 400],
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT * FROM quality_records WHERE created_at > '2024-01-01'"
      }
    },
    {
      "name": "Clean PII",
      "type": "n8n-nodes-base.code",
      "position": [750, 300],
      "parameters": {
        "jsCode": "..." // See Part 1 above
      }
    },
    {
      "name": "Format Q&A",
      "type": "n8n-nodes-base.code",
      "position": [1000, 300],
      "parameters": {
        "jsCode": "..." // See Part 1 above
      }
    },
    {
      "name": "Upload to Drive",
      "type": "n8n-nodes-base.googleDrive",
      "position": [1250, 300],
      "parameters": {
        "operation": "upload",
        "fileName": "training-data.csv",
        "folderId": "NAMAKAN_FOLDER_ID"
      }
    },
    {
      "name": "Trigger Colab",
      "type": "n8n-nodes-base.httpRequest",
      "position": [1500, 300],
      "parameters": {
        "url": "https://colab.research.google.com/github/...",
        "method": "POST",
        "bodyParameters": {
          "data_file_id": "={{ $json.id }}",
          "output_name": "={{ $vars.clientSlug }}-v1"
        }
      }
    },
    {
      "name": "Wait",
      "type": "n8n-nodes-base.wait",
      "position": [1750, 300],
      "parameters": {
        "amount": 45,
        "unit": "minutes"
      }
    },
    {
      "name": "Notify Success",
      "type": "n8n-nodes-base.telegram",
      "position": [2000, 200],
      "parameters": {
        "chatId": "7982591864",
        "text": "✅ Training complete!"
      }
    },
    {
      "name": "Notify Failure",
      "type": "n8n-nodes-base.telegram",
      "position": [2000, 400],
      "parameters": {
        "chatId": "7982591864",
        "text": "❌ Training failed"
      }
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [[{ "node": "Salesforce" }]]
    }
  }
}
```

---

## Troubleshooting

### Out of Memory in Colab

```python
# Reduce batch size
batch_size = 2  # instead of 4

# Or reduce sequence length
max_seq_length = 1024  # instead of 2048

# Or use gradient checkpointing
model.gradient_checkpointing_enable()
```

### Model Not Saving

```python
# Save with safe_serialization
model.save_pretrained("./output", safe_serialization=True)

# Or merge first
model = model.merge_and_unload()
model.save_pretrained("./output")
```

### Poor Output Quality

- Increase training data (500+ examples minimum)
- Increase LoRA rank (32 instead of 16)
- Increase epochs (5 instead of 3)
- Check data quality (garbage in = garbage out)

### Slow Inference

- Use quantization (GGUF with Q4_K_M)
- Use Flash Attention 2
- Batch requests if possible

---

## Quick Reference

| Item | Value |
|------|-------|
| Base Model | Qwen2.5-8B-Instruct |
| Technique | QLoRA |
| LoRA Rank | 16 |
| LoRA Alpha | 32 |
| Quantization | 4-bit NF4 |
| GPU Memory | ~12GB |
| Training Time | ~45 min |
| Training Data | 500-5000 examples |
| Context Length | 2048 tokens |
| Format | Instruction-following |

---

## Resources

- [PEFT GitHub](https://github.com/huggingface/peft)
- [BitsAndBytes](https://github.com/TimDettmers/bitsandbytes)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [Qwen2.5](https://huggingface.co/Qwen/Qwen2.5-8B-Instruct)
- [n8n Documentation](https://docs.n8n.io/)
