# RAG Pipelines Pipeline

*Namakan AI Engineering — Service Offering #2*

---

## The Offering

We connect AI to a client's documents, knowledge bases, CRM, and internal systems. The result: AI that doesn't guess — it searches YOUR files, YOUR data, YOUR records, and gives answers grounded in what you actually know.

---

## Engagement Pipeline

```
Discovery → Document Audit → Architecture → Build → Evaluation → Deploy → Handoff
```

---

## Phase 1: Discovery

### Discovery Call (45 min)

### Client-Specific Decisions Locked
- **Vector DB**: ChromaDB (client preference confirmed)
- **Data Ingestion**: Signed URLs via Azure Blob / AWS S3 — clients upload directly to Namakan private cloud bucket. No third-party file-sharing services.
- **Update Frequency**: Client-dependent — determine per engagement (static, weekly, daily, or real-time)

- [ ] What documents/systems does the client have?
- [ ] Who uses this information?
- [ ] What questions do people ask?
- [ ] Current pain points (Google searches internal docs? Lost information?)
- [ ] Estimate volume (pages, documents, data records)
- [ ] Budget qualification

### Discovery Output
- Document inventory (types, volumes, formats)
- User personas and query types
- Scope and timeline
- Ballpark: $5K-15K build + $500-2K/mo

---

## Phase 2: Document Audit

### Document Inventory
```python
DOCUMENT_TYPES = {
    "pdf": ["contracts", "reports", "manuals"],
    "docx": ["policies", "procedures", "templates"],
    "html": ["website", "knowledge base"],
    "database": ["CRM", "ERP", "product catalog"],
    "spreadsheet": ["reports", "inventories", "financials"],
    "email": ["communications", "support tickets"],
    "video": ["training", "meetings", "presentations"],
}

def audit_documents(root_dir):
    manifest = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            ext = file.split('.')[-1].lower()
            path = os.path.join(root, file)
            manifest.append({
                "file": file,
                "path": path,
                "type": DOCUMENT_TYPES.get(ext, "other"),
                "size": os.path.getsize(path),
                "modified": os.path.getmtime(path)
            })
    return pd.DataFrame(manifest)
```

### Content Quality Assessment
- Document completeness
- Accuracy of information
- Duplication rates
- Sensitive content (PII, confidential)
- Update frequency

---

## Phase 3: Architecture Design

### RAG Architecture
```
Documents → Ingestion → Chunking → Embedding → Vector Store → Retrieval → Generation
```

### Vector Store Selection

| Store | Best For | Scale | Cloud |
|-------|---------|-------|-------|
| **Pinecone** | Production RAG | Unlimited | Managed |
| **Qdrant** | Self-hosted | Large | Self or cloud |
| **Weaviate** | Multi-modal | Large | Both |
| **Chroma** | Prototyping | Small-medium | Self-hosted |
| **pgvector** | Existing Postgres | Medium | Self or cloud |

### Chunking Strategy
```python
CHUNK_STRATEGIES = {
    "fixed": {"size": 512, "overlap": 64},           # Simple, fast
    "sentence": {"min_sentences": 3, "max_tokens": 512},  # Preserve meaning
    "paragraph": {"overlap": 1},                    # For documents
    "recursive": {"separators": ["\n\n", "\n", ". ", " "]},  # Hierarchical
    "semantic": {"threshold": 0.7},                 # AI-guided splits
}

def chunk_document(text, strategy="recursive", chunk_size=512, overlap=64):
    if strategy == "fixed":
        return fixed_chunk(text, chunk_size, overlap)
    elif strategy == "recursive":
        return recursive_chunk(text, chunk_size, overlap)
    elif strategy == "semantic":
        return semantic_chunk(text, threshold=0.7)
```

### Embedding Model Selection
```python
EMBEDDING_MODELS = {
    "openai": {
        "text-embedding-3-small": {"dims": 1536, "cost": "low"},
        "text-embedding-3-large": {"dims": 3072, "cost": "medium"},
    },
    "open-source": {
        "nomic-embed-text-v1.5": {"dims": 768, "cost": "free"},
        "mxbai-embed-large": {"dims": 1024, "cost": "free"},
        "bge-m3": {"dims": 1024, "cost": "free"},
    },
    "specialized": {
        "symanto/snmn-xlm-roberta-base": {"dims": 768},  # Multilingual
        "nbai/nbai-base-32": {"dims": 1024},              # Scientific
    },
}
```

### Hybrid Search Design
```python
HYBRID_SEARCH = """
-- Combine dense embeddings with sparse BM25
SELECT 
    content,
    0.7 * cosine_similarity(embed(query), embedding) +
    0.3 * bm25_score(query, content) as combined_score
FROM documents
ORDER BY combined_score DESC
LIMIT 10
"""
```

---

## Phase 4: Build

