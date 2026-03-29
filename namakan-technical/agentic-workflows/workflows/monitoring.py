#!/usr/bin/env python3
"""
Namakan — Agentic Workflows: Monitoring
Prometheus metrics + Loki-compatible structured logging.
"""
import os
import json
import time
import logging
from typing import Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# ─── Prometheus Metrics ───────────────────────────────────────────────────────

try:
    from prometheus_client import (
        Counter, Histogram, Gauge, Info, 
        CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST,
        start_http_server, REGISTRY
    )
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

# ─── Loki Logger ───────────────────────────────────────────────────────────────

try:
    import structlog
    from structlog.processors import (
        add_log_level,
        TimeStamper,
        JSONRenderer,
        format_exc_info,
    )
    from structlog.stdlib import (
        filter_by_level,
        add_logger_name,
        PositionalArgumentsFormatter,
    )
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False

# ─── Metrics Definitions ─────────────────────────────────────────────────────

@dataclass
class MonitoringConfig:
    """Configuration for monitoring."""
    prometheus_port: int = 9090
    prometheus_enabled: bool = True
    loki_url: Optional[str] = None
    loki_enabled: bool = False
    log_level: str = "INFO"
    service_name: str = "namakan-agent"
    labels: dict = field(default_factory=dict)

class Metrics:
    """
    Prometheus metrics for agentic workflows.
    
    Metrics collected:
    - agent_executions_total: Total number of agent executions
    - agent_executions_running: Currently running executions
    - agent_execution_duration_seconds: Duration of executions
    - agent_step_duration_seconds: Duration of individual steps
    - agent_tool_calls_total: Total tool calls by tool and status
    - agent_tool_duration_seconds: Duration of tool calls by tool
    - agent_escalations_total: Human escalations by urgency
    - agent_errors_total: Errors by type
    - agent_self_corrections_total: Self-correction events
    - agent_llm_tokens_total: LLM tokens used by provider
    - agent_session_resumes_total: Session resume events
    """
    
    _instance: Optional["Metrics"] = None
    
    def __init__(self, config: MonitoringConfig = None):
        self.config = config or MonitoringConfig()
        self._metrics = {}
        self._setup_metrics()
        self.logger = self._setup_logger()
    
    @classmethod
    def get_instance(cls, config: MonitoringConfig = None) -> "Metrics":
        if cls._instance is None:
            cls._instance = cls(config)
        return cls._instance
    
    def _setup_metrics(self):
        """Initialize all Prometheus metrics."""
        if not PROMETHEUS_AVAILABLE:
            return
        
        labels = ["workflow", "agent", "provider"]
        
        self._metrics = {
            "executions_total": Counter(
                "agent_executions_total",
                "Total agent executions",
                ["workflow"]
            ),
            "executions_running": Gauge(
                "agent_executions_running",
                "Currently running executions",
                ["workflow"]
            ),
            "execution_duration": Histogram(
                "agent_execution_duration_seconds",
                "Execution duration in seconds",
                ["workflow", "status"],
                buckets=[0.1, 0.5, 1, 5, 10, 30, 60, 120, 300]
            ),
            "step_duration": Histogram(
                "agent_step_duration_seconds",
                "Step duration in seconds",
                ["workflow"],
                buckets=[0.01, 0.05, 0.1, 0.5, 1, 5, 10]
            ),
            "tool_calls_total": Counter(
                "agent_tool_calls_total",
                "Total tool calls",
                ["workflow", "tool", "status"]
            ),
            "tool_duration": Histogram(
                "agent_tool_duration_seconds",
                "Tool call duration in seconds",
                ["workflow", "tool"],
                buckets=[0.01, 0.05, 0.1, 0.5, 1, 5, 10]
            ),
            "escalations_total": Counter(
                "agent_escalations_total",
                "Human escalations",
                ["workflow", "urgency"]
            ),
            "errors_total": Counter(
                "agent_errors_total",
                "Total errors",
                ["workflow", "error_type"]
            ),
            "self_corrections": Counter(
                "agent_self_corrections_total",
                "Self-corrections triggered",
                ["workflow"]
            ),
            "llm_tokens": Counter(
                "agent_llm_tokens_total",
                "LLM tokens used",
                ["workflow", "provider", "model"]
            ),
            "session_resumes": Counter(
                "agent_session_resumes_total",
                "Session resume events",
                ["workflow"]
            ),
        }
        
        # Agent info metric
        self._metrics["info"] = Info(
            "agent_service",
            "Agent service information"
        )
        self._metrics["info"].info({
            "service_name": self.config.service_name,
            **self.config.labels
        })
    
    def _setup_logger(self):
        """Setup structured logger for Loki."""
        if not STRUCTLOG_AVAILABLE:
            # Fallback to standard logging
            logging.basicConfig(
                level=getattr(logging, self.config.log_level),
                format='%(asctime)s %(name)s %(levelname)s %(message)s'
            )
            return logging.getLogger(self.config.service_name)
        
        # Configure structlog
        processors = [
            filter_by_level,
            add_logger_name,
            add_log_level,
            PositionalArgumentsFormatter(),
            TimeStamper(fmt="iso"),
        ]
        
        # Add Loki if configured
        if self.config.loki_enabled and self.config.loki_url:
            try:
                from structlog_loki import LokiHandler
                processors.append(format_exc_info)
                processors.append(JSONRenderer())
                
                handler = LokiHandler(
                    url=self.config.loki_url,
                    labels={"service": self.config.service_name},
                )
                
                structlog.configure(
                    processors=processors,
                    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
                    logger_factory=structlog.PrintLoggerFactory(),
                    cache_logger_on_first_use=True,
                )
            except ImportError:
                # structlog_loki not available, use JSON to stdout
                processors.append(format_exc_info)
                processors.append(JSONRenderer())
                
                structlog.configure(
                    processors=processors,
                    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
                    context_class=dict,
                    logger_factory=structlog.PrintLoggerFactory(),
                    cache_logger_on_first_use=True,
                )
        else:
            processors.append(format_exc_info)
            processors.append(JSONRenderer())
            
            structlog.configure(
                processors=processors,
                context_class=dict,
                logger_factory=structlog.PrintLoggerFactory(),
                cache_logger_on_first_use=True,
            )
        
        return structlog.get_logger(self.config.service_name)
    
    def record_execution_start(self, workflow_id: str, **labels):
        """Record start of an agent execution."""
        self._metrics["executions_total"].labels(workflow=workflow_id).inc()
        self._metrics["executions_running"].labels(workflow=workflow_id).inc()
        
        self.logger.info(
            "execution_started",
            workflow=workflow_id,
            **labels
        )
    
    def record_execution_end(self, workflow_id: str, status: str, duration: float, **labels):
        """Record end of an agent execution."""
        self._metrics["executions_running"].labels(workflow=workflow_id).dec()
        self._metrics["execution_duration"].labels(
            workflow=workflow_id, 
            status=status
        ).observe(duration)
        
        self.logger.info(
            "execution_completed",
            workflow=workflow_id,
            status=status,
            duration=duration,
            **labels
        )
    
    def record_step(self, workflow_id: str, step_name: str, duration: float, **labels):
        """Record a step completion."""
        self._metrics["step_duration"].labels(
            workflow=workflow_id
        ).observe(duration)
        
        self.logger.debug(
            "step_completed",
            workflow=workflow_id,
            step=step_name,
            duration=duration,
            **labels
        )
    
    def record_tool_call(self, workflow_id: str, tool_name: str, status: str, duration: float, **labels):
        """Record a tool call."""
        self._metrics["tool_calls_total"].labels(
            workflow=workflow_id,
            tool=tool_name,
            status=status
        ).inc()
        
        self._metrics["tool_duration"].labels(
            workflow=workflow_id,
            tool=tool_name
        ).observe(duration)
        
        self.logger.info(
            "tool_called",
            workflow=workflow_id,
            tool=tool_name,
            status=status,
            duration=duration,
            **labels
        )
    
    def record_escalation(self, workflow_id: str, urgency: str, **labels):
        """Record a human escalation."""
        self._metrics["escalations_total"].labels(
            workflow=workflow_id,
            urgency=urgency
        ).inc()
        
        self.logger.warning(
            "human_escalation",
            workflow=workflow_id,
            urgency=urgency,
            **labels
        )
    
    def record_error(self, workflow_id: str, error_type: str, **labels):
        """Record an error."""
        self._metrics["errors_total"].labels(
            workflow=workflow_id,
            error_type=error_type
        ).inc()
        
        self.logger.error(
            "error_occurred",
            workflow=workflow_id,
            error_type=error_type,
            **labels
        )
    
    def record_self_correction(self, workflow_id: str, reason: str, **labels):
        """Record a self-correction."""
        self._metrics["self_corrections"].labels(
            workflow=workflow_id
        ).inc()
        
        self.logger.info(
            "self_correction",
            workflow=workflow_id,
            reason=reason,
            **labels
        )
    
    def record_tokens(self, workflow_id: str, provider: str, model: str, tokens: int, **labels):
        """Record LLM token usage."""
        self._metrics["llm_tokens"].labels(
            workflow=workflow_id,
            provider=provider,
            model=model
        ).inc(tokens)
    
    def record_session_resume(self, workflow_id: str, **labels):
        """Record a session resume."""
        self._metrics["session_resumes"].labels(
            workflow=workflow_id
        ).inc()
        
        self.logger.info(
            "session_resumed",
            workflow=workflow_id,
            **labels
        )
    
    def get_metrics(self) -> bytes:
        """Get Prometheus metrics in exposition format."""
        if not PROMETHEUS_AVAILABLE:
            return b""
        return generate_latest(REGISTRY)
    
    def start_server(self, port: int = None):
        """Start Prometheus metrics HTTP server."""
        if not PROMETHEUS_AVAILABLE:
            raise RuntimeError("prometheus_client not installed")
        
        port = port or self.config.prometheus_port
        start_http_server(port)
        self.logger.info("metrics_server_started", port=port)


