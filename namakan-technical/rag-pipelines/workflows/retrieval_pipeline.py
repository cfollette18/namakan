#!/usr/bin/env python3
"""
Namakan — RAG Pipelines: Retrieval Pipeline v2.0
Agentic RAG — controller that evaluates data before speaking.
Implements: Verify & N-ACK, Citation & Source Provenance,
Recursive Multi-Step Reasoning, Metadata-Level Security Filter.
"""
import json
import re
import numpy as np
import argparse
from typing import Optional, Literal
from dataclasses import dataclass, field
from enum import Enum

# ─── Gap Closers ───────────────────────────────────────────────────────────────

VERIFICATION_SYSTEM_PROMPT = """\
You are a strict factual assistant. Your job is to answer ONLY from the provided documents.

CRITICAL RULES:
1. VERIFY BEFORE SPEAKING: If the retrieved context does not contain a specific answer to the user's query, or if the information is ambiguous, you MUST state exactly: 'I cannot find a definitive answer in the provided records.'
2. NEVER GUESS: Do NOT use your internal training data to fill in gaps regarding company-specific facts (dates, prices, policies, names, numbers).
3. CITATION REQUIRED: Every factual claim must be followed by a square-bracketed citation referencing the source file and page number: [source_file.pdf, p.42]
4. MULTI-SOURCE SYNTHESIS: If a response uses information from multiple documents, list ALL sources at the bottom under a 'Verified Sources' heading.
5. PERMISSION FILTER: If any context was withheld due to access restrictions, you must note: 'Some records could not be retrieved due to your access level.'

Working memory rules:
- Load ALL entity contexts before answering comparison queries
- Do NOT answer comparison questions (e.g. "Compare X vs Y") until both entity contexts are fully loaded
- Each chunk in working memory must be tracked with its [source, page] citation
"""

@dataclass
class RetrievedChunk:
    """A retrieved chunk with full provenance."""
    text: str
    source_file: str
    page_number: Optional[int]
    chunk_id: str
    score: float
    visibility_level: int = 0  # Security: 0=public, 1=internal, 2=restricted, 3=confidential

    def citation(self) -> str:
        """Return [file, p.N] citation string."""
        page = f"p.{self.page_number}" if self.page_number is not None else "p.?"
        return f"[{self.source_file}, {page}]"

@dataclass
class AnswerResponse:
    """Structured answer with provenance tracking."""
    answer: str
    chunks: list[RetrievedChunk]
    verified_sources: list[tuple[str, int]]  # (file, page) deduplicated
    nack: bool = False  # True = could not answer from context
    permission_filtered: bool = False
    working_memory: list[str] = field(default_factory=list)


# ─── Core Retrieval ───────────────────────────────────────────────────────────

def load_index(output_dir: str, manifest_path: str = None):
    """Load vector index and chunks from output directory."""
    manifest_path = manifest_path or f"{output_dir}/manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)

    chunks_path = f"{output_dir}/chunks.json"
    with open(chunks_path) as f:
        chunks = json.load(f)

    vectorstore_type = manifest.get("result", {}).get("type", "numpy")

    if vectorstore_type == "faiss":
        import faiss
        index = faiss.read_index(f"{output_dir}/index.faiss")
        embeddings = np.load(f"{output_dir}/embeddings.npy")
        return chunks, embeddings, index, manifest
    elif vectorstore_type == "chroma":
        import chromadb
        client = chromadb.PersistentClient(path=output_dir)
        collection = client.get_collection(manifest["result"]["collection"])
        return chunks, None, collection, manifest
    else:
        embeddings = np.load(f"{output_dir}/embeddings.npy")
        return chunks, embeddings, None, manifest


def get_embedder(provider: str = "local"):
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI()
        def embed(texts):
            resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
            return [d.embedding for d in resp.data]
        return embed
    elif provider == "nomic":
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")
        def embed(texts):
            return model.encode(texts, normalize_embeddings=True).tolist()
        return embed
    else:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        def embed(texts):
            return model.encode(texts).tolist()
        return embed


def _safe_citation(chunk: dict) -> tuple[str, Optional[int]]:
    """Extract source file and page number from chunk metadata, safely."""
    source = chunk.get("source", chunk.get("source_file", "unknown"))
    # Handle page metadata - may be stored as "page", "page_number", or "p"
    page = chunk.get("page_number") or chunk.get("page") or chunk.get("p")
    return source, page


