# Namakan Reusable Fine-Tuning Notebook

## Overview

A fully parameterized, reusable Colab notebook for LoRA/QLoRA fine-tuning of any base model on any dataset. Designed for client engagements — plug in the parameters, run, done.

## Quick Start

1. Open `namakan-reusable-finetune.ipynb` in Google Colab
2. Fill in **Section 0 — Client Parameters** (all you need)
3. Run all cells top to bottom
4. Download your trained adapter from `/content/adapters/`

## Parameters (Section 0)

| Parameter | Description | Example |
|-----------|-------------|---------|
| `CLIENT_NAME` | Client identifier | `"Mayo Clinic"` |
| `BASE_MODEL` | HuggingFace model ID | `"Qwen/Qwen2.5-7B-Instruct"` |
| `HF_TOKEN` | HF token for gated models | Get from huggingface.co |
| `DATA_URL` | URL to JSONL training data (GCS signed URL, GitHub raw, or direct URL) | `"https://storage.googleapis.com/..."` |
| `DATA_FORMAT` | `"chat"` or `"plain"` | `"chat"` |
| `SYSTEM_PROMPT` | System persona for the model | `"You are a helpful medical records assistant..."` |
| `MAX_SEQ_LENGTH` | Max token length | `512` |
| `LORA_R` | LoRA rank | `16` |
| `LORA_ALPHA` | LoRA alpha | `32` |
| `LORA_DROPOUT` | Dropout | `0.05` |
| `EPOCHS` | Training epochs | `3` |
| `LR` | Learning rate | `2e-4` |
| `BATCH_SIZE` | Per-device batch size | `2` |
| `GRAD_ACCUM` | Gradient accumulation steps | `8` |
| `VAL_SPLIT` | Fraction of data for validation | `0.1` |
| `OUTPUT_DIR` | Where to save adapter | `"/content/adapters"` |
| `EARLY_STOPPING_PATIENCE` | epochs without improvement before stopping | `2` |

## Data Format

Training data must be JSONL with one JSON object per line:

**Chat format** (preferred):
```jsonl
{"instruction": "What is the warranty policy?", "output": "The warranty covers 12 months..."}
{"instruction": "How do I file a claim?", "output": "To file a claim, visit..."}
```

The notebook wraps each in a chat template:
```
System: {SYSTEM_PROMPT}
User: Task: {instruction}
Assistant: {output}
```

**Plain format**:
```jsonl
{"text": "This is a training example..."}
```

## Output

After training:
1. **Adapter weights** → `/content/adapters/{CLIENT_NAME}/final/`
2. **Training charts** → displayed inline
3. **Evaluation metrics** → displayed inline
4. **Test outputs** → sample generations printed

## Download Adapter

```python
from google.colab import drive
drive.mount('/content/drive')
import shutil
shutil.copytree("/content/adapters", "/content/drive/MyDrive/namakan/adapters/{CLIENT_NAME}/")
```

## Dependencies

Installed automatically:
```
transformers accelerate bitsandbytes peft trl
huggingface_hub datasets scipy torch
torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
