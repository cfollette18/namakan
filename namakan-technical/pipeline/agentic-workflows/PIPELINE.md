# Agentic Workflows Pipeline

*Namakan AI Engineering — Service Offering #3*

---

## The Offering

We build autonomous AI workers that complete multi-step tasks in a client's systems. Not chatbots that respond. AI agents that DO — processing documents, updating records, triggering actions, escalating when needed.

---

## Engagement Pipeline

```
Discovery → Process Mapping → Architecture → Build → Testing → Deploy → Monitor
```

---

## Phase 1: Discovery

### Discovery Call (60 min)


### Client-Specific Decisions Locked
- **Deployment**: Either client infrastructure OR Namakan-hosted on cloud with monthly subscription model
- **Human Touchpoints**: Determine per workflow — every step, confidence thresholds, or periodic batch review
- **Escalation**: Per-client policy — email, Slack, or manager notification

- [ ] What tasks do people repeat daily/weekly?
- [ ] What manual processes take the most time?
- [ ] What systems are involved? (CRM, ERP, email, documents)
- [ ] Where do errors happen most?
- [ ] What decisions require human judgment?
- [ ] Current workflow diagrams?

### Process Identification Framework
```
TIME-SPENT ANALYSIS:
- List top 5 most time-consuming tasks
- How many times per day/week/month?
- Total hours spent per month?

ERROR-LOOKUP:
- Where do mistakes happen most?
- What's the cost of each error type?
- What causes most rework?
```

### Discovery Output
- Top 3 candidate workflows for automation
- ROI estimate per workflow
- Priority ranking
- Ballpark: $5K-30K per workflow

---

## Phase 2: Process Mapping

### Process Documentation
```python
PROCESS_DOCUMENT = """
# Process: [Name]

## Steps
1. [Trigger] → [Action] → [System] → [Output]
2. ...

## Decision Points
- IF [condition] THEN [action A] ELSE [action B]

## Exception Handling
- [Exception type] → [Handling]
- [Exception type] → [Escalation]

## Human Touchpoints
- [Step] requires human approval
- [Step] requires human judgment

## Success Metrics
- Completion rate: > 95%
- Error rate: < 1%
- Time saved: X hours/week
"""
```

### Workflow Diagram
```
[TRIGGER]
    ↓
[STEP 1: Fetch Data] → [API / Database]
    ↓
[STEP 2: Validate] → [Rules Engine]
    ↓
[DECISION: Pass?] ─NO─→ [ESCALATE to Human]
    ↓ YES
[STEP 3: Process] → [CRM / Document / Email]
    ↓
[STEP 4: Update Records] → [Database]
    ↓
[COMPLETE / NOTIFY]
```

### Workflow Selection Criteria
| Criteria | Weight | Score |
|----------|--------|-------|
| Time saved | High | 1-5 |
| Error reduction | High | 1-5 |
| Complexity (fewer systems = easier) | Medium | 1-5 |
| Frequency | Medium | 1-5 |
| Data availability | Medium | 1-5 |

---

## Phase 3: Architecture Design

### Agent Architecture
```
┌─────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATOR                │
├─────────────────────────────────────────────────────┤
│  Memory    │  Tools    │  Planner   │  Executor    │
│  Context   │  API      │  ReAct     │  Actions    │
│  History   │  Browser   │  Loop      │  Webhooks   │
└────────────┴───────────┴────────────┴──────────────┘
                         ↓
        ┌──────────┬──────────┬──────────┐
        │  Tool 1  │  Tool 2  │  Tool 3  │
        │  CRM     │  Email   │  Docs   │
        └──────────┴──────────┴──────────┘
```

