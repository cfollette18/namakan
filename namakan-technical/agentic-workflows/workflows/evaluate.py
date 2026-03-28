#!/usr/bin/env python3
"""
Agentic Workflow Evaluation Harness
Tests an agent workflow against a set of task/scenario pairs.
Usage: python3 evaluate.py --tasks tasks.jsonl --workflow customer-service
"""
import argparse
import json
import os
import sys
import time

def color(tag, text):
    codes = {"PASS": "\033[92m", "FAIL": "\033[91m", "WARN": "\033[93m", "INFO": "\033[94m", "RESET": "\033[0m"}
    return f"{codes.get(tag, '')}{text}{codes['RESET']}"

def load_tasks(path):
    tasks = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    return tasks

def run_agent_task(task, agent_module="agent_engine"):
    """
    Run a single task through the agent.
    Returns: (success, steps_taken, escalation_needed, time_taken, error)
    """
    from importlib import import_module
    from types import SimpleNamespace
    
    try:
        agent = import_module(agent_module)
    except ImportError:
        # Run via CLI
        import subprocess
        result = subprocess.run(
            ["python3", f"{agent_module}.py", "--task", task["task"], "--evaluate"],
            capture_output=True, text=True, timeout=120
        )
        return result.returncode == 0, 1, False, 0, None
    
    state = SimpleNamespace(
        task=task["task"],
        history=[],
        current_step=0,
        confidence=1.0,
        should_escalate=False,
        escalation_message=None,
        result=None
    )
    
    start = time.time()
    max_steps = task.get("max_steps", 10)
    
    for step in range(max_steps):
        try:
            result = agent.execute_step(state)
            if isinstance(result, dict):
                if result.get("done"):
                    return True, step + 1, result.get("escalated", False), time.time() - start, None
                elif result.get("escalate"):
                    return False, step + 1, True, time.time() - start, result.get("reason")
        except Exception as e:
            return False, step + 1, False, time.time() - start, str(e)
    
    return False, max_steps, state.should_escalate, time.time() - start, "Max steps reached"

def evaluate_task(task, agent_module):
    """Evaluate a single task."""
    task_id = task.get("id", "unknown")
    expected_outcome = task.get("expected_action", "")
    task_text = task.get("task", "")
    
    print(f"\n  [{task_id}] {task_text[:60]}...")
    
    start = time.time()
    try:
        success, steps, escalated, duration, error = run_agent_task(task, agent_module)
    except Exception as e:
        success, steps, escalated, duration, error = False, 0, False, 0, str(e)
    
    # Check if escalation was expected
    expected_escalation = task.get("should_escalate", False)
    
    if success and not expected_escalation:
        status = "PASS"
        reason = "completed successfully"
    elif not success and expected_escalation and escalated:
        status = "PASS"
        reason = "escalated as expected"
    elif escalated and not expected_escalation:
        status = "FAIL"
        reason = f"unnecessary escalation: {error or 'unknown'}"
    elif not success:
        status = "FAIL"
        reason = f"failed: {error or 'did not complete'}"
    else:
        status = "PASS"
        reason = "completed"
    
    return {
        "id": task_id,
        "status": status,
        "success": success,
        "escalated": escalated,
        "steps": steps,
        "duration": round(duration, 1),
        "reason": reason,
        "task": task_text,
        "expected_action": expected_outcome
    }

def print_report(results):
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    escalated = sum(1 for r in results if r.get("escalated"))
    avg_steps = sum(r["steps"] for r in results) / total if total else 0
    avg_time = sum(r["duration"] for r in results) / total if total else 0
    
    print(f"\n{'='*60}")
    print(f"  AGENTIC WORKFLOW EVALUATION")
    print(f"{'='*60}")
    print(f"  Tasks:       {total}")
    print(f"  {color('PASS', f'Passed:')}    {passed} ({passed/total*100:.0f}%)")
    print(f"  {color('FAIL', f'Failed:')}    {failed}")
    print(f"  Escalations: {escalated}")
    print(f"\n  Avg steps:   {avg_steps:.1f}")
    print(f"  Avg time:    {avg_time:.1f}s")
    
    if failed > 0:
        print(f"\n  {color('FAIL', 'Failed tasks:')}")
        for r in results:
            if r["status"] == "FAIL":
                print(f"    - {r['id']}: {r['reason']}")
    
    print(f"\n{'='*60}")
    return passed >= total * 0.8

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", required=True, help="JSONL file with task definitions")
    parser.add_argument("--workflow", default="agent_engine", help="Agent module name")
    parser.add_argument("--output", help="Save results JSON")
    args = parser.parse_args()
    
    if not os.path.exists(args.tasks):
        print(f"ERROR: Tasks file not found: {args.tasks}")
        print("\nExample tasks.jsonl:")
        print(json.dumps({
            "id": "task-1",
            "task": "Look up the warranty policy for order #12345",
            "expected_action": "retrieve_warranty",
            "should_escalate": False,
            "max_steps": 5
        }, indent=2))
        sys.exit(1)
    
    tasks = load_tasks(args.tasks)
    print(f"Loaded {len(tasks)} tasks")
    
    results = []
    for task in tasks:
        result = evaluate_task(task, args.workflow)
        print(f"  → {color(result['status'], result['status'])} ({result['steps']} steps, {result['duration']}s)")
        results.append(result)
    
    passed = print_report(results)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
    
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
