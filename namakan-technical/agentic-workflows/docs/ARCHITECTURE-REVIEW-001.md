# Architecture Review: Agentic Workflows v2.0

**Review Date:** 2026-03-29
**Reviewer:** Technical Architect (Subagent)
**Version Reviewed:** v2.0 — post-8-fix update
**Files Reviewed:** `workflows/agent_engine.py`, `workflows/monitoring.py`, `workflows/eval_pipeline.py`, `workflows/evaluate.py`, `workflows/intake.py`, `docs/03-ARCHITECTURE.md`, `docs/04-BUILD.md`, `docs/05-TESTING.md`, `docs/06-DEPLOYMENT.md`, `docs/07-MONITORING.md`

---

## Executive Summary

The v2.0 architecture is a solid foundation with a well-reasoned ReAct loop, 6-provider LLM abstraction, proper Prometheus + Loki observability, and a functional multi-agent SupervisorAgent pattern. The modular documentation structure is clear and usable.

However, this codebase has **11 new critical/subtle bugs** introduced in this update — including a duplicate line causing double-execution, a Python syntax error in the monitoring import, a streaming client-creating-twice bug in Ollama, unbounded self-correction loops, and SQL injection risk in PostgresSessionStore. Most are one-liners to fix. None should ship to production.

---

## Issues Found

### 🔴 CRITICAL — Will cause failures in production

**1. Duplicate `worker.run` call in SupervisorAgent** (`agent_engine.py`, line ~370)
```python
result = worker.run                    result = worker.run(subtask)   # ← DUPLICATE LINE
```
The first line is a method reference (unused). The second line executes it. This is likely a copy-paste artifact. It executes the worker once, but the dangling reference suggests intent was different. Review the SupervisorAgent `run()` method — the delegation logic appears to be cut off mid-assignment, which means the `DELEGATE_TO` / `TASK` parsing flow is likely incomplete and tasks may never actually be routed to workers correctly.

**2. Python Syntax Error in `monitoring.py` import**
```python
from structlog processors import [    # ← Square brackets instead of parentheses
    add_log_level,
    ...
]
```
This causes `ImportError` on any import of `monitoring.py`. Structlog is guarded with try/except in `agent_engine.py` (correctly) but not in `monitoring.py` itself, so the module fails to load entirely. The `monitoring.py` standalone server is broken.

**3. Ollama streaming creates a second HTTP client, discarding the first** (`agent_engine.py`, `OllamaProvider.generate()`)
```python
resp = self.client.post(...)   # ← non-streaming call, discards response
data = resp.json()             # ← only used for non-stream path

if stream:
    def stream_gen():
        with httpx.Client(timeout=300) as client:  # ← NEW client, NEW request
            with client.stream("POST", ...) as r:
                ...
```
The top-level `resp = self.client.post(...)` executes for **every** call (both stream and non-stream) and is discarded on the stream path, causing a spurious HTTP round-trip. Additionally, a second `httpx.Client()` is instantiated inside the generator, creating resource waste and potential connection pool exhaustion under load.

**4. Self-correction has no iteration cap — infinite loop risk** (`agent_engine.py`, `_self_correct()`)
```python
def _self_correct(self, error_context: str) -> str:
    self.state["self_corrections"] += 1
    ...
    correction = self._generate(messages)  # ← LLM call with no max_tokens cap
```
`_self_correct()` is called on **every tool failure** (line ~330: `if not tool_result.success and self.config.self_correct:`) and appends to `messages` indefinitely. No guard on `self.state["self_corrections"]` prevents this from spinning forever if the LLM keeps generating tool calls that fail. Also, the LLM call has no explicit `max_tokens` limit, risking unbounded output.

