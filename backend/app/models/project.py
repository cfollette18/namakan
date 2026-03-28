from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    NEEDS_REVIEW = "needs_review"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ProjectComplexity(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10)
    user_id: str
    timeline: Optional[str] = None
    budget: Optional[float] = None

class AgentSpec(BaseModel):
    role: str
    responsibilities: List[str]
    tools: List[str]
    dependencies: List[str] = []

class ProjectPlan(BaseModel):
    project_id: str
    objective: str
    timeline: str
    complexity_score: float
    required_agents: List[AgentSpec]
    execution_plan: Dict[str, List[str]]
    estimated_completion: str
    checkpoints: List[Dict[str, str]]

class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str
    status: ProjectStatus
    complexity: ProjectComplexity
    user_id: str
    created_at: datetime
    updated_at: datetime
    agent_count: int
    completion_percentage: float
    estimated_cost: float

class ProjectDetail(ProjectResponse):
    plan: Optional[ProjectPlan] = None
    active_agents: List[str] = []
    completed_agents: List[str] = []
    deliverables: List[Dict[str, Any]] = []