### Tool Definition
```python
TOOL_DEFINITION = """
# Each tool the agent can use:

tools = [
    {
        "name": "search_crm",
        "description": "Search customer records in CRM by name, email, or account ID",
        "parameters": {
            "query": {"type": "string"},
            "limit": {"type": "integer", "default": 10}
        },
        "returns": "List of matching customer records"
    },
    {
        "name": "update_crm",
        "description": "Update a customer record in CRM",
        "parameters": {
            "record_id": {"type": "string"},
            "fields": {"type": "object"}
        },
        "returns": "Updated record"
    },
    {
        "name": "send_email",
        "description": "Send an email via SMTP",
        "parameters": {
            "to": {"type": "string"},
            "subject": {"type": "string"},
            "body": {"type": "string"}
        },
        "returns": "Send confirmation"
    },
    {
        "name": "read_document",
        "description": "Read and extract text from a document",
        "parameters": {
            "path": {"type": "string"},
            "format": {"type": "string"}
        },
        "returns": "Extracted text content"
    },
    {
        "name": "human_escalate",
        "description": "Pause workflow and notify human for decision",
        "parameters": {
            "reason": {"type": "string"},
            "context": {"type": "object"}
        },
        "returns": "Human decision"
    },
]
"""
```

### ReAct Loop Implementation
```python
class AgenticWorkflow:
    def __init__(self, tools, model):
        self.tools = tools
        self.model = model
        self.memory = []
    
    def run(self, trigger_input):
        state = {"input": trigger_input, "history": [], "pending": []}
        
        while not state.get("complete"):
            # Think: decide next action
            plan = self.plan(state)
            
            # Act: execute the planned action
            result = self.execute(plan, state)
            
            # Observe: update state
            state = self.observe(result, state)
            
            # Check if human escalation needed
            if plan.get("escalate"):
                human_decision = self.human_escalate(plan, state)
                state["human_decision"] = human_decision
        
        return state["output"]
    
    def plan(self, state):
        prompt = f"""
Task: {state['input']}
History: {state['history']}
Pending: {state['pending']}
Available tools: {list(self.tools.keys())}

Think: What is the next action?
Action: tool_name
Input: {{"param": "value"}}
"""
        response = self.model.generate(prompt)
        return parse_action(response)
```

---

## Phase 4: Build

### Tool Implementation
```python
# Example: CRM Integration Tool
class CRMTool:
    name = "crm"
    
    def __init__(self, crm_config):
        self.client = Salesforce(
            username=crm_config["username"],
            password=crm_config["password"],
            security_token=crm_config["token"]
        )
    
    def search(self, query):
        soql = f"SELECT Id, Name, Email, Status FROM Contact WHERE Name LIKE '%{query}%' LIMIT 10"
        results = self.client.query_all(soql)
        return results["records"]
    
    def update(self, record_id, fields):
        self.client.Contact.update(record_id, fields)
        return {"success": True, "id": record_id}

# Example: Email Tool
class EmailTool:
    name = "email"
    
    def __init__(self, smtp_config):
        self.smtp = smtplib.SMTP(smtp_config["host"], smtp_config["port"])
        self.smtp.starttls()
        self.smtp.login(smtp_config["username"], smtp_config["password"])
    
    def send(self, to, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_config["from"]
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        self.smtp.send_message(msg)
        return {"sent": True, "to": to}
```

### Error Handling
```python
ERROR_HANDLING = {
    "api_rate_limit": {
        "strategy": "retry_with_backoff",
        "max_retries": 3,
        "backoff_seconds": [1, 5, 30]
    },
    "api_auth_failure": {
        "strategy": "alert_and_escalate",
        "notify": "ops-team"
    },
    "invalid_data": {
        "strategy": "validate_and_retry",
        "max_retries": 1
    },
    "human_decision_needed": {
        "strategy": "pause_and_notify",
        "notify": "assigned_user",
        "timeout_hours": 24
    },
    "unknown_error": {
        "strategy": "log_and_escalate",
        "retry": False
    }
}

def handle_error(error, context):
    error_type = classify_error(error)
    handler = ERROR_HANDLING.get(error_type, ERROR_HANDLING["unknown_error"])
    
    if handler["strategy"] == "retry_with_backoff":
        return execute_with_backoff(context, handler)
    elif handler["strategy"] == "pause_and_notify":
        return pause_and_escalate(context, handler)
```

### Workflow State Machine
```python
STATE_MACHINE = """
States: PENDING → RUNNING → WAITING_HUMAN → COMPLETED → FAILED

Transitions:
PENDING + trigger() → RUNNING
RUNNING + step_complete() → RUNNING (next step)
RUNNING + need_human() → WAITING_HUMAN
RUNNING + all_steps_complete() → COMPLETED
RUNNING + error() → FAILED
WAITING_HUMAN + human_decision() → RUNNING
WAITING_HUMAN + timeout() → FAILED
FAILED + retry() → PENDING
"""
```