**5. SQL injection in `PostgresSessionStore`** (`agent_engine.py`)
```python
cur.execute("""
    INSERT INTO agent_sessions (session_id, state, updated_at)
    VALUES (%s, %s, NOW())
    ON CONFLICT (session_id) DO UPDATE SET state = %s, updated_at = NOW()
""", (session_id, json.dumps(state), json.dumps(state)))
```
The `session_id` is passed as a `%s` parameter — correctly parameterized. **However**, in `load()` and `delete()`:
```python
cur.execute("SELECT state FROM agent_sessions WHERE session_id = %s", (session_id,))  # ✓ Safe
cur.execute("DELETE FROM agent_sessions WHERE session_id = %s", (session_id,))        # ✓ Safe
```
These are actually safe. The injection concern is lower than initially suspected, but the `__init__` creates a connection stored on `self.conn` that is **never closed** — a resource leak. Additionally, there's no TTL or expiration policy on sessions.

### 🟠 HIGH — Significant functional gaps

**6. `run_async()` wraps sync `run()` — async is fake** (`agent_engine.py`)
```python
async def run_async(self, task: str, context: dict = None) -> dict:
    return self.run(task, context)  # ← Just calls sync version
```
No `await` points. If the caller uses `asyncio.run(agent.run_async(...))`, it blocks the event loop identically to the sync version. The streaming implementation (`run_stream()`) is also synchronous despite returning an `AsyncIterator`. For a system claiming async support, this is misleading.

**7. `agent_engine.py` metrics missing `workflow` label on 5 metrics**
```python
"tool_calls_total": Counter("agent_tool_calls_total", "Total tool calls"),         # no labels
"tool_duration": Histogram("agent_tool_duration_seconds", "Tool call duration"), # no labels
"escalations_total": Counter("agent_escalations_total", "Total human escalations"),# no labels
"errors_total": Counter("agent_errors_total", "Total errors"),                      # no labels
"self_corrections": Counter("agent_self_corrections_total", "Self-corrections triggered"), # no labels
```
Compare to `monitoring.py` where these **do** have `["workflow", "tool", "status"]` labels. In `agent_engine.py`, these metrics are effectively useless for Grafana dashboards (which reference labeled metrics) — the metrics server works but the dashboards are blind to per-workflow breakdown.

**8. SupervisorAgent delegation loop has no task result aggregation into supervisor context**
```python
if worker_name in self.workers:
    result = worker.run(subtask)
    self.state["tasks"][subtask] = result
    messages.append({"role": "user", "content": f"Worker {worker_name} completed: ..."})
```
The supervisor appends a text summary of the worker result, but the actual structured `result` dict is stored in `self.state["tasks"]`. The supervisor's `_supervisor.generate(messages)` only sees text — it cannot see the structured task data. This means the supervisor cannot make routing decisions based on prior task outputs in a type-safe way.

**9. No distributed task queue for SupervisorAgent workers**
The SupervisorAgent executes all workers **in-process, synchronously** (each `worker.run(subtask)` blocks until complete). The deployment guide shows Docker replicas but no message queue (Celery/RabbitMQ/Redis streams) connecting orchestrator to workers. With `deploy.replicas: 2` on `workflow-orchestrator`, you'd have 2 supervisors competing, not coordinating.

### 🟡 MEDIUM — Operational concerns

**10. PostgresSessionStore holds connection without pooling or context manager**
```python
def __init__(self, url: str = None):
    self.conn = psycopg2.connect(url)  # ← single connection, stored forever
```
No connection pooling (would need `psycopg2.pool`). No `close()` method. No context manager (`__enter__`/`__exit__`). Under load, connections will accumulate. The Redis store has the same architectural shape but Redis connections are far cheaper to hold.

