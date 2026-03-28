# RAG Pipeline Skill

**Purpose**: Build retrieval-augmented generation systems for client knowledge bases

## Architecture

```
Client Documents → Ingestion Pipeline → ChromaDB → Retrieval → Generation (LLM)
```

## Stack

- **Vector DB**: ChromaDB (client preference confirmed)
- **Embeddings**: `nomic-ai/nomic-embed-text-v1.5` (or OpenAI `text-embedding-3-small`)
- **Chunking**: Recursive character splitting, 512 tokens, 50-token overlap
- **Retrieval**: Hybrid search (dense + sparse), re-ranking with cross-encoder
- **Generation**: Client's LLM (OpenAI API or local)

## Data Ingestion

Client uploads via **signed URLs** (S3 or Azure Blob) — NO third-party services:
1. Client uploads documents to their private S3 bucket
2. Generate signed upload URL → client PUTs file
3. Download from signed URL → process → delete from Colab/server
4. Index into ChromaDB

**Supported formats**: PDF, DOCX, HTML, TXT, Markdown, CSV

## Workflow Scripts

```
namakan-technical/pipeline/rag-pipelines/workflows/
├── ingestion_pipeline.py    # Extract → chunk → embed → index
└── retrieval_pipeline.py    # Query → retrieve → re-rank → generate
```

## Key Decisions (Per Engagement)

Ask the client:
- [ ] Document types? (PDF, DOCX, spreadsheets, databases?)
- [ ] Volume? (<1K / 1K-10K / 10K+ docs)
- [ ] Update frequency? (static / weekly / daily / real-time)
- [ ] Source systems? (shared drive / CRM / Google Drive / SharePoint)
- [ ] Access control? (employees only / customers / public)
- [ ] Compliance? (HIPAA / GDPR / SOC 2)

## Retrieval Pattern

```python
# 1. Parse query
query_embedding = embed_model.encode(question)

# 2. Vector search (ChromaDB)
results = vector_store.query(query_embedding, n_results=10)

# 3. Re-rank with cross-encoder
reranked = cross_encoder.predict([(question, doc) for doc in results])

# 4. Build context
context = "\n\n".join(top_docs[:5])

# 5. Generate
response = llm.generate(f"Context: {context}\n\nQuestion: {question}")
```

## ChromaDB Per-Client

Each client gets their **own ChromaDB instance** (separate collection or DB):
```python
client = chromadb.Client(ChromaSettings)
collection = client.get_or_create_collection(f"client_{client_id}_documents")
```

## Monitoring

- Query latency p50/p95/p99
- Retrieval precision sampling (did retrieved docs actually answer the question?)
- ChromaDB collection size
- Update frequency compliance
