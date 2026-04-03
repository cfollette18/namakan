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
- Ballpark: $5K-15K build + $500/mo

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
Documents → Ingestion → Chunking → Embedding → Vector Store
                                                  ↓
    ┌─────────────────────────────────────────────┐
    │              AGENTIC RAG CONTROLLER          │
    │  ┌─────────┐  ┌──────────┐  ┌────────────┐  │
    │  │Gap 1:   │  │Gap 2:    │  │Gap 3:      │  │
    │  │Verify & │→ │Citation &│→ │Recursive   │  │
    │  │N-ACK    │  │Provenance│  │Multi-Step  │  │
    │  └─────────┘  └──────────┘  └────────────┘  │
    │       ↓            ↓             ↓            │
    │  ┌─────────────────────────────────────────┐ │
    │  │Gap 4: Metadata Security Filter          │ │
    │  │visibility_level ≤ user_clearance         │ │
    │  └─────────────────────────────────────────┘ │
    │                    ↓                         │
    │              Generation LLM                 │
    └─────────────────────────────────────────────┘
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

### 4.4 Agentic RAG — 4 Gap Closers

The RAG pipeline is upgraded from "retrieve and prompt" to **Agentic RAG** — a controller that evaluates data before speaking. Every retrieved answer passes through 4 enforcement gates.

#### Gap 1: Verify & N-ACK (Negative Acknowledgment)
**Problem:** AI hallucinates when documents are silent on a topic.
**Solution:** Before answering, verify that retrieved context actually contains the answer. If query terms don't appear in any chunk → return exact phrase: *"I cannot find a definitive answer in the provided records."* Never fill gaps with training data.

```python
VERIFICATION_SYSTEM_PROMPT = """\
You are a strict factual assistant. Your job is to answer ONLY from the provided documents.

CRITICAL RULES:
1. VERIFY BEFORE SPEAKING: If the retrieved context does not contain a specific
   answer to the user's query, or if the information is ambiguous, you MUST state
   exactly: 'I cannot find a definitive answer in the provided records.'
2. NEVER GUESS: Do NOT use your internal training data to fill in gaps regarding
   company-specific facts (dates, prices, policies, names, numbers).
3. CITATION REQUIRED: Every factual claim must be followed by a square-bracketed
   citation referencing the source file and page number: [source_file.pdf, p.42]
4. MULTI-SOURCE SYNTHESIS: If using multiple documents, list ALL sources under
   a 'Verified Sources' heading at the bottom.
5. PERMISSION FILTER: If any context was withheld due to access restrictions,
   you must note: 'Some records could not be retrieved due to your access level.'
"""

def _check_answerability(query, chunks):
    """
    Verify chunks actually contain the answer to the query.
    Returns (answerable: bool, reason: str).
    """
    if not chunks:
        return False, "No documents retrieved."
    query_keywords = set(re.findall(r'\b\w{3,}\b', query.lower()))
    query_keywords -= {'what', 'when', 'where', 'which', 'who', 'how',
                       'does', 'is', 'the', 'and', 'for', 'from', 'with',
                       'this', 'that', 'are', 'was', 'have', 'has', 'been'}
    coverage = max(
        sum(1 for kw in query_keywords if kw in c.text.lower())
        for c in chunks
    )
    if coverage < 1:
        return False, "Query terms not found in retrieved context."
    return True, "Context contains relevant information."
```

#### Gap 2: Citation & Source Provenance
**Problem:** User can't verify or audit where an answer came from.
**Solution:** Every factual claim is tagged `[source_file, p.N]`. Multi-source answers list all sources under a `**Verified Sources**` footer.

```python
@dataclass
class RetrievedChunk:
    text: str
    source_file: str
    page_number: Optional[int]   # None if not extractable
    chunk_id: str
    score: float
    visibility_level: int = 0     # 0=public, 1=internal, 2=restricted, 3=confidential

    def citation(self) -> str:
        page = f"p.{self.page_number}" if self.page_number is not None else "p.?"
        return f"[{self.source_file}, {page}]"

def _format_answer_with_citations(answer_text: str, chunks: list[RetrievedChunk]) -> str:
    """Post-process LLM answer to ensure citations are present."""
    source_map = {}
    for chunk in chunks:
        key = chunk.source_file
        if chunk.page_number is not None:
            if key not in source_map:
                source_map[key] = []
            if chunk.page_number not in source_map[key]:
                source_map[key].append(chunk.page_number)

    if source_map:
        footer_lines = ["\n\n---\n**Verified Sources**"]
        for source_file, pages in sorted(source_map.items()):
            page_str = ", ".join(f"p.{p}" for p in sorted(set(pages)))
            footer_lines.append(f"- {source_file} ({page_str})")
        answer_text += "".join(footer_lines)
    return answer_text
```