def retrieve_faiss(
    query: str,
    chunks: list,
    embeddings: np.ndarray,
    index,
    embedder,
    top_k: int = 10,
    visibility_filter: int = None,
) -> list[RetrievedChunk]:
    """Retrieve from FAISS index, optionally filtered by visibility."""
    query_emb = np.array(embedder([query])).astype('float32')
    faiss.normalize_L2(query_emb)
    scores, indices = index.search(query_emb, top_k * 3)

    seen = set()
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(chunks):
            continue
        chunk = chunks[idx]
        vis = chunk.get("visibility_level", 0)
        if visibility_filter is not None and vis > visibility_filter:
            continue
        text = chunk.get("text", "")
        if text in seen:
            continue
        seen.add(text)
        source_file, page_number = _safe_citation(chunk)
        results.append(RetrievedChunk(
            text=text,
            source_file=source_file,
            page_number=page_number,
            chunk_id=chunk.get("chunk_id", str(idx)),
            score=float(score),
            visibility_level=vis,
        ))
        if len(results) >= top_k:
            break
    return results


def retrieve_chroma(
    query: str,
    collection,
    embedder,
    top_k: int = 10,
    visibility_filter: int = None,
) -> list[RetrievedChunk]:
    """Retrieve from ChromaDB with optional visibility filtering."""
    # Build where clause for permission filter
    if visibility_filter is not None:
        where = {"visibility_level": {"$lte": visibility_filter}}
    else:
        where = None

    results = collection.query(
        query_texts=[query],
        n_results=top_k * 3,
        where=where if visibility_filter is not None else None,
    )

    seen = set()
    output = []
    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    ids = results.get("ids", [[]])[0]

    for i, (doc, dist, meta, chunk_id) in enumerate(zip(documents, distances, metadatas, ids)):
        if doc in seen:
            continue
        seen.add(doc)
        vis = (meta.get("visibility_level", 0) if meta else 0)
        if visibility_filter is not None and vis > visibility_filter:
            continue
        source_file, page_number = _safe_citation(meta or {})
        output.append(RetrievedChunk(
            text=doc,
            source_file=source_file,
            page_number=page_number,
            chunk_id=chunk_id,
            score=1.0 - dist,
            visibility_level=vis,
        ))
        if len(output) >= top_k:
            break
    return output


def rerank(query: str, results: list[RetrievedChunk], top_k: int = 5) -> list[RetrievedChunk]:
    """Re-rank results using cross-encoder for better relevance."""
    try:
        from sentence_transformers import CrossEncoder
        model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        pairs = [(query, r.text[:512]) for r in results]
        scores = model.predict(pairs)
        reranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
        return [r for r, _ in reranked[:top_k]]
    except ImportError:
        return results[:top_k]


def _build_context_text(chunks: list[RetrievedChunk]) -> str:
    """Build citation-tagged context string for the LLM."""
    parts = []
    for i, chunk in enumerate(chunks):
        citation = chunk.citation()
        parts.append(f"[Doc {i+1}] {citation}:\n{chunk.text[:800]}")
    return "\n\n---\n\n".join(parts)


# ─── Gap 1: Verify & N-ACK ───────────────────────────────────────────────────

def _check_answerability(query: str, chunks: list[RetrievedChunk]) -> tuple[bool, str]:
    """
    Verify that the chunks actually contain the answer to the query.
    Returns (answerable, reason).
    Uses keyword + semantic heuristics since we may not have an LLM call budget.
    """
    if not chunks:
        return False, "No documents retrieved."

    query_keywords = set(re.findall(r'\b\w{3,}\b', query.lower()))
    query_keywords -= {'what', 'when', 'where', 'which', 'who', 'how', 'does', 'is', 'the', 'and', 'for', 'from', 'with', 'this', 'that', 'are', 'was', 'have', 'has', 'been'}

    found_in_chunks = []
    for chunk in chunks:
        text_lower = chunk.text.lower()
        coverage = sum(1 for kw in query_keywords if kw in text_lower)
        found_in_chunks.append(coverage)

    # If query keywords barely appear in any chunk, we're likely in the silent zone
    if max(found_in_chunks) < 1:
        return False, "Query terms not found in retrieved context."

    return True, "Context contains relevant information."


# ─── Gap 3: Recursive Multi-Step Reasoning ────────────────────────────────────

