from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class AgentStatus(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class AgentType(str, Enum):
    ORCHESTRATOR = "orchestrator"
    SUPERVISOR = "supervisor"
    WORKER = "worker"

class AgentCreate(BaseModel):
    role: str
    agent_type: AgentType
    project_id: str
    responsibilities: List[str]
    tools: List[str]
    personality: Optional[str] = None

class AgentOutput(BaseModel):
    agent_id: str
    content: Dict[str, Any]
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime
    event_type: str

class AgentAction(BaseModel):
    agent_id: str
    action_type: str
    action_data: Dict[str, Any]
    reasoning: Optional[str] = None
    timestamp: datetime

class AgentResponse(BaseModel):
    id: str
    role: str
    agent_type: AgentType
    status: AgentStatus
    project_id: str
    progress: float = Field(..., ge=0.0, le=100.0)
    current_task: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class AgentDetail(AgentResponse):
    responsibilities: List[str]
    tools: List[str]
    recent_actions: List[AgentAction] = []
    outputs: List[AgentOutput] = []
    confidence_score: float = 0.0
