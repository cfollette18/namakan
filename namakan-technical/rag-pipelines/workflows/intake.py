#!/usr/bin/env python3
"""
RAG Pipeline Client Intake
Usage: python3 intake.py --client "Acme Corp" --output ./clients
"""
import argparse, json, os
from datetime import datetime

QUESTIONS = [
    {"id": "company", "question": "Company name?", "required": True},
    {"id": "industry", "question": "What industry?", "required": True},
    {"id": "doc_types", "question": "What types of documents? (PDFs, Word, spreadsheets, etc.)", "required": True},
    {"id": "doc_count", "question": "Approximate number of documents?", "required": True},
    {"id": "update_frequency", "question": "How often does content change? (static/daily/weekly)", "required": True},
    {"id": "sources", "question": "Where are documents stored? (shared drive, Google Drive, SharePoint, CRM)", "required": True},
    {"id": "users", "question": "Who will query the RAG? (employees only / customers / public)", "required": True},
    {"id": "language", "question": "Primary language of documents?", "required": False},
    {"id": "security", "question": "Any compliance? (HIPAA, GDPR, SOC 2, none)", "required": False},
    {"id": "contacts", "question": "Primary contact name and email?", "required": True},
]

def ask(q):
    print(f"\n>>> {q['question']}", end="")
    if q.get("required"): print(" [REQUIRED]", end="")
    print(": ", end="")
    ans = input().strip()
    if q.get("required") and not ans:
        print("  Required — please enter a value")
        return ask(q)
    return ans

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client")
    parser.add_argument("--output", default="./clients")
    args = parser.parse_args()
    
    answers = {"company": args.client} if args.client else {}
    for q in QUESTIONS:
        if q["id"] != "company":
            answers[q["id"]] = ask(q)
    
    slug = answers.get("company", "unknown").lower().replace(" ", "-")
    client_dir = os.path.join(args.output, slug)
    for sub in ["", "data", "chromadb", "tests", "docs"]:
        os.makedirs(f"{client_dir}/{sub}", exist_ok=True)
    
    config = {**answers, "intake_date": datetime.now().isoformat(), "pipeline": "rag-pipelines"}
    
    with open(f"{client_dir}/config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    with open(f"{client_dir}/status.json", "w") as f:
        json.dump({
            "client": answers.get("company"),
            "pipeline": "rag-pipelines",
            "phases": {k: "pending" for k in ["discovery", "doc_audit", "architecture", "build", "eval", "deploy"]}
        }, f, indent=2)
    
    print(f"\n✅ Intake complete → {client_dir}/config.json")
    print("\nNext steps:")
    print(f"  1. Receive docs via S3 signed URL → save to {client_dir}/data/")
    print(f"  2. python3 workflows/ingestion_pipeline.py --input {client_dir}/data --output {client_dir}/chromadb")
    print(f"  3. python3 workflows/evaluate.py --questions {client_dir}/tests/questions.jsonl --collection {slug}")

if __name__ == "__main__":
    main()
