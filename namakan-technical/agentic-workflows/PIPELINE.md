# Agentic Workflows — Index

This document has been split into separate files for easier maintenance.

## Documentation Structure

| Doc | Contents |
|-----|----------|
| [01-ENGAGEMENT-PIPELINE.md](./docs/01-ENGAGEMENT-PIPELINE.md) | Discovery, Process Mapping, Pricing |
| [03-ARCHITECTURE.md](./docs/03-ARCHITECTURE.md) | Agent Architecture, State Machine, LLM Providers |
| [04-BUILD.md](./docs/04-BUILD.md) | Tool Implementation, Error Handling, Multi-Agent |
| [05-TESTING.md](./docs/05-TESTING.md) | Test Suites, Eval Pipeline |
| [06-DEPLOYMENT.md](./docs/06-DEPLOYMENT.md) | Docker, Kubernetes, Environment Variables |
| [07-MONITORING.md](./docs/07-MONITORING.md) | Prometheus, Loki, Grafana Dashboards |

## Code Structure

```
workflows/
├── agent_engine.py      # Core engine (v2.0 with multi-LLM, streaming, self-correction)
├── eval_pipeline.py     # Test suite
├── monitoring.py         # Prometheus + Loki metrics
└── __init__.py

docs/
├── 01-ENGAGEMENT-PIPELINE.md
├── 03-ARCHITECTURE.md
├── 04-BUILD.md
├── 05-TESTING.md
├── 06-DEPLOYMENT.md
└── 07-MONITORING.md
```

## Quick Reference

### Run Agent
```bash
python workflows/agent_engine.py --task "Your task" --provider ollama
```

### Run Tests
```bash
pytest workflows/eval_pipeline.py -v
```

### Start Monitoring
```bash
python workflows/monitoring.py --port 9090 --loki-url http://loki:3100
```

---

*Namakan AI Consulting — Technical Reference*
