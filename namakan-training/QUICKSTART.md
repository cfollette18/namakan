# Kaizen-Namakan: Quick Start Guide

## Option 1: Ollama + RAG (Fastest - Do Today)

Use Ollama with RAG to augment Llama with Namakan docs:

```bash
# 1. Install Ollama (if not already)
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull base model
ollama pull llama3.3:70b

# 3. Install RAG tools
pip install langchain langchain-community chromadb

# 4. Index Namakan docs
python3 index_docs.py

# 5. Run augmented model with LangChain RAG
#    (create rag_server.py using index_docs.py output + LangChain + Ollama)
```

## Option 2: Fine-tune with Axolotl (Production)

For best results, fine-tune on the dataset:

```bash
# 1. Install Axolotl
pip install axolotl

# 2. Configure (see config/finetune.yaml)

# 3. Launch training (needs 40GB+ VRAM)
accelerate launch config/finetune.yaml

# 4. Merge LoRA weights
python -m axolotl.cli.merge_lora ./models/kaizen-namakan-v1

# 5. Create Ollama model
ollama create kaizen-namakan -f Modelfile
```

## Option 3: Use as Kaizen's Context (No Training Needed)

Even without fine-tuning, Kaizen can use these docs as context:

```
System: When answering questions about Namakan, 
refer to /workspace/namakan/**/*.md files.
```

## Files Included

- `training_examples.jsonl` - 323 training examples
- `test_examples.jsonl` - 36 test examples  
- `prepare_data.py` - Data preparation script
- `Modelfile` - Ollama model definition
- `config/finetune.yaml` - Axolotl fine-tune config
- `index_docs.py` - RAG indexing script
- `rag_server.py` - RAG server for Ollama

## Next Steps

1. Run `python3 prepare_data.py` to regenerate data
2. Choose approach above
3. Deploy and test

## Questions?

See Namakan team docs at: namakan/teams/
