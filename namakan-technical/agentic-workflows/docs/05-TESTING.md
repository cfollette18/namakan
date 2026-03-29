# Agentic Workflows — Testing

## Testing Strategy

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

## Running the Eval Pipeline

```bash
# Run all tests
python workflows/eval_pipeline.py

# Run specific test
python workflows/eval_pipeline.py --test happy_path

# Run with JSON output
python workflows/eval_pipeline.py --json

# Or use pytest directly
pytest workflows/eval_pipeline.py -v
```

## Metrics Collected

| Metric | Type | Description |
|--------|------|-------------|
| `agent_executions_total` | Counter | Total executions |
| `agent_execution_duration_seconds` | Histogram | Execution time |
| `agent_tool_calls_total` | Counter | Tool calls by tool/status |
| `agent_escalations_total` | Counter | Human escalations |
| `agent_errors_total` | Counter | Errors by type |
| `agent_self_corrections_total` | Counter | Self-corrections |

## Parallel Testing

```python
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
