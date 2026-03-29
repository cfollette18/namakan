# Agentic Workflows — Monitoring

## Stack

- **Prometheus** — Metrics collection
- **Loki** — Log aggregation (Grafana-compatible)
- **Grafana** — Dashboards and alerting

## Metrics

See [workflows/monitoring.py](../workflows/monitoring.py) for full implementation.

```python
from workflows.monitoring import Metrics, MonitoringConfig

config = MonitoringConfig(
    prometheus_port=9090,
    loki_url="http://loki:3100",
    loki_enabled=True,
)

metrics = Metrics.get_instance(config)
metrics.start_server()
```

## Grafana Dashboard

Import `workflows/monitoring.py::GRAFANA_DASHBOARD` into Grafana.

### Key Panels

1. **Executions Over Time** — Rate of executions per workflow
2. **Execution Duration (p95)** — Latency percentiles
3. **Tool Call Success Rate** — Per-tool reliability
4. **Human Escalation Rate** — When humans are needed
5. **Error Rate by Type** — What errors occur
6. **Self-Correction Rate** — Agent self-healing
7. **Running Executions** — Current load
8. **LLM Token Usage** — Cost tracking

## Loki Logs

Logs are output in JSON format for Loki ingestion:

```json
{
  "event": "tool_called",
  "workflow": "lead-scoring",
  "tool": "crm_search",
  "status": "success",
  "duration": 0.234,
  "timestamp": "2026-03-29T10:00:00Z"
}
```

### Log Events

| Event | Level | Description |
|-------|-------|-------------|
| `execution_started` | INFO | New execution started |
| `execution_completed` | INFO | Execution finished |
| `tool_called` | INFO | Tool was executed |
| `human_escalation` | WARN | Human intervention needed |
| `error_occurred` | ERROR | Error occurred |
| `self_correction` | INFO | Agent self-corrected |

## Alerting Rules

```yaml
groups:
  - name: agent_alerts
    rules:
      - alert: HighEscalationRate
        expr: rate(agent_escalations_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High human escalation rate"
      
      - alert: ExecutionFailures
        expr: rate(agent_execution_duration_seconds_count{status="failed"}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Agent executions failing"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(agent_execution_duration_seconds_bucket[5m])) > 60
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Execution latency > 60s p95"
```

## Health Check

```bash
curl http://localhost:9090/health
# Returns: {"status": "healthy", "checks": {"prometheus": true, "structlog": true}}
```

## Quick Start

```bash
# Start monitoring stack
docker-compose up -d prometheus loki grafana

# View metrics
curl http://localhost:9090/metrics

# Import dashboard into Grafana
# Navigate to: Dashboards → Import → Paste GRAFANA_DASHBOARD JSON
```
