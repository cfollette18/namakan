#!/usr/bin/env python3
"""
Namakan — Agentic Workflows: Core Agent Engine v2.0
ReAct-based agent with multi-LLM support, streaming, multi-agent orchestration,
self-correction, metrics, and session persistence.
"""
import os
import json
import re
import time
import asyncio
import logging
from dataclasses import dataclass, field
from typing import Optional, Callable, Any, AsyncIterator, Union
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
import threading
import queue

# ─── Observability Setup ───────────────────────────────────────────────────────

try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False

# ─── Metrics ───────────────────────────────────────────────────────────────────

if PROMETHEUS_AVAILABLE:
    METRICS = {
        "executions_total": Counter("agent_executions_total", "Total agent executions", ["workflow"]),
        "executions_running": Gauge("agent_executions_running", "Currently running executions", ["workflow"]),
        "execution_duration": Histogram("agent_execution_duration_seconds", "Execution duration", ["workflow"], buckets=[0.1, 0.5, 1, 5, 10, 30, 60, 120]),
        "step_duration": Histogram("agent_step_duration_seconds", "Step duration", ["workflow"], buckets=[0.01, 0.05, 0.1, 0.5, 1, 5]),
        "tool_calls_total": Counter("agent_tool_calls_total", "Total tool calls", ["workflow", "tool_name", "status"]),
        "tool_duration": Histogram("agent_tool_duration_seconds", "Tool call duration", ["workflow", "tool_name"]),
        "escalations_total": Counter("agent_escalations_total", "Total human escalations", ["workflow", "urgency"]),
        "errors_total": Counter("agent_errors_total", "Total errors", ["workflow", "error_type"]),
        "self_corrections": Counter("agent_self_corrections_total", "Self-corrections triggered", ["workflow"]),
        "llm_tokens_total": Counter("agent_llm_tokens_total", "LLM tokens used", ["workflow", "provider", "model"]),
    }
else:
    METRICS = {k: None for k in ["executions_total", "executions_running", "execution_duration", 
                                   "step_duration", "tool_calls_total", "tool_duration",
                                   "escalations_total", "errors_total", "self_corrections", "llm_tokens_total"]}

# ─── Structured Logging ────────────────────────────────────────────────────────

def get_logger(name: str = "namakan.agent"):
    """Get structured logger with Loki-compatible JSON output."""
    if STRUCTLOG_AVAILABLE:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
        return structlog.get_logger(name)
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')
        return logging.getLogger(name)

LOG = get_logger()

# ─── State ────────────────────────────────────────────────────────────────────

class AgentState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING_HUMAN = "waiting_human"
    CORRECTING = "correcting"
    COMPLETED = "completed"
    FAILED = "failed"

# ─── Tool Base ─────────────────────────────────────────────────────────────────

@dataclass
class ToolResult:
    success: bool
    output: Any
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)

class Tool(ABC):
    """Base class for agent tools."""
    name: str = ""
    description: str = ""
    parameters: dict = field(default_factory=dict)
    
    @abstractmethod
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

# ─── LLM Provider Interface ──────────────────────────────────────────────────

class LLMProvider(ABC):
    """Abstract base for LLM providers."""
    
    @abstractmethod
    def generate(self, messages: list[dict], stream: bool = False, **kwargs) -> Union[str, AsyncIterator[str]]:
        """Generate text from messages."""
        pass
    
    @abstractmethod
    def get_token_count(self, text: str) -> int:
        """Estimate token count for text."""
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, model: str = "gpt-4o", api_key: str = None, base_url: str = None):
        from openai import OpenAI
        self.model = model
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"), 
                            base_url=base_url)
    
    def generate(self, messages: list[dict], stream: bool = False, **kwargs):
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.1),
            stream=stream,
            **kwargs
        )
        if stream:
            return (c.choices[0].delta.content or "" for c in resp)
        return resp.choices[0].message.content
    
    def get_token_count(self, text: str) -> int:
        # Rough estimate: ~4 chars per token
        return len(text) // 4

class AnthropicProvider(LLMProvider):
    def __init__(self, model: str = "claude-sonnet-4-20250514", api_key: str = None):
        import anthropic
        self.model = model
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
    
    def generate(self, messages: list[dict], stream: bool = False, **kwargs):
        # Extract system message
        system = None
        if messages and messages[0].get("role") == "system":
            system = messages[0]["content"]
            messages = messages[1:]
        
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 4096),
            system=system,
            messages=messages,
            stream=stream,
            **kwargs
        )
        if stream:
            return (c.delta.text or "" for c in resp)
        return resp.content[0].text
    
    def get_token_count(self, text: str) -> int:
        return len(text) // 4

