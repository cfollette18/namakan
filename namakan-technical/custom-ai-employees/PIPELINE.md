# Custom AI Employees Pipeline

*Namakan AI Engineering — Service Offering #4*

---

## The Offering

We create permanent AI workers trained exclusively on a client's business, integrated into their operations. Think of it as hiring an AI employee who already knows their industry, their processes, and their standards — and works 24/7.

This is the highest-value, most retentive offering. It's a permanent addition to the client's team.

---

## Engagement Pipeline

```
Discovery → Role Definition → Training Data → Agent Build → Integration →
Onboarding → Monitoring → Ongoing Optimization
```

---

## Phase 1: Discovery

### Discovery Call (60-90 min)


### Client-Specific Decisions Locked
- **Deployment**: Namakan-hosted on cloud — clients pay monthly subscription ($2K-$5K/mo)
- **Supervisor**: Client assigns human manager per AI Employee
- **Retraining Cadence**: Per-client — monthly, quarterly, or on-demand

- [ ] What role does this AI employee fill?
- [ ] What does a day in this role look like?
- [ ] Who does this AI report to?
- [ ] Who are its colleagues / who does it interact with?
- [ ] What decisions can it make autonomously?
- [ ] What requires human escalation?
- [ ] What success looks like (KPIs)?

### Role Framework
```python
ROLE_DOCUMENT = """
# Custom AI Employee Role: [Title]

## Core Responsibilities
- [Primary task 1]
- [Primary task 2]
- [Primary task 3]

## Daily Tasks
- Morning: [startup tasks]
- Ongoing: [continuous tasks]
- End of day: [shutdown tasks]

## Weekly Tasks
- [Task 1] - [day]
- [Task 2] - [day]

## Decision Authority
CAN DO AUTONOMOUSLY:
- [Decision type 1]
- [Decision type 2]

MUST ESCALATE:
- [Escalation type 1]
- [Escalation type 2]

## Interactions
- Reports to: [Manager name/title]
- Collaborates with: [Team/role]
- Communicates with: [Clients/customers?]

## Success Metrics
- [KPI 1]: Target > [X]%
- [KPI 2]: Target < [Y] hours/week of human time
- [KPI 3]: Accuracy > [Z]%

## Training Data Sources
- [Source 1]: [what it contains]
- [Source 2]: [what it contains]
"""
```

### Discovery Output
- Detailed role document
- Training data inventory
- Integration requirements
- Pricing: $2K-5K/mo retainer

---

## Phase 2: Role Definition

### Role Persona Development
```python
AI_EMPLOYEE_PERSONA = """
# Name: [AI Employee Name]
# Role: [Job Title]
# Personality: [Professional, friendly, precise, etc.]
# Tone: [How it communicates]

# Communication Style:
- Writes like: [professional, technical, conversational]
- Explains things: [simply, thoroughly, with examples]
- Handles conflict: [de-escalates, escalates, redirects]

# Domain Knowledge:
- Industry: [specific industry]
- Company: [specific company]
- Products: [product names, descriptions]
- Processes: [how work gets done]
- People: [key roles, names, relationships]

# Constraints:
- Never: [hard limits]
- Always: [non-negotiables]
- When unsure: [escalation protocol]
"""
```

### Workflow Integration Map
```python
INTEGRATION_MAP = """
AI Employee → [Systems it accesses]
               ├── CRM (read/write)
               ├── Email (send/receive)
               ├── Documents (read/write)
               ├── Calendar (read/write)
               ├── Database (query/update)
               └── [External APIs]

AI Employee ← [Triggers]
               ├── Scheduled times (daily, weekly)
               ├── Email received
               ├── Form submitted
               ├── Document uploaded
               └── Human request

AI Employee → [Notifications]
               ├── Email to manager
               ├── Slack to team
               ├── CRM notes
               └── Dashboard update
"""
```

---

## Phase 3: Training Data Collection

### Data Sources by Role Type

| Role Type | Primary Data Sources | Volume |
|-----------|---------------------|--------|
| Sales | CRM data, email threads, deals, calls | High |
| Customer Service | Tickets, knowledge base, responses | High |
| Operations | SOPs, schedules, reports | Medium |
| Finance | Reports, invoices, communications | Medium-Low |
| HR | Policies, employee data, processes | Medium |
| Legal | Contracts, precedents, templates | Medium |

### Data Collection Pipeline
```python
DATA_COLLECTION = """
For each data source:

1. SECURE ACCESS
   - Set up read-only API access
   - Or client exports data to encrypted folder
   - Document all data sources accessed

2. DATA EXTRACTION
   - Pull historical examples (6-12 months ideal)
   - Get successful examples AND failures
   - Include edge cases and exceptions

3. ANONYMIZATION
   - Remove PII (names, emails, phone numbers)
   - Replace with role-appropriate placeholders
   - Keep business context intact

4. QUALITY FILTERING
   - Remove ambiguous responses
   - Remove incorrect responses
   - Keep high-quality examples

5. FORMAT CONVERSION
   - Convert to instruction/chat format
   - Include system prompt, user, assistant turns
"""
```

