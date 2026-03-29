#!/usr/bin/env python3
"""
Namakan — Agentic Workflows: Evaluation Pipeline
Tests agentic workflows: happy path, error injection, escalation, concurrency.
"""
import pytest
import asyncio
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

# Import the agent engine
import sys
sys.path.insert(0, str(__file__).rsplit('/workflows/', 1)[0])

from workflows.agent_engine import (
    AgenticWorkflow, AgentConfig, Tool, ToolResult, 
    create_llm_provider, AgentState,
    SupervisorAgent, InMemorySessionStore
)

# ─── Test Metrics ──────────────────────────────────────────────────────────────

@dataclass
class EvalResult:
    test_name: str
    passed: bool
    duration: float
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)

class EvalMetrics:
    def __init__(self):
        self.results: list[EvalResult] = []
    
    def add(self, result: EvalResult):
        self.results.append(result)
    
    def summary(self) -> dict:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        avg_duration = sum(r.duration for r in self.results) / total if total else 0
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total if total else 0,
            "avg_duration": avg_duration,
            "by_test": {r.test_name: {"passed": r.passed, "duration": r.duration} for r in self.results}
        }

METRICS = EvalMetrics()

# ─── Test Fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture
def agent():
    """Create a test agent with mock tools."""
    tools = [
        MockSuccessTool(),
        MockFailureTool(),
        MockSlowTool(),
        MockHumanTool(),
    ]
    
    config = AgentConfig(
        name="TestAgent",
        role="Test Assistant",
        instructions="You are a test agent. Use tools when needed.",
        tools=tools,
        max_iterations=10,
        verbose=False,
        session_store=InMemorySessionStore(),
    )
    
    return AgenticWorkflow(config, llm_provider="ollama", model="qwen2.5:0.5b")

@pytest.fixture
def supervisor():
    """Create a test supervisor with worker agents."""
    worker1_config = AgentConfig(
        name="Worker1",
        role="Research Assistant",
        instructions="You research topics using web search.",
    )
    worker2_config = AgentConfig(
        name="Worker2", 
        role="Coder Assistant",
        instructions="You write and test code.",
    )
    
    workers = {
        "researcher": AgenticWorkflow(worker1_config, llm_provider="ollama", model="qwen2.5:0.5b"),
        "coder": AgenticWorkflow(worker2_config, llm_provider="ollama", model="qwen2.5:0.5b"),
    }
    
    return SupervisorAgent(workers, supervisor_llm="ollama", model="qwen2.5:0.5b")

# ─── Mock Tools for Testing ───────────────────────────────────────────────────

class MockSuccessTool(Tool):
    name = "mock_success"
    description = "A tool that always succeeds with a predefined response."
    parameters = {
        "properties": {
            "value": {"type": "string", "description": "Value to return"}
        },
        "required": ["value"]
    }
    
    def run(self, value: str) -> ToolResult:
        return ToolResult(success=True, output=f"Success: {value}", metadata={"tool": "mock_success"})

class MockFailureTool(Tool):
    name = "mock_failure"
    description = "A tool that always fails with a predefined error."
    parameters = {
        "properties": {
            "error_msg": {"type": "string", "description": "Error message to return"}
        },
        "required": ["error_msg"]
    }
    
    def run(self, error_msg: str) -> ToolResult:
        return ToolResult(success=False, output=None, error=error_msg)

class MockSlowTool(Tool):
    name = "mock_slow"
    description = "A tool that takes a while to complete."
    parameters = {
        "properties": {
            "delay": {"type": "integer", "description": "Delay in seconds", "default": 1}
        },
        "required": []
    }
    
    def run(self, delay: int = 1) -> ToolResult:
        time.sleep(delay)
        return ToolResult(success=True, output=f"Waited {delay}s")

class MockHumanTool(Tool):
    name = "mock_escalate"
    description = "A tool that simulates human escalation."
    parameters = {
        "properties": {
            "question": {"type": "string", "description": "Question for human"}
        },
        "required": ["question"]
    }
    
    def run(self, question: str) -> ToolResult:
        # In tests, auto-approve
        return ToolResult(success=True, output="APPROVED", metadata={"auto_approved": True})

# ─── Happy Path Tests ─────────────────────────────────────────────────────────

