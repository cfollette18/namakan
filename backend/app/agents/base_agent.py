from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
import structlog

logger = structlog.get_logger()

class AgentContext(BaseModel):
    """Context passed to agents"""
    project_id: str
    task_description: str
    shared_context: Dict[str, Any] = {}
    user_feedback: List[Dict[str, Any]] = []
    dependencies_outputs: Dict[str, Any] = {}

class AgentOutput(BaseModel):
    """Output produced by an agent"""
    agent_id: str
    agent_role: str
    content: Dict[str, Any]
    confidence: float
    timestamp: datetime
    event_type: str
    reasoning: Optional[str] = None

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(
        self,
        agent_id: str,
        role: str,
        responsibilities: List[str],
        tools: List[str],
        personality: str = "professional",
        constraints: List[str] = None
    ):
        self.agent_id = agent_id
        self.role = role
        self.responsibilities = responsibilities
        self.tools = tools
        self.personality = personality
        self.constraints = constraints or []
        self.memory: List[Dict[str, Any]] = []
    
    @abstractmethod
    async def execute(self, context: AgentContext) -> AgentOutput:
        """Execute the agent's task"""
        pass
    
    @abstractmethod
    async def reason(self, context: AgentContext) -> Dict[str, Any]:
        """Agent decides its next action"""
        pass
    
    def add_to_memory(self, item: Dict[str, Any]):
        """Add item to agent's memory"""
        self.memory.append(item)
    
    async def critique_output(self, output: AgentOutput, context: AgentContext) -> Dict[str, Any]:
        """Agent critiques its own work"""
        # Default implementation - can be overridden
        return {
            "quality_score": 0.8,
            "issues": [],
            "strengths": ["Completed task"],
            "overall_assessment": "Task completed successfully"
        }
    
    def get_system_prompt(self) -> str:
        """Generate system prompt for this agent"""
        return f"""
You are a world-class {self.role}.

Your responsibilities include:
{chr(10).join(f"- {r}" for r in self.responsibilities)}

Your personality: {self.personality}

You have access to these tools:
{chr(10).join(f"- {t}" for t in self.tools)}

Constraints:
{chr(10).join(f"- {c}" for c in self.constraints)}

When working with other agents:
- Share findings transparently
- Ask clarifying questions when uncertain
- Flag risks and limitations
- Cite sources for all claims
"""
