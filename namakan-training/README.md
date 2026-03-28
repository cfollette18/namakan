# Training Data Preparation

This directory contains scripts to prepare training data for the Kaizen-Namakan model.

## Data Sources

1. **Namakan Business Docs** (~436KB)
   - Teams structure
   - Pipelines
   - Sales playbook
   - Legal docs
   - Marketing materials
   - Business plans

2. **Kaizen Workspace** (for operational patterns)
   - How to handle tasks
   - Team delegation
   - Memory management
   - Autonomy patterns

## Dataset Format

We use instruction-tuning format:

```json
{
  "instruction": "What team should handle customer service automation?",
  "input": "",
  "output": "The Product Pipeline team with the Customer Service Pipeline sub-team specializes in autonomous customer service agents including FAQ Agent, Return Processing Agent, and Booking Agent."
}
```

## Files

- `prepare_data.py` - Script to process .md files into training examples
- `training_examples.jsonl` - Generated training data
- `test_examples.jsonl` - Test set

## Run Preparation

```bash
cd /home/cfollette18/.openclaw/workspace/namakan/namakan-training
python3 prepare_data.py
```

## Training

```bash
# Using Axolotl
accelerate launch config/finetune.yaml

# Or using Ollama (for local)
ollama create kaizen-namakan -f ./Modelfile
```