#### Gap 3: Recursive Multi-Step Reasoning (Chain-of-Search)
**Problem:** Answer is fragmented across multiple files (e.g., "Compare X vs Y").
**Solution:** Detect comparison/multi-entity queries → load Entity A context → load Entity B context → only then answer.

```python
def _detect_multi_entity_query(query: str) -> tuple[bool, list[str]]:
    """Detect comparison queries. Returns (is_multi, list_of_entity_names)."""
    comparison_patterns = [
        r'\bcompare\s+(\w+)\s+vs\.?\s+(\w+)',
        r'\b(\w+)\s+vs\.?\s+(\w+)',
        r'\bdifference\s+between\s+(\w+)\s+and\s+(\w+)',
        r'(\w+)\s+or\s+(\w+)\s+\?',
    ]
    entities = []
    for pattern in comparison_patterns:
        matches = re.findall(pattern, query, re.IGNORECASE)
        for m in matches:
            if isinstance(m, tuple):
                entities.extend([e.strip() for e in m if e.strip()])
    seen, unique = set(), []
    for e in entities:
        if e.lower() not in seen:
            seen.add(e.lower())
            unique.append(e)
    return len(unique) >= 2, unique

def _recursive_search(query, embedder, retrieve_fn, top_k=10):
    """
    Multi-step retrieval for comparison queries.
    Step 1: Load Entity A → Step 2: Load Entity B → then synthesize.
    """
    is_multi, entities = _detect_multi_entity_query(query)
    if not is_multi:
        return retrieve_fn(query, top_k=top_k), [f"Step 1: Retrieved for: {query}"]

    all_chunks, seen_texts, working_log = [], set(), []
    for entity in entities:
        entity_query = f"{entity} {query}"
        results = retrieve_fn(entity_query, top_k=top_k)
        new_results = [r for r in results if r.text not in seen_texts]
        seen_texts.update(r.text for r in new_results)
        all_chunks.extend(new_results)
        working_log.append(f"Step: Loaded {len(new_results)} chunks for entity '{entity}'")
    working_log.append(f"Final: {len(all_chunks)} chunks combined for comparison across {entities}")
    return all_chunks, working_log
```

#### Gap 4: Metadata-Level Security Filter
**Problem:** Agent sees documents the user isn't allowed to access.
**Solution:** Append visibility filter to every vector search. User clearance gates chunk visibility.

```python
@dataclass
class UserSession:
    user_role: str = "employee"       # public, employee, manager, admin
    user_clearance: int = 1           # 0=public, 1=internal, 2=restricted, 3=confidential

    @staticmethod
    def from_role(role: str) -> "UserSession":
        clearance_map = {
            "public": 0, "employee": 1, "manager": 2, "admin": 3, "confidential": 3
        }
        return UserSession(user_role=role,
                           user_clearance=clearance_map.get(role.lower(), 1))

def _apply_visibility_filter(chunks: list[RetrievedChunk],
                               user_clearance: int) -> tuple[list, bool]:
    """
    Remove chunks where visibility_level > user_clearance.
    Returns (filtered_chunks, had_restricted_content).
    """
    filtered, had_restricted = [], False
    for chunk in chunks:
        if chunk.visibility_level > user_clearance:
            had_restricted = True
        else:
            filtered.append(chunk)
    return filtered, had_restricted

# ChromaDB-level filter (applied at query time for efficiency)
# collection.query(query_texts=[query], where={"visibility_level": {"$lte": user_clearance}})

# When all content is filtered:
if not filtered_chunks and had_restricted:
    return AnswerResponse(
        answer="I cannot find a definitive answer in the provided records.\n"
               "Note: Some records could not be retrieved due to your access level.",
        chunks=[],
        nack=True,
        permission_filtered=True,
    )
```

#### Ingestion: Metadata Enrichment (Required for Gaps 2 & 4)

