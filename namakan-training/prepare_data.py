#!/usr/bin/env python3
"""
Kaizen-Namakan Training Data Generator

Processes Namakan documentation into instruction-tuning examples
for fine-tuning a specialized business operations model.
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict

# Configuration
NAMAKAN_ROOT = "/home/cfollette18/.openclaw/workspace/namakan"
KAIZEN_ROOT = "/home/cfollette18/.openclaw/workspace"
OUTPUT_FILE = "/home/cfollette18/.openclaw/workspace/namakan/namakan-training/training_examples.jsonl"
TEST_FILE = "/home/cfollette18/.openclaw/workspace/namakan/namakan-training/test_examples.jsonl"

# Domain configurations
DOMAINS = {
    "teams": {
        "path": "teams",
        "description": "AI agent teams and their specializations",
        "examples": [
            {
                "instruction": "What teams does Namakan have for building AI agents?",
                "output": "Namakan has 8 teams: Product Pipeline (9 pipelines), Customer Service, Lead Qualification, Document Processing, Social Media, Meeting Agents, Internal LLM, and Autonomous Agents. Each team specializes in specific AI automation domains."
            },
            {
                "instruction": "Which team handles customer service automation?",
                "output": "The Customer Service team handles autonomous customer service agents including FAQ Agent, Return Processing Agent, Booking Agent, Intent Classifier, and Escalation Agent."
            },
            {
                "instruction": "What is the Product Pipeline team?",
                "output": "The Product Pipeline team builds reusable AI pipelines including Customer Service, Lead Generation, Content, Operations, Data, HR, Internal LLM, RAG, and Fine-Tuning pipelines."
            }
        ]
    },
    "sales": {
        "path": "namakan-sales",
        "description": "Sales processes and playbook",
        "examples": [
            {
                "instruction": "What is Namakan's sales playbook?",
                "output": "Namakan's sales playbook includes: 30 cold call scripts, 5-email cold email sequence, LinkedIn outreach templates, lead qualification checklist (BANT), and objection handling guide (top 10 objections)."
            },
            {
                "instruction": "How do I qualify a lead?",
                "output": "Use the qualification checklist: Budget ($500-5K/mo target), Authority (decision maker?), Timeline (<60 days ideal), Need (clear pain point?). Score 18+/25 = strong fit."
            }
        ]
    },
    "legal": {
        "path": "namakan-legal",
        "description": "Legal documents and contracts",
        "examples": [
            {
                "instruction": "What legal documents does Namakan have?",
                "output": "Namakan has: Operating Agreement, Master Service Agreement, Statement of Work, Mutual NDA, One-Way NDA, Liability Waiver, Contract Terms, and Client Onboarding form."
            },
            {
                "instruction": "What are Namakan's payment terms?",
                "output": "50% upfront, 50% on delivery. Liability capped at fees paid. 14-day termination notice. Client owns data, Namakan owns tools/frameworks."
            }
        ]
    },
    "business": {
        "path": "namakan-business",
        "description": "Business plans and strategy",
        "examples": [
            {
                "instruction": "What is Namakan's business model?",
                "output": "Namakan builds AUTONOMOUS AI AGENTS for local businesses. Revenue: Monthly agent subscriptions ($500-5K/mo) + Implementation fees ($2K-25K). Focus on Blaine, MN SMBs."
            },
            {
                "instruction": "What are Namakan's pricing tiers?",
                "output": "Starter Agent: $500-1.5K/mo, Growth Suite: $1.5-3.5K/mo, Enterprise Workforce: $3.5-5K/mo. Project pricing: Single Agent $2-5K, Multi-Agent $5-15K, Full Automation $15-25K."
            }
        ]
    },
    "technical": {
        "path": "namakan-technical",
        "description": "Technical workflows and AI systems",
        "examples": [
            {
                "instruction": "What AI workflows does Namakan recommend?",
                "output": "Common workflows: Customer Service (classify → route → agent → act → confirm), Lead Qualification (enrich → score → route → nurture → close), Document Processing (classify → extract → validate → store), Social Media (plan → generate → review → post → monitor), Meeting Summarization (transcribe → summarize → distribute → follow-up)."
            },
            {
                "instruction": "What stack does Namakan use?",
                "output": "LangChain/LangGraph/CrewAI for agents, Temporal/Airflow for workflows, Claude/GPT-4/Ollama for LLMs, Pinecone/Weaviate for vector DB, Docker/Kubernetes for deployment."
            }
        ]
    }
}

def extract_content_sections(md_content: str, filename: str) -> List[str]:
    """Extract meaningful sections from markdown files."""
    sections = []
    
    # Split by headers
    parts = re.split(r'^#{1,6}\s+', md_content, flags=re.MULTILINE)
    
    for part in parts[1:]:  # Skip first empty part
        lines = part.strip().split('\n')
        title = lines[0].strip()
        content = ' '.join(lines[1:]).strip()
        
        if len(content) > 50:  # Skip very short sections
            sections.append(f"{title}: {content[:500]}")
    
    return sections

def generate_qa_pairs(section: str, domain: str) -> List[Dict]:
    """Generate question-answer pairs from content sections."""
    pairs = []
    
    # Pattern-based generation
    title_match = re.match(r'^([^:]+):', section)
    if not title_match:
        return pairs
    
    title = title_match.group(1).strip()
    content = section[title_match.end():].strip()
    
    # What is / What are questions
    if title:
        pairs.append({
            "instruction": f"What is {title}?",
            "input": "",
            "output": f"{title}: {content[:400]}"
        })
    
    # How questions
    if 'process' in title.lower() or 'flow' in title.lower():
        pairs.append({
            "instruction": f"Explain the {title} process",
            "input": "",
            "output": f"The {title} process: {content[:400]}"
        })
    
    return pairs

def create_domain_examples() -> List[Dict]:
    """Create training examples from domain configs."""
    examples = []
    
    for domain, config in DOMAINS.items():
        examples.extend(config["examples"])
    
    return examples

def process_markdown_files() -> List[Dict]:
    """Process all markdown files into training examples."""
    examples = []
    
    for domain, config in DOMAINS.items():
        domain_path = os.path.join(NAMAKAN_ROOT, config["path"])
        
        if not os.path.exists(domain_path):
            continue
        
        for md_file in Path(domain_path).glob("*.md"):
            try:
                content = md_file.read_text()
                sections = extract_content_sections(content, md_file.name)
                
                for section in sections:
                    pairs = generate_qa_pairs(section, domain)
                    examples.extend(pairs)
                    
            except Exception as e:
                print(f"Error processing {md_file}: {e}")
    
    return examples

def create_kaizen_pattern_examples() -> List[Dict]:
    """Examples that teach operational patterns."""
    return [
        {
            "instruction": "How do I handle a new task from Clint?",
            "input": "",
            "output": "1. Check TASK-BOARD.md for existing tasks. 2. Check AUTONOMY.md for boundaries. 3. If clear task: execute and update board. 4. If unclear: ask clarifying questions. 5. If complex: spawn subagent. 6. Report completion."
        },
        {
            "instruction": "How do I delegate work to teams?",
            "input": "",
            "output": "1. Read TEAMS.md to identify right team. 2. Spawn subagent with task. 3. Provide clear instructions and file paths. 4. Wait for completion event. 5. Compile results. 6. Report to Clint."
        },
        {
            "instruction": "What files should I read at session start?",
            "input": "",
            "output": "At session start read in order: SOUL.md (who I am), USER.md (who I'm helping), MEMORY.md (long-term), TASK-BOARD.md (current tasks), AUTONOMY.md (boundaries), TEAMS.md (delegation), then today's memory file."
        },
        {
            "instruction": "How do I save memory for continuity?",
            "input": "",
            "output": "1. After significant actions, update memory/YYYY-MM-DD.md. 2. Use labels: [task], [conversation], [heartbeat]. 3. For important learnings, update MEMORY.md. 4. For quick recall, update knowledge graph."
        },
        {
            "instruction": "When should I spawn a subagent vs handle directly?",
            "input": "",
            "output": "Spawn subagent when: task is complex (>5 min), needs parallel execution, or requires different expertise. Handle directly when: quick task (<2 min), single step, or needs my context."
        }
    ]

def main():
    print("Generating Kaizen-Namakan training data...")
    
    all_examples = []
    
    # Domain examples from configs
    all_examples.extend(create_domain_examples())
    print(f"  Domain examples: {len(all_examples)}")
    
    # Process markdown files
    md_examples = process_markdown_files()
    all_examples.extend(md_examples)
    print(f"  Markdown examples: {len(md_examples)}")
    
    # Kaizen operational patterns
    pattern_examples = create_kaizen_pattern_examples()
    all_examples.extend(pattern_examples)
    print(f"  Pattern examples: {len(pattern_examples)}")
    
    # Split into train/test (90/10)
    import random
    random.shuffle(all_examples)
    split = int(len(all_examples) * 0.9)
    train_examples = all_examples[:split]
    test_examples = all_examples[split:]
    
    # Write train set
    with open(OUTPUT_FILE, 'w') as f:
        for ex in train_examples:
            f.write(json.dumps(ex) + '\n')
    print(f"  Wrote {len(train_examples)} training examples to {OUTPUT_FILE}")
    
    # Write test set
    with open(TEST_FILE, 'w') as f:
        for ex in test_examples:
            f.write(json.dumps(ex) + '\n')
    print(f"  Wrote {len(test_examples)} test examples to {TEST_FILE}")
    
    print(f"\nDone! Total: {len(all_examples)} examples")

if __name__ == "__main__":
    main()