### 4.1 Document Ingestion
```python
INGESTION_PIPELINE = """
PDF → Text Extraction → Cleaning → Chunking → 
Embedding → Deduplication → Vector Store
"""

def ingest_documents(source_dir, vector_store):
    documents = []
    
    for filepath in find_documents(source_dir):
        # Extract text
        if filepath.endswith('.pdf'):
            text = extract_pdf(filepath)
        elif filepath.endswith('.docx'):
            text = extract_docx(filepath)
        elif filepath.endswith('.txt'):
            text = extract_txt(filepath)
        
        # Clean
        text = clean_text(text)
        
        # Chunk
        chunks = chunk_document(text)
        
        # Embed and store
        for chunk in chunks:
            embedding = embed_model.encode(chunk)
            vector_store.add(chunk, embedding)
    
    return len(documents)
```

### 4.2 Connector Libraries
```python
CONNECTORS = {
    "google_drive": "google-api-python-client",
    "sharepoint": "office365-rest-python-client",
    "s3": "boto3",
    "salesforce": "simple-salesforce",
    "notion": "notion-client",
    "confluence": "atlassian-python-api",
    "slack": "slack-sdk",
    "database": "sqlalchemy + psycopg2",
}
```

### 4.3 Retrieval Optimization
```python
# Query expansion for better retrieval
def expand_query(query):
    """Add synonyms and related terms."""
    expanded = query
    synonyms = get_synonyms(query)
    expanded += " " + " ".join(synonyms[:5])
    return expanded

# Re-ranking for relevance
def rerank_results(query, results, top_k=5):
    """Re-rank retrieved results using cross-encoder."""
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    pairs = [(query, doc) for doc in results]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
```

---

## Phase 5: Evaluation

### RAG Evaluation Framework
```python
RAG_EVALUATION = """
Metrics:
- Precision@K: Are the retrieved docs relevant?
- Context Precision: Is the retrieved context high quality?
- Faithfulness: Does answer match retrieved context?
- Answer Relevance: Does answer address the question?
- Hallucination Rate: Is the answer grounded?
"""

def evaluate_rag_system(rag_system, eval_questions):
    results = []
    for question in eval_questions:
        answer, contexts, metrics = rag_system.answer(question)
        results.append({
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "precision": metrics["context_precision"],
            "faithfulness": metrics["faithfulness"],
            "relevance": metrics["answer_relevance"],
        })
    return aggregate_metrics(results)
```

### Test Question Set
```python
EVAL_QUESTIONS = [
    # Factual queries
    "What is the warranty period for X?",
    "How do I return a product?",
    "What are the payment terms?",
    # Analytical queries
    "Compare our top 3 products by margin.",
    "What trends do you see in Q3 data?",
    # Complex queries
    "Given our policy on X, how should we handle Y?",
    "What's the risk of Z based on our documents?",
]
```

---

## Phase 6: Deployment

### Deployment Architecture
```
Client Systems → API Gateway → RAG Service → Vector Store
                              ↓
                       Generation LLM
                              ↓
                       Response API
```

### Production Stack
```yaml
# docker-compose.yml
services:
  rag-api:
    image: namakan/rag-api:latest
    ports: ["8000:8000"]
    environment:
      - VECTOR_STORE_HOST=pinecone
      - LLM_PROVIDER=openai
      - EMBEDDING_MODEL=nomic-embed-text-v1.5

  vector-store:
    image: qdrant/qdrant
    ports: ["6333:6333"]
    volumes:
      - ./qdrant_storage:/qdrant/storage
```

### API Endpoint
```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/query")
async def query(question: str, top_k: int = 5):
    # Retrieve
    contexts = vector_store.search(question, top_k=top_k)
    
    # Generate
    response = llm.generate(
        prompt=f"Context: {contexts}\n\nQuestion: {question}"
    )
    
    return {
        "answer": response,
        "sources": [c.metadata for c in contexts],
        "confidence": compute_confidence(contexts)
    }
```

---

## Phase 7: Monitoring

### Production Monitoring
```python
MONITORING = {
    "latency_p95": "< 2 seconds",
    "retrieval_recall": "> 0.8",
    "faithfulness_score": "> 0.9",
    "daily_queries": "track per user",
    "stale_content_alerts": "flag outdated sources",
}
```

### Content Freshness
```python
def check_content_freshness():
    """Alert when indexed content is older than threshold."""
    for doc in vector_store.get_all_documents():
        age = datetime.now() - doc.last_updated
        if age > timedelta(days=90):
            alert(f"Document {doc.id} is {age.days} days old")
```

---

## Deliverables

1. **Deployed RAG API** (client infrastructure or ours)
2. **Document ingestion pipeline** (automated updates)
3. **Evaluation report** with benchmark questions
4. **API documentation** for integration
5. **Admin dashboard** for content management
6. **3-month support** included

---

## Pricing

| Tier | Document Volume | Complexity | Price |
|------|----------------|-------------|-------|
| **Starter** | < 10K docs | Single source | $5K-8K |
| **Professional** | 10K-100K docs | 2-3 sources | $8K-15K |
| **Enterprise** | 100K+ docs | Multiple + real-time | $15K-25K |
| **Monthly Maintenance** | Ongoing | Updates, monitoring | $500-2K/mo |

---

## Timeline

```
Week 1:    Discovery + Document Audit
Week 2:    Architecture + Initial Build
Week 3-4:  Document Ingestion + Evaluation
Week 4-5:  Integration + Testing
Week 5-6:  Deployment + User Training
```

Total: 5-6 weeks typical