class OllamaProvider(LLMProvider):
    """Ollama local inference provider."""
    def __init__(self, model: str = "qwen2.5:3b", base_url: str = "http://localhost:11434"):
        import httpx
        self.model = model
        self.base_url = base_url
        self.client = httpx.Client(timeout=300)
    
    def generate(self, messages: list[dict], stream: bool = False, **kwargs):
        # Convert messages to Ollama format
        ollama_messages = []
        for msg in messages:
            if msg.get("role") == "system":
                continue  # Ollama uses 'system' field
            ollama_messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Get system prompt
        system = None
        for msg in messages:
            if msg.get("role") == "system":
                system = msg.get("content")
                break
        
        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "stream": stream,
            "options": {
                "temperature": kwargs.get("temperature", 0.1),
            }
        }
        if system:
            payload["system"] = system
        
        if stream:
            def stream_gen():
                import httpx
                with httpx.Client(timeout=300) as client:
                    with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as r:
                        for line in r.iter_lines():
                            if line:
                                d = json.loads(line)
                                if d.get("message", {}).get("content"):
                                    yield d["message"]["content"]
            return stream_gen()
        
        resp = self.client.post(f"{self.base_url}/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        
        return data.get("message", {}).get("content", "")
    
    def get_token_count(self, text: str) -> int:
        return len(text) // 4

class GroqProvider(LLMProvider):
    """GroqCloud API provider (fast inference)."""
    def __init__(self, model: str = "llama-3.3-70b-versatile", api_key: str = None):
        self.model = model
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
    
    def generate(self, messages: list[dict], stream: bool = False, **kwargs):
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
            **kwargs
        )
        if stream:
            return (c.choices[0].delta.content or "" for c in resp)
        return resp.choices[0].message.content
    
    def get_token_count(self, text: str) -> int:
        return len(text) // 4

class GeminiProvider(LLMProvider):
    """Google Gemini API provider."""
    def __init__(self, model: str = "gemini-2.0-flash", api_key: str = None):
        self.model = model
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
    
    def generate(self, messages: list[dict], stream: bool = False, **kwargs):
        import httpx
        # Extract content from messages
        contents = []
        for msg in messages:
            if msg.get("role") == "system":
                continue
            contents.append({
                "role": "user" if msg.get("role") != "assistant" else "model",
                "parts": [{"text": msg.get("content", "")}]
            })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.1),
                "maxOutputTokens": kwargs.get("max_tokens", 4096),
            }
        }
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        resp = httpx.post(url, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        
        return data["candidates"][0]["content"]["parts"][0]["text"]
    
    def get_token_count(self, text: str) -> int:
        return len(text) // 4

class VLLMProvider(LLMProvider):
    """vLLM inference server provider."""
    def __init__(self, model: str, base_url: str, api_key: str = None):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key or "dummy", base_url=f"{self.base_url}/v1")
    
    def generate(self, messages: list[dict], stream: bool = False, **kwargs):
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
            **kwargs
        )
        if stream:
            return (c.choices[0].delta.content or "" for c in resp)
        return resp.choices[0].message.content
    
    def get_token_count(self, text: str) -> int:
        return len(text) // 4

# ─── LLM Factory ──────────────────────────────────────────────────────────────

LLM_PROVIDERS = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "ollama": OllamaProvider,
    "groq": GroqProvider,
    "gemini": GeminiProvider,
    "vllm": VLLMProvider,
}

def create_llm_provider(provider: str, **kwargs) -> LLMProvider:
    """Create an LLM provider by name."""
    provider = provider.lower()
    if provider not in LLM_PROVIDERS:
        raise ValueError(f"Unknown provider: {provider}. Available: {list(LLM_PROVIDERS.keys())}")
    return LLM_PROVIDERS[provider](**kwargs)

# ─── Session Persistence ──────────────────────────────────────────────────────

class SessionStore(ABC):
    """Abstract base for session persistence."""
    
    @abstractmethod
    def save(self, session_id: str, state: dict) -> None:
        pass
    
    @abstractmethod
    def load(self, session_id: str) -> Optional[dict]:
        pass
    
    @abstractmethod
    def delete(self, session_id: str) -> None:
        pass

