# Colab Fine-Tuning Guide

**Per-Client Isolated Training for Qwen2.5-8B**

---

## Overview

Each client gets a dedicated Colab instance for training. This ensures:
- **Data isolation** — No mixing between clients
- **No data retention** — Runtime deleted after training
- **Clean slate** — Fresh environment per job

---

## Notebook Setup

### 1. Upload to Google Drive

Upload `colab-notebook.ipynb` to your Namakan training folder:

```
/Namakan/
├── training/
│   ├── colab-notebook.ipynb
│   └── client-folders/
│       ├── acme_corp/
│       ├── client_b/
│       └── client_c/
└── models/
```

### 2. Share with Service Account

Share the training folder with: `namakan-colab@PROJECT.iam.gserviceaccount.com`

Grant: **Editor** access

### 3. Per-Client Configuration

Before running, update these variables:

```python
CLIENT_NAME = "acme_corp"           # Client identifier
CLIENT_SLUG = "acme"                # URL-safe name
TRAINING_DATA_FILE_ID = "1XKmj..."  # CSV file ID in Drive
MODEL_OUTPUT_FOLDER_ID = "1Ykml..."  # Output folder ID
WEBHOOK_URL = "https://..."         # n8n callback URL
```

---

## Training Flow

```
1. Download CSV from Drive
2. PII validation check
3. Load Qwen2.5-8B with QLoRA (4-bit)
4. Fine-tune for 3 epochs
5. Merge LoRA weights
6. Upload model to Drive
7. Send webhook notification
```

---

## Security Features

### Per-Client Isolation

Each training job:
1. Creates new notebook copy
2. Sets client-specific variables
3. Uses client's Drive folder
4. Runtime deleted after completion

### PII Validation

Final check before training:
- Detects remaining names, emails, phones
- Flags any [REDACTED] bypass attempts
- Training won't proceed if PII detected

### No Data Retention

After training:
- Colab runtime deleted
- Local files wiped
- Only model weights in Drive

---

## Configuration Options

### Model Size

```python
BASE_MODEL = "Qwen/Qwen2.5-8B-Instruct"  # 8B model
# Or for faster/smaller:
BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"  # 3B model
```

### LoRA Settings

```python
LORA_RANK = 16           # Higher = more capacity
LORA_ALPHA = 32          # 2x rank typical
LORA_DROPOUT = 0.05      # Light regularization
```

### Training Settings

```python
EPOCHS = 3               # Usually enough
BATCH_SIZE = 4           # Reduce if OOM
LEARNING_RATE = 2e-4      # Standard for LoRA
MAX_SEQ_LENGTH = 2048    # Qwen context window
```

---

## GPU Requirements

| Model | GPU | Memory | Time |
|-------|-----|--------|------|
| Qwen2.5-3B | T4 | 8GB | 20-30 min |
| Qwen2.5-8B | T4 | 16GB | 45-60 min |
| Qwen2.5-8B | A10G | 24GB | 25-35 min |

---

## Troubleshooting

### Out of Memory (OOM)

```python
# Reduce batch size
BATCH_SIZE = 2  # or 1

# Or reduce sequence length
MAX_SEQ_LENGTH = 1024
```

### Slow Training

Normal on T4 GPU. Expected times:
- 3B model: ~20 minutes
- 8B model: ~45 minutes

### Webhook Fails

Check:
1. n8n instance is running
2. Webhook URL is accessible
3. Firewall allows outbound

Manual check:
```bash
curl -X POST https://your-webhook.com/callback \
  -H "Content-Type: application/json" \
  -d '{"status": "test"}'
```

---

## Cost

| Resource | Cost |
|----------|------|
| Colab (free) | $0 |
| Colab Pro | $10/mo |
| Colab Pro+ | $50/mo |

For production: Colab Pro is sufficient.

---

## Files

- `colab-notebook.ipynb` — The training notebook (upload this to Drive)

---

## Next Steps

1. Upload notebook to Drive
2. Share with service account
3. Test with sample data
4. Configure per-client variables
5. Run training
6. Model auto-uploads to Drive
