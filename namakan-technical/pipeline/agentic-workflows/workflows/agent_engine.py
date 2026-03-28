#!/usr/bin/env python3
"""
Namakan — Agentic Workflows: Core Agent Engine
ReAct-based agent with tool definitions, state management, and human escalation.
"""
import os
import json
import re
import time
import argparse
import inspect
from dataclasses import dataclass, field
from typing import Optional, Callable, Any
from enum import Enum

class AgentState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING_HUMAN = "waiting_human"
    COMPLETED = "completed"
    FAILED = "failed"

# ─── Tool Base ────────────────────────────────────────────────────────────────

@dataclass
class ToolResult:
    success: bool
    output: Any
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)

class Tool:
    """Base class for agent tools."""
    name: str = ""
    description: str = ""
    parameters: dict = field(default_factory=dict)
    
    def run(self, **kwargs) -> ToolResult:
        raise NotImplementedError
    
    def to_openai_schema(self) -> dict:
        """Return OpenAI function-calling schema."""
        props = {}
        required = self.parameters.get("required", [])
        for param_name, param_info in self.parameters.get("properties", {}).items():
            props[param_name] = {
                "type": param_info.get("type", "string"),
                "description": param_info.get("description", ""),
            }
            if "enum" in param_info:
                props[param_name]["enum"] = param_info["enum"]
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": props,
                    "required": required,
                }
            }
        }

# ─── Built-in Tools ──────────────────────────────────────────────────────────

class WebSearchTool(Tool):
    name = "web_search"
    description = "Search the web for information. Use when you need current info or don't know something."
    parameters = {
        "properties": {
            "query": {"type": "string", "description": "The search query"},
            "max_results": {"type": "integer", "description": "Max results to return", "default": 5}
        },
        "required": ["query"]
    }
    
    def run(self, query: str, max_results: int = 5) -> ToolResult:
        try:
            import urllib.request
            url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}&kl=us-en"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode()
            
            # Simple extraction
            snippets = re.findall(r'<a class="result__snippet"[^>]*>([^<]+)<', html)
            results = []
            for s in snippets[:max_results]:
                clean = re.sub(r'<[^>]+>', '', s).strip()
                if clean:
                    results.append(clean)
            
            return ToolResult(success=True, output=results)
        except Exception as e:
            return ToolResult(success=False, output=None, error=str(e))

class FileReadTool(Tool):
    name = "file_read"
    description = "Read the contents of a file. Returns the file text content."
    parameters = {
        "properties": {
            "path": {"type": "string", "description": "Absolute path to the file"},
            "max_lines": {"type": "integer", "description": "Max lines to read", "default": 100}
        },
        "required": ["path"]
    }
    
    def run(self, path: str, max_lines: int = 100) -> ToolResult:
        try:
            with open(path, 'r') as f:
                lines = [f.readline() for _ in range(max_lines)]
            return ToolResult(success=True, output=''.join(lines))
        except Exception as e:
            return ToolResult(success=False, output=None, error=str(e))

class FileWriteTool(Tool):
    name = "file_write"
    description = "Write content to a file. Creates the file if it doesn't exist."
    parameters = {
        "properties": {
            "path": {"type": "string", "description": "Absolute path to the file"},
            "content": {"type": "string", "description": "Content to write"},
            "append": {"type": "boolean", "description": "Append instead of overwrite", "default": False}
        },
        "required": ["path", "content"]
    }
    
    def run(self, path: str, content: str, append: bool = False) -> ToolResult:
        try:
            mode = "a" if append else "w"
            with open(path, mode) as f:
                f.write(content)
            return ToolResult(success=True, output=f"{'Appended to' if append else 'Wrote'} {path}", metadata={"path": path})
        except Exception as e:
            return ToolResult(success=False, output=None, error=str(e))

class CommandTool(Tool):
    name = "run_command"
    description = "Run a shell command. Returns the command output."
    parameters = {
        "properties": {
            "command": {"type": "string", "description": "The shell command to run"},
            "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 30},
            "cwd": {"type": "string", "description": "Working directory"}
        },
        "required": ["command"]
    }
    
    def run(self, command: str, timeout: int = 30, cwd: str = None) -> ToolResult:
        try:
            import subprocess
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
            )
            output = result.stdout + (result.stderr if result.stderr else "")
            return ToolResult(
                success=result.returncode == 0,
                output=output,
                metadata={"returncode": result.returncode, "command": command}
            )
        except Exception as e:
            return ToolResult(success=False, output=None, error=str(e))

