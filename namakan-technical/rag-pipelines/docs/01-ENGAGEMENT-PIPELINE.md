# RAG Pipelines — Engagement Pipeline

*Namakan AI Engineering — Service Offering #2*

---

## The Offering

We build retrieval-augmented generation pipelines that search a client's entire knowledge base before answering. Contracts, CRM, emails, databases, manuals — all indexed and accessible in seconds, with answers always citing the source.

---

## Engagement Pipeline

```
Discovery → Data Inventory → Architecture → Build → Testing → Deploy → Monitor
```

---

### Phase 1: Discovery

**Discovery Call (60 min)**
- What knowledge does the team need to answer but can't find quickly?
- What documents are referenced most often in support tickets?
- Where do people go to find information today? (shared drive, Confluence, Notion)
- What happens when they can't find it? (escalations, delays, errors)
- Who are the subject matter experts whose knowledge should be captured?

**Knowledge Audit Framework**
```
RETRIEVAL GAPS:
- Top 10 questions that take >10 minutes to answer
- Documents people ask for most often
- Knowledge that exists only in people's heads

SYSTEM INVENTORY:
- Where does knowledge live? (SharePoint, Google Drive, Confluence, databases)
- What's searchable today? What's dark/unstructured?
- What authentication/permission systems exist?

QUALITY REQUIREMENTS:
- How critical is accuracy? (low stakes vs. compliance-critical)
- Must answers cite sources? (always required for Namakan)
- Real-time data needed or daily sync acceptable?
```

**Discovery Output**
- Knowledge inventory with gap analysis
- Top 3 retrieval use cases ranked by impact
- Architecture recommendation
- Ballpark: $5K–$15K build + $500–$2K/mo hosting

---

### Phase 2: Data Inventory

**Document Processing:**
```
TYPES WE HANDLE:
- PDFs (scanned + text), DOCX, TXT, Markdown
- Structured: CSV, XLSX, JSON
- Database exports (Postgres, MySQL dumps)
- CRM exports (Salesforce, HubSpot)
- Email archives (PST, mbox)

PROCESSING STEPS:
1. Extract text (pdfplumber, python-docx, BeautifulSoup)
2. Chunk by semantic boundaries (not fixed token count)
3. Embed with nomic-ai/nomic-embed-text-v1.5
4. Store in ChromaDB with metadata (source, date, tags)

STORAGE ARCHITECTURE:
- ChromaDB (client-hosted, no data leaves)
- Or: FAISS for local-only, Chroma for cloud
- Metadata: source file, page number, section, date
```

**Output:** Data Inventory Report → confirms what will be indexed and how

---

### Phase 3: Architecture Design

**RAG Architecture:**
```
┌─────────────────────────────────────────────────────┐
│                    QUERY INPUT                       │
└─────────────────────┬───────────────────────────────┘
                      ↓
         ┌────────────────────────┐
         │   Query Embedding      │
         │   (nomic-embed-text)    │
         └────────────┬───────────┘
                      ↓
         ┌────────────────────────┐
         │   Vector Similarity    │  ← ChromaDB / FAISS
         │   Top-K retrieval      │
         └────────────┬───────────┘
                      ↓
         ┌────────────────────────┐
         │   Context Assembly     │  ← Inject retrieved chunks
         │   + Source Citation    │     into prompt
         └────────────┬───────────┘
                      ↓
         ┌────────────────────────┐
         │   LLM Response         │
         │   (cite sources)       │
         └────────────────────────┘
```

**Key Design Decisions:**
- Chunk size: 512–1024 tokens with 50-token overlap
- Retrieval top-K: 5–10 chunks depending on document length
- Reranking: optional, adds latency but improves accuracy
- Hybrid search: keyword + vector for best of both

---

### Phase 4: Build

See [../workflows/ingestion_pipeline.py](../workflows/ingestion_pipeline.py) and [../workflows/retrieval_pipeline.py](../workflows/retrieval_pipeline.py)

**Build Components:**
1. **Ingestion pipeline** — document processing, chunking, embedding, storage
2. **Retrieval pipeline** — query embedding, similarity search, context assembly
3. **Query API** — FastAPI endpoint returning answer + citations
4. **Admin interface** — add/remove documents, view index stats

---

### Phase 5: Testing

**Testing Protocol:**
- Retrieve on known queries → verify correct sources cited
- Edge case: queries outside the indexed corpus → should say "I don't know" not hallucinate
- Load test: concurrent queries with latency <2s
- Citation accuracy: verify every claim has a backing source

**Output:** Test Report with pass/fail on accuracy, latency, coverage

---

### Phase 6: Deployment

**Deployment Options:**
- **Client infra:** ChromaDB on their server, no data leaves
- **Namakan cloud:** Managed ChromaDB, client retains ownership
- **Hybrid:** Sensitive docs on-prem, general knowledge cloud

**Integrations:**
- Slack app (chat with the knowledge base)
- CRM plugin (surfaced in ticket context)
- API for custom integrations

---

### Phase 7: Monitoring

**Post-deployment checks:**
- Query volume and latency (P50, P95, P99)
- "I don't know" rate (queries outside corpus)
- Index freshness (when was last document added?)
- Citation accuracy (spot-check responses)

**Maintenance:**
- Weekly: new documents indexed
- Monthly: embedding model updated if needed
- Quarterly: retrieval quality evaluation

---

## Deliverables

1. **Deployed RAG pipeline** (ChromaDB + FastAPI)
2. **Indexed knowledge base** (documents, chunk counts, metadata)
3. **API documentation** (endpoint specs, example queries)
4. **Admin runbook** (how to add documents, monitor health)
5. **3-month support** included

---

## Pricing

| Tier | Data Size | Sources | Build | Monthly |
|------|-----------|---------|-------|---------|
| **Starter** | <10K docs | 1–3 systems | $5K–$8K | $500/mo |
| **Professional** | 10K–50K docs | 3–5 systems | $8K–$12K | $1K–$1.5K/mo |
| **Enterprise** | 50K+ docs | 5+ systems | $12K–$15K | $1.5K–$2K/mo |

**Annual maintenance:** Included for first year, then 20% of build cost/year

---

## Timeline

```
Week 1:    Discovery + Data Inventory
Week 2:    Architecture + Document Processing
Week 3:    RAG Pipeline Build + Embedding
Week 4:    Integration + Testing
Week 5:    Deployment + User Training
Week 6:    Monitoring Setup + Handoff

Total: 5-6 weeks typical
```