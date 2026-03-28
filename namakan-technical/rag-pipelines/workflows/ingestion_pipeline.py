#!/usr/bin/env python3
"""
Namakan — RAG Pipelines: Ingestion Pipeline
Document extraction, cleaning, chunking, embedding, and vector store indexing.
"""
import os
import re
import json
import hashlib
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Literal

# ─── Document Extraction ────────────────────────────────────────────────────────

EXTRACTORS = {}

def extract_pdf(filepath: str) -> str:
    """Extract text from PDF using pdfplumber or PyPDF2."""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_parts.append(t)
        return "\n\n".join(text_parts)
    except ImportError:
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(filepath)
            return "\n\n".join(p.extract_text() or "" for p in reader.pages)
        except ImportError:
            return "[PDF extraction requires: pip install pdfplumber]"

EXTRACTORS[".pdf"] = extract_pdf

def extract_docx(filepath: str) -> str:
    """Extract text from DOCX."""
    try:
        from docx import Document
        doc = Document(filepath)
        return "\n\n".join(p.text for p in doc.paragraphs)
    except ImportError:
        return "[DOCX extraction requires: pip install python-docx]"

EXTRACTORS[".docx"] = extract_docx

def extract_html(filepath: str) -> str:
    """Extract visible text from HTML."""
    try:
        from bs4 import BeautifulSoup
        with open(filepath) as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text(separator="\n", strip=True)
    except ImportError:
        with open(filepath) as f:
            import re
            text = re.sub(r"<script.*?</script>", "", f.read(), flags=re.DOTALL)
            text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL)
            text = re.sub(r"<[^>]+>", "", text)
            return text.strip()

EXTRACTORS[".html"] = extract_html
EXTRACTORS[".htm"] = extract_html

def extract_txt(filepath: str) -> str:
    with open(filepath, errors="ignore") as f:
        return f.read()

EXTRACTORS[".txt"] = extract_txt
EXTRACTORS[".md"] = extract_txt
EXTRACTORS[".csv"] = extract_txt

def extract_json(filepath: str) -> str:
    """Extract text from structured JSON."""
    with open(filepath) as f:
        data = json.load(f)
    return json.dumps(data, indent=2)

EXTRACTORS[".json"] = extract_json
EXTRACTORS[".jsonl"] = extract_json

# ─── Text Processing ────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Clean extracted text."""
    import unicodedata
    # Normalize unicode
    text = unicodedata.normalize('NFKC', text)
    # Remove null bytes
    text = text.replace('\x00', '')
    # Remove control characters
    text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C' or c in '\n\t')
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def chunk_text(
    text: str,
    chunk_size: int = 512,
    overlap: int = 64,
    strategy: Literal["fixed", "recursive", "sentence"] = "recursive"
) -> list[dict]:
    """Split text into chunks with metadata."""
    import hashlib
    
    if strategy == "fixed":
        # Simple fixed-token chunks
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(text)
        chunks = []
        for i in range(0, len(tokens), chunk_size - overlap):
            chunk_tokens = tokens[i:i + chunk_size]
            chunk_text = enc.decode(chunk_tokens)
            if len(chunk_text.strip()) > 20:
                chunks.append({
                    "text": chunk_text,
                    "chunk_id": hashlib.sha256(chunk_text.encode()).hexdigest()[:16],
                    "start_token": i,
                    "end_token": i + len(chunk_tokens),
                })
    
    elif strategy == "recursive":
        # Recursive character splitting with semantic breaks
        separators = ["\n\n", "\n", ". ", " ", ""]
        chunks = []
        
        def split_recursive(text: str, sep_idx: int) -> list[str]:
            if sep_idx >= len(separators):
                return [text] if len(text) > 20 else []
            
            sep = separators[sep_idx]
            if not sep:
                return [text[i:i+chunk_size*4] for i in range(0, len(text), chunk_size*4)]
            
            parts = text.split(sep)
            result, current = [], ""
            
            for part in parts:
                if len(current) + len(sep) + len(part) <= chunk_size * 4:
                    current += sep + part
                else:
                    if current:
                        result.append(current.strip())
                    current = part
            
            if current:
                result.append(current.strip())
            
            # If any chunk too big, recurse
            final = []
            for r in result:
                if len(r) > chunk_size * 4:
                    final.extend(split_recursive(r, sep_idx + 1))
                elif len(r) > 20:
                    final.append(r)
            return final
        
        texts = split_recursive(text, 0)
        for t in texts:
            chunks.append({
                "text": t,
                "chunk_id": hashlib.sha256(t.encode()).hexdigest()[:16],
            })
    
    elif strategy == "sentence":
        # Split by sentences, group into chunks
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks, current = [], ""
        for sent in sentences:
            if len(current) + len(sent) <= chunk_size * 4:
                current += " " + sent
            else:
                if current.strip():
                    chunks.append({"text": current.strip()})
                current = sent
        if current.strip():
            chunks.append({"text": current.strip()})
    
    # Add metadata
    for i, chunk in enumerate(chunks):
        chunk["index"] = i
        chunk["total_chunks"] = len(chunks)
    
    return chunks