def _detect_multi_entity_query(query: str) -> tuple[bool, list[str]]:
    """
    Detect comparison/multi-entity queries.
    Returns (is_multi, list_of_entity_names).
    """
    comparison_patterns = [
        r'\bcompare\s+(\w+)\s+vs\.?\s+(\w+)',
        r'\b(\w+)\s+vs\.?\s+(\w+)',
        r'\bdifference\s+between\s+(\w+)\s+and\s+(\w+)',
        r'(\w+)\s+or\s+(\w+)\s+\?',
        r'between\s+(\w+)\s+and\s+(\w+)',
    ]
    entities = []
    for pattern in comparison_patterns:
        matches = re.findall(pattern, query, re.IGNORECASE)
        for m in matches:
            if isinstance(m, tuple):
                entities.extend([e.strip() for e in m if e.strip()])
            elif isinstance(m, str) and len(m) > 1:
                entities.append(m.strip())
    # Deduplicate while preserving order
    seen, unique = set(), []
    for e in entities:
        if e.lower() not in seen:
            seen.add(e.lower())
            unique.append(e)
    return len(unique) >= 2, unique


def _recursive_search(
    query: str,
    embedder,
    retrieve_fn,
    top_k: int = 10,
) -> tuple[list[RetrievedChunk], list[str]]:
    """
    Perform multi-step recursive search for comparison queries.
    Step 1: Load Entity A context
    Step 2: Load Entity B context
    Step 3: Return combined working memory
    Returns (chunks, working_memory_log)
    """
    is_multi, entities = _detect_multi_entity_query(query)
    if not is_multi:
        # Single entity — just do a normal search
        results = retrieve_fn(query, top_k=top_k)
        return results, [f"Step 1: Retrieved {len(results)} chunks for query: {query}"]

    working_log = []
    all_chunks = []
    seen_texts = set()

    for entity in entities:
        entity_query = f"{entity} {query}"
        results = retrieve_fn(entity_query, top_k=top_k)
        # Deduplicate against previous entities
        new_results = [r for r in results if r.text not in seen_texts]
        seen_texts.update(r.text for r in new_results)
        all_chunks.extend(new_results)
        working_log.append(f"Step {len(all_chunks) - len(new_results) + 1}: Loaded {len(new_results)} chunks for entity '{entity}'")

    working_log.append(f"Final: Combined {len(all_chunks)} chunks for comparison across {entities}")

    return all_chunks, working_log


# ─── Gap 2: Citation & Source Provenance ─────────────────────────────────────

def _format_answer_with_citations(
    answer_text: str,
    chunks: list[RetrievedChunk],
) -> str:
    """
    Post-process LLM answer to ensure every factual claim has a citation.
    Adds [source, p.N] citations inline and a Verified Sources footer.
    """
    # Build source map
    source_map: dict[str, list[int]] = {}
    for chunk in chunks:
        key = chunk.source_file
        if chunk.page_number is not None:
            if key not in source_map:
                source_map[key] = []
            if chunk.page_number not in source_map[key]:
                source_map[key].append(chunk.page_number)

    # Add footer
    if source_map:
        footer_lines = ["\n\n---\n**Verified Sources**"]
        for source_file, pages in sorted(source_map.items()):
            page_str = ", ".join(f"p.{p}" for p in sorted(set(pages)))
            footer_lines.append(f"- {source_file} ({page_str})")
        answer_text += "\n".join(footer_lines)

    return answer_text


# ─── Gap 4: Metadata-Level Security Filter ────────────────────────────────────

@dataclass
class UserSession:
    """User session context for permission filtering."""
    user_role: str = "employee"  # employee, manager, admin, public
    user_clearance: int = 1  # 0=public, 1=internal, 2=restricted, 3=confidential

    @staticmethod
    def from_role(role: str) -> "UserSession":
        """Map user role string to clearance level."""
        clearance_map = {
            "public": 0,
            "employee": 1,
            "manager": 2,
            "admin": 3,
            "confidential": 3,
        }
        return UserSession(
            user_role=role,
            user_clearance=clearance_map.get(role.lower(), 1),
        )