```python
# During chunk creation, inject visibility_level and page_number:
for chunk in doc_chunks:
    chunk["source_file"] = doc["filename"]
    chunk["page_number"] = extract_page_number(filepath, chunk["text"])  # from PDF
    # Visibility by path convention:
    restricted_paths = ["/restricted/", "/confidential/", "/hr/", "/finance/"]
    chunk["visibility_level"] = 2 if any(p in doc["path"] for p in restricted_paths) else 1

    # ChromaDB metadata
    collection.add(
        embeddings=embeddings,
        documents=texts,
        ids=ids,
        metadatas=[{
            "source_file": c["source_file"],
            "page_number": c["page_number"],
            "visibility_level": c["visibility_level"],  # Gap 4 key field
        } for c in batch]
    )
```

### 4.5 Layout-Aware Ingestion
**Problem:** Tables, headers, and multi-column PDFs lose structure when flattened to plain text — causing the LLM to receive incoherent data fragments.
**Solution:** Use layout-aware parsers to detect table structures and preserve them during chunking.

```python
LAYOUT_EXTRACTORS = {
    "azure": {
        "name": "Azure AI Document Intelligence",
        "extract": extract_azure_layout,    # Preserves tables, headers, columns
        "output": "markdown",                # Tables → | col | col | format
    },
    "unstructured": {
        "name": "Unstructured.io",
        "extract": extract_unstructured,      # Multi-modal: PDF, DOCX, HTML
        "output": "markdown",
    },
    "pdfplumber": {
        "name": "pdfplumber (fallback)",
        "extract": extract_pdfplumber_layout, # Page layout + table detection
        "output": "markdown",
    },
}

def extract_azure_layout(filepath: str) -> list[dict]:
    """Extract with Azure Document Intelligence, preserving table structure."""
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    client = DocumentIntelligenceClient(endpoint=ENDPOINT, credential=CRED)
    with open(filepath, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-layout", body=f)
    result = poller.result()

    pages = []
    for page in result.pages:
        tables = []
        for table in result.tables:
            if table.bounding_region.page_number == page.page_number:
                # Convert table to Markdown
                md_table = table_to_markdown(table)
                tables.append({"type": "table", "content": md_table, "bbox": table.bbox})

        text_blocks = [Line for Line in page.lines if Line.role not in ("pageHeader", "pageFooter")]
        pages.append({"tables": tables, "text": text_blocks})
    return pages

def table_to_markdown(table) -> str:
    """Convert Azure table result to Markdown format."""
    rows = []
    for cell in table.cells:
        content = cell.content.replace("\n", " ")
        alignment = ":-" if cell.column_header else "-"  # Header row alignment
        rows.append((cell.row_index, cell.column_index, content, alignment))

    # Build Markdown grid
    max_col = max(r[1] for r in rows) + 1
    grid = [[""] * max_col for _ in range(max(r[0] for r in rows) + 1)]
    for row_idx, col_idx, content, _ in rows:
        grid[row_idx][col_idx] = content

    md_lines = []
    for r_idx, row in enumerate(grid):
        md_lines.append("| " + " | ".join(row) + " |")
        if r_idx == 0:  # Separator after header row
            md_lines.append("|" + "|".join(["---" for _ in row]) + "|")
    return "\n".join(md_lines)

def layout_aware_chunk(doc_pages: list[dict], chunk_size: int = 512) -> list[dict]:
    """
    Chunk with table awareness — tables are kept intact as single chunks
    and tagged has_table: true so the LLM knows context is tabular.
    """
    chunks = []
    for page_num, page in enumerate(doc_pages):
        # Tables as standalone chunks (never split mid-table)
        for table in page.get("tables", []):
            chunk_id = sha256(f"{table['content'][:50]}".encode()).hexdigest()[:16]
            chunks.append({
                "text": table["content"],
                "chunk_id": chunk_id,
                "source": f"page_{page_num}",
                "has_table": True,
                "type": "table",
            })

        # Text chunks — respect paragraph and heading boundaries
        text = extract_text_with_roles(page["text"])
        text_chunks = recursive_chunk(text, chunk_size=chunk_size)
        for chunk_text in text_chunks:
            chunk_id = sha256(chunk_text.encode()).hexdigest()[:16]
            chunks.append({
                "text": chunk_text,
                "chunk_id": chunk_id,
                "source": f"page_{page_num}",
                "has_table": False,
                "type": "text",
            })

    return chunks

# Chunk metadata enriched with layout info
# ChromaDB: collection.add(metadatas=[{"has_table": c["has_table"], "type": c["type"]} for c in chunks])
```

