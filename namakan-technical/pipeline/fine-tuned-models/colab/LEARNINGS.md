# Colab Fine-Tuning Learnings

## From Project Vermicelli (Qwen2.5-3B LoRA Fine-Tuning)

These are the hard-won lessons from running actual Colab training sessions.

---

## Chart / Callback Fixes (Critical)

The original live chart code **crashed constantly**. The fixes:

### 1. Use `display.clear_output(wait=True)` + `display.display(fig)` NOT `plt.show()`
```python
# WRONG — crashes after first update
plt.show()

# RIGHT — works reliably
display.clear_output(wait=True)
display.display(fig)
```

### 2. Guard EVERY log value against None and NaN
```python
if loss is not None and isinstance(loss, (int, float)) and not np.isnan(float(loss)):
    all_losses.append(float(loss))
```

### 3. Track last_train_loss and last_eval_loss SEPARATELY
Between eval steps, `loss` logs but `eval_loss` doesn't. Use the last known value:
```python
if eval_loss is not None:
    self.last_eval_loss = eval_loss
else:
    eval_loss = self.last_eval_loss  # interpolation
```

### 4. The callback must be defined BEFORE the TrainingArguments
And pass the chart update function as a callable:
```python
class LiveChartCallback(TrainerCallback):
    def __init__(self, update_fn):
        self.update_fn = update_fn
```

---

## Training Args That Work

### The Good:
```python
TrainingArguments(
    optim="paged_adamw_8bit",          # Memory-efficient optimizer
    lr_scheduler_type="cosine",         # Better than linear
    max_grad_norm=0.3,                 # Prevents gradient explosion
    weight_decay=0.1,                   # Regularization
    load_best_model_at_end=True,       # Restore best checkpoint
    metric_for_best_model="eval_loss",
    remove_unused_columns=False,        # CRITICAL — don't remove columns
    fp16=True,                          # Half precision on T4
)
```

### The Bad (avoid):
```python
# WRONG — causes issues
optim="adamw_torch"              # Use paged_adamw_8bit instead
evaluation_strategy="steps"      # Deprecated, use eval_strategy
```

### The Ugly (colab-specific):
- Colab kills idle runtimes after ~90 min — set `max_steps` not just epochs
- T4 GPU = ~16GB VRAM — max ~7B model at 4-bit with batch_size=2, grad_accum=8
- For larger models: use QLoRA (4-bit) or go to Colab Pro for A100

---

## Data Loading

### GitHub Raw URL (what Vermicelli used):
```python
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
api_url = "https://api.github.com/repos/cfollette18/project-vermicelli/contents/dataset/vermicelli_training_500.jsonl"
response = requests.get(api_url, headers=headers)
content = response.json()["content"]
dataset_content = base64.b64decode(content).decode("utf-8")
```

### GCS Signed URL (preferred for clients):
```python
response = requests.get(DATA_URL)  # Signed URL bypasses auth
response.raise_for_status()
lines = response.text.strip().split('\n')
examples = [json.loads(line) for line in lines if line.strip()]
```

### Direct URL:
```python
response = requests.get(DATA_URL)
response.raise_for_status()
```

---

## Per-Step Validation Loss

The original notebook only evaluated at epoch end — too slow to catch issues early. Fixed:
```python
eval_strategy="steps",
eval_steps=50,        # Evaluate every 50 steps
save_steps=50,         # Save checkpoint every 50 steps
```

This means:
- You see val loss every 50 steps (not just at epoch boundaries)
- Best model auto-saved and restored at end
- Can stop early if val loss plateaus or diverges

---

## Chat Template Gotcha

Different models use different chat templates. Always test:
```python
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
inputs = tokenizer(text, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, ...)
```

If `apply_chat_template` fails, fall back to manual formatting:
```python
text = f"System: {system}\\nUser: {instruction}\\nAssistant: {output}"
```

---

## What Actually Matters

| Factor | Impact | Notes |
|--------|--------|-------|
| Data quality | ⭐⭐⭐⭐⭐ | Garbage in, garbage out. More important than model size |
| LoRA R | ⭐⭐⭐ | 8-16 for small data, 32-64 for large |
| Learning rate | ⭐⭐⭐ | 2e-4 for LoRA, 1e-5 for full fine-tune |
| Epochs | ⭐⭐ | Early stopping is your friend. 3 is usually enough |
| Batch size | ⭐ | Larger = more stable, less iterations |
| Model size | ⭐ | Better data > bigger model |

---

## Common Failures

1. **Loss goes NaN** → LR too high. Halve it.
2. **Val loss >> Train loss** → Overfitting. More data or reduce epochs.
3. **Val loss < Train loss** → Weird but okay, means model generalizes well.
4. **Colab runtime disconnect** → Set `max_steps` not just epochs. Save frequently.
5. **Model outputs garbage** → Check chat template format. Instruction/output order wrong.
6. **OOM on T4** → Reduce `BATCH_SIZE` or `MAX_SEQ_LENGTH`. Use 4-bit quantization.

---

## Workflow

```
1. Client sends data via S3 signed URL → GCS bucket
2. Trainer: generate Colab notebook with client params
3. Trainer: upload notebook to Colab, run training
4. Watch live charts — if loss NaN or diverging, stop + adjust LR
5. Save adapter + best checkpoint
6. Download adapter weights
7. Deploy to inference stack
8. Share notebook with client
```