class HumanEscalateTool(Tool):
    name = "human_escalate"
    description = "Ask a human for help or a decision. Use when you need clarification or human approval."
    parameters = {
        "properties": {
            "question": {"type": "string", "description": "The question or decision needed from human"},
            "context": {"type": "string", "description": "Relevant context for the human"},
            "urgency": {"type": "string", "description": "urgency level", "enum": ["low", "medium", "high"], "default": "medium"}
        },
        "required": ["question"]
    }
    
    def run(self, question: str, context: str = "", urgency: str = "medium") -> ToolResult:
        # In production: integrate with Slack, email, or notification system
        print(f"\n{'='*60}")
        print(f"🤖 HUMAN ESCALATION [{urgency.upper()}]")
        print(f"{'='*60}")
        print(f"Question: {question}")
        if context:
            print(f"Context: {context}")
        print(f"{'='*60}")
        response = input("Your response: ")
        return ToolResult(success=True, output=response, metadata={"urgency": urgency})

# ─── Built-in Tools Registry ─────────────────────────────────────────────────

BUILTIN_TOOLS = {
    "web_search": WebSearchTool,
    "file_read": FileReadTool,
    "file_write": FileWriteTool,
    "run_command": CommandTool,
    "human_escalate": HumanEscalateTool,
}

# ─── Agent ───────────────────────────────────────────────────────────────────

@dataclass
class AgentConfig:
    name: str
    role: str
    instructions: str
    tools: list[Tool] = field(default_factory=list)
    max_iterations: int = 20
    escalation_threshold: int = 3
    verbose: bool = True