---

### 4.6 Regression & Golden Set Validation
**Problem:** New data ingestions or system changes can silently degrade answer quality — no safety net.
**Solution:** Maintain a "Golden Dataset" of validated Q-C-A triples. Every production deployment or index update triggers an automated benchmark.

```python
import uuid, hashlib

class GoldenSet:
    """
    Immutable dataset of validated Question-Context-Answer triples.
    Stored in PostgreSQL with versioned baselines.
    """
    def __init__(self, db_url: str, name: str, version: str):
        self.db = psycopg2.connect(db_url)
        self.name = name
        self.version = version

    def add_case(self, question: str, context_chunks: list[dict], expected_answer: str, tags: list[str] = []):
        """Add a validated case to the golden set."""
        chunk_uuids = [c["chunk_id"] for c in context_chunks]
        context_hash = hashlib.sha256(str(chunk_uuids).encode()).hexdigest()[:12]

        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO golden_cases (id, name, version, question, context_hash,
                                         expected_answer, chunk_uuids, tags, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """, (str(uuid.uuid4()), self.name, self.version,
                  question, context_hash, expected_answer,
                  chunk_uuids, tags))

    def benchmark(self, agentic_rag, threshold_drop: float = 0.05) -> dict:
        """
        Run full golden set against current system.
        Returns scores and flags if regression detected.
        """
        results = []
        baseline = self._load_baseline()

        for case in self._get_all_cases():
            result = agentic_rag.verify_and_answer(case["question"])
            faithful = self._compute_faithfulness(result.answer, case["expected_answer"])
            relevant = self._compute_relevance(result.answer, case["question"])
            results.append({
                "case_id": case["id"],
                "faithfulness": faithful,
                "relevance": relevant,
                "passed": faithful >= 0.8 and relevant >= 0.8,
            })

        # Aggregate
        current_scores = {
            "faithfulness": sum(r["faithfulness"] for r in results) / len(results),
            "relevance": sum(r["relevance"] for r in results) / len(results),
        }

        regression_detected = False
        for metric in ["faithfulness", "relevance"]:
            delta = current_scores[metric] - baseline.get(metric, 1.0)
            if delta < -threshold_drop:
                regression_detected = True
                self._alert(f"REGRESSION: {metric} dropped {abs(delta):.1%} on {self.name} v{self.version}")

        return {
            "scores": current_scores,
            "passed": sum(1 for r in results if r["passed"]) / len(results),
            "total_cases": len(results),
            "regression_detected": regression_detected,
            "baseline": baseline,
        }

    def _compute_faithfulness(self, answer: str, expected: str) -> float:
        """Keyword overlap / semantic similarity to expected answer."""
        answer_words = set(re.findall(r'\b\w{3,}\b', answer.lower()))
        expected_words = set(re.findall(r'\b\w{3,}\b', expected.lower()))
        overlap = len(answer_words & expected_words) / max(len(expected_words), 1)
        return min(1.0, overlap + 0.1)  # Soft bonus

    def _compute_relevance(self, answer: str, question: str) -> float:
        """Does answer actually address the question?"""
        q_words = set(re.findall(r'\b\w{3,}\b', question.lower())) - STOP_WORDS
        a_words = set(re.findall(r'\b\w{3,}\b', answer.lower()))
        return min(1.0, len(q_words & a_words) / max(len(q_words), 1))
```

---

### 4.7 Cold Storage & Hot Index Strategy
**Problem:** Scaling to millions of documents inflates vector store costs — most historical data is rarely queried but still needs to be accessible.
**Solution:** Tiered storage with Hot (sub-second) and Cold (archival) tiers.

