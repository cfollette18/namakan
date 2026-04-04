# Fine-Tuned Models — Engagement Pipeline

*Namakan AI Engineering — Service Offering #1*

---

## The Offering

We build custom AI models fine-tuned on a client's proprietary data — contracts, policies, historical decisions, taxonomies, and approved responses. The result: an AI that thinks like their business, not like generic internet priors.

---

## Engagement Pipeline

```
Discovery → Data Assessment → Secure Intake → Training → Evaluation → Deployment → Monitoring
```

---

### Phase 1: Discovery

**Discovery Call (60 min)**
- What decisions does AI need to make that generic AI currently gets wrong?
- What proprietary knowledge exists only in people's heads?
- What data volumes are available? (contracts, tickets, CRM notes, SOPs)
- Who are the power users whose judgment we should train on?
- Current AI tooling and what's failing?

**Data Audit Framework**
```
ASSET INVENTORY:
- Document types: contracts, policies, manuals, playbooks?
- Volume: # of documents, # of pages, # of decisions captured
- Quality signals: structured labels, outcomes, approved responses?
- Gaps: what's missing that would improve the model?

STAKEHOLDER MAPPING:
- Who has the best judgment? (these become training sources)
- Who will use the model daily?
- Who signs off on training quality?
```

**Discovery Output**
- Data asset inventory with quality assessment
- Top 3 model use cases ranked by ROI
- Training data candidate list
- Ballpark: $5K–$15K depending on scope

---

### Phase 2: Data Assessment

See [../workflows/data_pipeline.py](../workflows/data_pipeline.py) for the intake workflow.

**Assessment Criteria**
| Factor | Score | Implication |
|--------|-------|-------------|
| Document volume | 1-5 | Affects training time and approach |
| Labeled examples | 1-5 | High labels = better evaluation metrics |
| Expert annotation available | Yes/No | Enables preference learning |
| PII present | Yes/No | Requires redaction pipeline |
| Multi-domain content | Yes/No | May need domain splitting |

**Output:** Data Assessment Report → go/no-go on training

---

### Phase 3: Secure Intake

See [SECURE-DATA-PIPELINE.md](./SECURE-DATA-PIPELINE.md)

All client data handled via signed URL transfer only. No third-party uploads. PII redacted before training.

---

### Phase 4: Training

See [../workflows/training_pipeline.py](../workflows/training_pipeline.py)

**Training Approach:**
- Base model: Qwen2.5-7B-Instruct (default), up to 72B depending on budget
- Method: LoRA/QLoRA (low-rank adaptation — no full fine-tune needed)
- Environment: Google Colab (T4 GPU available free tier)
- Monitoring: Live loss curves, perplexity tracking per epoch

**Training Phases:**
1. Data formatting → conversation pairs or instruction pairs
2. Hyperparameter sweep (rank, learning rate, epoch count)
3. Training run with checkpointing
4. Best checkpoint selection based on eval loss

---

### Phase 5: Evaluation

See [../workflows/evaluation_pipeline.py](../workflows/evaluation_pipeline.py)

**Evaluation Metrics:**
- Perplexity on held-out test set
- Accuracy on structured decision tasks
- Red-teaming: does it hallucinate on out-of-distribution queries?
- Business-specific: does it match approved language and tone?

**Evaluation Output:** Model Report Card with pass/fail on each metric

---

### Phase 6: Deployment

See [../workflows/deployment_pipeline.py](../workflows/deployment_pipeline.py)

**Deployment Options:**
- **Client infra:** Ollama on their machines (no data leaves)
- **Namakan cloud:** Dedicated endpoint, client owns the model
- **API integration:** FastAPI wrapper for enterprise systems

---

### Phase 7: Monitoring

**Post-deployment checks:**
- Query volume and latency
- Error rate on out-of-distribution inputs
- User satisfaction (thumbs up/down on outputs)
- Drift detection: is model quality degrading over time?

**Maintenance:**
- Retrain quarterly on new labeled examples
- Monitor for concept drift in response quality

---

## Deliverables

1. **Trained model** (LoRA adapter + base model reference)
2. **Training report** (data used, hyperparameters, loss curves)
3. **Evaluation report** (metrics, red-teaming results)
4. **Deployment artifacts** (Ollama modelfile or FastAPI service)
5. **Runbook** (how to retrain, how to monitor)

---

## Pricing

| Tier | Training Data | Base Model | Timeline | Price |
|------|---------------|------------|----------|-------|
| **SMB** | 500–5K examples | Qwen / Llama 3B–7B | 4–8 weeks | $5K–$15K |
| **Mid-Market** | 5K–20K examples | Llama 8B–13B | 8–12 weeks | $15K–$25K |
| **Enterprise** | 20K+ examples | Llama 70B or multimodal | 12–16 weeks | $25K–$40K |

**Quarterly retraining:** $500–$2,500/quarter (scales with new data volume)
*See [service-offerings.md](../../namakan-business/service-offerings.md) for full pricing details.*

---

## Timeline

```
SMB (4–8 weeks):
  Week 1–2:    Discovery + Data Assessment + Secure Intake
  Week 3–4:    Data Pipeline + Training Run
  Week 5–6:    Evaluation + QA + Deployment
  Week 7–8:    Monitoring Setup + Handoff

Mid-Market (8–12 weeks): + discovery depth, larger dataset processing, additional evaluation rounds
Enterprise (12–16 weeks): + multimodal components, larger model licensing, extended UAT
```