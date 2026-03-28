# Training Fixes — Common Problems and Solutions

## Fine-Tuning Fixes

### Fix: Loss Goes NaN

**Symptom**: Training loss becomes `nan` within first few steps.

**Cause**: Learning rate too high for the model/data combination.

**Fix**: Halve the learning rate:
```python
LEARNING_RATE = 1e-4  # was 2e-4
```

Also check:
- Data has no encoding issues (run `tokenizer.decode(tokenizer.encode(sample)) == sample`)
- No very long sequences slipping through truncation

---

### Fix: Out of Memory on T4

**Symptom**: `CUDA out of memory` when loading model or during training.

**Fix** — reduce batch size first:
```python
BATCH_SIZE = 1  # was 2
GRAD_ACCUM = 16  # compensate with more accumulation steps
```

If that doesn't work, reduce sequence length:
```python
MAX_SEQ_LENGTH = 256  # was 512
```

Still OOM? Use more aggressive quantization:
```python
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16,
)
```

---

### Fix: Val Loss >> Train Loss (Severe Overfitting)

**Cause**: Too few training examples, too many epochs.

**Fix**:
1. Add more training data
2. Reduce epochs (try 1 instead of 3)
3. Increase dropout: `LORA_DROPOUT = 0.1`
4. Reduce LoRA rank: `LORA_R = 8`

---

### Fix: Colab Runtime Disconnects Mid-Training

**Cause**: Idle timeout (~90 min).

**Fix**:
1. Set `max_steps` not just `epochs`:
```python
max_steps = 500  # instead of epochs=3
```
2. Save checkpoints every 50 steps:
```python
save_steps = 50
```
3. Use `paged_adamw_8bit` optimizer to reduce memory churn

---

### Fix: Model Outputs Garbage / Wrong Format

**Symptom**: Trained model produces gibberish or ignores instruction format.

**Cause**: Chat template mismatch between training and inference.

**Fix**:
```python
# Make sure tokenizer settings match during training AND inference
tokenizer.pad_token = tokenizer.eos_token
tokenizer.chat_template = ...  # set explicitly
```

Also verify instruction format in training data matches the format used at inference time.

---

## RAG Fixes

### Fix: Retrieval Returns Irrelevant Docs

**Cause**: Embedding model doesn't match domain.

**Fix**: Try a domain-specific embedding:
```python
# Medical: "pritish/MedEmbed-small-v0.1"
# Code: "nomic-ai/nomic-embed-text-v1.5"
# General: "text-embedding-3-small"
```

Also try hybrid search instead of pure vector similarity.

---

### Fix: ChromaDB Query Times Out

**Cause**: Collection too large, no index.

**Fix**:
```python
# Enable hnsw index on the collection
collection.modify(
    metadata={"hnsw:space": "cosine"}
)
```

Or paginate large result sets.

---

## Backend Fixes

### Fix: SQLAlchemy Session Detached

**Symptom**: `DetachedInstanceError: Instance <X> is not bound to a session`

**Cause**: Returning ORM object after session closes.

**Fix**: Always use `session.expunge_all()` or convert to dict before returning:
```python
result = db.query(Agent).all()
return [dict(r) for r in result]  # convert before closing session
```

---

### Fix: Redis Connection Refused

**Symptom**: `redis.exceptions.ConnectionError: Error 111 connecting to redis:6379.`

**Cause**: Redis not running or wrong host.

**Fix**:
```bash
docker-compose up -d redis
```

Or check `REDIS_URL` env var matches docker network.

---

### Fix: Pydantic Validation Error on Nested Objects

**Symptom**: `ValidationError: 1 validation error for X`

**Cause**: Nested model not imported correctly.

**Fix**:
```python
from ..models.pydantic import ParentModel, ChildModel  # import both

class ParentModel(BaseModel):
    child: ChildModel  # reference nested model
```

---

## Frontend Fixes

### Fix: Next.js "Cannot find module"

**Cause**: Wrong path alias or missing extension.

**Fix**: Always use `.js`, `.ts`, or `.tsx` extensions in imports on Next.js:
```typescript
// WRONG
import { Button } from './Button'

// RIGHT
import { Button } from './Button.tsx'
```

---

### Fix: Hydration Mismatch

**Symptom**: React hydration error — server HTML doesn't match client.

**Cause**: Using `Date.now()` or `Math.random()` in render.

**Fix**: Move dynamic values to `useEffect`:
```typescript
'use client'
const [time, setTime] = useState(null)
useEffect(() => { setTime(Date.now()) }, [])
```
