# Business Architecture
## How Namakan Operates

---

## 1. DECISION-MAKING FRAMEWORK

### 1.1 Decision Types

| Decision Type | Who Decides | Examples |
|--------------|-------------|----------|
| **Strategic** | CEO + Board | Fundraising, M&A, major pivots |
| **Product** | CPO + CEO | Features, roadmap, pricing |
| **Technical** | CTO + Tech Lead | Architecture, tech stack, scaling |
| **Operational** | COO | Processes, hiring, operations |
| **Day-to-Day** | Team Leads | Task priorities, bug fixes |

### 1.2 Decision Process

```
1. PROBLEM IDENTIFICATION
   - Customer feedback
   - Data/analytics
   - Team ideas
   
2. OPTIONS GENERATION
   - Brainstorm alternatives
   - Research similar solutions
   - Talk to users

3. ANALYSIS
   - Impact assessment
   - Cost/benefit analysis
   - Risk evaluation

4. DECISION
   - Make the call
   - Document rationale
   - Set timeline

5. EXECUTION
   - Assign owner
   - Set milestones
   - Track progress

6. REVIEW
   - Did it work?
   - Learnings
   - Iterate
```

### 1.3 RACI for Major Decisions

| Decision | CEO | CPO | CTO | COO | CSO |
|----------|-----|-----|-----|-----|-----|
| Product roadmap | A | R | C | I | C |
| Technical architecture | I | C | R | A | I |
| Pricing strategy | A | R | I | C | C |
| GTM strategy | A | C | I | I | R |
| Hiring plan | C | I | C | R | I |

R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## 2. TEAM STRUCTURE & WORKFLOWS

### 2.1 Team Layout

```
┌─────────────────────────────────────────────────────────────┐
│                      EXECUTIVE TEAM                         │
│   CEO ─── CFO ─── CMO ─── COO ─── CSO ─── CTO             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PRODUCT & ENGINE                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │  Product    │  │  Engineering │  │   Design    │       │
│  │  Team       │  │  Team        │  │  Team       │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    GROWTH & OPERATIONS                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   Sales     │  │  Marketing   │  │  Customer   │       │
│  │  Team       │  │  Team       │  │  Success    │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Team Workflows

#### Engineering Workflow
```
Ticket Created → Code Review → QA → Staging → Production
    ↑              ↓           ↓       ↓          ↓
  Backlog    Feedback    Testing  Deploy    Monitor
```

#### Product Workflow
```
Idea → Research → Design → Build → Test → Launch → Learn
```

#### Sales Workflow
```
Lead → Discovery → Demo → Proposal → Negotiation → Close
    ↓         ↓        ↓        ↓          ↓         ↓
  MQL      SQL      Opportunity  Deal     Contract  Customer
```

---

## 3. COMMUNICATION PROTOCOLS

### 3.1 Meeting Cadence

| Meeting | Frequency | Duration | Attendees |
|---------|-----------|----------|-----------|
| Daily Standup | Daily | 15 min | Team |
| Sprint Planning | Bi-weekly | 1 hour | Team |
| Product Review | Weekly | 1 hour | Product + Engineering |
| All-Hands | Monthly | 1 hour | Everyone |
| Executive Sync | Weekly | 30 min | Execs |
| Board Meeting | Quarterly | Half day | Board + Execs |

### 3.2 Communication Channels

| Channel | Use For | Response Time |
|---------|---------|---------------|
| Slack #general | Company announcements | 1 hour |
| Slack #engineering | Tech discussions | 30 min |
| Slack #product | Feature requests | Same day |
| Slack #customers | Customer issues | 15 min |
| Email | External, formal | 24 hours |
| Notion/Wiki | Documentation | No SLA |

### 3.3 Escalation Path

```
Level 1: Team Lead (within 30 min)
    ↓
Level 2: Manager (within 2 hours)
    ↓
Level 3: Director (within 4 hours)
    ↓
Level 4: VP/Executive (within 24 hours)
```

---

## 4. IDEA TO FEATURE PROCESS

### 4.1 Stage 1: Idea Collection

**Sources:**
- Customer feedback (support tickets, surveys, calls)
- Team ideas (anyone can submit)
- Market research (competitor analysis)
- Data analysis (usage patterns)

**Process:**
1. Submit idea to product backlog
2. Tag with category (feature, bug, improvement)
3. Initial triage by PM

### 4.2 Stage 2: Evaluation

**Criteria:**
| Criteria | Weight | Questions |
|----------|--------|-----------|
| Customer Value | 30% | How many customers want this? |
| Strategic Fit | 25% | Aligns with vision? |
| Effort | 20% | How long to build? |
| Revenue Impact | 15% | Will this drive growth? |
| Differentiation | 10% | Competitive advantage? |

### 4.3 Stage 3: Prioritization

**Framework: RICE**
- **R**each: How many customers?
- **I**mpact: How much value?
- **C**onfidence: How sure are we?
- **E**ffort: How long to build?

**Priority Matrix:**
```
        High Impact
           │
    P0    │    P1
    ──────┼───────
    P2    │    P3
           │
        Low Impact
    Low Effort ────── High Effort
