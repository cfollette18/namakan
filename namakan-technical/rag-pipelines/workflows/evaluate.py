#!/usr/bin/env python3
"""
RAG Evaluation Harness
Tests a RAG pipeline against a set of question/answer pairs.
Usage: python3 evaluate.py --questions questions.jsonl --collection client_collection
"""
import argparse
import json
import os
import sys
import time
import re

try:
    import chromadb
    from sentence_transformers import CrossEncoder
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

def color(tag, text):
    codes = {"PASS": "\033[92m", "FAIL": "\033[91m", "WARN": "\033[93m", "INFO": "\033[94m", "RESET": "\033[0m"}
    return f"{codes.get(tag, '')}{text}{codes['RESET']}"

def load_questions(path):
    """Load question/answer pairs from JSONL."""
    pairs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                pairs.append(json.loads(line))
    return pairs

def keyword_match(prediction, reference):
    """Check if prediction contains the reference answer."""
    pred_norm = re.sub(r'[^\w\s]', '', prediction.lower())
    ref_norm = re.sub(r'[^\w\s]', '', reference.lower())
    return ref_norm in pred_norm

def rag_query(question, collection_name, embed_model="nomic-ai/nomic-embed-text-v1.5"):
    """
    Execute a RAG query against ChromaDB.
    Returns: (retrieved_context, generated_answer)
    """
    # Connect to ChromaDB
    client = chromadb.Client()
    collection = client.get_collection(name=collection_name)
    
    # Encode query
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(embed_model)
    query_embedding = model.encode([question])
    
    # Retrieve
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=5
    )
    
    # Build context
    docs = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    
    context_parts = []
    for i, (doc, dist, meta) in enumerate(zip(docs, distances, metadatas)):
        source = meta.get("source", "unknown") if meta else "unknown"
        page = meta.get("page", "?") if meta else "?"
        context_parts.append(f"[Doc {i+1}] (source: {source}, page {page}, score: {1-dist:.3f})\n{doc[:500]}")
    
    context = "\n\n---\n\n".join(context_parts)
    return context, docs

def evaluate_rag(qa_pairs, collection_name, llm_api=None):
    """Run RAG evaluation against question/answer pairs."""
    results = {
        "total": len(qa_pairs),
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "avg_retrieval_time": 0,
        "avg_total_time": 0,
        "details": []
    }
    
    retrieval_times = []
    total_times = []
    
    for i, pair in enumerate(qa_pairs):
        question = pair["question"]
        expected = pair["answer"]
        pair_id = pair.get("id", f"q-{i}")
        
        print(f"\n  [{i+1}/{len(qa_pairs)}] {pair_id}")
        print(f"    Q: {question[:80]}")
        
        start_total = time.time()
        try:
            start_ret = time.time()
            context, docs = rag_query(question, collection_name)
            retrieval_time = time.time() - start_ret
            retrieval_times.append(retrieval_time)
            
            # Simple answer quality check (no LLM needed)
            # Check if context actually contains the answer
            context_text = " ".join(docs)
            matched = keyword_match(context_text, expected)
            
            retrieval_time_s = round(retrieval_time, 3)
            total_time = time.time() - start_total
            total_times.append(total_time)
            
            if matched:
                results["passed"] += 1
                status = color("PASS", "✓ PASS")
            else:
                results["failed"] += 1
                status = color("FAIL", "✗ FAIL")
            
            print(f"    {status} | retrieval: {retrieval_time_s}s")
            print(f"    Retrieved {len(docs)} docs | top doc: {docs[0][:100] if docs else 'none'}...")
            
            # Show what we found vs expected
            if not matched:
                print(f"    {color('WARN', '  Expected keyword:')} {expected[:60]}")
                print(f"    {color('INFO', '  Top retrieved:')} {docs[0][:100] if docs else 'none'}...")
            
            results["details"].append({
                "id": pair_id,
                "question": question,
                "expected": expected,
                "status": "passed" if matched else "failed",
                "retrieval_time": retrieval_time_s,
                "total_time": round(total_time, 3),
                "num_docs": len(docs),
                "top_doc": docs[0][:200] if docs else ""
            })
            
        except Exception as e:
            results["errors"] += 1
            print(f"    {color('FAIL', 'ERROR')} {e}")
            results["details"].append({
                "id": pair_id,
                "status": "error",
                "error": str(e)
            })
    
    n = results["total"] - results["errors"]
    results["pass_rate"] = results["passed"] / n if n else 0
    results["avg_retrieval_time"] = sum(retrieval_times) / len(retrieval_times) if retrieval_times else 0
    results["avg_total_time"] = sum(total_times) / len(total_times) if total_times else 0
    
    return results

def print_report(results):
    print(f"\n{'='*60}")
    print(f"  RAG EVALUATION REPORT")
    print(f"{'='*60}")
    print(f"  Total questions: {results['total']}")
    print(f"  Passed:          {results['passed']} ({results['pass_rate']:.1%})")
    print(f"  Failed:          {results['failed']}")
    print(f"  Errors:          {results['errors']}")
    print(f"\n  Avg retrieval time: {results['avg_retrieval_time']:.3f}s")
    print(f"  Avg total time:    {results['avg_total_time']:.3f}s")
    
    threshold = 0.8
    if results["pass_rate"] >= threshold:
        print(f"\n  {color('PASS', '✓ RAG pipeline meets quality threshold (≥80%)')}")
    else:
        print(f"\n  {color('FAIL', f'✗ RAG pipeline below threshold ({results[\"pass_rate\"]:.1%} < {threshold:.0%})')}")
        print(f"\n  {color('WARN', 'Recommendations:')}")
        print(f"    - Increase chunk overlap")
        print(f"    - Try a domain-specific embedding model")
        print(f"    - Add hybrid search (dense + sparse)")
        print(f"    - Increase n_results from 5 to 10")
    print(f"{'='*60}")

def main():
    if not HAS_DEPS:
        print("ERROR: Missing dependencies. Run: pip install chromadb sentence-transformers")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="Namakan RAG Evaluation")
    parser.add_argument("--questions", required=True, help="JSONL file with question/answer pairs")
    parser.add_argument("--collection", required=True, help="ChromaDB collection name")
    parser.add_argument("--embed-model", default="nomic-ai/nomic-embed-text-v1.5", help="Embedding model")
    parser.add_argument("--output", help="Save results to JSON")
    args = parser.parse_args()
    
    if not os.path.exists(args.questions):
        print(f"ERROR: Questions file not found: {args.questions}")
        sys.exit(1)
    
    qa_pairs = load_questions(args.questions)
    print(f"Loaded {len(qa_pairs)} question/answer pairs")
    
    results = evaluate_rag(qa_pairs, args.collection, args.embed_model)
    print_report(results)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved to {args.output}")
    
    sys.exit(0 if results["pass_rate"] >= 0.8 else 1)

if __name__ == "__main__":
    main()
