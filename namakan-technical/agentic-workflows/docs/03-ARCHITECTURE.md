# Agentic Workflows — Architecture

## Agent Architecture

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

## ReAct Loop Implementation

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
```

## State Machine

```
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
```

## LLM Provider Architecture

The engine supports multiple LLM providers:

| Provider | Use Case | Notes |
|----------|----------|-------|
| **Ollama** | Local inference, privacy | Running on Jetson Orin Nano |
| **OpenAI** | Best quality | GPT-4o, GPT-4o-mini |
| **Anthropic** | Claude models | Sonnet, Opus |
| **Groq** | Fast inference | Llama, Mixtral |
| **Gemini** | Google's models | Gemini 2.0 Flash |
| **vLLM** | Self-hosted, fast | For local clusters |

## Session Persistence

```
┌─────────────────────────────────────────┐
│           Agentic Workflow                │
│  - In-memory state                       │
│  - Session ID                           │
└────────────┬──────────────────────────────┘
             │ save/load
             ↓
┌─────────────────────────────────────────┐
│     Session Store (Redis/Postgres)        │
│  - State serialization                   │
│  - Resume interrupted workflows           │
└─────────────────────────────────────────┘
```

## Monitoring Architecture

```
┌─────────────────────────────────────────┐
│         Agentic Workflow Engine            │
│  - Prometheus metrics                    │
│  - Structured logs (JSON)                │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        ↓                 ↓
┌───────────────┐  ┌───────────────┐
│  Prometheus   │  │     Loki      │
│  :9090        │  │  :3100        │
└───────┬───────┘  └───────┬───────┘
        │                  │
        ↓                  ↓
┌───────────────┐  ┌───────────────┐
│   Grafana     │  │   Grafana     │
│   Dashboards  │  │   Logs View   │
└───────────────┘  └───────────────┘
```