# ─── Embedding ─────────────────────────────────────────────────────────────────

def get_embedder(provider: Literal["openai", "nomic", "local"] = "nomic"):
    """Factory for embedding models."""
    if provider == "openai":
        try:
            from openai import OpenAI
            client = OpenAI()
            def embed(texts: list[str]) -> list[list[float]]:
                resp = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=texts
                )
                return [item.embedding for item in resp.data]
            return embed
        except ImportError:
            raise RuntimeError("pip install openai")
    
    elif provider == "nomic":
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")
            def embed(texts: list[str]) -> list[list[float]]:
                return model.encode(texts, normalize_embeddings=True).tolist()
            return embed
        except ImportError:
            raise RuntimeError("pip install sentence-transformers")
    
    elif provider == "local":
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer("all-MiniLM-L6-v2")
            def embed(texts: list[str]) -> list[list[float]]:
                return model.encode(texts).tolist()
            return embed
        except ImportError:
            raise RuntimeError("pip install sentence-transformers")

# ─── Vector Store ────────────────────────────────────────────────────────────────

def index_to_vectorstore(
    chunks: list[dict],
    embedder,
    vectorstore: Literal["qdrant", "pinecone", "chroma", "local"],
    output_dir: str,
    collection_name: str = "documents",
    batch_size: int = 100,
):
    """Index chunks to vector database."""
    import hashlib
    
    if vectorstore == "chroma":
        try:
            import chromadb
            client = chromadb.PersistentClient(path=output_dir)
            collection = client.get_or_create_collection(collection_name)
            
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i+batch_size]
                texts = [c["text"][:2000] for c in batch]
                embeddings = embedder(texts)
                ids = [c["chunk_id"] for c in batch]
                metadatas = [{"index": c["index"], "total": c["total_chunks"]} for c in batch]
                
                collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
                print(f"[INDEX] Indexed {min(i+batch_size, len(chunks))}/{len(chunks)}")
            
            return {"type": "chroma", "path": output_dir, "collection": collection_name}
        
        except ImportError:
            raise RuntimeError("pip install chromadb")
    
    elif vectorstore == "local":
        # Simple numpy vector store
        import numpy as np
        os.makedirs(output_dir, exist_ok=True)
        
        all_embeddings = []
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            texts = [c["text"][:2000] for c in batch]
            embeddings = embedder(texts)
            all_embeddings.extend(embeddings)
            print(f"[INDEX] Embedded {min(i+batch_size, len(chunks))}/{len(chunks)}")
        
        # Save as numpy
        emb_array = np.array(all_embeddings).astype('float32')
        np.save(os.path.join(output_dir, "embeddings.npy"), emb_array)
        
        # Save chunks as JSON
        with open(os.path.join(output_dir, "chunks.json"), "w") as f:
            json.dump(chunks, f)
        
        # Build FAISS index
        try:
            import faiss
            dim = emb_array.shape[1]
            index = faiss.IndexFlatIP(dim)
            faiss.normalize_L2(emb_array)
            index.add(emb_array)
            faiss.write_index(index, os.path.join(output_dir, "index.faiss"))
            print(f"[INDEX] FAISS index built: {len(chunks)} vectors, dim={dim}")
            return {"type": "faiss", "path": output_dir, "vectors": len(chunks)}
        except ImportError:
            print("[WARN] pip install faiss-cpu or faiss-gpu")
            return {"type": "numpy", "path": output_dir, "vectors": len(chunks)}

