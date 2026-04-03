# Namakan AI — Business Model

**Version:** 2.0 (April 2026)  
**Focus:** Fine-Tuning First, Agentic Expansion

---

## Core Business Model

### The Sequence

Every client engagement starts with **fine-tuning** and expands into **agentic services**.

```
1. Fine-Tuning ($2.5K–$10K)
       ↓
   [Client gets trained model]
       ↓
2. Add Hosting ($200–400/mo)
       ↓
3. Add Retraining ($500–2.5K/quarter)
       ↓
4. Add Workflows ($5K–$20K)
       ↓
5. Add AI Employees ($2K–4K/mo)
```

**Key insight:** Fine-tuning is the beachhead. Agents are the upsell.

---

## Revenue Streams

### 1. Initial Training (One-Time)
| Tier | Price | Margin |
|------|-------|--------|
| Starter | $2,500 | ~85% |
| Professional | $5,000 | ~85% |
| Enterprise | $10,000 | ~85% |

**Cost drivers:**
- n8n setup (2–4 hours @ $0 if self-hosted)
- Data cleaning (4–8 hours @ Clint's time)
- Colab training ($0–$10 for Pro)
- Model delivery (~1 hour)

**Clint's time per project:** 10–20 hours  
**Effective hourly rate:** $250–$500/hr

### 2. Hosting MRR (Recurring)
| Tier | Price | Cost | Margin |
|------|-------|------|--------|
| API Standard | $200/mo | $50/mo | 75% |
| API Performance | $400/mo | $100/mo | 75% |

**Cost:** Dedicated GPU VM (Lambda Labs, RunPod, or similar)  
**Per client cost:** ~$50–100/mo at scale

### 3. Retraining NRR (Quarterly)
| Tier | Price | Margin |
|------|-------|--------|
| Light | $500 | ~90% |
| Standard | $1,000 | ~90% |
| Heavy | $2,500 | ~90% |

**Cost:** Mostly Clint's time (2–4 hours) + Colab ($0)  
**Frequency:** Every quarter, keeps model fresh, prevents churn

### 4. Agentic Workflows (One-Time + Upsell)
| Tier | Price | Margin |
|------|-------|--------|
| Starter | $5,000 | ~80% |
| Professional | $10,000 | ~80% |
| Enterprise | $20,000 | ~80% |

**Requires:** Fine-tuning completed first  
**Upsell rate target:** 50% of fine-tuning clients

### 5. Custom AI Employees (Recurring)
| Tier | Price | Margin |
|------|-------|--------|
| Standard | $2,000/mo | ~70% |
| Senior | $4,000/mo | ~70% |

**Requires:** Fine-tuning + agentic workflow  
**Upsell rate target:** 30% of agentic workflow clients

---

## Client Value Journey

### Year 1 Economics (Target Client)

```
MONTH 1: Initial Training
  Revenue:  $2,500
  Cost:      ~$500
  Margin:    ~$2,000

MONTH 3: Add Hosting
  MRR:       +$200/mo
  Revenue:  +$200

MONTH 6: Add Retraining (Q1)
  Revenue:  +$500

MONTH 9: Add Retraining (Q2)
  Revenue:  +$500

MONTH 12: Add Retraining (Q3)
  Revenue:  +$500
  Hosting:  +$2,400 (12 months)

YEAR 1 TOTAL: $6,600
MRR BY MONTH 12: $200
```

### Expanded Client Economics

```
SCENARIO: Full Expansion (Training + Hosting + Retraining + Workflow + Employee)

Initial Training:      $5,000
Retraining (4x):       $4,000
Hosting (12x):         $2,400
Agentic Workflow:      $10,000
AI Employee (12x):     $24,000
─────────────────────────────
YEAR 1 TOTAL:         $45,400
MRR AT END:           $2,200

COST:                 ~$8,000 (mostly Clint time)
NET PROFIT YEAR 1:    ~$37,400
```

---

## Unit Economics

| Metric | Current | Target |
|--------|---------|--------|
| Avg Initial Training | — | $5,000 |
| Avg MRR per Client | — | $800 |
| Gross Margin (Training) | — | 85% |
| Gross Margin (Hosting) | — | 75% |
| Gross Margin (Agents) | — | 70% |
| Clint Hours per Training | — | 15 hrs |
| Effective Hourly Rate | — | $300+ |
| Sales Cycle | — | 2–4 weeks |

---

## Cost Structure

### Fixed Costs (Monthly)
| Item | Cost |
|------|------|
| n8n hosting (localhost) | $0 |
| Domain (namakanai.com) | $0 |
| Email (clint@namakanai.com) | $0 |
| Vercel (frontend) | $0 |
| **Total Fixed** | **$0** |

### Variable Costs (Per Client)

**Hosting:**
- Shared GPU VM: $50–100/client/mo
- At 10 clients: $500–1,000/mo

**Training:**
- Colab: $0–10/client
- Clint time: 15 hrs/client

### Break-Even

**Minimum:** 1 training project/month = $2,500 revenue  
**Comfortable:** 2 projects/month = $5,000+ revenue  
**MRR Target:** $3K–5K MRR from hosting + employees

---

## Growth Model

### Phase 1: Foundation (Q2 2026)
- Land 3–5 initial training clients
- Prove the process works
- Refine n8n workflows
- Build case studies

**Target:** $15K–$30K revenue in Q2

### Phase 2: Add Recurring (Q3–Q4 2026)
- Convert training clients to hosting
- Upsell 2–3 to agentic workflows
- Add 1–2 AI employees
- Build referral engine

**Target:** $5K MRR by end of 2026

### Phase 3: Scale (2027)
- 10–15 active clients
- $15K–$25K MRR
- Hire part-time technical help
- Expand to new verticals

**Target:** $200K–$400K ARR

---

## Competitive Positioning

### Against Enterprise AI Firms
- **Us:** $2.5K–$10K, 1–4 weeks, Colab-based
- **Them:** $100K+, 6+ months, custom infrastructure
- **Our Advantage:** Fast, cheap, proven stack

### Against DIY / No-Code Tools
- **Us:** We do the work, you get the model
- **Them:** You figure it out yourself
- **Our Advantage:** Done-for-you, not DIY

### Against Freelancers
- **Us:** Professional contracts, recurring, accountable
- **Them:** Unreliable, no SLA, single-project
- **Our Advantage:** MRR relationship, continuous support

---

## Risk Factors

| Risk | Mitigation |
|------|------------|
| Colab pricing changes | Build alternative (Lambda, RunPod) into pricing |
| Client churn | Quarterly retraining keeps us relevant |
| Competition | Focus on niche (manufacturing, professional services) |
| Clint burnout | Document processes, hire help at 10+ clients |
| Data security | Clear protocols, NDA-first approach |

---

## Key Performance Indicators (KPIs)

| KPI | Q2 Target | Q4 Target | 2027 Target |
|-----|-----------|-----------|-------------|
| Clients | 3–5 | 8–12 | 15–25 |
| MRR | $500 | $3K–$5K | $15K–$25K |
| ARR | $10K | $30K–$50K | $200K–$400K |
| Avg Client Revenue | $4K | $6K | $12K |
| Clint Utilization | 50% | 70% | 60% |

---

## Operations

### Delivery Process (2–4 weeks)

```
Week 1: Data Connection
  - Client grants read access (Salesforce, DB, files)
  - n8n workflow pulls sample data
  - Review and approve training set

Week 2: Data Cleaning + Training
  - PII removal and formatting
  - Trigger Colab training (~45 min)
  - Notify when complete

Week 3: Delivery + Testing
  - Deliver .gguf model file
  - Client tests on sample cases
  - Approve or iterate

Week 4: Expand (Optional)
  - Propose hosting
  - Design agentic workflow
  - Quote AI employee
```

### Tools

| Tool | Use | Cost |
|------|-----|------|
| n8n | Data connectors, automation | $0 |
| Google Colab | Model training | $0–10 |
| Ollama | Local inference | $0 |
| Telegram | Client notifications | $0 |
| Vercel | Frontend hosting | $0 |
| GitHub | Code and doc storage | $0 |

---

## Strategic Priorities

### 1. Nail the Fine-Tuning Process
- Document every step
- Build reusable n8n templates
- Prove ROI with case studies

### 2. Land First 5 Clients
- Target: Manufacturing + professional services
- Minneapolis market first
- Referral-based acquisition

### 3. Build Recurring Revenue
- Convert every client to hosting
- Upsell workflows and employees
- Quarterly touchpoints (retraining)

### 4. Develop Expertise
- Own "fine-tuning for manufacturing"
- Build vertical-specific playbooks
- Create case studies and testimonials

---

## 3-Year Vision

**Year 1:** Prove the model, land 10 clients, hit $50K revenue  
**Year 2:** Scale to 25 clients, $200K revenue, hire help  
**Year 3:** $500K–$1M revenue, team of 3–5, regional leader in custom AI engineering

---

## Appendix: Pricing at a Glance

| Service | One-Time | Recurring |
|---------|----------|-----------|
| Fine-Tuning | $2,500–$10,000 | — |
| Hosting | — | $200–$400/mo |
| Retraining | $500–$2,500 | — |
| Agentic Workflow | $5,000–$20,000 | — |
| AI Employee | — | $2,000–$4,000/mo |

**Typical Client Year 1:** $5K–$45K depending on expansion depth
