# Fine-Tuned Models Workflow

## Overview
Connect to your existing data sources → Clean and structure the data → Train a custom 8B model that actually knows your business.

## The Differentiator
Most AI companies start with your documents. We start with your data sources — CRM, database, documents — and build the model from your live data.

## Workflow Steps

### 1. Data Source Connection
- Connect to CRM (Salesforce, HubSpot, custom)
- Connect to database (PostgreSQL, MySQL, etc.)
- Connect to document storage (S3, SharePoint, local files)
- Export historical data (tickets, emails, contracts)
- API access or data export + transfer

**Output:** Connected data sources

### 2. Data Cleaning & Structuring
- Extract and parse all data formats (JSON, CSV, PDF, DOCX, etc.)
- Remove PII/sensitive data
- Deduplicate and normalize
- Structure into training format (conversational Q&A pairs)
- Create validation set (10-20% of data)

**Output:** Clean training dataset + validation dataset

### 3. Model Training
- Choose base model (Qwen2.5-8B or similar)
- Configure LoRA (r=16, lora_alpha=32)
- Train on your cleaned data
- Monitor loss curves and validation metrics
- Early stop if overfitting

**Output:** Trained 8B model adapter

### 4. Evaluation
- Run eval pipeline on held-out validation set
- Human review of sample outputs
- Compare against baseline (generic AI)
- Measure accuracy, relevance, brand voice

**Output:** Eval report with metrics

### 5. Deployment
- Deploy model to your infrastructure (Ollama, FastAPI)
- Set up inference endpoint
- Configure monitoring and logging
- Optional: run alongside generic AI for comparison

**Output:** Production 8B model endpoint

### 6. Iteration
- Gather user feedback
- Monitor quality metrics
- Retrain monthly or when data changes significantly

---

## Timeline
- **Total:** 2-3 weeks
- Data Connection: 3-5 days
- Data Cleaning: 3-5 days
- Training: 1-2 days
- Eval + Deploy: 2-3 days
- Buffer: 3-5 days

## Pricing
- Starting at $15K
- Includes data connection, cleaning, training, and deployment

## Technical Stack
- Data: Custom connectors for CRM/DB/file sources
- Training: Ollama + Axolotl, or cloud GPU
- Base model: Qwen2.5-8B (efficient, runs on modest hardware)
- LoRA: QLoRA for efficient fine-tuning
- Inference: Ollama server or custom FastAPI
