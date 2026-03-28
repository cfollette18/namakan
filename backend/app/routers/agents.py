from fastapi import APIRouter, HTTPException
from typing import List
from app.models.agent import AgentResponse, AgentDetail
from app.services.agent_service import AgentService
import structlog

logger = structlog.get_logger()

router = APIRouter()

@router.get("/project/{project_id}", response_model=List[AgentResponse])
async def list_project_agents(project_id: str):
    """List all agents for a project"""
    try:
        service = AgentService()
        agents = await service.list_project_agents(project_id)
        return agents
    except Exception as e:
        logger.error("Error listing agents", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}", response_model=AgentDetail)
async def get_agent(agent_id: str):
    """Get detailed agent information"""
    try:
        service = AgentService()
        agent = await service.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting agent", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{agent_id}/feedback")
async def provide_feedback(agent_id: str, feedback: dict):
    """Provide feedback to an agent"""
    try:
        service = AgentService()
        await service.process_feedback(agent_id, feedback)
        return {"status": "feedback_received", "agent_id": agent_id}
    except Exception as e:
        logger.error("Error providing feedback", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