class InMemorySessionStore(SessionStore):
    """In-memory session store (for single-instance deployments)."""
    
    def __init__(self):
        self._store: dict[str, dict] = {}
        self._lock = threading.Lock()
    
    def save(self, session_id: str, state: dict) -> None:
        with self._lock:
            self._store[session_id] = {
                "state": state,
                "updated_at": datetime.utcnow().isoformat()
            }
    
    def load(self, session_id: str) -> Optional[dict]:
        with self._lock:
            return self._store.get(session_id, {}).get("state")
    
    def delete(self, session_id: str) -> None:
        with self._lock:
            self._store.pop(session_id, None)

class RedisSessionStore(SessionStore):
    """Redis-backed session store (for distributed deployments)."""
    
    def __init__(self, url: str = "redis://localhost:6379"):
        import redis
        self.redis = redis.from_url(url)
        self.prefix = "namakan:session:"
    
    def save(self, session_id: str, state: dict) -> None:
        self.redis.set(f"{self.prefix}{session_id}", json.dumps(state))
    
    def load(self, session_id: str) -> Optional[dict]:
        data = self.redis.get(f"{self.prefix}{session_id}")
        return json.loads(data) if data else None
    
    def delete(self, session_id: str) -> None:
        self.redis.delete(f"{self.prefix}{session_id}")

