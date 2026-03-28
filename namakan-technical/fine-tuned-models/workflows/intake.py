#!/usr/bin/env python3
"""
Client Intake — Fine-Tuned Models Pipeline
Runs discovery questions, generates config, and sets up the project directory.
Usage: python3 intake.py --client "Acme Corp" --output ./clients/acme
"""
import argparse
import json
import os
import sys
from datetime import datetime

QUESTIONS = [
    {
        "id": "company",
        "question": "What is the client's company name?",
        "required": True,
        "type": "text"
    },
    {
        "id": "industry",
        "question": "What industry are they in?",
        "required": True,
        "type": "text"
    },
    {
        "id": "use_case",
        "question": "What specific task should the AI help with?",
        "required": True,
        "type": "textarea"
    },
    {
        "id": "data_available",
        "question": "How much training data do they have? (files count, approximate size)",
        "required": True,
        "type": "textarea"
    },
    {
        "id": "data_format",
        "question": "What format is their data in? (JSONL, CSV, PDFs, plain text, etc.)",
        "required": True,
        "type": "select",
        "options": ["JSONL (instruction/output pairs)", "CSV", "PDF documents", "Plain text files", "Not sure yet"]
    },
    {
        "id": "base_model",
        "question": "Preferred base model? (or say 'your recommendation')",
        "required": False,
        "type": "select",
        "options": ["Qwen/Qwen2.5-7B-Instruct", "Qwen/Qwen2.5-3B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3", "meta-llama/Llama-3.1-8B-Instruct", "Your recommendation"]
    },
    {
        "id": "security",
        "question": "Any compliance requirements? (HIPAA, GDPR, SOC 2, none)",
        "required": False,
        "type": "text"
    },
    {
        "id": "deployment",
        "question": "Where should the model be deployed? (client infra, Namakan cloud, hybrid)",
        "required": True,
        "type": "select",
        "options": ["Client's own infrastructure", "Namakan hosted (monthly subscription)", "Hybrid (training on Namakan, deploy to client")]
    },
    {
        "id": "budget",
        "question": "What budget have they indicated?",
        "required": False,
        "type": "text"
    },
    {
        "id": "timeline",
        "question": "When do they need this live?",
        "required": False,
        "type": "text"
    },
    {
        "id": "success_metric",
        "question": "How will we know the model is 'good enough'? (accuracy %, human eval, specific test cases)",
        "required": True,
        "type": "textarea"
    },
    {
        "id": "contacts",
        "question": "Primary contact name and email?",
        "required": True,
        "type": "text"
    }
]

def ask_question(q):
    print(f"\n{'='*60}")
    print(f"  {q['question']}")
    print(f"{'='*60}")
    if q.get('options'):
        for i, opt in enumerate(q['options'], 1):
            print(f"  {i}. {opt}")
    
    required_marker = " (REQUIRED)" if q.get('required') else " (optional)"
    while True:
        prompt = f"\n>>> {q['id']}{required_marker}: "
        answer = input(prompt).strip()
        if q.get('required') and not answer:
            print("  ⚠️  This field is required.")
            continue
        if q.get('options') and answer.isdigit():
            idx = int(answer) - 1
            if 0 <= idx < len(q['options']):
                answer = q['options'][idx]
        break
    return answer

def generate_config(answers):
    """Generate training config from answers."""
    # Estimate LoRA config based on data size
    data_size = answers.get("data_available", "").lower()
    
    # Parse data size estimate
    import re
    mb_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mb|gb)', data_size.lower())
    files_match = re.search(r'(\d+)\s*(?:files?|docs?|examples?|records?)', data_size.lower())
    
    if mb_match:
        size_gb = float(mb_match.group(1)) / 1000 if 'mb' in mb_match.group(0) else float(mb_match.group(1))
    else:
        size_gb = 1.0
    
    if files_match:
        num_files = int(files_match.group(1))
    else:
        num_files = 100
    
    # Size-based config
    if size_gb > 5 or num_files > 10000:
        lora_r = 32
        epochs = 5
        batch_size = 4
    elif size_gb > 1 or num_files > 1000:
        lora_r = 16
        epochs = 3
        batch_size = 2
    else:
        lora_r = 8
        epochs = 3
        batch_size = 2
    
    # Model selection
    model = answers.get("base_model", "")
    if "recommendation" in model.lower() or not model:
        if size_gb > 2:
            model = "Qwen/Qwen2.5-7B-Instruct"
        else:
            model = "Qwen/Qwen2.5-3B-Instruct"
    
    return {
        "client": answers.get("company", "unknown"),
        "industry": answers.get("industry", ""),
        "use_case": answers.get("use_case", ""),
        "base_model": model,
        "training": {
            "lora_r": lora_r,
            "lora_alpha": lora_r * 2,
            "lora_dropout": 0.05,
            "epochs": epochs,
            "batch_size": batch_size,
            "grad_accumulation_steps": 8,
            "learning_rate": 2e-4,
            "max_seq_length": 512,
            "warmup_steps": 10,
            "early_stopping_patience": 2
        },
        "deployment": answers.get("deployment", ""),
        "security": answers.get("security", "none"),
        "budget": answers.get("budget", ""),
        "timeline": answers.get("timeline", ""),
        "success_metric": answers.get("success_metric", ""),
        "contacts": answers.get("contacts", ""),
        "data_format": answers.get("data_format", ""),
        "intake_date": datetime.now().isoformat(),
        "status": "discovery_complete"
    }

