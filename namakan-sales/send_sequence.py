#!/usr/bin/env python3
"""
Cold Email Execution Engine — Namakan Sales
Generates personalized emails, tracks sequence state, manages outreach.

Usage:
  python3 send_sequence.py --prospect "polaris" --email 1        # Generate email 1
  python3 send_sequence.py --prospect "polaris" --status          # Check sequence status
  python3 send_sequence.py --prospect "polaris" --advance          # Mark replied, advance sequence
  python3 send_sequence.py --list                                  # List all prospects + status
  python3 send_sequence.py --generate-all                           # Generate emails for all prospects
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta

SEQUENCE = [
    {"num": 1, "name": "intro",        "day": 0,  "subject_prefix": "Question about", "goal": "Get reply"},
    {"num": 2, "name": "value_demo",   "day": 7,  "subject_prefix": "Re:",             "goal": "Get reply"},
    {"num": 3, "name": "domain_specific","day": 14,"subject_prefix": "A custom AI idea for","goal": "Get reply"},
    {"num": 4, "name": "resource",    "day": 21, "subject_prefix": "Research on AI adoption","goal": "Keep warm"},
    {"num": 5, "name": "close",       "day": 28, "subject_prefix": "Last note from",  "goal": "Close file"},
]

PROSPECTS_DIR = os.path.join(os.path.dirname(__file__), "prospects")

def load_prospect(name):
    path = os.path.join(PROSPECTS_DIR, f"{name}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)

def save_prospect(name, data):
    os.makedirs(PROSPECTS_DIR, exist_ok=True)
    path = os.path.join(PROSPECTS_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path

def create_prospect(name, contact_name, contact_title, contact_email,
                    company, industry, ai_opportunity, proprietary_data,
                    notes="", phone="", linkedin=""):
    """Create a new prospect record."""
    data = {
        "name": name,
        "company": company,
        "contact_name": contact_name,
        "contact_title": contact_title,
        "contact_email": contact_email,
        "phone": phone,
        "linkedin": linkedin,
        "industry": industry,
        "ai_opportunity": ai_opportunity,
        "proprietary_data": proprietary_data,
        "notes": notes,
        "created": datetime.now().isoformat(),
        "last_contact": None,
        "last_email_sent": None,
        "sequence_day": 0,
        "sequence_status": "active",  # active, replied, converted, closed
        "emails_sent": [],
        "replied_email": None,
        "converted": False,
        "closed_reason": None,
    }
    path = save_prospect(name, data)
    print(f"✅ Created prospect: {name} → {path}")
    return data

def generate_subject(seq, company, contact_name):
    """Generate personalized subject line."""
    prefixes = {
        1: f"Question about {company}'s custom AI strategy",
        2: f"Re: Question about {company}'s custom AI strategy",
        3: f"A custom AI idea for {company}",
        4: f"Research on AI adoption in {company}'s industry — might be useful",
        5: f"Last note from Clint at Namakan",
    }
    return prefixes.get(seq["num"], f"{seq['subject_prefix']} {company}")

def generate_email_body(seq, prospect):
    """Generate email body from sequence + prospect data."""
    num = seq["num"]
    company = prospect["company"]
    contact_name = prospect["contact_name"]
    contact_title = prospect["contact_title"]
    industry = prospect["industry"]
    ai_opp = prospect["ai_opportunity"]
    prop_data = prospect["proprietary_data"]
    notes = prospect.get("notes", "")

    if num == 1:
        subject = generate_subject(seq, company, contact_name)
        body = f"""Hi {contact_name},

I came across {company}'s work on {ai_opp}.

It got me thinking about something specific: you have years of {prop_data} that have never been fully leveraged — and the gap between what you have and what a generic AI model can do with it is massive.

That's what we do at Namakan AI Engineering. We build custom AI systems — fine-tuned models, RAG pipelines, and AI employees — trained specifically on a client's proprietary data, integrated into their specific systems.

**The difference is significant:**

- A generic model knows what a CNC machine is. A model fine-tuned on your quality inspection logs knows what YOUR machines do wrong under specific conditions.
- A generic RAG knows about medical guidelines. One built on your patient population data knows what's predictive for YOUR patients.

We recently worked with a mid-size manufacturer in the Midwest to build a RAG pipeline on their service records and technical documentation. Their field service team now gets AI-generated repair recommendations in seconds — pulling from 15 years of internal data a generic model never saw.