class PostgresSessionStore(SessionStore):
    """PostgreSQL-backed session store."""
    
    def __init__(self, url: str = None):
        import os
        url = url or os.environ.get("DATABASE_URL")
        import psycopg2
        self.conn = psycopg2.connect(url)
        self._url = url  # Store for reconnect if needed
        # Create table if not exists
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS agent_sessions (
                    session_id VARCHAR(255) PRIMARY KEY,
                    state JSONB NOT NULL,
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
            self.conn.commit()
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    def save(self, session_id: str, state: dict) -> None:
        import psycopg2.extras
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO agent_sessions (session_id, state, updated_at)
                VALUES (%s, %s, NOW())
                ON CONFLICT (session_id) DO UPDATE SET state = %s, updated_at = NOW()
            """, (session_id, json.dumps(state), json.dumps(state)))
        self.conn.commit()
    
    def load(self, session_id: str) -> Optional[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT state FROM agent_sessions WHERE session_id = %s", (session_id,))
            row = cur.fetchone()
            return row[0] if row else None
    
    def delete(self, session_id: str) -> None:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM agent_sessions WHERE session_id = %s", (session_id,))
        self.conn.commit()

# ─── Metrics Helper ───────────────────────────────────────────────────────────

def record_metric(name: str, value: float = 1, labels: dict = None):
    """Record a metric if prometheus is available."""
    if METRICS.get(name) is not None:
        metric = METRICS[name]
        if labels:
            metric.labels(**labels).inc(value) if isinstance(metric, Counter) or isinstance(metric, Gauge) else metric.labels(**labels).observe(value)
        else:
            metric.inc(value) if isinstance(metric, Counter) else metric.observe(value)

# ─── Agent ─────────────────────────────────────────────────────────────────────

@dataclass
class AgentConfig:
    name: str
    role: str
    instructions: str
    tools: list[Tool] = field(default_factory=list)
    max_iterations: int = 20
    max_self_corrections: int = 3  # Cap self-correction loops to prevent infinite loops
    escalation_threshold: int = 3
    self_correct: bool = True  # Enable self-correction
    verbose: bool = True
    session_id: str = None
    session_store: SessionStore = None

class AgenticWorkflow:
    """
    ReAct-style agentic workflow engine with:
    - Multi-LLM support (OpenAI, Anthropic, Ollama, Groq, Gemini, vLLM)
    - Streaming responses
    - Self-correction loops
    - Prometheus metrics
    - Structured logging (Loki-compatible)
    - Session persistence
    """
    
    def __init__(self, config: AgentConfig, llm_provider: str = "ollama", **llm_kwargs):
        self.config = config
        self.llm_provider_name = llm_provider
        self._llm: Optional[LLMProvider] = None
        self._llm_kwargs = llm_kwargs
        
        # Session management
        self.session_store = config.session_store or InMemorySessionStore()
        self.session_id = config.session_id or f"agent_{int(time.time())}_{os.urandom(4).hex()}"
        
        # Load existing session state
        self.state = self.session_store.load(self.session_id) or {
            "status": AgentState.PENDING,
            "history": [],
            "tool_calls": [],
            "iterations": 0,
            "escalations": 0,
            "self_corrections": 0,
            "last_output": None,
            "messages": [],
            "context": {},
        }
        
        # Register tools
        self.tools: dict[str, Tool] = {}
        for tool in config.tools:
            self.tools[tool.name] = tool
        
        # Built-in tools
        for name, cls in BUILTIN_TOOLS.items():
            if name not in self.tools:
                self.tools[name] = cls()
        
        self._setup_llm()
    
    def _setup_llm(self):
        """Initialize LLM provider."""
        self._llm = create_llm_provider(self.llm_provider_name, **self._llm_kwargs)
        LOG.info("llm_initialized", provider=self.llm_provider_name, model=self._llm_kwargs.get("model", "default"))
    
    def _save_session(self):
        """Persist session state."""
        self.session_store.save(self.session_id, self.state)
    
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
- If a tool fails or returns unexpected results, try a different approach

When using a tool, respond in this format:
THINK: [what you're going to do]
ACTION: tool_name
ACTION_INPUT: {{"param": "value"}}
"""
    
    def _generate(self, messages: list[dict], stream: bool = False, **kwargs):
        """Generate from LLM with metrics."""
        start = time.time()
        try:
            result = self._llm.generate(messages, stream=stream, **kwargs)
            duration = time.time() - start
            
            # Record metrics
            if not stream:
                tokens = self._llm.get_token_count(str(result))
                record_metric("llm_tokens_total", tokens, {"workflow": self.session_id, "provider": self.llm_provider_name, "model": self._llm_kwargs.get("model", "default")})
                LOG.info("llm_generated", provider=self.llm_provider_name, tokens=tokens, duration=duration)
            
            return result
        except Exception as e:
            LOG.error("llm_error", error=str(e), provider=self.llm_provider_name)
            record_metric("errors_total", 1, {"workflow": self.session_id, "error_type": "llm_error"})
            raise
    
    def _parse_response(self, response: str) -> tuple[Optional[str], Optional[dict]]:
        """Parse LLM response for action blocks."""
        action_match = re.search(r'ACTION:\s*(\w+)', response)
        input_match = re.search(r'ACTION_INPUT:\s*(\{.*?\})', response, re.DOTALL)
        
        action_name = action_match.group(1) if action_match else None
        input_data = {}
        if input_match:
            try:
                input_data = json.loads(input_match.group(1))
            except json.JSONDecodeError:
                pass
        
        return action_name, input_data
    
    def _self_correct(self, error_context: str) -> str:
        """
        Self-correction: Analyze error and generate a corrected approach.
        This is called when a tool fails or returns unexpected results.
        Respects max_self_corrections to prevent infinite loops.
        """
        # Check if we've exceeded the correction limit
        if self.state["self_corrections"] >= self.config.max_self_corrections:
            LOG.warning("self_correction_skipped", reason="max_corrections_reached", 
                       corrections=self.state["self_corrections"], 
                       max=self.config.max_self_corrections)
            return f"SKIP: Max self-corrections ({self.config.max_self_corrections}) reached. Aborting correction."
        
        self.state["self_corrections"] += 1
        record_metric("self_corrections", labels={"workflow": self.session_id})
        
        LOG.info("self_correction_triggered", reason=error_context, corrections=self.state["self_corrections"])
        
        messages = self.state.get("messages", [])
        correction_prompt = f"""\
The previous approach failed or produced unexpected results.
Error context: {error_context}

Analyze what went wrong and provide a NEW approach to complete the task.
Think carefully about an alternative strategy.

THINK: [analysis of what went wrong]
THINK: [alternative approach]
ACTION: tool_name (or "done" if task is complete)
ACTION_INPUT: {{"param": "value"}}
"""
        messages.append({"role": "user", "content": correction_prompt})
        
        response = self._generate(messages)
        self.state["messages"].append({"role": "assistant", "content": response})
        return response
    
    def _execute_tool(self, action_name: str, action_input: dict) -> ToolResult:
        """Execute a tool with metrics."""
        if action_name not in self.tools:
            return ToolResult(success=False, output=None, error=f"Unknown tool: {action_name}")
        
        tool = self.tools[action_name]
        start = time.time()
        workflow_label = {"workflow": self.session_id}
        
        try:
            result = tool.run(**action_input)
            duration = time.time() - start
            
            record_metric("tool_calls_total", 1, {"workflow": self.session_id, "tool_name": action_name, "status": "success" if result.success else "failure"})
            record_metric("tool_duration", duration, {"workflow": self.session_id, "tool_name": action_name})
            
            LOG.info("tool_executed", tool=action_name, success=result.success, duration=duration)
            
            return result
        except Exception as e:
            duration = time.time() - start
            record_metric("tool_calls_total", 1, {"workflow": self.session_id, "tool_name": action_name, "status": "error"})
            record_metric("errors_total", 1, {"workflow": self.session_id, "error_type": "tool_error"})
            
            LOG.error("tool_error", tool=action_name, error=str(e))
            
            return ToolResult(success=False, output=None, error=str(e))
    
    def run(self, task: str, context: dict = None) -> dict:
        """Run the agent workflow synchronously."""
        self.state["status"] = AgentState.RUNNING
        workflow_label = {"workflow": self.session_id}
        record_metric("executions_total", labels=workflow_label)
        record_metric("executions_running", 1, labels=workflow_label)
        
        start_time = time.time()
        
        try:
            messages = [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": f"Task: {task}"}
            ]
            if context:
                messages.append({"role": "system", "content": f"Context: {json.dumps(context)}"})
            
            self.state["messages"] = messages
            self.state["context"] = context or {}
            
            while self.state["iterations"] < self.config.max_iterations:
                self.state["iterations"] += 1
                step_start = time.time()
                
                if self.config.verbose:
                    print(f"\n[Iteration {self.state['iterations']}]")
                
                # Generate
                response = self._generate(messages)
                messages.append({"role": "assistant", "content": response})
                self.state["messages"] = messages
                self.state["history"].append(("assistant", response))
                
                # Parse action
                action_name, action_input = self._parse_response(response)
                
                if self.config.verbose and action_name:
                    print(f"  → Action: {action_name}")
                
                # Execute
                if action_name == "human_escalate":
                    tool_result = self.tools["human_escalate"].run(**action_input)
                    self.state["escalations"] += 1
                    record_metric("escalations_total", 1, {"workflow": self.session_id, "urgency": action_input.get("urgency", "medium")})
                    
                    messages.append({
                        "role": "user",
                        "content": f"Human responded: {tool_result.output}"
                    })
                    self.state["messages"] = messages
                    self.state["history"].append(("human", tool_result.output))
                    continue
                
                elif action_name and action_name in self.tools:
                    tool_result = self._execute_tool(action_name, action_input)
                    
                    result_text = f"Tool result: {tool_result.output}"
                    if tool_result.error:
                        result_text += f"\nError: {tool_result.error}"
                    
                    messages.append({"role": "user", "content": result_text})
                    self.state["messages"] = messages
                    self.state["history"].append(("tool", result_text))
                    self.state["tool_calls"].append({
                        "tool": action_name,
                        "input": action_input,
                        "result": tool_result.output,
                        "success": tool_result.success,
                    })
                    
                    if self.config.verbose:
                        output_str = str(tool_result.output)[:100] if tool_result.output else "None"
                        print(f"    Result: {output_str}")
                    
                    # Self-correction on failure
                    if not tool_result.success and self.config.self_correct:
                        correction = self._self_correct(f"Tool {action_name} failed: {tool_result.error}")
                        messages.append({"role": "assistant", "content": correction})
                        self.state["messages"] = messages
                        continue
                    
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
                
                # Record step duration
                record_metric("step_duration", time.time() - step_start, labels=workflow_label)
            
            else:
                self.state["status"] = AgentState.FAILED
                self.state["last_output"] = "Max iterations reached"
            
            # Record execution duration
            record_metric("execution_duration", time.time() - start_time, labels=workflow_label)
            
            # Save session
            self._save_session()
            
            return self.state
        
        finally:
            record_metric("executions_running", -1)
    
    async def run_async(self, task: str, context: dict = None) -> dict:
        """Run the agent workflow asynchronously."""
        # For now, just run sync and wrap
        return self.run(task, context)
    
    def run_stream(self, task: str, context: dict = None) -> AsyncIterator[dict]:
        """
        Stream the agent's response as SSE events.
        Yields dicts with keys: type (think/action/result/stream), content.
        """
        self.state["status"] = AgentState.RUNNING
        record_metric("executions_total")
        
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": f"Task: {task}"}
        ]
        if context:
            messages.append({"role": "system", "content": f"Context: {json.dumps(context)}"})
        
        self.state["messages"] = messages
        
        try:
            while self.state["iterations"] < self.config.max_iterations:
                self.state["iterations"] += 1
                
                # Stream the LLM response
                full_response = ""
                for chunk in self._generate(messages, stream=True):
                    full_response += chunk
                    yield {"type": "stream", "content": chunk}
                
                messages.append({"role": "assistant", "content": full_response})
                self.state["messages"] = messages
                
                # Parse and execute action
                action_name, action_input = self._parse_response(full_response)
                
                yield {"type": "think", "content": f"Action: {action_name}"}
                
                if action_name and action_name in self.tools:
                    tool_result = self._execute_tool(action_name, action_input)
                    
                    result_text = f"Tool result: {tool_result.output}"
                    if tool_result.error:
                        result_text += f"\nError: {tool_result.error}"
                    
                    yield {"type": "result", "content": result_text, "success": tool_result.success}
                    
                    messages.append({"role": "user", "content": result_text})
                    self.state["messages"] = messages
                    
                    if "DONE" in full_response.upper():
                        self.state["status"] = AgentState.COMPLETED
                        self.state["last_output"] = full_response
                        break
                elif not action_name:
                    if any(word in full_response.upper() for word in ["DONE", "COMPLETE"]):
                        self.state["status"] = AgentState.COMPLETED
                        self.state["last_output"] = full_response
                        break
            
            self._save_session()
            yield {"type": "done", "status": self.state["status"].value}
        
        except Exception as e:
            yield {"type": "error", "content": str(e)}
            self.state["status"] = AgentState.FAILED
    
    def resume(self) -> dict:
        """Resume an interrupted session."""
        if self.state["status"] not in (AgentState.RUNNING, AgentState.WAITING_HUMAN):
            raise RuntimeError(f"Cannot resume session in state: {self.state['status']}")
        
        self.state["status"] = AgentState.RUNNING
        messages = self.state.get("messages", [])
        
        if not messages:
            raise RuntimeError("No messages in session to resume from")
        
        # Continue the loop
        while self.state["iterations"] < self.config.max_iterations:
            self.state["iterations"] += 1
            
            response = self._generate(messages)
            messages.append({"role": "assistant", "content": response})
            
            action_name, action_input = self._parse_response(response)
            
            if action_name and action_name in self.tools:
                tool_result = self._execute_tool(action_name, action_input)
                
                messages.append({"role": "user", "content": f"Tool result: {tool_result.output}"})
                
                if "DONE" in response.upper():
                    self.state["status"] = AgentState.COMPLETED
                    break
            elif not action_name and any(word in response.upper() for word in ["DONE", "COMPLETE"]):
                self.state["status"] = AgentState.COMPLETED
                break
        
        self.state["messages"] = messages
        self._save_session()
        return self.state

