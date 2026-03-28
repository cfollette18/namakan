#!/usr/bin/env python3
"""Agentic Workflow Intake — python3 intake.py --client 'Acme Corp'"""
import argparse, json, os
from datetime import datetime

QUESTIONS = [
    {"id": "company", "q": "Company name?", "required": True},
    {"id": "role", "q": "What should the AI employee do? (job title/function)", "required": True},
    {"id": "tasks", "q": "What are the top 3 tasks it should handle?", "required": True},
    {"id": "systems", "q": "What systems does it need access to? (CRM, email, calendar, API)", "required": True},
    {"id": "escalation", "q": "Who gets notified when human input is needed?", "required": True},
    {"id": "frequency", "q": "How often does it run? (real-time, daily batch, hourly)", "required": True},
    {"id": "success", "q": "How do we measure success? (tasks/hour, accuracy, satisfaction)", "required": True},
    {"id": "credentials", "q": "How do we get system access? (API keys, SSO, read-only)", "required": True},
    {"id": "contacts", "q": "Supervisor name and email?", "required": True},
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client")
    parser.add_argument("--output", default="./clients")
    args = parser.parse_args()
    
    answers = {"company": args.client} if args.client else {}
    for q in QUESTIONS:
        if q["id"] != "company":
            print(f"\n>>> {q['q']}", end=" [REQUIRED]: " if q["required"] else ": ")
            answers[q["id"]] = input().strip()
    
    slug = answers.get("company", "unknown").lower().replace(" ", "-")
    client_dir = os.path.join(args.output, slug)
    for sub in ["", "tasks", "configs", "logs"]:
        os.makedirs(f"{client_dir}/{sub}", exist_ok=True)
    
    config = {**answers, "intake_date": datetime.now().isoformat(), "pipeline": "agentic-workflows"}
    
    with open(f"{client_dir}/config.json", "w") as f:
        json.dump(config, f, indent=2)
    with open(f"{client_dir}/status.json", "w") as f:
        json.dump({"client": answers.get("company"), "pipeline": "agentic-workflows",
            "phases": {k: "pending" for k in ["discovery","process_mapping","build","testing","deploy"]}}, f, indent=2)
    
    print(f"\n✅ Done → {client_dir}/config.json")
    print(f"\nNext: python3 workflows/agent_engine.py --setup --client {slug}")

if __name__ == "__main__":
    main()