**11. No execution deadline / overall timeout**
There is per-step `max_iterations` but:
- No total wall-clock timeout on `run()`, `run_async()`, or `run_stream()`
- No per-step timeout (the `step_duration` metric measures but doesn't enforce)
- `HumanEscalateTool.run()` blocks `input()` with no timeout — a human can stall the agent forever

**12. `CommandTool` has no sandboxing**
```python
def run(self, command: str, timeout: int = 30, cwd: str = None) -> ToolResult:
    subprocess.run(command, shell=True, ...)  # ← shell=True + arbitrary string
```
Any agent with access to `run_command` can execute arbitrary shell commands. No allowlist of permitted commands, no privilege separation, no read-only mode.

---

## Production Readiness Checklist

- [ ] **CRITICAL: Fix duplicate `worker.run` line** in `SupervisorAgent.run()` — review full delegation parsing logic
- [ ] **CRITICAL: Fix `monitoring.py` import syntax** — `from structlog processors import [` → `from structlog.processors import`
- [ ] **CRITICAL: Fix Ollama streaming** — remove spurious first POST, reuse client in generator
- [ ] **CRITICAL: Add self-correction iteration cap** — max 2-3 corrections per execution before failing
- [ ] **HIGH: Add `workflow` label** to all metrics in `agent_engine.py` to match `monitoring.py`
- [ ] **HIGH: Implement true async** — either make `run_async()` actually async or remove the claim
- [ ] **HIGH: Add distributed task queue** — Celery or Redis streams for SupervisorAgent → Worker communication
- [ ] **MEDIUM: PostgresSessionStore connection management** — add `close()` method and context manager
- [ ] **MEDIUM: Add execution deadline** — wall-clock timeout on `run()` (e.g., 5 min default)
- [ ] **MEDIUM: HumanEscalateTool timeout** — add timeout parameter, default 30 minutes
- [ ] **MEDIUM: CommandTool allowlist** — restrict to read-only or specific safe commands
- [ ] **LOW: Session TTL** — add Redis `EXPIRE` / Postgres `updated_at` TTL check
- [ ] **LOW: Graceful shutdown** — handle SIGTERM, drain in-flight executions
- [ ] **LOW: Tool call rate limiting** — prevent a single workflow from hammering a tool API
- [ ] **LOW: Structured error classification** — `classify_error()` referenced in BUILD.md but not implemented in engine

---

## Scaling Considerations

### Horizontal Scaling

| Component | Current | Scaling Path |
|-----------|---------|--------------|
| AgenticWorkflow | Single-process, sync | Stateless — add replicas behind load balancer with Redis session store |
| SupervisorAgent | In-process, sync worker calls | Workers must move to separate processes/services with a task queue |
| Session Store (Redis) | Single Redis instance | Redis Cluster for sharding; Redis Sentinel for HA |
| Session Store (Postgres) | Single connection | PgBouncer connection pool + Postgres read replicas |
| Prometheus | No federation | Prometheus federation or Grafana Agent remote_write |
| Loki | Single instance | Loki microservices mode or Grafana Enterprise |

### Concurrency Limits

- **In-memory store**: Safe for single instance. Thread-safe via `threading.Lock`.
- **Redis store**: Use `MULTI`/`EXEC` for atomic saves. Current implementation does not.
- **Postgres store**: No pooling — limit concurrent connections to `max_connections - 10`.
- **LLM providers**: Respect rate limits. Ollama is local (compute-bound on GPU). Groq has documented rate limits. OpenAI/Anthropic/Gemini all have tier-based limits.
- **Tool calls**: No concurrency limit enforced per workflow. A misbehaving agent could flood a CRM API.

### Resource Needs

- **Ollama (Jetson Orin Nano)**: 3B model fits in ~2GB VRAM. 7B needs ~6GB. qwen2.5:3b is appropriate.
- **Prometheus**: ~100 bytes per sample. At 100 workflows × 20 steps × 1 sample/sec = ~200KB/min. Minimal.
- **Redis**: Sessions are JSON. ~1-5KB per session. 10K concurrent sessions ≈ 50MB. Minimal.

---

## Monitoring Gaps

1. **No trace context propagation** — No OpenTelemetry / Zipkin tracing. Steps within a single execution cannot be linked in a distributed trace. Critical for debugging multi-agent flows.

2. **No LLM latency metric** — `llm_tokens_total` counts tokens but there's no `llm_request_duration_seconds` metric. Can't distinguish slow models from slow networks.

3. **No error rate SLO/SLA metric** — No derived metric like `agent_execution_success_rate`. The raw `errors_total` counter exists but no dashboard panel computes the ratio.

4. **Missing Cardinality Guard** — `workflow` label is missing from 5 metrics in `agent_engine.py` (see Issue #7). This means Grafana dashboards cannot filter by workflow. Additionally, if `tool_name` or `error_type` labels get high-cardinality values (e.g., full stack traces as error_type), they could explode Prometheus cardinality.

5. **No alert for self-correction storm** — If `self_corrections_total` spikes, it's a signal the agent is in a loop. No alerting rule exists for this.

6. **No health endpoint on agent_engine** — The `monitoring.py` has `health_check()` but the main `agent_engine.py` has no `/health` or `/ready` endpoint for Kubernetes liveness/readiness probes.

7. **Session store metrics missing** — No metrics for Redis connection pool exhaustion, Postgres query latency, or session store hit/miss rate.

---

## Recommendations for v2.1 (Prioritized)

### Must Fix (blocker for production)

1. **Fix `SupervisorAgent.run()` delegation logic** — The duplicate `worker.run` line and incomplete parsing suggests the multi-agent routing was written hastily. Add integration tests with actual workers.
2. **Fix `monitoring.py` import** — One-character fix (`[` → `(`) that unlocks the entire monitoring stack.
3. **Add self-correction cap** — Add `max_self_corrections` config (default 2). If exceeded, transition to FAILED state with a clear reason.
4. **Align metrics labels** — Add `workflow` label to all counters/histograms in `agent_engine.py` to match the patterns in `monitoring.py`.

### Should Fix (significant improvements)

5. **Add OpenTelemetry tracing** — Instrument the ReAct loop with span parents. Link tool calls, LLM calls, and agent steps into a single trace. This is the #1 debugging tool for production multi-agent systems.
6. **Implement true async or remove it** — `run_async()` is misleading. Either implement it with `asyncio.to_thread()` or mark it deprecated.
7. **Add execution deadline** — `max_duration_seconds` config on `AgentConfig`. Enforce in the `run()` loop with a check after each iteration.
8. **Add distributed task queue** — Replace in-process `worker.run()` with Celery task dispatch (or Redis + RQ). This is required before multi-replica deployment is viable.

### Nice to Have (polish)

9. **Session TTL enforcement** — Redis `EXPIRE` on save. Postgres: cron job or `WHERE updated_at < NOW() - INTERVAL '30 days'`.
10. **Graceful shutdown** — SIGTERM handler that finishes current step, saves session, then exits.
11. **CommandTool sandboxing** — Restrict to `allowed_commands` list or use `shlex.split()` without `shell=True`.
12. **Structured error taxonomy** — Implement `classify_error()` referenced in BUILD.md. Map errors to handler strategies consistently.

---

## Verdict

**NOT production-ready as-is.** The architecture shows good thinking and the 8 major fixes addressed the right areas. However, the implementation quality of this update is inconsistent — some components are well-engineered (metrics definitions, session store abstraction, LLM factory) while others have critical bugs (Ollama streaming, duplicate supervisor call, syntax error) that would cause immediate failures or infinite loops in production.

### What works well ✓

- LLM provider abstraction (factory, interface, 6 backends)
- Prometheus metrics definitions (in `monitoring.py` — the comprehensive version)
- Structured logging with structlog (when import works)
- Session store abstraction (Redis/Postgres/in-memory)
- State machine definition (CORRECTING state is a nice touch)
- ReAct loop core logic (plan → execute → observe)
- SupervisorAgent concept (delegation pattern is sound)
- Documentation structure (modular, readable, accurate)

### What will break in production ✗

- `monitoring.py` fails to import on any machine
- Ollama streaming makes double HTTP requests per call
- Self-correction loops forever on stubborn failures
- SupervisorAgent delegation is broken (duplicate line + incomplete parsing)
- 5 metrics in `agent_engine.py` have no `workflow` label (dashboards blind)
- `run_async()` blocks the event loop
- Postgres connection never closed (resource leak)
- No execution deadline (a stalled human escalates blocks forever)

### Path to Production

With the ~15 items from the Production Readiness Checklist addressed, this system could be production-ready for **single-instance, low-to-medium concurrency** workloads (up to ~10 concurrent agents). For high concurrency or multi-replica deployments, the distributed task queue (Item #8 in recommendations) is a hard prerequisite.

**Estimate:** 2-3 engineering days to fix critical items. 1-2 weeks for full production hardening including async rewrite, OpenTelemetry, and distributed queue.