```python
TIER_CONFIG = {
    "hot": {
        "age_days": 180,          # Recent documents
        "vector_store": "chroma",  # Full embeddings, sub-second retrieval
        "index_type": "hnsw",      # ANN index for speed
        "cost_per_doc": 0.001,     # $/doc/month estimate
    },
    "cold": {
        "age_days": None,         # Everything older than hot threshold
        "vector_store": "postgres", # pgvector with metadata-only or compressed vectors
        "index_type": "ivfflat",    # Lower memory, slightly slower but cheaper
        "cost_per_doc": 0.00005,
    },
}

class TieredVectorStore:
    """
    Hot/Cold tiered vector store.
    Hot: full ANN index for recent docs (< 180 days)
    Cold: metadata-only index for archived docs, falls back to BM25 + full retrieval
    """

    def __init__(self, hot_dir: str, cold_db_url: str, hot_threshold_days: int = 180):
        self.hot = load_chroma(hot_dir)          # Sub-second retrieval
        self.cold = PostgresVectorStore(cold_db_url)  # Metadata + BM25
        self.hot_threshold_days = hot_threshold_days
        self._build_cold_metadata_index()

    def query(self, query_text: str, top_k: int = 10, user_session: UserSession = None):
        """
        Query hot first, then cold if hot results insufficient.
        Always apply visibility filter (Gap 4) across both tiers.
        """
        # Hot tier
        hot_results = self._query_hot_tier(query_text, top_k * 2, user_session)

        if len(hot_results) < top_k:
            # Fetch from cold tier — user notified of longer latency
            cold_results = self._query_cold_tier(query_text, top_k, user_session)
            all_results = hot_results + cold_results
        else:
            all_results = hot_results[:top_k]

        # Deduplicate by chunk_id
        seen, deduped = set(), []
        for r in all_results:
            if r.chunk_id not in seen:
                seen.add(r.chunk_id)
                deduped.append(r)

        return deduped[:top_k]

    def _query_cold_tier(self, query_text: str, top_k: int, user_session):
        """
        Cold query — notify user of archive fetch.
        Uses BM25 + metadata filter for relevance.
        """
        cold_results = self.cold.search(
            query=query_text,
            n_results=top_k,
            where={"last_modified": {"$lt": days_ago(self.hot_threshold_days)}}
        )
        # Return with flag that these came from cold storage
        for r in cold_results:
            r.from_cold = True
            r.cold_notice = "Historical record retrieved from archive."
        return cold_results

    def _build_cold_metadata_index(self):
        """Build a metadata-only index of cold documents for fast filtering."""
        # Postgres table: chunk_id, source_file, page_number, last_modified, visibility_level
        # Enables pre-filtering without loading full embeddings
        pass
```

---

### 4.8 Immutable Trace & Audit Logging
**Problem:** When hallucinations or errors occur, there's no way to reconstruct exactly what the system did — no audit trail.
**Solution:** Every production query logs a complete, immutable trace object.