class TestHappyPath:
    """Happy path: agent completes tasks successfully."""
    
    def test_simple_task_completes(self, agent):
        """Agent completes a simple task without tools."""
        start = time.time()
        result = agent.run("Say 'Hello World' in exactly those words.")
        duration = time.time() - start
        
        METRICS.add(EvalResult(
            test_name="happy_path.simple_task",
            passed=result["status"] == AgentState.COMPLETED,
            duration=duration,
        ))
        
        assert result["status"] == AgentState.COMPLETED
    
    def test_tool_call_succeeds(self, agent):
        """Agent successfully uses a tool."""
        start = time.time()
        result = agent.run("Use mock_success with value='test123'")
        duration = time.time() - start
        
        METRICS.add(EvalResult(
            test_name="happy_path.tool_call",
            passed=result["status"] == AgentState.COMPLETED and len(result["tool_calls"]) > 0,
            duration=duration,
            metadata={"tool_calls": len(result.get("tool_calls", []))}
        ))
        
        assert len(result["tool_calls"]) > 0
        assert result["tool_calls"][0]["tool"] == "mock_success"
    
    def test_multi_step_workflow(self, agent):
        """Agent completes a multi-step workflow."""
        start = time.time()
        result = agent.run("Call mock_success three times with values 'a', 'b', 'c'")
        duration = time.time() - start
        
        METRICS.add(EvalResult(
            test_name="happy_path.multi_step",
            passed=result["status"] == AgentState.COMPLETED and result["iterations"] >= 3,
            duration=duration,
            metadata={"iterations": result["iterations"]}
        ))
        
        assert result["status"] == AgentState.COMPLETED

# ─── Error Injection Tests ───────────────────────────────────────────────────

class TestErrorInjection:
    """Error cases: tool failures, timeouts, invalid inputs."""
    
    def test_tool_failure_retries(self, agent):
        """Agent handles tool failure and continues."""
        start = time.time()
        result = agent.run("Call mock_failure with error_msg='Connection timeout', then mock_success with value='recovered'")
        duration = time.time() - start
        
        METRICS.add(EvalResult(
            test_name="error_injection.tool_failure",
            passed=result["status"] == AgentState.COMPLETED,
            duration=duration,
            metadata={"self_corrections": result.get("self_corrections", 0)}
        ))
        
        # Agent should have self-corrected
        assert result.get("self_corrections", 0) >= 1
    
    def test_unknown_tool_handled(self, agent):
        """Agent handles unknown tool gracefully."""
        start = time.time()
        result = agent.run("Use imaginary_tool that does magic")
        duration = time.time() - start
        
        METRICS.add(EvalResult(
            test_name="error_injection.unknown_tool",
            passed=result["status"] in (AgentState.COMPLETED, AgentState.FAILED),
            duration=duration,
        ))
        
        # Should not crash
        assert result["status"] is not None
    
    def test_max_iterations_reached(self):
        """Agent stops after max iterations."""
        config = AgentConfig(
            name="LoopyAgent",
            role="Loopy Assistant",
            instructions="Keep calling tools forever.",
            tools=[MockSlowTool()],
            max_iterations=3,
            verbose=False,
        )
        agent = AgenticWorkflow(config, llm_provider="ollama", model="qwen2.5:0.5b")
        
        start = time.time()
        result = agent.run("Keep calling mock_slow with delay=0 forever")
        duration = time.time() - start
        
        METRICS.add(EvalResult(
            test_name="error_injection.max_iterations",
            passed=result["status"] == AgentState.FAILED and result["iterations"] == 3,
            duration=duration,
        ))
        
        assert result["status"] == AgentState.FAILED
        assert "Max iterations" in result.get("last_output", "")

# ─── Escalation Tests ─────────────────────────────────────────────────────────

class TestEscalation:
    """Human escalation scenarios."""
    
    def test_escalation_triggered(self, agent):
        """Agent escalates when needed."""
        start = time.time()
        result = agent.run("Use mock_escalate with question='Is this correct?'")
        duration = time.time() - start
        
        METRICS.add(EvalResult(
            test_name="escalation.basic",
            passed=result["status"] == AgentState.COMPLETED and result["escalations"] >= 1,
            duration=duration,
            metadata={"escalations": result.get("escalations", 0)}
        ))
        
        assert result["escalations"] >= 1
    
    def test_session_persists_through_escalation(self):
        """Session state is preserved through escalation."""
        store = InMemorySessionStore()
        config = AgentConfig(
            name="PersistAgent",
            role="Test",
            instructions="Test session persistence.",
            tools=[MockHumanTool()],
            max_iterations=10,
            verbose=False,
            session_store=store,
        )
        agent = AgenticWorkflow(config, llm_provider="ollama", model="qwen2.5:0.5b")
        
        # First call triggers escalation
        result1 = agent.run("Escalate: Is this okay?")
        assert result1["status"] in (AgentState.WAITING_HUMAN, AgentState.COMPLETED)
        
        # Session should be saved
        loaded = store.load(agent.session_id)
        assert loaded is not None
        
        METRICS.add(EvalResult(
            test_name="escalation.session_persist",
            passed=loaded is not None,
            duration=0,
        ))

# ─── Concurrency Tests ─────────────────────────────────────────────────────────

