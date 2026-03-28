# Agentic Workflows Skill

**Purpose**: Build autonomous agent systems that execute complex multi-step tasks

## Architecture

```
User Task → ReAct Loop → Tool Execution → Observation → Response
                    ↓
              Human Escalation (if confidence < threshold)
```

## Stack

- **Runtime**: LangGraph (stateful multi-agent orchestration)
- **Pattern**: ReAct (Reason + Act + Observe loop)
- **Tools**: web_search, file_read, file_write, run_command, human_escalate

## Key Files

```
namakan-technical/pipeline/agentic-workflows/
├── PIPELINE.md                     # Full pipeline doc
└── workflows/
    └── agent_engine.py            # ReAct agent + tool registry
```

## Tool Registry

Defined in `agent_engine.py`:

| Tool | Description |
|------|-------------|
| `web_search` | Search DuckDuckGo for current info |
| `web_fetch` | Extract readable content from URL |
| `file_read` | Read local files |
| `file_write` | Write/edit local files |
| `run_command` | Execute shell commands |
| `human_escalate` | Pause and notify human for input |

## State Machine

```python
class AgentState(TypedDict):
    task: str
    history: List[Dict[str, str]]  # {"role": "user/assistant/tool", "content": "..."}
    current_step: int
    confidence: float
    should_escalate: bool
```

## Confidence Thresholds

- **> 0.8**: Execute and respond
- **0.5–0.8**: Execute, show reasoning, respond
- **< 0.5**: Escalate to human

## Human Escalation

```python
if state["confidence"] < 0.5:
    yield {
        "should_escalate": True,
        "escalation_message": "I'm unsure how to proceed. [specific question]"
    }
    # Human reviews, provides input
    # Agent continues with human guidance
```

## Per-Client Decisions

Ask the client:
- [ ] What systems does the agent interact with? (CRM, email, calendar, ERP?)
- [ ] Where does a human need to approve or decide?
- [ ] Who gets escalation notifications? (email, Slack, manager?)
- [ ] Frequency: one-time task, daily batch, or real-time?
- [ ] Credentials: API keys, SSO, read-only accounts?
- [ ] Monitoring: who watches the agent? What is success?