# ─── Grafana Dashboard Config ──────────────────────────────────────────────────

GRAFANA_DASHBOARD = {
    "title": "Namakan Agentic Workflows",
    "panels": [
        {
            "title": "Executions Over Time",
            "type": "graph",
            "targets": [
                {
                    "expr": "rate(agent_executions_total[5m])",
                    "legendFormat": "{{workflow}}"
                }
            ]
        },
        {
            "title": "Execution Duration (p95)",
            "type": "graph", 
            "targets": [
                {
                    "expr": "histogram_quantile(0.95, rate(agent_execution_duration_seconds_bucket[5m]))",
                    "legendFormat": "{{workflow}} - {{status}}"
                }
            ]
        },
        {
            "title": "Tool Call Success Rate",
            "type": "graph",
            "targets": [
                {
                    "expr": "sum(rate(agent_tool_calls_total{status=\"success\"}[5m])) by (tool) / sum(rate(agent_tool_calls_total[5m])) by (tool)",
                    "legendFormat": "{{tool}}"
                }
            ]
        },
        {
            "title": "Human Escalation Rate",
            "type": "graph",
            "targets": [
                {
                    "expr": "rate(agent_escalations_total[5m])",
                    "legendFormat": "{{workflow}} - {{urgency}}"
                }
            ]
        },
        {
            "title": "Error Rate by Type",
            "type": "graph",
            "targets": [
                {
                    "expr": "rate(agent_errors_total[5m])",
                    "legendFormat": "{{error_type}}"
                }
            ]
        },
        {
            "title": "Self-Correction Rate",
            "type": "graph",
            "targets": [
                {
                    "expr": "rate(agent_self_corrections_total[5m])",
                    "legendFormat": "{{workflow}}"
                }
            ]
        },
        {
            "title": "Running Executions",
            "type": "stat",
            "targets": [
                {
                    "expr": "agent_executions_running",
                    "legendFormat": "{{workflow}}"
                }
            ]
        },
        {
            "title": "LLM Token Usage",
            "type": "graph",
            "targets": [
                {
                    "expr": "rate(agent_llm_tokens_total[5m])",
                    "legendFormat": "{{provider}} - {{model}}"
                }
            ]
        },
    ]
}

