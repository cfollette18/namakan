#!/usr/bin/env python3
"""Custom AI Employee Intake — python3 intake.py --client 'Acme Corp' --role 'customer-service'"""
import argparse, json, os
from datetime import datetime

QUESTIONS = [
    {"id": "company", "q": "Company name?", "required": True},
    {"id": "name", "q": "What should we call this AI employee? (job title/role)", "required": True},
    {"id": "role", "q": "Detailed role description (what does this person do all day?)", "required": True},
    {"id": "supervisor_name", "q": "Supervisor name?", "required": True},
    {"id": "supervisor_email", "q": "Supervisor email?", "required": True},
    {"id": "systems", "q": "What systems does this AI need access to? (CRM, email, calendar, etc.)", "required": True},
    {"id": "data_sources", "q": "What data does it need to learn from? (ticket history, emails, docs)", "required": True},
    {"id": "workflows", "q": "Top 5 workflows it should handle?", "required": True},
    {"id": "success_metric", "q": "How do we measure success? (tickets/hour, CSAT, time saved)", "required": True},
    {"id": "escalation_policy", "q": "When should it escalate to a human?", "required": True},
    {"id": "pricing_tier", "q": "Pricing tier? (Standard $2K/mo, Professional $3K/mo, Enterprise $5K/mo)", "required": True},
]

def ask(q):
    print(f"\n>>> {q['q']}", end=" [REQUIRED]: " if q.get("required") else ": ")
    ans = input().strip()
    if q.get("required") and not ans:
        print("  Required.")
        return ask(q)
    return ans

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client")
    parser.add_argument("--role")
    parser.add_argument("--output", default="./clients")
    args = parser.parse_args()
    
    answers = {}
    if args.client: answers["company"] = args.client
    if args.role: answers["name"] = args.role
    
    for q in QUESTIONS:
        if q["id"] not in answers:
            answers[q["id"]] = ask(q)
    
    slug = answers.get("name", answers.get("company", "unknown")).lower().replace(" ", "-")
    emp_dir = os.path.join(args.output, slug)
    os.makedirs(f"{emp_dir}/data", exist_ok=True)
    
    config = {
        **answers,
        "intake_date": datetime.now().isoformat(),
        "pipeline": "custom-ai-employees",
        "current_phase": "shadow",
        "phase_history": [],
        "status": "onboarding_pending",
        "monthly_cost": answers.get("pricing_tier", "$2,000/mo")
    }
    
    with open(f"{emp_dir}/config.json", "w") as f:
        json.dump(config, f, indent=2)
    with open(f"{emp_dir}/status.json", "w") as f:
        json.dump({"employee": slug, "phase": "shadow", "status": "onboarding_pending"}, f, indent=2)
    
    print(f"\n✅ AI Employee created: {slug}")
    print(f"   Directory: {emp_dir}/config.json")
    print(f"\nNext: python3 workflows/onboarding.py --employee {slug} --status")

if __name__ == "__main__":
    main()