### Training Data Format
```json
{
  "messages": [
    {"role": "system", "content": "You are [AI Employee Name], a [job title] at [Company]. You are [personality description]. Your job is to [core responsibilities]."},
    {"role": "user", "content": "[Task or question from human]"},
    {"role": "assistant", "content": "[High-quality response the AI should learn to produce]"}
  ],
  "metadata": {
    "role_type": "[sales|cs|ops|finance|hr|legal]",
    "difficulty": "[simple|medium|complex]",
    "escalation": "[yes|no]"
  }
}
```

### Data Volume Targets
```python
TRAINING_VOLUME = {
    "minimal_viable": 500,      # Can work, basic quality
    "good": 2000,              # Solid, covers common cases
    "excellent": 5000,         # High quality, handles edge cases
    "expert": 10000,           # Very rare edge cases covered
}

SPLIT = {
    "train": 0.8,
    "validation": 0.1,
    "test": 0.1
}
```

---

## Phase 4: Agent Build

### Custom Agent Architecture
```python
class CustomAIEmployee:
    def __init__(self, config):
        # Fine-tuned model for domain knowledge
        self.llm = load_fine_tuned_model(config["model_path"])
        
        # Tools specific to this role
        self.tools = self.load_tools(config["tools"])
        
        # Memory for conversation context
        self.memory = Memory(
            max_history=100,
            summary_mode="recurrent"
        )
        
        # Escalation handler
        self.escalation = EscalationHandler(
            rules=config["escalation_rules"],
            notify=config["notify_person"]
        )
    
    def respond(self, user_input):
        # 1. Check memory for context
        context = self.memory.get_context()
        
        # 2. Check if escalation required
        if self.needs_escalation(user_input):
            return self.escalate(user_input)
        
        # 3. Generate response using fine-tuned model + tools
        response = self.llm.generate(
            prompt=f"Context: {context}\nInput: {user_input}",
            tools=self.available_tools
        )
        
        # 4. Execute any tool calls
        if response.tool_calls:
            results = self.execute_tools(response.tool_calls)
            response = self.llm.generate(
                f"Tool results: {results}\nBased on these results: {response.text}"
            )
        
        # 5. Update memory
        self.memory.add(user_input, response.text)
        
        # 6. Log interaction
        self.log_interaction(user_input, response)
        
        return response
    
    def needs_escalation(self, user_input):
        """Check against escalation rules."""
        for rule in self.escalation.rules:
            if rule.matches(user_input):
                return True
        return False
```

### System Prompt Engineering
```python
SYSTEM_PROMPT_TEMPLATE = """
You are {employee_name}, {job_title} at {company_name}.

{company_description}

YOUR ROLE:
{role_responsibilities}

YOUR STYLE:
- Communication: {communication_style}
- Tone: {tone}
- Level of detail: {detail_level}

YOUR CONSTRAINTS:
{hard_limits}

WHEN UNSURE:
{escalation_protocol}

CURRENT DATE: {date}
COMPANY POLICIES:
{relevant_policies}
"""
```

### Tool Permissions Matrix
```python
TOOL_PERMISSIONS = {
    "crm": {
        "read": ["customer_data", "deal_status", "contact_history"],
        "write": ["update_notes", "log_activity", "update_status"],
        "never": ["delete_records", "modify_pricing"]
    },
    "email": {
        "send": ["internal_team", "approved_external"],
        "never": ["send_to_executives", "send_to_board"]
    },
    "documents": {
        "read": ["approved_knowledge_base"],
        "write": ["approved_templates"],
        "never": ["modify_contracts", "delete_records"]
    }
}
```

---

## Phase 5: Integration

### Integration Checklist
```python
INTEGRATION_CHECKLIST = """
SYSTEM ACCESS:
☐ CRM (Salesforce/HubSpot/other)
☐ Email (Gmail/Outlook)
☐ Calendar (Google/Outlook)
☐ Documents (Google Drive/SharePoint)
☐ Database (if applicable)
☐ External APIs

ACCESS LEVELS:
☐ Read permissions
☐ Write permissions
☐ Delete permissions (restricted)
☐ API keys configured

NOTIFICATION SETUP:
☐ Manager email/Slack
☐ Escalation channel
☐ Weekly summary reports

TESTING:
☐ Sandbox integration test
☐ User acceptance testing
☐ Edge case testing
☐ Escalation testing
"""
```

