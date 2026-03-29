# BUG-FIXES-001: Critical Bugs in Agentic Workflows Engine

**Date:** 2026-03-29  
**Status:** FIXED

## Summary

Fixed 5 critical bugs in the Namakan agentic workflows engine that would cause runtime failures, memory leaks, and infinite loops.

---

## Bug 1: Duplicate `worker.run` Line in SupervisorAgent.run()

**File:** `workflows/agent_engine.py`  
**Location:** `SupervisorAgent.run()` method  
**Severity:** Critical - prevents delegation from working

**Problem:**
```python
# Run the worker
result = worker.run                    result = worker.run(subtask)
```
Two lines merged into one, causing a syntax/logic error.

**Fix:** Removed the spurious `result = worker.run` line.

---

## Bug 2: Syntax Error in monitoring.py

**File:** `workflows/monitoring.py`  
**Location:** import statement  
**Severity:** Critical - prevents module from loading

**Problem:**
```python
from structlog processors import [  # WRONG - space instead of dot
```

**Fix:** Changed to:
```python
from structlog.processors import [  # CORRECT
```

---

## Bug 3: Ollama Streaming Bug

**File:** `workflows/agent_engine.py`  
**Location:** `OllamaProvider.generate()` method  
**Severity:** High - causes spurious non-streaming API call before every streaming call

**Problem:**
When `stream=True`, the code first made a non-streaming POST request, then checked for streaming and made a second streaming request. This doubles API usage and adds latency.

**Fix:** Reordered logic to check `stream` flag BEFORE making the request:
```python
if stream:
    # Return stream generator immediately
    return stream_gen()

# Only here for non-streaming
resp = self.client.post(...)
```

---

## Bug 4: Unbounded Self-Correction Loop

**File:** `workflows/agent_engine.py`  
**Location:** `AgentConfig` and `_self_correct()` method  
**Severity:** Critical - infinite loop if LLM keeps failing

**Problem:** No cap on self-correction attempts. If the LLM keeps failing, the agent would loop forever.

**Fix:**
1. Added `max_self_corrections: int = 3` to `AgentConfig`
2. Added check at start of `_self_correct()`:
```python
if self.state["self_corrections"] >= self.config.max_self_corrections:
    return f"SKIP: Max self-corrections ({self.config.max_self_corrections}) reached."
```

---

## Bug 5: PostgresSessionStore Connection Leak

**File:** `workflows/agent_engine.py`  
**Location:** `PostgresSessionStore` class  
**Severity:** High - database connections never closed

**Problem:** `self.conn` was opened in `__init__` but never closed, causing connection pool exhaustion over time.

**Fix:** Added proper cleanup:
```python
def close(self):
    if self.conn:
        self.conn.close()
        self.conn = None

def __enter__(self):
    return self

def __exit__(self, exc_type, exc_val, exc_tb):
    self.close()
    return False
```

---

## Additional Fix: Missing `workflow` Label on Metrics

**File:** `workflows/agent_engine.py`  
**Severity:** Medium - metrics lacked workflow identification

**Problem:** The `METRICS` dict definitions were missing the `workflow` label on all metrics.

**Fix:** Added `["workflow"]` label to all 10 metrics:
- `executions_total`
- `executions_running`
- `execution_duration`
- `step_duration`
- `tool_calls_total`
- `tool_duration`
- `escalations_total`
- `errors_total`
- `self_corrections`
- `llm_tokens_total`

Updated all `record_metric()` calls to pass `labels={"workflow": self.session_id}`.

---

## Testing

A test file `tests/test_bug_fixes.py` verifies:
1. SupervisorAgent delegation works without duplicate line error
2. monitoring.py imports without syntax error
3. OllamaProvider.generate() with stream=True doesn't make spurious non-streaming call
4. Self-correction respects max_self_corrections limit
5. PostgresSessionStore can be used as context manager and properly closes connections
6. All metrics have workflow label