```python
import uuid, hashlib, json
from datetime import datetime, timezone

class ImmutableAuditLogger:
    """
    Append-only audit log for every RAG query.
    Stores in PostgreSQL with Row-Level Security (RLS) —
    no UPDATE or DELETE permissions even for admins.
    """

    def __init__(self, db_url: str):
        self.db = psycopg2.connect(db_url)
        # Enforce immutability — no UPDATE/DELETE role
        with self.db.cursor() as cur:
            cur.execute("SET LOCAL app.current_role = 'audit_writer'")

    def log_query(self, trace: "TraceObject"):
        """Append an immutable trace record."""
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO rag_traces (
                    id, query_timestamp, user_id, user_role,
                    original_prompt, system_prompt_version,
                    retrieved_chunk_uuids, retrieved_sources,
                    llm_raw_output, final_answer,
                    latency_ms, nack, permission_filtered,
                    trace_hash
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                trace.id, trace.query_timestamp, trace.user_id, trace.user_role,
                trace.original_prompt, trace.system_prompt_version,
                trace.chunk_uuids, trace.retrieved_sources,
                trace.llm_raw_output, trace.final_answer,
                trace.latency_ms, trace.nack, trace.permission_filtered,
                trace.compute_hash(),
            ))
        self.db.commit()

@dataclass
class TraceObject:
    """
    Immutable trace record for every production query.
    Designed for post-mortem analysis and legal compliance.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    user_id: str = ""
    user_role: str = "employee"
    original_prompt: str = ""
    system_prompt_version: str = ""         # Maps to specific prompt version
    retrieved_chunk_uuids: list[str] = []    # Exact chunk IDs retrieved
    retrieved_sources: list[tuple[str, int]] = []  # [(file, page)]
    llm_raw_output: str = ""                 # Unmodified LLM output before formatting
    final_answer: str = ""
    latency_ms: float = 0
    nack: bool = False
    permission_filtered: bool = False
    working_memory_log: list[str] = []       # Gap 3 multi-step steps

    def compute_hash(self) -> str:
        """Content-addressable hash for integrity verification."""
        return hashlib.sha256(
            f"{self.id}{self.query_timestamp}{self.original_prompt}".encode()
        ).hexdigest()[:24)

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)

# PostgreSQL schema with Row-Level Security
TRACE_SCHEMA = """
CREATE TABLE rag_traces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id TEXT,
    user_role TEXT,
    original_prompt TEXT NOT NULL,
    system_prompt_version TEXT NOT NULL,
    retrieved_chunk_uuids UUID[],
    retrieved_sources TEXT[],         -- [(file, page)] as JSON
    llm_raw_output TEXT NOT NULL,
    final_answer TEXT NOT NULL,
    latency_ms FLOAT,
    nack BOOLEAN DEFAULT FALSE,
    permission_filtered BOOLEAN DEFAULT FALSE,
    working_memory_log TEXT[],
    trace_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row-Level Security: append-only, no deletes
ALTER TABLE rag_traces ENABLE ROW LEVEL SECURITY;

CREATE POLICY "audit_append_only" ON rag_traces
    FOR INSERT WITH CHECK (current_setting('app.current_role') = 'audit_writer');

CREATE POLICY "audit_no_delete" ON rag_traces
    FOR DELETE USING (FALSE);  -- No deletes ever

CREATE POLICY "audit_no_update" ON rag_traces
    FOR UPDATE USING (FALSE);  -- No updates ever
"""

# Usage in AgenticRAG.verify_and_answer():
#   trace = TraceObject(
#       original_prompt=query,
#       system_prompt_version="v2.0-agentic-2026-04",
#       retrieved_chunk_uuids=[c.chunk_id for c in result.chunks],
#       ...
#   )
#   audit_logger.log_query(trace)
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
- N-ACK Rate: Does system correctly decline when context is silent?
- Citation Coverage: Are all factual claims tagged with [source, p.N]?
- Multi-Step Detection: Are comparison queries handled in multiple steps?
- Permission Filtering: Are restricted chunks hidden from unauthorized users?
"""

# Gap-Closer Test Suite (run with --gaps flag)
GAP_TESTS = {
    "g1-silent":   ("N-ACK on silent query", "cannot find"),
    "g1-noisy":    ("N-ACK on ambiguous query", "cannot find"),
    "g2-citation": ("Citation [file, p.N] present", "["),
    "g2-multi":    ("Verified Sources footer", "Verified Sources"),
    "g3-compare":  ("Multi-entity query detected", ""),  # detection test
    "g4-filter":   ("Chunks within clearance", ""),  # metadata test
    "g4-denied":   ("Permission denial notice", "access level"),
}

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
            "nack": metrics.get("nack", False),
            "citations": metrics.get("citations", []),
            "permission_filtered": metrics.get("permission_filtered", False),
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
from fastapi import FastAPI, Header, HTTPException
from typing import Optional

app = FastAPI()

@app.post("/query")
async def query(
    question: str,
    top_k: int = 5,
    x_user_role: str = Header(default="employee"),  # From session token
):
    # User session from auth header → clearance level (Gap 4)
    session = UserSession.from_role(x_user_role)

    # Agentic RAG pipeline (all 4 gaps enforced)
    result = agentic_rag.verify_and_answer(
        query=question,
        user_session=session,
        top_k=top_k,
    )

    # Gap 1: N-ACK response
    if result.nack:
        return {
            "answer": result.answer,
            "status": "nack",
            "permission_filtered": result.permission_filtered,
            "sources": [],
        }

    # Gap 2: Verified sources attached
    return {
        "answer": result.answer,
        "status": "ok",
        "sources": [
            {"file": src, "page": pg}
            for src, pg in result.verified_sources
        ],
        "working_memory": result.working_memory,  # Gap 3 audit trail
        "permission_filtered": result.permission_filtered,
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
    "nack_rate": "< 15%",          # Gap 1: How often system correctly declines
    "citation_coverage": "> 95%",   # Gap 2: % of claims with [file, p.N]
    "multi_step_rate": "> 5%",     # Gap 3: % of queries requiring multi-step
    "permission_denials": "track",  # Gap 4: Who tried to access restricted docs
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
| **Monthly Maintenance** | Ongoing | Updates, monitoring | $500/mo |

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