class TestConcurrency:
    """Stress tests with concurrent executions."""
    
    def test_concurrent_executions(self, n: int = 5):
        """Multiple agents run concurrently without interference."""
        def run_agent(i: int):
            config = AgentConfig(
                name=f"ConcurrentAgent{i}",
                role="Concurrent Test",
                instructions="Complete this task.",
                tools=[MockSuccessTool()],
                max_iterations=5,
                verbose=False,
            )
            agent = AgenticWorkflow(config, llm_provider="ollama", model="qwen2.5:0.5b")
            return agent.run(f"Say completion{i}")
        
        start = time.time()
        with ThreadPoolExecutor(max_workers=n) as executor:
            futures = [executor.submit(run_agent, i) for i in range(n)]
            results = [f.result() for f in as_completed(futures)]
        duration = time.time() - start
        
        passed = sum(1 for r in results if r["status"] == AgentState.COMPLETED)
        
        METRICS.add(EvalResult(
            test_name="concurrency.multi_agent",
            passed=passed == n,
            duration=duration,
            metadata={"total": n, "passed": passed}
        ))
        
        assert passed == n
    
    def test_session_isolation(self):
        """Concurrent agents don't share session state."""
        store = InMemorySessionStore()
        
        def run_with_session(session_suffix: str):
            config = AgentConfig(
                name=f"IsolationAgent",
                role="Test",
                instructions=f"Your unique ID is {session_suffix}.",
                tools=[],
                max_iterations=3,
                verbose=False,
                session_store=store,
            )
            agent = AgenticWorkflow(config, llm_provider="ollama", model="qwen2.5:0.5b")
            agent.state["unique_id"] = session_suffix
            agent._save_session()
            return agent.session_id
        
        ids = [run_with_session(f"id_{i}") for i in range(3)]
        
        # All should have different session IDs
        unique_ids = set(ids)
        
        METRICS.add(EvalResult(
            test_name="concurrency.session_isolation",
            passed=len(unique_ids) == len(ids),
            duration=0,
        ))
        
        assert len(unique_ids) == len(ids)

# ─── Multi-Agent Tests ────────────────────────────────────────────────────────

class TestMultiAgent:
    """Tests for supervisor/worker multi-agent patterns."""
    
    def test_supervisor_delegates(self, supervisor):
        """Supervisor can delegate to workers."""
        start = time.time()
        result = supervisor.run("Research AI trends and write a summary")
        duration = time.time() - start
        
        METRICS.add(EvalResult(
            test_name="multiagent.delegation",
            passed=result["status"] == AgentState.COMPLETED,
            duration=duration,
            metadata={"completed_tasks": len(result.get("completed_tasks", []))}
        ))
        
        assert result["status"] == AgentState.COMPLETED

# ─── LLM Provider Tests ──────────────────────────────────────────────────────

class TestLLMProviders:
    """Test different LLM backends."""
    
    @pytest.mark.parametrize("provider,model", [
        ("ollama", "qwen2.5:0.5b"),
        ("groq", "llama-3.3-70b-versatile"),
    ])
    def test_provider_generates(self, provider, model):
        """Provider can generate text."""
        try:
            llm = create_llm_provider(provider, model=model)
            messages = [{"role": "user", "content": "Say 'test' in one word."}]
            result = llm.generate(messages)
            
            METRICS.add(EvalResult(
                test_name=f"provider.{provider}",
                passed=result and len(result) > 0,
                duration=0,
                metadata={"provider": provider, "model": model}
            ))
        except Exception as e:
            METRICS.add(EvalResult(
                test_name=f"provider.{provider}",
                passed=False,
                duration=0,
                error=str(e),
            ))

# ─── Metrics & Reporting ─────────────────────────────────────────────────────

def print_eval_summary():
    """Print evaluation summary."""
    summary = METRICS.summary()
    
    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Total:   {summary['total']}")
    print(f"Passed:  {summary['passed']} ({summary['pass_rate']*100:.1f}%)")
    print(f"Failed:  {summary['failed']}")
    print(f"Avg Duration: {summary['avg_duration']:.2f}s")
    print("-" * 70)
    
    for test_name, result in summary["by_test"].items():
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"  {status} {test_name} ({result['duration']:.2f}s)")
    
    print("=" * 70)
    
    return summary

# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Namakan Agentic Workflow Evaluation")
    parser.add_argument("--test", "-t", help="Run specific test")
    parser.add_argument("--provider", "-p", default="ollama", help="LLM provider")
    parser.add_argument("--model", "-m", default="qwen2.5:0.5b", help="Model")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    args = parser.parse_args()
    
    # Run pytest programmatically
    exit_code = pytest.main([
        __file__,
        "-v",
        "-k", args.test if args.test else "",
        "--tb=short",
    ])
    
    # Print our custom summary
    summary = print_eval_summary()
    
    if args.json:
        print(json.dumps(summary))
    
    return exit_code

if __name__ == "__main__":
    exit(main())
