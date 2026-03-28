#!/usr/bin/env python3
"""
RAG Indexer for Namakan Documentation

Indexes all Namakan markdown files into ChromaDB
for retrieval-augmented generation with Ollama.
"""

import os
from pathlib import Path
from typing import List
import chromadb
from chromadb.config import Settings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration
NAMAKAN_ROOT = "/home/cfollette18/.openclaw/workspace/namakan"
CHROMA_PATH = "/home/cfollette18/.openclaw/workspace/namakan/namakan-training/chroma_db"
OLLAMA_BASE = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"

def load_markdown_files(root: str) -> List[str]:
    """Load all markdown files from Namakan directory."""
    docs = []
    for md_path in Path(root).glob("**/*.md"):
        if ".git" in str(md_path):
            continue
        try:
            content = md_path.read_text()
            rel_path = md_path.relative_to(root)
            docs.append(f"<!-- File: {rel_path} -->\n\n{content}")
        except Exception as e:
            print(f"Error loading {md_path}: {e}")
    return docs

def split_documents(documents: List[str]) -> List:
    """Split documents into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "]
    )
    return splitter.create_documents(documents)

def main():
    print("Loading Namakan documentation...")
    docs = load_markdown_files(NAMAKAN_ROOT)
    print(f"Loaded {len(docs)} documents")
    
    print("Splitting documents...")
    chunks = split_documents(docs)
    print(f"Created {len(chunks)} chunks")
    
    print(f"Connecting to Ollama embeddings at {OLLAMA_BASE}...")
    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_BASE
    )
    
    print(f"Creating ChromaDB at {CHROMA_PATH}...")
    os.makedirs(CHROMA_PATH, exist_ok=True)
    
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="namakan-knowledge"
    )
    
    print(f"Indexed {db._collection.count()} chunks into ChromaDB")
    print("\nDone! RAG index ready.")
    print(f"Use: rag_server.py to query the knowledge base")

if __name__ == "__main__":
    main()