```

### 4.4 Stage 4: Build

1. Write detailed spec (PRD)
2. Design review
3. Engineering estimation
4. Sprint planning
5. Build + testing
6. Code review
7. QA
8. Staging release

### 4.5 Stage 5: Launch

1. Release notes
2. Marketing/communications
3. Customer announcement
4. Monitor metrics
5. Gather feedback

### 4.6 Stage 6: Iterate

1. Analyze usage data
2. Collect feedback
3. Identify improvements
4. Plan next iteration

---

## 5. CUSTOMER FEEDBACK LOOP

### 5.1 Feedback Sources

| Source | Volume | Quality | Priority |
|--------|--------|---------|----------|
| Support tickets | High | Medium | High |
| Customer calls | Medium | High | High |
| Surveys | High | Medium | Medium |
| NPS | Low | High | Medium |
| Sales calls | Medium | High | High |
| Social media | Variable | Low | Low |

### 5.2 Feedback Flow

```
Customer Feedback
       │
       ▼
┌──────────────────┐
│  Triage (PM)    │ → Quick wins → Sprint
│                  │
│  Categorize:     │
│  - Bug          │
│  - Feature      │
│  - Improvement  │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Prioritize      │ → Product Backlog
│  (RICE Scoring) │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Build           │
│  (Sprint)        │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Release         │
│  (Notify users)  │
└──────────────────┘
```

### 5.3 Metrics We Track

| Metric | Target | Action If Low |
|--------|--------|----------------|
| NPS | >40 | Investigate feedback |
| CSAT | >4.5/5 | Review support |
| Feature adoption | >50% | Improve onboarding |
| Time to resolution | <24 hours | Add resources |

---

## 6. SALES TO PRODUCT LOOP

### 6.1 Sales Process

```
Lead → MQL → SQL → Opportunity → Proposal → Negotiation → Close
  │       │        │              │          │            │
  ▼       ▼        ▼              ▼          ▼            ▼
Source  Marketing  Discovery    Demo      Pricing     Contract
```

### 6.2 Feedback to Product

**Weekly:**
- Win/loss analysis in sales meeting
- Common objections documented
- Feature requests logged

**Monthly:**
- Product review with sales
- Competitive intelligence
- Pricing feedback

**Quarterly:**
- Roadmap input from sales
- Market trends
- Customer segments

### 6.3 What Sales Reports to Product

| Report | Frequency | Content |
|--------|-----------|----------|
| Win/loss reasons | Weekly | Why we won/lost |
| Feature requests | Weekly | What's missing |
| Competitive intel | Monthly | What competitors offer |
| Pricing feedback | Monthly | Price objections |
| Customer health | Monthly | At-risk accounts |

---

## 7. OKR FRAMEWORK

### 7.1 OKR Structure

**Company OKRs** (set quarterly)
  ↓
**Team OKRs** (derived from company)
  ↓
**Individual OKRs** (derived from team)

### 7.2 Example OKRs

**Company Q1 OKRs:**

| Objective | Key Results |
|-----------|-------------|
| Launch MVP | 1. MVP shipped by Feb 28 |
| | 2. 10 beta customers |
| | 3. NPS >30 |
| Acquire Customers | 1. 50 MQLs |
| | 2. 10 paying customers |
| | 3. CAC <$10K |
| Build Team | 1. Hire 5 engineers |
| | 2. All roles staffed |

### 7.3 OKR Cadence

- **Set:** Beginning of quarter
- **Check-in:** Weekly in all-hands
- **Review:** End of quarter
- **Score:** 0.0 - 1.0 (target 0.7)

---

## 8. OPERATING PRINCIPLES

### 8.1 Core Principles

1. **Bias toward action** - Done > perfect
2. **Default to transparency** - Share information freely
3. **Be customer-obsessed** - Customer success = our success
4. **Think long-term** - Sustainable over flashy
5. **No ego** - Best idea wins
6. **High velocity** - Move fast, learn faster

### 8.2 How We Work

- **Asynchronous-first** - Document decisions, not just discuss
- **Write things down** - If it's not written, it didn't happen
- **Small teams** - Max 5 people per initiative
- **Single threaded** - One person owns each project
- **No surprises** - Escalate early

---

*Document: Business Architecture*
*Date: February 21, 2026*