class AgenticWorkflow:
    """
    ReAct-style agentic workflow engine.
    
    Loop:
    1. THINK - Decide what to do next
    2. ACT - Execute the chosen tool
    3. OBSERVE - Update state with result
    4. CHECK - Done? Failed? Need human? Loop.
    """
    
    def __init__(self, config: AgentConfig, llm_provider: str = "openai"):
        self.config = config
        self.llm_provider = llm_provider
        self.state: dict = {
            "status": AgentState.PENDING,
            "history": [],  # List of (role, content) tuples
            "tool_calls": [],
            "iterations": 0,
            "escalations": 0,
            "last_output": None,
        }
        
        # Register tools
        self.tools: dict[str, Tool] = {}
        for tool in config.tools:
            self.tools[tool.name] = tool
        
        # Register built-ins
        for name, cls in BUILTIN_TOOLS.items():
            if name not in self.tools:
                self.tools[name] = cls()
        
        self._setup_llm()
    
    def _setup_llm(self):
        if self.llm_provider == "openai":
            try:
                from openai import OpenAI
                self.llm = OpenAI()
            except ImportError:
                raise RuntimeError("pip install openai")
        elif self.llm_provider == "anthropic":
            try:
                import anthropic
                self.llm = anthropic.Anthropic()
            except ImportError:
                raise RuntimeError("pip install anthropic")
    
    def _build_system_prompt(self) -> str:
        tools_desc = "\n".join(
            f"- {t.name}: {t.description}"
            for t in self.tools.values()
        )
        return f"""\
You are {self.config.name}, a {self.config.role}.

{self.config.instructions}

You have access to these tools:
{tools_desc}

Important rules:
- ALWAYS use tools when you need to get information or take actions
- If you need human input or approval, use human_escalate
- If you've completed the task, say "DONE" with a summary
- Think step by step before acting

When using a tool, respond in this format:
THINK: [what you're going to do]
ACTION: tool_name
ACTION_INPUT: {{"param": "value"}}
"""

    def _generate(self, messages: list[dict], stream: bool = False):
        """Generate from LLM."""
        if self.llm_provider == "openai":
            resp = self.llm.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1,
                stream=stream,
            )
            if stream:
                return (c.choices[0].delta.content or "" for c in resp)
            return resp.choices[0].message.content
        elif self.llm_provider == "anthropic":
            resp = self.llm.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                system=self._build_system_prompt(),
                messages=messages,
            )
            return resp.content[0].text
    
    def _parse_response(self, response: str) -> tuple[Optional[str], Optional[dict]]:
        """Parse LLM response for action blocks."""
        action_match = re.search(r'ACTION:\s*(\w+)', response)
        input_match = re.search(r'ACTION_INPUT:\s*(\{.*?\})', response, re.DOTALL)
        
        action_name = action_match.group(1) if action_match else None
        input_data = json.loads(input_match.group(1)) if input_match else {}
        
        return action_name, input_data
    
    def run(self, task: str, context: dict = None) -> dict:
        """Run the agent workflow."""
        self.state["status"] = AgentState.RUNNING
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": f"Task: {task}"}
        ]
        if context:
            messages.append({"role": "system", "content": f"Context: {json.dumps(context)}"})
        
        while self.state["iterations"] < self.config.max_iterations:
            self.state["iterations"] += 1
            
            if self.config.verbose:
                print(f"\n[Iteration {self.state['iterations']}]")
            
            # Generate
            response = self._generate(messages)
            messages.append({"role": "assistant", "content": response})
            self.state["history"].append(("assistant", response))
            
            # Parse action
            action_name, action_input = self._parse_response(response)
            
            if self.config.verbose and action_name:
                print(f"  → Action: {action_name}")
            
            # Execute
            if action_name == "human_escalate":
                tool_result = self.tools["human_escalate"].run(**action_input)
                self.state["escalations"] += 1
                messages.append({
                    "role": "user",
                    "content": f"Human responded: {tool_result.output}"
                })
                self.state["history"].append(("human", tool_result.output))
                continue
            
            elif action_name and action_name in self.tools:
                tool = self.tools[action_name]
                tool_result = tool.run(**action_input)
                
                result_text = f"Tool result: {tool_result.output}"
                if tool_result.error:
                    result_text += f"\nError: {tool_result.error}"
                
                messages.append({"role": "user", "content": result_text})
                self.state["history"].append(("tool", result_text))
                self.state["tool_calls"].append({
                    "tool": action_name,
                    "input": action_input,
                    "result": tool_result.output,
                    "success": tool_result.success,
                })
                
                if self.config.verbose:
                    print(f"    Result: {str(tool_result.output)[:100]}")
                
                # Check for done
                if "DONE" in response.upper() or "TASK COMPLETE" in response.upper():
                    self.state["status"] = AgentState.COMPLETED
                    self.state["last_output"] = response
                    break
            
            elif action_name and action_name not in self.tools:
                messages.append({"role": "user", "content": f"Unknown tool: {action_name}. Available tools: {list(self.tools.keys())}"})
            
            else:
                # No action found, check if task is done
                if any(word in response.upper() for word in ["DONE", "COMPLETE", "FINISHED"]):
                    self.state["status"] = AgentState.COMPLETED
                    self.state["last_output"] = response
                    break
        
        else:
            self.state["status"] = AgentState.FAILED
            self.state["last_output"] = "Max iterations reached"
        
        return self.state
    
    def run_stream(self, task: str, context: dict = None):
        """Stream the agent's response."""
        # Similar to run() but with streaming for the initial LLM response
        pass

# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Namakan Agentic Workflow Engine")
    parser.add_argument("--task", "-t", required=True, help="The task to perform")
    parser.add_argument("--role", "-r", default="AI Assistant", help="Agent role")
    parser.add_argument("--instructions", help="System instructions file")
    parser.add_argument("--tools", nargs="*", default=[], help="Additional tools to register")
    parser.add_argument("--max-iterations", type=int, default=20)
    args = parser.parse_args()
    
    instructions = ""
    if args.instructions:
        with open(args.instructions) as f:
            instructions = f.read()
    
    config = AgentConfig(
        name="NamakanAgent",
        role=args.role,
        instructions=instructions or "You are a helpful AI assistant.",
        max_iterations=args.max_iterations,
    )
    
    agent = AgenticWorkflow(config)
    result = agent.run(args.task)
    
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"Status: {result['status'].value}")
    print(f"Iterations: {result['iterations']}")
    print(f"Escalations: {result['escalations']}")
    print(f"Output: {result['last_output']}")

if __name__ == "__main__":
    main()
