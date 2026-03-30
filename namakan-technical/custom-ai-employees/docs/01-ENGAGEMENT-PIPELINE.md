# Custom AI Employees — Engagement Pipeline

*Namakan AI Engineering — Service Offering #4*

---

## The Offering

We deploy AI workers — autonomous agents that complete specific jobs daily without constant input. Research leads, draft emails, update CRM records, schedule follow-ups, handle tier-1 support. They work 24/7, report productivity, and escalate only when they need judgment.

---

## Engagement Pipeline

```
Discovery → Role Definition → Skill Building → Training → Deployment → Monitoring
```

---

### Phase 1: Discovery

**Discovery Call (60 min)**
- What repetitive tasks consume the most team time?
- What's the current process for this task? (step-by-step)
- Where do humans currently make judgment calls?
- What systems does this task touch? (CRM, email, calendar, docs)
- How do you measure if the task was done well?
- What's the cost of a wrong decision?

**Role Identification Framework**
```
TASK ANALYSIS:
- Frequency: How many times per day/week does this happen?
- Volume: How many records/cases/emails per occurrence?
- Repetition: Same steps, same systems, same decision points?
- Autonomy level: Can it complete without human input? Or does it need approval checkpoints?

JUDGMENT REQUIREMENTS:
- Low judgment: Rule-based, clear right/wrong → AI can do autonomously
- Medium judgment: Pattern-based, mostly clear → AI does + escalates edge cases
- High judgment: Novel situations, business-critical → AI assists, human decides

STAKEHOLDER PAIN:
- Who is doing this task today and hates it?
- What would they do with those hours back?
- What's the error cost when humans get tired/busy?
```

**Discovery Output**
- Top 3 AI employee roles identified
- ROI estimate per role
- Autonomy level assessment
- Ballpark: $2K–$5K/month per AI employee

---

### Phase 2: Role Definition

**Role Document Template:**
```markdown
# Role: [Job Title]

## Core Responsibility
One sentence describing what this employee does.

## Daily Tasks
1. [Task] — triggered by [event/time], completes [action]
2. ...

## Success Metrics
- Completion rate: >95%
- Error rate: <1%
- Escalation rate: <5%
- Time saved: X hours/week

## Systems Accessed
- CRM: [what it reads/writes]
- Email: [what it sends/reads]
- Calendar: [what it checks/creates]
- Docs: [what it references]

## Escalation Triggers
- [Condition A] → escalate to [who]
- [Condition B] → escalate to [who]
- All escalations include: context, attempted action, suggested next step

## Boundaries
- Can do: [list]
- Cannot do: [list]
- Requires approval: [list]
```

**Output:** Signed Role Document from client stakeholder

---

### Phase 3: Skill Building

**Skills define what the AI employee can do:**

```
SKILL TYPES:
- Research: Web search, company lookup, data enrichment
- Comms: Email drafting, follow-up sequences, Slack messages
- CRM: Record creation, updates, status changes, data quality
- Calendar: Scheduling, conflict detection, reminder setting
- Documents: Reading, summarizing, extracting key info

SKILL CONSTRUCTION:
- Trigger: What starts this skill? (email received, new record, schedule)
- Input: What data does the skill receive?
- Process: What steps does the skill execute?
- Output: What does the skill produce?
- Escalation: When does it hand off to a human?
```

**Tools the AI employee uses:**
- Web search (DuckDuckGo/Brave)
- Email client (Gmail API, Brevo)
- CRM (Salesforce, HubSpot, custom)
- Calendar (Google Calendar, Outlook)
- Document search (ChromaDB/RAG pipeline)

**Output:** Skill inventory with each skill documented

---

### Phase 4: Training

**Training the AI employee on client-specific context:**

```
TRAINING INPUTS:
- Company background, terminology, brand voice
- Approved templates, response language, escalation paths
- Historical examples of good outputs (labeled)
- CRM data structure, field meanings, valid values

SKILL-SPECIFIC TRAINING:
- Research: Train on ideal company profiles, data quality standards
- Comms: Train on brand voice, email templates, response patterns
- CRM: Train on data standards, taxonomy, expected field values
- Escalation: Train on boundary conditions, when to escalate

FINE-TUNING:
- Role-specific fine-tuning on client's historical data (optional)
- RAG pipeline on company knowledge base (required)
```

**Output:** Trained AI employee ready for testing

---

### Phase 5: Deployment

**Deployment Approach:**
```
PHASE 1 — Shadow Mode (1-2 weeks):
- AI employee works in parallel with human
- All outputs reviewed by human before use
- AI observes decisions, learns from corrections

PHASE 2 — Assisted Mode (1-2 weeks):
- AI completes tasks autonomously
- Human reviews final output before it goes live
- Escalations routed to human for approval

PHASE 3 — Full Autonomy (ongoing):
- AI completes tasks without human review
- Escalations only for boundary conditions
- Weekly report of productivity + exceptions
```

**Integration Points:**
- CRM webhook for new records/triggers
- Email parsing for inbound requests
- Slack bot for team communication
- API endpoint for custom integrations

---

### Phase 6: Monitoring

**AI Employee Dashboard:**
```
PRODUCTIVITY METRICS:
- Tasks completed: X per day/week
- Time saved: X hours equivalent
- Completion rate: X%
- Error rate: X%

QUALITY METRICS:
- Escalation rate: X%
- Human override rate: X%
- Task success (verified by human): X%

ACTIVITY LOG:
- Timestamped record of every action taken
- Filterable by date, task type, outcome
- Exportable for audit/compliance

WEEKLY REPORT:
- Summary of week's work
- Exceptions and escalations
- Recommended improvements
```

**Maintenance:**
- Monthly: review escalation log, adjust boundaries
- Quarterly: retrain on new examples, update skills
- Ongoing: human feedback loop for continuous improvement

---

## Deliverables

1. **Deployed AI employee** (working 24/7 in client's systems)
2. **Role document** (signed, defines scope + boundaries)
3. **Skill inventory** (what it can do, how it does it)
4. **Dashboard access** (productivity + quality metrics)
5. **Weekly reports** (automated, delivered to stakeholder)
6. **3-month support** included

---

## Pricing

| Tier | Role Complexity | Systems | Autonomy | Price |
|------|----------------|---------|----------|-------|
| **Starter** | Simple, 2-3 skills | 1 system | Shadow → Assisted | $2K–$3K/mo |
| **Professional** | Medium, 4-6 skills | 2-3 systems | Assisted → Full | $3K–$4K/mo |
| **Enterprise** | Complex, 7+ skills | 4+ systems | Full autonomy | $4K–$5K/mo |

**Role expansion:** $500–$1K/month per additional skill or system

---

## Timeline

```
Week 1:    Discovery + Role Definition
Week 2:    Skill Building + Tool Integration
Week 3:    Training + Shadow Mode Setup
Week 4:    Shadow → Assisted Transition
Week 5:    Assisted → Full Autonomy
Week 6:    Monitoring Dashboard + Handoff

Total: 5-6 weeks to full autonomy
Ongoing: monthly monitoring + quarterly retraining
```