# ─── Multi-Agent Orchestration ────────────────────────────────────────────────

class SupervisorAgent:
    """
    Multi-agent supervisor that can delegate tasks to worker agents.
    Implements a supervisor/worker pattern similar to LangGraph's supervisor.
    """
    
    def __init__(self, workers: dict[str, AgenticWorkflow], supervisor_llm: str = "ollama", **llm_kwargs):
        self.workers = workers
        self.worker_names = list(workers.keys())
        
        # Supervisor uses its own LLM for routing decisions
        self._supervisor = create_llm_provider(supervisor_llm, **llm_kwargs)
        
        self.state = {
            "status": AgentState.PENDING,
            "tasks": {},
            "completed_tasks": [],
            "failed_tasks": [],
        }
    
    def _get_worker_prompt(self) -> str:
        """Build prompt describing available workers."""
        worker_descs = []
        for name, worker in self.workers.items():
            tools = list(worker.tools.keys())
            worker_descs.append(f"- {name}: {worker.config.role}. Tools: {', '.join(tools)}")
        
        return f"""\
You are a Supervisor Agent that coordinates multiple specialized workers.

Available workers:
{chr(10).join(worker_descs)}

Your job:
1. Analyze the user's complex task
2. Break it into subtasks
3. Delegate each subtask to the appropriate worker
4. Synthesize results from all workers
5. Present a unified response

When delegating, respond in this format:
DELEGATE_TO: worker_name
TASK: [specific task description]
"""
    
    def run(self, task: str) -> dict:
        """Run a multi-agent task with supervisor routing."""
        self.state["status"] = AgentState.RUNNING
        
        messages = [
            {"role": "system", "content": self._get_worker_prompt()},
            {"role": "user", "content": f"Complex task: {task}"}
        ]
        
        max_loops = 10
        loops = 0
        
        while loops < max_loops:
            loops += 1
            
            response = self._supervisor.generate(messages)
            messages.append({"role": "assistant", "content": response})
            
            # Check if done
            if "COMPLETE" in response.upper():
                self.state["status"] = AgentState.COMPLETED
                break
            
            # Parse delegation
            delegate_match = re.search(r'DELEGATE_TO:\s*(\w+)', response)
            task_match = re.search(r'TASK:\s*(.+?)(?=\n\n|$)', response, re.DOTALL)
            
            if delegate_match and task_match:
                worker_name = delegate_match.group(1)
                subtask = task_match.group(1).strip()
                
                if worker_name in self.workers:
                    worker = self.workers[worker_name]
                    
                    # Run the worker
                    result = worker.run(subtask)
                    self.state["tasks"][subtask] = result
                    
                    if result["status"] == AgentState.COMPLETED.value:
                        self.state["completed_tasks"].append(subtask)
                        messages.append({"role": "user", "content": f"Worker {worker_name} completed: {result.get('last_output', '')}"})
                    else:
                        self.state["failed_tasks"].append(subtask)
                        messages.append({"role": "user", "content": f"Worker {worker_name} failed: {result.get('last_output', '')}"})
                else:
                    messages.append({"role": "user", "content": f"Unknown worker: {worker_name}. Available: {self.worker_names}"})
            else:
                # No more delegation, assume complete
                self.state["status"] = AgentState.COMPLETED
                break
        
        self.state["last_output"] = messages[-1]["content"] if messages else ""
        return self.state

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