### Integration Implementation
```python
INTEGRATION_IMPL = """
# Each integration is a tool the AI can call:

class CRMIntegration:
    def __init__(self, credentials):
        self.client = CRMClient(credentials)
    
    def search_customer(self, query):
        return self.client.search(query)
    
    def update_record(self, id, data):
        # Validation before write
        validated = self.validate(data)
        return self.client.update(id, validated)
    
    def create_activity(self, type, data):
        return self.client.create_activity(type, data)

class EmailIntegration:
    def __init__(self, credentials):
        self.client = EmailClient(credentials)
    
    def send(self, to, subject, body):
        # Pre-send review for external emails
        if self.is_external(to):
            self.flag_for_review(to, subject, body)
        return self.client.send(to, subject, body)
"""
```

---

## Phase 6: Onboarding

### Onboarding Timeline

| Week | Activity | Participants |
|------|----------|-------------|
| 1 | Training complete, testing | Namakan + Client Manager |
| 2 | Shadow mode — AI observes, human does | Manager shadows AI |
| 3 | Assist mode — AI suggests, human approves | Manager reviews all |
| 4 | Partial autonomy — AI does, human spot-checks | Manager spot checks |
| 5 | Full autonomy — AI operates, human monitors | AI operates |
| 6+ | Optimization — Based on feedback | Continuous |

### Onboarding Checklist
```python
ONBOARDING_CHECKLIST = """
WEEK 1: Launch
☐ Fine-tuned model deployed
☐ All integrations connected
☐ Escalation rules tested
☐ Manager trained on monitoring dashboard
☐ First week goals set

WEEK 2: Shadow Mode
☐ AI observes 10+ examples
☐ Manager reviews AI suggestions
☐ Feedback loop established
☐ Document edge cases for training

WEEK 3: Assist Mode
☐ AI works alongside manager
☐ Manager reviews and approves all
☐ AI accuracy tracked
☐ Weekly calibration meeting

WEEK 4: Partial Autonomy
☐ AI handles routine tasks
☐ Complex cases escalated
☐ Manager spot-checks 20% of outputs
☐ Begin reducing escalation frequency

WEEK 5+: Full Autonomy
☐ AI operates independently
☐ Weekly review meetings
☐ Monthly performance reports
☐ Quarterly model retraining
"""
```

---

## Phase 7: Monitoring

### Performance Metrics
```python
PERFORMANCE_METRICS = """
QUANTITATIVE:
- Tasks completed: X per day/week
- Accuracy rate: Target > 95%
- Escalation rate: Target < 5%
- Response time: Target < X seconds
- Task completion time: Target < X minutes

QUALITATIVE:
- Manager satisfaction: [1-5 scale, target > 4]
- Colleague feedback: [collaborative?]
- Error severity: [minor/major/critical]

COST METRICS:
- Human hours saved: X hours/week
- Cost per task: $X
- ROI: [savings - cost] / cost
"""
```

### Monthly Review
```python
MONTHLY_REVIEW = """
1. PERFORMANCE DASHBOARD REVIEW
   - Tasks completed
   - Accuracy rate
   - Escalation rate
   - Response times

2. QUALITATIVE FEEDBACK
   - Manager feedback
   - Quality issues flagged
   - Edge cases discovered

3. MODEL UPDATES
   - New training examples from recent work
   - Retraining triggers
   - Tool additions/removals

4. OPTIMIZATION ACTIONS
   - Process improvements
   - Prompt adjustments
   - New capabilities added
"""
```

---

## Phase 8: Retraining

### Retraining Triggers
```python
RETRAINING_TRIGGERS = {
    "quarterly": True,  # Automatic quarterly refresh
    "escalation_rate_above_10_percent": True,
    "new_product_launch": True,
    "process_change": True,
    "manager_feedback_satisfaction_below_3": True,
}

def should_retrain():
    if quarterly_review_due():
        return True
    if get_escalation_rate() > 0.10:
        return True
    if get_manager_satisfaction() < 3:
        return True
    if new_data_volume() > 500:
        return True
    return False
```

---

## Deliverables

1. **Trained AI employee model** (fine-tuned, client owns)
2. **Deployed AI employee** (API + monitoring)
3. **Role document** (complete description)
4. **Integration documentation** (all system connections)
5. **Onboarding guide** (manager training)
6. **Monitoring dashboard** (performance metrics)
7. **Weekly reports** (ongoing)

---

## Pricing

| Tier | Role Complexity | Data Volume | Price |
|------|----------------|-------------|-------|
| **Starter** | Single domain, 1-2 tools | < 5K examples | $2K-3K/mo |
| **Professional** | Multi-domain, 3-5 tools | 5K-15K examples | $3K-4K/mo |
| **Enterprise** | Complex, 5+ tools, multi-language | 15K+ examples | $4K-5K/mo |

**Setup Fee:** $5K-15K (includes training data collection, fine-tuning, integration)

---

## Timeline

```
Week 1-2:    Discovery + Role Definition
Week 2-4:    Training Data Collection
Week 4-6:    Agent Build + Testing
Week 6-7:    Integration
Week 8-9:    Onboarding (Shadow → Assist → Autonomy)
Ongoing:     Monitoring + Monthly Retraining
```