# ─── Main Ingestion Pipeline ────────────────────────────────────────────────────

def run_ingestion(
    input_dir: str,
    output_dir: str,
    vectorstore: Literal["chroma", "pinecone", "qdrant", "local"] = "local",
    embedder: Literal["openai", "nomic", "local"] = "local",
    chunk_size: int = 512,
    chunk_strategy: str = "recursive",
):
    """Run full RAG ingestion pipeline."""
    import time
    start = time.time()
    
    print("=" * 60)
    print("NAMAKAN RAG INGESTION PIPELINE")
    print("=" * 60)
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Vector store: {vectorstore}")
    print(f"Embedder: {embedder}")
    print("=" * 60)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Extract
    print("\n[1/4] Extracting documents...")
    documents = []
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in EXTRACTORS:
                continue
            filepath = os.path.join(root, filename)
            try:
                text = EXTRACTORS[ext](filepath)
                text = clean_text(text)
                documents.append({"filename": filename, "path": filepath, "text": text})
                print(f"  Extracted: {filename} ({len(text)} chars)")
            except Exception as e:
                print(f"  ERROR {filename}: {e}")
    
    print(f"  Total documents: {len(documents)}")
    
    # 2. Chunk
    print(f"\n[2/4] Chunking documents (strategy={chunk_strategy})...")
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"], chunk_size=chunk_size, strategy=chunk_strategy)
        for chunk in chunks:
            chunk["source"] = doc["filename"]
        all_chunks.extend(chunks)
        print(f"  {doc['filename']}: {len(chunks)} chunks")
    
    print(f"  Total chunks: {len(all_chunks)}")
    
    # 3. Embed
    print(f"\n[3/4] Embedding chunks...")
    embed_fn = get_embedder(embedder)
    
    # 4. Index
    print(f"\n[4/4] Indexing to {vectorstore}...")
    result = index_to_vectorstore(all_chunks, embed_fn, vectorstore, output_dir)
    
    # Save chunks for retrieval
    chunks_path = os.path.join(output_dir, "chunks.json")
    with open(chunks_path, "w") as f:
        json.dump(all_chunks, f, indent=2)
    
    elapsed = time.time() - start
    print(f"\n[DONE] Ingestion complete in {elapsed:.1f}s")
    print(f"  Documents: {len(documents)}")
    print(f"  Chunks: {len(all_chunks)}")
    print(f"  Vector store: {result}")
    
    # Write manifest
    manifest = {
        "input_dir": input_dir,
        "output_dir": output_dir,
        "vectorstore": vectorstore,
        "embedder": embedder,
        "chunk_size": chunk_size,
        "chunk_strategy": chunk_strategy,
        "documents": len(documents),
        "chunks": len(all_chunks),
        "duration_seconds": elapsed,
        "result": result,
    }
    with open(os.path.join(output_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    
    return manifest

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--vectorstore", "-v", default="local", choices=["chroma", "pinecone", "qdrant", "local"])
    parser.add_argument("--embedder", "-e", default="local", choices=["openai", "nomic", "local"])
    parser.add_argument("--chunk-size", "-c", type=int, default=512)
    parser.add_argument("--strategy", "-s", default="recursive", choices=["fixed", "recursive", "sentence"])
    args = parser.parse_args()
    run_ingestion(**vars(args))
