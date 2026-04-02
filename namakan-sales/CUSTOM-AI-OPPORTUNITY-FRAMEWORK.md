# Custom AI Opportunity Framework

*A structured guide for evaluating where custom AI engineering delivers the highest ROI for your organization.*

---

## The Core Question

**Generic AI knows information. Custom AI knows YOUR business.**

Before investing in custom AI, evaluate: *Do we have proprietary data that would meaningfully improve an AI's understanding of our domain?*

If yes → custom AI is likely a high-ROI investment.  
If no → a generic AI tool may be sufficient for now.

---

## Opportunity Scoring Matrix

Rate each area 1–5 for your organization.

| Factor | Score (1–5) | Notes |
|--------|-------------|-------|
| **Proprietary Data Volume** — How many years of domain-specific data do you have? | | |
| **Data Access** — Is your data searchable, structured, or at least accessible to humans? | | |
| **Domain Complexity** — Does your industry/organization have specialized terminology, workflows, or judgment calls? | | |
| **Operational Frequency** — How often does this process/workflow occur? (Higher = more ROI) | | |
| **Error Cost** — What's the consequence of a wrong answer? (Higher = more validation needed) | | |
| **Decision-Maker Urgency** — Is leadership actively trying to solve this problem? | | |
| | | |
| **TOTAL** | **/30** | |

**Scoring Key:**
- 24–30: Strong custom AI candidate — prioritize this
- 15–23: Viable candidate — do deeper discovery
- Below 15: Generic AI likely sufficient for now

---

## Where Custom AI Wins vs. Generic AI

### Generic AI Handles Well:
- General knowledge questions
- Writing first drafts of standard documents
- Simple translations
- Code snippets for common patterns
- Broad industry concepts

### Custom AI Delivers Clear Advantage When:
- The answer requires YOUR organization's specific context
- Decisions depend on proprietary data a generic model has never seen
- Speed + accuracy both matter for high-volume workflows
- The domain has specialized terminology, acronyms, or judgment standards
- Outputs must be traceable to YOUR source documents

---

## The 4 Custom AI Pipelines

### 1. Fine-Tuned Models ($5K–$40K)
**Best for:** Classification, prediction, recommendation, domain-specific generation

**Evaluates:** Do we have 500+ labeled examples of good outputs from experts in our organization?

Example: A manufacturing company fine-tuned a model on 3 years of inspection decisions made by senior quality inspectors. The model learned institutional judgment — what "good enough" looks like for their specific products — that no generic model could replicate.

**Typical ROI trigger:** 6+ months of repetitive domain-specific decisions where expertise varies or is departing.

---

### 2. RAG Pipelines ($5K–$15K build + $500/mo)
**Best for:** Question answering, document search, knowledge retrieval

**Evaluates:** Do we have a large archive of documents, records, or knowledge that would be valuable to query natural language?

Example: A legal firm built a RAG pipeline on 20 years of case outcomes, contract templates, and deal structures. Attorneys now query institutional knowledge in seconds — surfacing precedents that would take days to find manually.

**Typical ROI trigger:** Teams spend significant time searching or reading through documentation to answer common questions.

---

### 3. Agentic Workflows ($5K–$30K)
**Best for:** Multi-step processes, routing, automated decision support

**Evaluates:** Do we have multi-step workflows where human judgment is needed at some, but not all, steps?

Example: A field service organization built an agentic workflow that receives incoming service tickets, queries RAG for similar historical issues, generates a recommended resolution, and routes to the right technician — with escalation for novel problems.

**Typical ROI trigger:** A process that requires multiple systems, approvals, or data lookups that currently takes significant human time.

---

### 4. Custom AI Employees ($2K/mo)
**Best for:** Ongoing, repeatable knowledge work with consistent performance expectations

**Evaluates:** Is there a defined role with measurable outputs that could run 24/7 on our data?

Example: A compliance team deployed a Custom AI Employee that reviews incoming contracts against established playbook criteria, flags high-risk clauses, and routes for human review. The AI handles 80% of routine reviews — freeing senior counsel for complex negotiations.

**Typical ROI trigger:** A role that requires significant training time for new hires, where institutional knowledge is a constraint.

---

## Discovery Questions

Before scoping a custom AI project, clarify:

1. **What decision/problem are we trying to solve?**
2. **What data would the AI need to be accurate?**
3. **Who are the domain experts — and are they available for intake?**
4. **How will outputs be validated — and by whom?**
5. **What does "success" look like in 90 days? In 12 months?**
6. **What integration points exist — and what's the workflow in practice?**

---

## What We Handle vs. What You Handle

| | Namakan Handles | Client Handles |
|---|---|---|
| **Data Intake** | Secure transfer, ingestion pipeline | Providing data in agreed format |
| **Model Training** | Fine-tuning, evaluation, iteration | Labeling review (we guide) |
| **Integration** | API, embedding, workflow hook | IT approval, access provisioning |
| **Testing** | Unit tests, eval harness, red-teaming | User acceptance testing |
| **Deployment** | Cloud or on-prem, monitoring | Production access, change management |
| **Ongoing** | Retraining triggers, performance monitoring | Business feedback loop |

---

## Ready to Explore?

**Namakan AI Engineering**  
hello@namakan.ai  
namakanai.com

*We engineer custom AI systems built on YOUR data — not generic tools, bespoke systems for your specific domain.*