def create_client_directory(output_dir, client_slug, config):
    """Create client project directory structure."""
    client_dir = os.path.join(output_dir, client_slug)
    
    dirs = [
        client_dir,
        f"{client_dir}/data/raw",
        f"{client_dir}/data/prepared",
        f"{client_dir}/data/val",
        f"{client_dir}/adapters",
        f"{client_dir}/outputs",
        f"{client_dir}/colab",
        f"{client_dir}/tests",
        f"{client_dir}/docs",
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # Write config
    config_path = f"{client_dir}/config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    # Write status file
    status = {
        "client": config["client"],
        "status": "discovery_complete",
        "pipeline": "fine-tuned-models",
        "created": datetime.now().isoformat(),
        "phases": {
            "discovery": "complete",
            "data_preparation": "pending",
            "training": "pending",
            "evaluation": "pending",
            "deployment": "pending"
        }
    }
    with open(f"{client_dir}/status.json", "w") as f:
        json.dump(status, f, indent=2)
    
    # Write README
    readme = f"""# {config['client']} — Fine-Tuned Model Project

**Industry:** {config['industry']}
**Use Case:** {config['use_case']}
**Base Model:** {config['base_model']}
**Deployment:** {config['deployment']}
**Intake Date:** {config['intake_date']}

## Directory Structure

```
{client_slug}/
├── config.json        # Training configuration
├── status.json        # Project status tracker
├── data/
│   ├── raw/          # Raw client data (SECURE — delete after prep)
│   ├── prepared/      # Processed training data
│   └── val/          # Validation set
├── adapters/          # Trained LoRA adapters
├── outputs/          # Final model outputs
├── colab/            # Colab notebooks
├── tests/            # Evaluation benchmarks
└── docs/             # Project documentation
```

## Pipeline Phases

- [x] Discovery
- [ ] Data Preparation
- [ ] Training
- [ ] Evaluation
- [ ] Deployment

## Next Steps

1. Receive data via S3 signed URL → save to `data/raw/`
2. Run `../workflows/data_pipeline.py --input data/raw --output data/prepared`
3. Generate Colab notebook: `../colab/generate_colab.py --client "{config['client']}" --model "{config['base_model']}" --train data/prepared/train.jsonl`
4. Upload Colab notebook to Google Drive, share with client
5. Run training in Colab
6. Evaluate with `../workflows/evaluation_pipeline.py --adapter adapters/final`
7. Deploy with `../workflows/deployment_pipeline.py --adapter adapters/final --method [ollama|vllm|fastapi]`
"""
    with open(f"{client_dir}/README.md", "w") as f:
        f.write(readme)
    
    return client_dir

def main():
    parser = argparse.ArgumentParser(description="Namakan Fine-Tuned Models — Client Intake")
    parser.add_argument("--client", help="Client company name (skip interactive if provided)")
    parser.add_argument("--output", default="./clients", help="Output directory for client projects")
    parser.add_argument("--non-interactive", action="store_true", help="Use defaults for optional fields")
    args = parser.parse_args()
    
    print("="*60)
    print("  NAMAKAN — Fine-Tuned Models Client Intake")
    print("="*60)
    print()
    
    answers = {}
    
    # Pre-fill if client name provided
    if args.client:
        answers["company"] = args.client
    
    # Interactive questions
    for q in QUESTIONS:
        if args.non_interactive and not q.get("required"):
            answers[q["id"]] = ""
            continue
        # Skip company if already provided
        if q["id"] == "company" and args.client:
            answers["company"] = args.client
            continue
        answers[q["id"]] = ask_question(q)
    
    # Generate config
    config = generate_config(answers)
    
    # Create client slug
    client_slug = config["client"].lower().replace(" ", "-").replace(",", "")
    
    # Create directory
    client_dir = create_client_directory(args.output, client_slug, config)
    
    print(f"\n{'='*60}")
    print(f"  ✅ INTAKE COMPLETE — {config['client']}")
    print(f"{'='*60}")
    print(f"\n  Project directory: {client_dir}")
    print(f"  Config: {client_dir}/config.json")
    print(f"  README: {client_dir}/README.md")
    print(f"\n  Suggested next step:")
    print(f"  python3 workflows/data_pipeline.py --input {client_dir}/data/raw --output {client_dir}/data/prepared")
    print()
    
    # Print config summary
    print("  Config summary:")
    print(f"    Base model: {config['base_model']}")
    print(f"    LoRA R: {config['training']['lora_r']}")
    print(f"    Epochs: {config['training']['epochs']}")
    print(f"    Deployment: {config['deployment']}")
    print()

if __name__ == "__main__":
    main()