I'd love to understand what proprietary data assets {company} has and whether a custom AI approach could move the needle. Not a pitch — just a conversation.

Do you have 20 minutes in the next few weeks?

—  
Clint Follette  
Namakan AI Engineering  
clint@namakan.ai"""

    elif num == 2:
        subject = f"Re: Question about {company}'s custom AI strategy"
        body = f"""Hi {contact_name},

Following up — I wanted to share a specific example that might illustrate what "custom AI engineering" actually means.

**What we built for a mid-size manufacturer in the Midwest:**

Their problem: Quality inspectors were reviewing CNC parts against specifications manually — using tribal knowledge passed down from senior inspectors that was never documented. Every new hire took 6+ months to reach full effectiveness.

What we did:
1. Captured inspectors' decision-making heuristics
2. Built a fine-tuning dataset from 3 years of inspection records, labeled by their senior inspectors
3. Fine-tuned a model to flag defects in their inspectors' own terminology
4. Integrated it into their existing workflow

Result: New inspector onboarding dropped from 6 months to 6 weeks. Defect escape rate dropped 34% in the first quarter.

**Why this matters for {company}:**

You've likely spent years building {prop_data}. Generic AI can't access that context. But a custom AI system built on YOUR data doesn't just know the problem — it knows how YOUR organization thinks about it.

If any of this resonates — or if you've already been thinking about proprietary AI — I'd love to hear what's on your mind.

{contact_name},

—  
Clint Follette  
Namakan AI Engineering"""

    elif num == 3:
        subject = f"A custom AI idea for {company}"
        body = f"""Hi {contact_name},

I've spent some time thinking about {company}'s specific situation — specifically, {ai_opp}. Here's what stands out:

**Opportunity 1: RAG pipeline on your {prop_data}**

You have years of {prop_data} that's never been systematically indexed. A RAG pipeline would let your team query that institutional knowledge in natural language — surfacing patterns in seconds instead of days.

**Opportunity 2: Fine-tuning on your proprietary data**

Generic models don't know what {ai_opp}. With fine-tuning on your proprietary data, an AI system could recognize and flag specific scenarios with significant accuracy improvements.

**Opportunity 3: Workflow-integrated AI for your team**

Your team likely spends significant time on tasks that could be automated with a custom AI employee trained on your data and workflows.

I put together a brief on each of these. Happy to walk through in 20 minutes if any resonates — or tell me if I'm off base. Either way, no follow-up if you're not interested.

—  
Clint Follette  
Namakan AI Engineering"""

    elif num == 4:
        subject = f"Research on AI adoption in {industry} — might be useful"
        body = f"""Hi {contact_name},

I'll keep this one light — I wanted to share some research on custom AI adoption in {industry}, and then close your file unless you want to keep the conversation open.

**What the data shows:**

Across manufacturing, healthcare, and financial services companies that have moved past generic AI into custom AI engineering:

- **RAG pipelines** on proprietary knowledge bases consistently deliver 40–60% time savings on research and retrieval
- **Fine-tuned models** for domain-specific tasks show 20–40% accuracy improvements over generic models
- **AI employees** handling routine decisions free up 15–25 hours/week per knowledge worker

The pattern: generic AI gives you 10–20% improvement. Custom AI built on your data gives you 60–80%.

I've attached a one-page framework we use with clients to evaluate custom AI opportunities — not a sales document, just something that helps leaders think through where to start.

If anything is useful, I'm happy to continue. If not — I won't keep reaching out.

Thanks for your time.

—  
Clint Follette  
Namakan AI Engineering  
clint@namakan.ai"""

    else:  # num == 5
        subject = f"Last note from Clint at Namakan — closing your file"
        body = f"""Hi {contact_name},

I've reached out a few times and haven't heard back — so I'm going to close your file for now. No hard feelings.

I genuinely believe custom AI engineering is the biggest productivity opportunity for companies like {company} over the next 3–5 years. The businesses that build AI systems on their proprietary data will have a durable competitive advantage.

But that doesn't mean the timing is right for you right now — and I'd rather respect your inbox than add noise.

If the time ever comes when you're evaluating custom AI options, I'd welcome the conversation. Here's my direct line: (612) 805-8867. I also respond to LinkedIn messages.

Best of luck with everything.