---

## Phase 5: Testing

### Testing Strategy
```python
TEST_SUITES = {
    "happy_path": [
        # Complete a workflow with all valid inputs
        # Verify all steps execute correctly
        # Verify final output is correct
    ],
    "error_cases": [
        # API timeout → should retry
        # Invalid data → should reject with clear error
        # Missing required field → should ask for clarification
    ],
    "edge_cases": [
        # Very long input
        # Special characters
        # Empty result sets
        # Concurrent execution
    ],
    "escalation_cases": [
        # Unknown error → escalates
        # Ambiguous decision → escalates
        # Manual approval step → pauses
    ],
}

def run_test_suite(suite):
    results = []
    for test in suite:
        try:
            result = execute_workflow(test["input"])
            passed = validate_result(result, test["expected"])
            results.append({"test": test["name"], "passed": passed})
        except Exception as e:
            results.append({"test": test["name"], "passed": False, "error": str(e)})
    return aggregate_results(results)
```

### Parallel Testing
```python
# Test multiple workflows concurrently
def stress_test(n_concurrent=10):
    """Run workflow under concurrent load."""
    import concurrent.futures
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_concurrent) as executor:
        futures = [executor.submit(execute_workflow, test_input) for test_input in inputs]
        results = [f.result() for f in futures]
    
    return {
        "total": len(results),
        "completed": sum(1 for r in results if r["status"] == "completed"),
        "failed": sum(1 for r in results if r["status"] == "failed"),
        "avg_time": sum(r["duration"] for r in results) / len(results)
    }
```

---

## Phase 6: Deployment

### Production Architecture
```yaml
services:
  workflow-orchestrator:
    image: namakan/workflow-orchestrator:latest
    environment:
      - REDIS_URL=redis://redis:6379
      - POSTGRES_URL=postgres://workflows:prod
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure

  workflow-worker:
    image: namakan/workflow-worker:latest
    environment:
      - QUEUE_URL=redis://redis/workflows
      - LLM_PROVIDER=openai
    deploy:
      replicas: 4

  redis:
    image: redis:7-alpine
  
  postgres:
    image: postgres:15
```

### Monitoring
```python
WORKFLOW_METRICS = {
    "executions_total": "Counter",
    "executions_by_workflow": "Counter(labels=['workflow'])",
    "execution_duration_seconds": "Histogram",
    "step_duration_seconds": "Histogram(labels=['step'])",
    "error_rate": "Gauge(labels=['workflow'])",
    "human_escalation_rate": "Gauge(labels=['workflow'])",
}

def record_execution(workflow_id, steps, duration, errors):
    metrics.executions_total.inc()
    metrics.executions_by_workflow.labels(workflow=workflow_id).inc()
    metrics.execution_duration_seconds.observe(duration)
    if errors:
        metrics.error_rate.labels(workflow=workflow_id).set(errors / len(steps))
```

---

## Deliverables

1. **Deployed workflow system** (client infra or ours)
2. **Workflow documentation** (step-by-step)
3. **Admin dashboard** (monitor, retry, audit)
4. **API for integrations**
5. **Runbook** for common issues
6. **3-month support** included

---

## Pricing

| Tier | Complexity | Systems | Price |
|------|------------|---------|-------|
| **Starter** | Simple, 1-2 steps | 1 system | $5K-10K |
| **Professional** | Medium, 3-5 steps | 2-3 systems | $10K-20K |
| **Enterprise** | Complex, 5+ steps | Multiple | $20K-30K |
| **Monthly Ops** | Ongoing | Monitoring | $500-1.5K/mo |

---

## Timeline

```
Week 1:    Discovery + Process Mapping
Week 2:    Architecture + Tool Building
Week 3:    Core Workflow + Testing
Week 4:    Integration + Error Handling
Week 5:    UAT + Training
Week 6:    Deployment
```

Total: 5-6 weeks typical
