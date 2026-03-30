from typing import List, Optional
from app.models.agent import AgentResponse, AgentDetail, AgentStatus
from app.db.models import Agent as AgentModel, Project as ProjectModel
import structlog

logger = structlog.get_logger()


class AgentService:
    """Service for managing agents"""

    async def list_project_agents(self, project_id: str) -> List[AgentResponse]:
        """List all agents for a project"""
        try:
            agents = await AgentModel.filter(project_id=project_id)
            return [
                AgentResponse(
                    id=a.id,
                    name=a.role,
                    project_id=a.project_id,
                    role=a.role,
                    status=AgentStatus(a.status or "idle"),
                    created_at=a.created_at.isoformat() if a.created_at else "",
                    updated_at=a.updated_at.isoformat() if a.updated_at else "",
                )
                for a in agents
            ]
        except Exception as e:
            logger.warning("Failed to list project agents", project_id=project_id, error=str(e))
            return []

    async def get_agent(self, agent_id: str) -> Optional[AgentDetail]:
        """Get agent details with events"""
        try:
            agent = await AgentModel.find_first(where={"id": agent_id})
            if not agent:
                return None
            return AgentDetail(
                id=agent.id,
                name=agent.role,
                project_id=agent.project_id,
                role=agent.role,
                status=AgentStatus(agent.status or "idle"),
                created_at=agent.created_at.isoformat() if agent.created_at else "",
                updated_at=agent.updated_at.isoformat() if agent.updated_at else "",
                events=[],
            )
        except Exception as e:
            logger.warning("Failed to get agent", agent_id=agent_id, error=str(e))
            return None

    async def process_feedback(self, agent_id: str, feedback: dict):
        """Process user feedback for an agent"""
        logger.info("Processing feedback", agent_id=agent_id)
        try:
            # Log feedback as an event on the agent
            from app.core.event_store import EventStore
            store = EventStore()
            await store.append(
                project_id=feedback.get("project_id", ""),
                agent_id=agent_id,
                event_type="user_feedback",
                event_data={"feedback": feedback},
                confidence_score=1.0,
            )
            store.close()
            logger.info("Feedback processed and stored", agent_id=agent_id)
        except Exception as e:
            logger.warning("Failed to process feedback", agent_id=agent_id, error=str(e))