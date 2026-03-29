# Agentic Workflows — Build Guide

## Tool Implementation

### Example: CRM Integration Tool

```python
from agent_engine import Tool, ToolResult

class CRMTool(Tool):
    name = "crm"
    description = "Search and update customer records in CRM"
    parameters = {
        "properties": {
            "operation": {"type": "string", "enum": ["search", "update", "create"]},
            "query": {"type": "string", "description": "Search query"},
            "record_id": {"type": "string", "description": "Record ID for update"},
            "fields": {"type": "object", "description": "Fields to update"}
        },
        "required": ["operation"]
    }
    
    def __init__(self, crm_config):
        from salesforce import Salesforce
        self.client = Salesforce(
            username=crm_config["username"],
            password=crm_config["password"],
            security_token=crm_config["token"]
        )
    
    def run(self, operation, query=None, record_id=None, fields=None, **kwargs) -> ToolResult:
        try:
            if operation == "search":
                soql = f"SELECT Id, Name, Email FROM Contact WHERE Name LIKE '%{query}%'"
                results = self.client.query_all(soql)
                return ToolResult(success=True, output=results["records"])
            
            elif operation == "update":
                self.client.Contact.update(record_id, fields)
                return ToolResult(success=True, output={"success": True, "id": record_id})
            
            else:
                return ToolResult(success=False, output=None, error=f"Unknown operation: {operation}")
        
        except Exception as e:
            return ToolResult(success=False, output=None, error=str(e))
```

### Example: Email Tool

```python
class EmailTool(Tool):
    name = "email"
    description = "Send emails via SMTP"
    parameters = {
        "properties": {
            "to": {"type": "string"},
            "subject": {"type": "string"},
            "body": {"type": "string"}
        },
        "required": ["to", "subject", "body"]
    }
    
    def run(self, to, subject, body) -> ToolResult:
        import smtplib
        from email.mime.text import MIMEText
        
        msg = MIMEText(body, 'html')
        msg['From'] = self.config["from"]
        msg['To'] = to
        msg['Subject'] = subject
        
        try:
            with smtplib.SMTP(self.config["host"], self.config["port"]) as server:
                server.starttls()
                server.login(self.config["username"], self.config["password"])
                server.send_message(msg)
            return ToolResult(success=True, output={"sent": True, "to": to})
        except Exception as e:
            return ToolResult(success=False, output=None, error=str(e))
```

## Error Handling

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

## Multi-Agent Patterns

### Supervisor/Worker Pattern

```python
from agent_engine import SupervisorAgent, AgenticWorkflow, AgentConfig

# Create worker agents
researcher = AgenticWorkflow(
    AgentConfig(name="Researcher", role="Research Assistant"),
    llm_provider="ollama"
)
coder = AgenticWorkflow(
    AgentConfig(name="Coder", role="Coder Assistant"),
    llm_provider="ollama"
)

# Create supervisor
supervisor = SupervisorAgent(
    workers={"researcher": researcher, "coder": coder},
    supervisor_llm="ollama"
)

# Run complex task
result = supervisor.run("Research AI trends and write a report")
```

### Crew Pattern

```python
# Multiple agents work on the same task in parallel
from agent_engine import CrewAgent

crew = CrewAgent(
    agents=[researcher, coder, reviewer],
    task="Build a complete web scraper",
    mode="parallel"  # or "sequential"
)
result = crew.run()
```