BUILTIN_TOOLS = {
    "web_search": WebSearchTool,
    "file_read": FileReadTool,
    "file_write": FileWriteTool,
    "run_command": CommandTool,
    "human_escalate": HumanEscalateTool,
}

# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Namakan Agentic Workflow Engine v2.0")
    parser.add_argument("--task", "-t", required=True, help="The task to perform")
    parser.add_argument("--role", "-r", default="AI Assistant", help="Agent role")
    parser.add_argument("--instructions", help="System instructions file")
    parser.add_argument("--provider", "-p", default="ollama", help="LLM provider (openai|anthropic|ollama|groq|gemini|vllm)")
    parser.add_argument("--model", "-m", default=None, help="Model name")
    parser.add_argument("--base-url", default=None, help="Base URL for Ollama/vLLM")
    parser.add_argument("--session-id", default=None, help="Session ID for persistence")
    parser.add_argument("--stream", "-s", action="store_true", help="Stream responses")
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
        session_id=args.session_id,
    )
    
    llm_kwargs = {}
    if args.model:
        llm_kwargs["model"] = args.model
    if args.base_url:
        llm_kwargs["base_url"] = args.base_url
    
    agent = AgenticWorkflow(config, llm_provider=args.provider, **llm_kwargs)
    
    if args.stream:
        print("Starting streaming response...")
        for event in agent.run_stream(args.task):
            if event["type"] == "stream":
                print(event["content"], end="", flush=True)
            elif event["type"] == "think":
                print(f"\n[Thinking] {event['content']}", flush=True)
            elif event["type"] == "result":
                print(f"\n[Result] {event['content'][:100]}...", flush=True)
            elif event["type"] == "done":
                print(f"\n\nCompleted with status: {event['status']}")
    else:
        result = agent.run(args.task)
        
        print("\n" + "=" * 60)
        print("RESULT")
        print("=" * 60)
        print(f"Status: {result['status'].value}")
        print(f"Iterations: {result['iterations']}")
        print(f"Escalations: {result['escalations']}")
        print(f"Self-corrections: {result.get('self_corrections', 0)}")
        print(f"Output: {result['last_output']}")
        print(f"Session ID: {agent.session_id}")

if __name__ == "__main__":
    main()
