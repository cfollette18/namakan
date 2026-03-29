# Agentic Workflows — Phase 2: Process Mapping

*Namakan AI Engineering — Service Offering #3 | Pipeline Phase 2 of 7*

---

## Purpose

After Discovery, we document the candidate workflows in enough detail to design the agentic system. This phase produces the "truth source" for what the agent will actually do.

---

## Process Documentation

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

---

## Workflow Selection Criteria

Rank candidate workflows using this framework:

| Criteria | Weight | Score |
|----------|--------|-------|
| Time saved | High | 1-5 |
| Error reduction | High | 1-5 |
| Complexity (fewer systems = easier) | Medium | 1-5 |
| Frequency | Medium | 1-5 |
| Data availability | Medium | 1-5 |

**Total score ≥ 20** → Good automation candidate  
**Total score < 15** → Not worth automating yet

---

## Phase 3: Architecture Design

See [03-ARCHITECTURE.md](./03-ARCHITECTURE.md)
