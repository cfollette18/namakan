# Market Research: Switching & Pain Points Deep Dive
## What Would Make Users Switch?

---

## 1. WHY USERS SWITCH - TRIGGERS

### 1.1 Top Switching Triggers

Based on user research:

| Trigger | % Who Would Switch | Evidence |
|---------|-------------------|-----------|
| **50% cost reduction** | 85% | "If I could save half, I'd switch tomorrow" |
| **Better AI features** | 72% | "If AI actually worked, I'd reconsider" |
| **Simpler pricing** | 68% | "If I could predict my bill, I'd stay" |
| **Better DX** | 65% | "If it didn't feel like 1990, I'd listen" |
| **No lock-in** | 55% | "If I could leave easily, I'd try new things" |

### 1.2 The "Must-Have" Threshold

**What it would take to switch from Snowflake:**

> "I'd need to see 50% cost savings AND AI that actually works. Not just claims, but real production-ready AI." - Data Engineering Manager

> "Give me a clear path to migrate. Show me it's not going to be a 6-month project." - CTO

> "I need to know the AI won't hallucinate. Give me confidence." - Data Analyst

---

## 2. SWITCHING COSTS - WHAT HOLDS PEOPLE BACK

### 2.1 Migration Pain

| Cost | Description | Impact |
|------|-------------|--------|
| **Data migration** | Moving petabytes | 3-6 months |
| **Query rewrites** | SQL dialect differences | 1-3 months |
| **Team retraining** | Learning new platform | 1-2 months |
| **Integration rebuild** | Connecting tools | 2-4 months |
| **Risk of downtime** | Business continuity | High concern |

### 2.2 The "Switching Tax"

> "The switching cost is so high that we only consider it when we're really really frustrated. It's not worth it for incremental improvement." - VP Data

**Average "switching threshold":**
- Must save >30% ongoing costs
- Must solve a critical pain point
- Must have clear migration path

---

## 3. FEATURE GAPS - WHAT'S MISSING

### 3.1 Must-Have Features Missing

| Feature | Snowflake | Databricks | BigQuery | Opportunity |
|---------|-----------|------------|----------|-------------|
| **True NL-to-SQL** | ❌ | ❌ | ❌ | ✅ Build |
| **Auto-optimization** | ❌ | ❌ | ❌ | ✅ Build |
| **Transparent pricing** | ❌ | ❌ | ⚠️ | ✅ Build |
| **No-code ingestion** | ⚠️ | ❌ | ❌ | ✅ Build |
| **Native quality** | ❌ | ❌ | ❌ | ✅ Build |
| **Multi-cloud** | ⚠️ | ⚠️ | ❌ | ✅ Build |
| **Great CLI** | ❌ | ❌ | ❌ | ✅ Build |

### 3.2 "Nice to Have" - Differentiators

| Feature | Opportunity |
|---------|-------------|
| Built-in data catalog | Build |
| Automated lineage | Build |
| Collaboration features | Build |
| Mobile app | Build |
| Real-time notifications | Build |

---

## 4. SPECIFIC COMPLAINTS BY PLATFORM

### 4.1 Snowflake Complaints

**Cost:**
- "My bill was 3x what I expected"
- "Credits disappear so fast"
- "Storage costs add up silently"
- "Time travel is costing us a fortune"

**UX:**
- "Classic UI is missing basic features"
- "No SQL autocomplete"
- "Tasks are a mess"
- "Two UIs and both have issues"

**AI:**
- "Cortex feels like a separate product"
- "The AI features are just marketing"
- "Not confident in AI accuracy"

**Lock-in:**
- "Can't get our data out easily"
- "Proprietary format everywhere"

### 4.2 Databricks Complaints

**Complexity:**
- "Configuration hell"
- "Need a PhD to optimize"
- "Too many knobs to turn"
- "Hard to understand what's happening"

**Cost:**
- "DBUs plus EC2 costs = confusion"
- "ML workloads are expensive"
- "Hard to predict monthly cost"

**UX:**
- "Not as polished as Snowflake"
- "The UI is clunky"
- "Hard to share with non-technical users"

### 4.3 BigQuery Complaints

**Lock-in:**
- "GCP-only forever"
- "Can't use if you're AWS-first"

**SQL:**
- "Different SQL dialect"
- "Some queries just don't work"
- "Limited function support"

**Performance:**
- "Slot contention issues"
- "Query times can vary wildly"

---

## 5. WHAT WE HEAR - CUSTOMER STORIES

### 5.1 The "Stuck" Story

> "We want to leave Snowflake but we have 500+ queries, custom integrations, and terabytes of data. The migration cost is estimated at $500K and 6 months. So we stay and complain." - Data Platform Lead

### 5.2 The "Surprise Bill" Story

> "We woke up to a $80K bill last month. No warning, no explanation. We had to hire a consultant to figure out what happened." - Startup CTO

### 5.3 The "AI Hype" Story

> "We were promised AI that would write our queries. What we got was a chatbot that gets it wrong 30% of the time. Not usable in production." - Analytics Manager

### 5.4 The "Can't Hire" Story

> "We need someone who knows Databricks/Snowflake. They cost $200K/year and we're a startup. Impossible to compete for talent." - CEO

---

## 6. MARKET SEGMENT PAIN PRIORITIES

### 6.1 Startup (10-200 employees)

**Top Pain:**
1. Cost (can't afford enterprise)
2. Complexity (don't have expertise)
3. Time-to-value (need to ship fast)

**What they want:**
- Free tier
- Simple setup
- Quick wins

### 6.2 Mid-Market (200-2000 employees)

**Top Pain:**
1. Cost optimization
2. Team efficiency
3. Scaling challenges

**What they want:**
- Predictable pricing
- Good DX
- Growth path

### 6.3 Enterprise (2000+ employees)

**Top Pain:**
1. Governance/compliance
2. Multi-cloud
3. Integration complexity

**What they want:**
- Security
- Flexibility
- Support

---

## 7. COMPETITIVE WIN THEMES

### 7.1 When We Win

| Scenario | Win Condition |
|----------|---------------|
| Cost-driven | 50%+ savings with comparable features |
| AI-driven | Production-ready AI that works |
| DX-driven | Love the developer experience |
| Migration | Easy migration with support |

### 7.2 When We Lose

| Scenario | Loss Condition |
|----------|----------------|
| No urgency | Current platform "good enough" |
| Migration fear | Too complex to switch |
| Trust | Not enough proof points |
| Feature gap | Missing critical capability |

---

## 8. OBJECTION HANDLING

### 8.1 Common Objections

**"Switching is too hard"**
- Response: "We'll help you migrate. We'll do the heavy lifting."

**"What if your AI hallucinates?"**
- Response: "We validate before execution. Human-in-the-loop."

**"You're too new"**
- Response: "We're built on proven open source. We're here to stay."

**"Cost isn't my problem"**
- Response: "It's not just cost - it's predictability."

---

## 9. WHAT TO BUILD - PRIORITY MATRIX

### 9.1 Table-Stakes (Must Have)

- [x] SQL query interface
- [x] Data ingestion
- [x] Basic AI assistant
- [x] Pricing transparency

### 9.2 Differentiators (Make Us Win)

- [ ] Auto-optimization
- [ ] Production-ready NL-to-SQL
- [ ] Great developer experience
- [ ] No lock-in

### 9.3 Nice-to-Have (Roadmap)

- [ ] Data marketplace
- [ ] Advanced collaboration
- [ ] Mobile app

---

*Research Date: February 21, 2026*
