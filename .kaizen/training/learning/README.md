# Training Learning — Namakan Engineering

## Internal Knowledge Base

Compiled lessons from building real client systems.

---

## Fine-Tuning Learnings (from Vermicelli)

### The Live Chart Problem

The original Colab notebook used `plt.show()` in a callback — it crashed after the first update.

**Fix**: Use `display.clear_output(wait=True)` + `display.display(fig)` instead.

```python
# WRONG — crashes
plt.show()

# RIGHT — works reliably
display.clear_output(wait=True)
display.display(fig)
```

### None/NaN Guard

Trainer logs `loss` but NOT `eval_loss` between evaluation steps. Without guards, you get NaN propagation.

```python
if loss is not None and not np.isnan(float(loss)):
    all_losses.append(float(loss))
```

### Interpolation

Between eval steps, use the last known `eval_loss` to interpolate:
```python
if eval_loss is not None:
    self.last_eval_loss = eval_loss
else:
    eval_loss = self.last_eval_loss  # use last known
```

### paged_adamw_8bit > adamw_torch

Memory-efficient optimizer that doesn't balloon VRAM:
```python
optim="paged_adamw_8bit"
```

### Cosine > Linear

Cosine LR scheduler converges better for fine-tuning:
```python
lr_scheduler_type="cosine"
```

### max_grad_norm=0.3

Prevents gradient explosion, especially with LoRA:
```python
max_grad_norm=0.3
```

---

## RAG Learnings

### Chunk Overlap Matters

50-token overlap prevents context from being split mid-sentence:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)
```

### Metadata is Everything

Always store source document, page number, and chunk index as metadata:
```python
vector_store.add(texts, metadatas=[{"source": doc.name, "page": p}])
```

### Hybrid Search > Vector Only

Combine dense (semantic) + sparse (BM25) retrieval:
```python
# Dense: vector similarity
# Sparse: keyword matching
# Combined: rerank with cross-encoder
```

---

## Agent Workflow Learnings

### ReAct Loop Must Have Exit Condition

Always cap max iterations to prevent infinite loops:
```python
max_iterations = 10
if iteration >= max_iterations:
    return {"error": "Max iterations reached, escalating"}
```

### Confidence Scores are Hard

LLMs are bad at calibrating their own confidence. Use task completion rate instead:
```python
# Instead of: if confidence > 0.8
# Use: if tool_results match expected patterns
```

### Human Escalation is a Feature

Always provide a clean escalation path:
```python
if not confident:
    yield {"type": "human_escalation", "question": specific_question}
    # Wait for human input before continuing
```

---

## Database Learnings

### pgvector vs ChromaDB

| Use Case | Choice |
|----------|--------|
| Production RAG | ChromaDB (per-client isolation) |
| Internal embeddings | pgvector (single DB) |
| Scale | Pinecone/Qdrant for >1M vectors |

### Connection Pooling

Always use connection pooling for PostgreSQL:
```python
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=10)
```

### Index Everything You Query

```sql
CREATE INDEX idx_agent_role ON agents(role);
CREATE INDEX idx_document_client ON documents(client_id);
```