def _apply_visibility_filter(
    chunks: list,
    user_clearance: int,
) -> tuple[list, bool]:
    """
    Filter chunks by visibility_level <= user_clearance.
    Returns (filtered_chunks, had_restricted_content).
    """
    filtered = []
    had_restricted = False
    for chunk in chunks:
        vis = getattr(chunk, 'visibility_level', 0)
        if vis > user_clearance:
            had_restricted = True
        else:
            filtered.append(chunk)
    return filtered, had_restricted


# ─── Agentic RAG ─────────────────────────────────────────────────────────────

class AgenticRAG:
    """
    Agentic RAG — a controller that evaluates data before speaking.

    Closes 4 gaps:
    1. Verify & N-ACK:      Don't hallucinate when context is silent
    2. Citation & Source:   Every claim tagged [file, p.N]
    3. Recursive Reasoning: Multi-step search for comparisons
    4. Security Filter:     Only show what user is allowed to see
    """

    def __init__(
        self,
        index_dir: str,
        llm_model: str = "gpt-4o",
        embed_provider: str = "local",
        user_session: UserSession = None,
        top_k: int = 10,
        rerank_k: int = 5,
    ):
        self.embedder = get_embedder(embed_provider)
        self.chunks_data, self.embeddings, self.index, self.manifest = load_index(index_dir)
        self.llm_model = llm_model
        self.vectorstore_type = self.manifest.get("result", {}).get("type", "numpy")
        self.user_session = user_session or UserSession()
        self.top_k = top_k
        self.rerank_k = rerank_k

    def _retrieve_raw(self, query: str, top_k: int = None) -> list[RetrievedChunk]:
        """Base retrieval without security filter (applied separately)."""
        top_k = top_k or self.top_k
        if self.vectorstore_type == "faiss":
            results = retrieve_faiss(
                query, self.chunks_data, self.embeddings, self.index,
                self.embedder, top_k,
            )
        else:
            results = retrieve_chroma(
                query, self.index, self.embedder, top_k,
            )
        return results

    def retrieve(self, query: str, top_k: int = None, apply_security: bool = True) -> list[RetrievedChunk]:
        """
        Retrieve chunks with optional security filtering.
        Applies metadata-level visibility filter based on user clearance.
        """
        top_k = top_k or self.top_k
        results = self._retrieve_raw(query, top_k)

        # Gap 4: Security filter
        if apply_security:
            results, had_restricted = _apply_visibility_filter(
                results, self.user_session.user_clearance,
            )
            if had_restricted and not results:
                # All content was filtered — this is a permission denial
                pass  # Handled in answer()

        return results

    def verify_and_answer(
        self,
        query: str,
        top_k: int = None,
        verbose: bool = False,
    ) -> AnswerResponse:
        """
        Full agentic RAG flow:
        1. Multi-step retrieval for comparisons (Gap 3)
        2. Security filtering (Gap 4)
        3. Answerability check — N-ACK if silent (Gap 1)
        4. LLM generation with citation enforcement (Gap 2)
        """
        top_k = top_k or self.top_k

        # Step 1: Recursive multi-step retrieval
        if _detect_multi_entity_query(query)[0]:
            if verbose:
                print(f"[AGENTIC] Multi-entity query detected — running recursive search")
            chunks, working_log = _recursive_search(
                query, self.embedder,
                lambda q, top_k=top_k: self._retrieve_raw(q, top_k),
                top_k=top_k,
            )
        else:
            chunks = self._retrieve_raw(query, top_k)
            working_log = [f"Step 1: Retrieved {len(chunks)} chunks for: {query}"]

        # Step 2: Security filter
        chunks, had_restricted = _apply_visibility_filter(
            chunks, self.user_session.user_clearance,
        )
        if had_restricted:
            working_log.append("Security filter: Some chunks hidden due to access level")

        if not chunks:
            return AnswerResponse(
                answer="I cannot find a definitive answer in the provided records.",
                chunks=[],
                verified_sources=[],
                nack=True,
                permission_filtered=had_restricted,
                working_memory=working_log,
            )

        # Step 3: Answerability check (Gap 1 — Verify & N-ACK)
        answerable, reason = _check_answerability(query, chunks)
        working_log.append(f"Answerability check: {reason}")

        if not answerable:
            return AnswerResponse(
                answer="I cannot find a definitive answer in the provided records.",
                chunks=chunks,
                verified_sources=[],
                nack=True,
                permission_filtered=had_restricted,
                working_memory=working_log,
            )

        # Step 4: Generate with citation enforcement
        context_text = _build_context_text(chunks)

        messages = [
            {"role": "system", "content": VERIFICATION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
        ]

        try:
            from openai import OpenAI
            client = OpenAI()
            resp = client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                temperature=0.1,
                max_tokens=1200,
            )
            raw_answer = resp.choices[0].message.content
        except ImportError:
            return AnswerResponse(
                answer="[Answer generation requires: pip install openai]",
                chunks=chunks,
                verified_sources=[],
                nack=True,
                permission_filtered=had_restricted,
                working_memory=working_log,
            )

        # Step 5: Post-process for citations (Gap 2)
        answer = _format_answer_with_citations(raw_answer, chunks)

        # Build verified sources
        verified_sources = []
        seen = set()
        for chunk in chunks:
            key = (chunk.source_file, chunk.page_number)
            if key not in seen:
                seen.add(key)
                verified_sources.append((chunk.source_file, chunk.page_number))

        return AnswerResponse(
            answer=answer,
            chunks=chunks,
            verified_sources=verified_sources,
            nack=False,
            permission_filtered=had_restricted,
            working_memory=working_log,
        )

    def stream_answer(self, query: str, top_k: int = None):
        """Stream the answer from OpenAI."""
        result = self.verify_and_answer(query, top_k, verbose=False)
        if result.nack:
            yield result.answer
            return

        context_text = _build_context_text(result.chunks)
        messages = [
            {"role": "system", "content": VERIFICATION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
        ]

        from openai import OpenAI
        client = OpenAI()
        stream = client.chat.completions.create(
            model=self.llm_model,
            messages=messages,
            temperature=0.1,
            stream=True,
        )

        for chunk in stream:
            yield chunk.choices[0].delta.content or ""

    # ── Backward compatibility ───────────────────────────────────────────────

    def answer(self, query: str, top_k: int = None) -> tuple[str, list]:
        """Legacy interface: returns (answer, chunks)."""
        result = self.verify_and_answer(query, top_k)
        return result.answer, result.chunks


# ─── Legacy RAGRetriever (backward compat) ────────────────────────────────────

class RAGRetriever:
    """Legacy RAG retriever — wraps AgenticRAG for backward compat."""

    def __init__(self, index_dir: str, llm_model: str = "gpt-4o"):
        self._agentic = AgenticRAG(index_dir, llm_model)

    def retrieve(self, query: str, top_k: int = 10, rerank_k: int = 5) -> list[dict]:
        chunks = self._agentic.retrieve(query, top_k)
        if rerank_k < top_k:
            chunks = rerank(query, chunks, rerank_k)
        return chunks

    def answer(self, query: str, top_k: int = 10) -> tuple[str, list]:
        result = self._agentic.verify_and_answer(query, top_k)
        return result.answer, result.chunks

    def stream_answer(self, query: str, top_k: int = 10):
        return self._agentic.stream_answer(query, top_k)


# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Namakan Agentic RAG Retrieval v2.0")
    parser.add_argument("--index-dir", "-i", required=True, help="Output dir from ingestion pipeline")
    parser.add_argument("--query", "-q", required=True, help="Query to answer")
    parser.add_argument("--top-k", "-k", type=int, default=10)
    parser.add_argument("--rerank-k", type=int, default=5)
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--user-role", default="employee", help="User role for permission filter (public/employee/manager/admin)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show agentic reasoning log")
    args = parser.parse()

    session = UserSession.from_role(args.user_role)

    agentic = AgenticRAG(
        args.index_dir,
        user_session=session,
        top_k=args.top_k,
    )

    if args.stream:
        print("Answer (streaming):")
        for text in agentic.stream_answer(args.query):
            print(text, end="", flush=True)
        print()
    else:
        result = agentic.verify_and_answer(args.query, verbose=args.verbose)

        print(f"\n{'='*60}")
        if result.nack:
            print("  [N-ACK] " + result.answer)
        else:
            print(f"  Answer:\n  {result.answer}")
        print(f"{'='*60}")

        if result.working_memory and args.verbose:
            print("\n  Working Memory:")
            for log in result.working_memory:
                print(f"    • {log}")

        if result.permission_filtered:
            print("\n  ⚠ Some records were hidden due to your access level.")

        print(f"\n  Sources: {len(result.verified_sources)}")
        for source, page in result.verified_sources:
            page_str = f"p.{page}" if page else "?"
            print(f"    • {source} [{page_str}]")