# ─── Loki Dashboard Config ──────────────────────────────────────────────────

LOKI_DASHBOARD = {
    "title": "Namakan Agentic Workflows - Logs",
    "panels": [
        {
            "title": "Execution Logs",
            "type": "logs",
            "targets": [
                {
                    "expr": '{service="namakan-agent"}'
                }
            ]
        },
        {
            "title": "Errors",
            "type": "logs",
            "targets": [
                {
                    "expr": '{service="namakan-agent", level="error"}'
                }
            ]
        },
        {
            "title": "Human Escalations",
            "type": "logs",
            "targets": [
                {
                    "expr": '{service="namakan-agent"} |= "human_escalation"'
                }
            ]
        },
    ]
}

# ─── Health Check ─────────────────────────────────────────────────────────────

def health_check() -> dict:
    """Return service health status."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "prometheus": PROMETHEUS_AVAILABLE,
            "structlog": STRUCTLOG_AVAILABLE,
        }
    }

# ─── CLI ────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Namakan Agentic Workflow Monitoring")
    parser.add_argument("--port", "-p", type=int, default=9090, help="Prometheus port")
    parser.add_argument("--loki-url", "-l", help="Loki URL")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARN", "ERROR"])
    args = parser.parse_args()
    
    config = MonitoringConfig(
        prometheus_port=args.port,
        loki_url=args.loki_url,
        loki_enabled=bool(args.loki_url),
        log_level=args.log_level,
    )
    
    metrics = Metrics.get_instance(config)
    
    if args.loki_url:
        print(f"Starting monitoring with Loki at {args.loki_url}")
    else:
        print("Starting monitoring (logs to stdout)")
    
    metrics.start_server()
    print(f"Prometheus metrics at http://localhost:{args.port}/metrics")
    
    # Keep running
    import time
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
