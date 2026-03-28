#!/usr/bin/env python3
"""
Namakan — RAG Pipelines: Retrieval Pipeline
Hybrid search, re-ranking, and generation.
"""
import json
import numpy as np
import argparse
from typing import Optional

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

def retrieve_faiss(
    query: str,
    chunks: list,
    embeddings: np.ndarray,
    index,
    embedder,
    top_k: int = 10,
) -> list[dict]:
    """Retrieve from FAISS index."""
    query_emb = np.array(embedder([query])).astype('float32')
    faiss.normalize_L2(query_emb)
    scores, indices = index.search(query_emb, top_k * 2)
    
    seen = set()
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(chunks):
            continue
        chunk = dict(chunks[idx])
        chunk["score"] = float(score)
        if chunk["text"] not in seen:
            seen.add(chunk["text"])
            results.append(chunk)
            if len(results) >= top_k:
                break
    return results

def retrieve_chroma(
    query: str,
    chunks: list,
    collection,
    embedder,
    top_k: int = 10,
) -> list[dict]:
    """Retrieve from ChromaDB."""
    results = collection.query(query_texts=[query], n_results=top_k * 2)
    
    seen = set()
    output = []
    for i, (texts, scores, metas) in enumerate(zip(
        results["documents"][0],
        results["distances"][0] if "distances" in results else [1.0]*len(results["documents"][0]),
        results["metadatas"][0] if "metadatas" in results else [{}]*len(results["documents"][0])
    )):
        chunk = {"text": texts, "score": 1.0 - scores, **metas}
        if chunk["text"] not in seen:
            seen.add(chunk["text"])
            output.append(chunk)
            if len(output) >= top_k:
                break
    return output

def rerank(query: str, results: list, top_k: int = 5) -> list[dict]:
    """Re-rank results using cross-encoder for better relevance."""
    try:
        from sentence_transformers import CrossEncoder
        model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
        pairs = [(query, r["text"][:512]) for r in results]
        scores = model.predict(pairs)
        
        reranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
        return [dict(r[0], rerank_score=float(r[1])) for r in reranked[:top_k]]
    except ImportError:
        print("[WARN] pip install sentence-transformers for re-ranking")
        return results[:top_k]

def generate_answer(
    query: str,
    contexts: list,
    model: str = "gpt-4o",
    system_prompt: str = None,
) -> str:
    """Generate answer using retrieved context."""
    try:
        from openai import OpenAI
        client = OpenAI()
        
        if system_prompt is None:
            system_prompt = (
                "You are a helpful assistant. Use the provided context to answer the question. "
                "If the context doesn't contain enough information, say so. "
                "Always cite which source you're drawing from."
            )
        
        context_text = "\n\n".join(
            f"[Source {i+1}]: {c['text'][:500]}"
            for i, c in enumerate(contexts)
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
        ]
        
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            max_tokens=1000,
        )
        return resp.choices[0].message.content
    except ImportError:
        return "[Answer generation requires: pip install openai]"

class RAGRetriever:
    """Full RAG retrieval + generation pipeline."""
    
    def __init__(self, index_dir: str, llm_model: str = "gpt-4o"):
        self.embedder = get_embedder("local")
        self.chunks, self.embeddings, self.index, self.manifest = load_index(index_dir)
        self.llm_model = llm_model
        self.vectorstore_type = self.manifest.get("result", {}).get("type", "numpy")
    
    def retrieve(self, query: str, top_k: int = 10, rerank_k: int = 5) -> list[dict]:
        if self.vectorstore_type == "faiss":
            results = retrieve_faiss(query, self.chunks, self.embeddings, self.index, self.embedder, top_k)
        else:
            results = retrieve_chroma(query, self.chunks, self.index, self.embedder, top_k)
        
        if rerank_k < top_k:
            results = rerank(query, results, rerank_k)
        
        return results
    
    def answer(self, query: str, top_k: int = 10) -> tuple[str, list]:
        contexts = self.retrieve(query, top_k)
        answer = generate_answer(query, contexts, self.llm_model)
        return answer, contexts
    
    def stream_answer(self, query: str, top_k: int = 10):
        """Stream the answer from OpenAI."""
        from openai import OpenAI
        client = OpenAI()
        
        contexts = self.retrieve(query, top_k)
        context_text = "\n\n".join(f"[Source {i+1}]: {c['text'][:500]}" for i, c in enumerate(contexts))
        
        messages = [
            {"role": "system", "content": "Use the provided context to answer. Cite sources."},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
        ]
        
        stream = client.chat.completions.create(
            model=self.llm_model,
            messages=messages,
            temperature=0.2,
            stream=True,
        )
        
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Namakan RAG Retrieval")
    parser.add_argument("--index-dir", "-i", required=True, help="Output dir from ingestion pipeline")
    parser.add_argument("--query", "-q", required=True, help="Query to answer")
    parser.add_argument("--top-k", "-k", type=int, default=10)
    parser.add_argument("--rerank-k", type=int, default=5)
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()
    
    retriever = RAGRetriever(args.index_dir)
    
    if args.stream:
        print("Answer (streaming):")
        for text in retriever.stream_answer(args.query, args.top_k):
            print(text, end="", flush=True)
        print()
    else:
        answer, contexts = retriever.answer(args.query, args.top_k)
        print(f"Answer: {answer}\n")
        print(f"Sources ({len(contexts)}):")
        for i, c in enumerate(contexts[:3]):
            print(f"\n[{i+1}] (score={c.get('score', 'N/A'):.3f}) {c['text'][:200]}...")