—  
Clint Follette  
Namakan AI Engineering"""

    return subject, body

def print_email(seq, prospect):
    """Print a generated email to stdout."""
    subject, body = generate_email_body(seq, prospect)
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  EMAIL {seq['num']} — {seq['name']}")
    print(f"  Day: {seq['day']} | Goal: {seq['goal']}")
    print(f"{sep}")
    print(f"\nTo: {prospect['contact_name']} <{prospect['contact_email']}>")
    print(f"Subject: {subject}\n")
    print(body)
    print(f"\n{sep}")
    return subject, body

def advance_sequence(prospect_name):
    """Mark current email as sent, advance to next."""
    prospect = load_prospect(prospect_name)
    if not prospect:
        print(f"ERROR: Prospect '{prospect_name}' not found")
        return
    
    if prospect["sequence_status"] in ("closed", "converted"):
        print(f"Prospect is already {prospect['sequence_status']}")
        return
    
    current_day = prospect["sequence_day"]
    
    # Find next email
    next_seq = None
    for seq in SEQUENCE:
        if seq["day"] > current_day:
            next_seq = seq
            break
    
    if next_seq:
        prospect["sequence_day"] = next_seq["day"]
        prospect["last_contact"] = datetime.now().isoformat()
        prospect["last_email_sent"] = next_seq["num"]
        prospect["emails_sent"].append({
            "num": next_seq["num"],
            "sent_at": datetime.now().isoformat()
        })
        save_prospect(prospect_name, prospect)
        print(f"Advanced to Email {next_seq['num']} ({next_seq['name']}) — Day {next_seq['day']}")
    else:
        print("Sequence complete — no more emails")

def mark_replied(prospect_name):
    """Mark prospect as replied."""
    prospect = load_prospect(prospect_name)
    if not prospect:
        print(f"ERROR: Prospect '{prospect_name}' not found")
        return
    
    prospect["sequence_status"] = "replied"
    prospect["last_contact"] = datetime.now().isoformat()
    save_prospect(prospect_name, prospect)
    print(f"Marked as replied: {prospect['company']}")

def mark_converted(prospect_name):
    """Mark prospect as converted (signed contract)."""
    prospect = load_prospect(prospect_name)
    if not prospect:
        print(f"ERROR: Prospect '{prospect_name}' not found")
        return
    
    prospect["sequence_status"] = "converted"
    prospect["converted"] = True
    prospect["last_contact"] = datetime.now().isoformat()
    save_prospect(prospect_name, prospect)
    print(f"🎉 CONVERTED: {prospect['company']}")

def close_prospect(prospect_name, reason=""):
    """Close a prospect (no reply, not interested, etc.)."""
    prospect = load_prospect(prospect_name)
    if not prospect:
        print(f"ERROR: Prospect '{prospect_name}' not found")
        return
    
    prospect["sequence_status"] = "closed"
    prospect["closed_reason"] = reason
    save_prospect(prospect_name, prospect)
    print(f"Closed: {prospect['company']} ({reason})")

def list_prospects():
    """List all prospects with status."""
    if not os.path.exists(PROSPECTS_DIR):
        print("No prospects yet. Create one with --create")
        return
    
    files = [f for f in os.listdir(PROSPECTS_DIR) if f.endswith(".json")]
    if not files:
        print("No prospects yet.")
        return
    
    print(f"\n{'='*70}")
    print(f"  NAMAKAN SALES PROSPECTS")
    print(f"{'='*70}")
    print(f"  {'Name':<20} {'Company':<25} {'Status':<10} {'Last Email':<12} {'Day'}")
    print(f"  {'-'*70}")
    
    for fname in sorted(files):
        name = fname[:-5]
        p = load_prospect(name)
        if not p:
            continue
        
        status = p.get("sequence_status", "?")
        last = p.get("last_email_sent") or "—"
        day = p.get("sequence_day", 0) or 0
        company = p.get("company", "?")[:23]
        cname = p.get("contact_name", "?")[:18]
        
        status_icon = {"active": "🟡", "replied": "🟢", "converted": "✅", "closed": "⚫"}.get(status, "?")
        
        print(f"  {status_icon} {name:<18} {company:<25} {status:<10} {last:<12} {day}")
    
    print(f"{'='*70}\n")

def add_prospect_from_args(args):
    """Create a new prospect from CLI arguments."""
    name = args.name or args.company.lower().replace(" ", "-")
    data = create_prospect(
        name=name,
        contact_name=args.contact,
        contact_title=args.title or "",
        contact_email=args.email,
        company=args.company,
        industry=args.industry or "",
        ai_opportunity=args.opportunity or "",
        proprietary_data=args.data or "",
        notes=args.notes or "",
        phone=args.phone or "",
        linkedin=args.linkedin or "",
    )
    return data

def main():
    parser = argparse.ArgumentParser(description="Namakan Cold Email Execution Engine")
    sub = parser.add_subparsers(dest="cmd")
    
    # List
    sub.add_parser("list", help="List all prospects")
    
    # Create
    create = sub.add_parser("create", help="Create a new prospect")
    create.add_argument("--name", help="Prospect slug (e.g. polaris)")
    create.add_argument("--company", required=True, help="Company name")
    create.add_argument("--contact", required=True, help="Contact name")
    create.add_argument("--email", required=True, help="Contact email")
    create.add_argument("--title", help="Contact title")
    create.add_argument("--industry", help="Industry")
    create.add_argument("--opportunity", help="AI opportunity")
    create.add_argument("--data", help="Proprietary data description")
    create.add_argument("--notes", help="Additional notes")
    create.add_argument("--phone", help="Phone number")
    create.add_argument("--linkedin", help="LinkedIn URL")
    
    # Generate
    gen = sub.add_parser("generate", help="Generate next email for a prospect")
    gen.add_argument("name", help="Prospect name")
    gen.add_argument("--num", type=int, choices=[1,2,3,4,5], help="Generate specific email number")
    
    # Send / Advance
    advance = sub.add_parser("advance", help="Advance sequence (mark email sent)")
    advance.add_argument("name", help="Prospect name")
    
    # Mark replied
    replied = sub.add_parser("replied", help="Mark prospect as replied")
    replied.add_argument("name", help="Prospect name")
    
    # Convert
    converted = sub.add_parser("converted", help="Mark prospect as converted")
    converted.add_argument("name", help="Prospect name")
    
    # Close
    close = sub.add_parser("close", help="Close a prospect")
    close.add_argument("name", help="Prospect name")
    close.add_argument("--reason", default="no reply", help="Reason for closing")
    
    # Status
    status_p = sub.add_parser("status", help="Show prospect status")
    status_p.add_argument("name", help="Prospect name")
    
    args = parser.parse_args()
    
    if args.cmd == "list":
        list_prospects()
    
    elif args.cmd == "create":
        add_prospect_from_args(args)
    
    elif args.cmd == "generate":
        prospect = load_prospect(args.name)
        if not prospect:
            print(f"ERROR: Prospect '{args.name}' not found")
            sys.exit(1)
        
        if args.num:
            seq = next((s for s in SEQUENCE if s["num"] == args.num), None)
            if not seq:
                print(f"ERROR: Invalid email number {args.num}")
                sys.exit(1)
        else:
            # Find next email to send
            current_day = prospect.get("sequence_day", 0)
            seq = None
            for s in SEQUENCE:
                if s["day"] > current_day:
                    seq = s
                    break
            if not seq:
                print("Sequence complete!")
                sys.exit(0)
        
        subject, body = print_email(seq, prospect)
        
        # Save to file for review (prospects stored as flat JSON, not directories)
        out_dir = os.path.join(PROSPECTS_DIR, "drafts")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{args.name}-email-{seq['num']}-{datetime.now().strftime('%Y%m%d')}.txt")
        with open(out_path, "w") as f:
            f.write(f"Subject: {subject}\n\n")
            f.write(body)
        print(f"\nDraft saved to: {out_path}")
    
    elif args.cmd == "advance":
        advance_sequence(args.name)
    
    elif args.cmd == "replied":
        mark_replied(args.name)
    
    elif args.cmd == "converted":
        mark_converted(args.name)
    
    elif args.cmd == "close":
        close_prospect(args.name, args.reason)
    
    elif args.cmd == "status":
        p = load_prospect(args.name)
        if not p:
            print(f"ERROR: Prospect '{args.name}' not found")
            sys.exit(1)
        print(f"\n{p['company']} — {p['contact_name']} ({p['contact_title']})")
        print(f"  Email: {p['contact_email']}")
        print(f"  Status: {p['sequence_status']}")
        print(f"  Sequence day: {p['sequence_day']}")
        print(f"  Last email: {p.get('last_email_sent', 'none')}")
        print(f"  Last contact: {p.get('last_contact', 'never')}")
        print(f"  Emails sent: {len(p.get('emails_sent', []))}")
        print(f"  Notes: {p.get('notes', '')}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
