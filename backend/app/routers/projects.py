from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.project import ProjectCreate, ProjectResponse, ProjectDetail
from app.services.project_service import ProjectService
import structlog

logger = structlog.get_logger()

router = APIRouter()

@router.post("/", response_model=ProjectDetail)
async def create_project(project: ProjectCreate):
    """Create a new project and generate agent team"""
    try:
        service = ProjectService()
        result = await service.create_project(project)
        return result
    except Exception as e:
        logger.error("Error creating project", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(user_id: str, skip: int = 0, limit: int = 20):
    """List all projects for a user"""
    try:
        service = ProjectService()
        projects = await service.list_projects(user_id, skip, limit)
        return projects
    except Exception as e:
        logger.error("Error listing projects", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}", response_model=ProjectDetail)
async def get_project(project_id: str):
    """Get detailed project information"""
    try:
        service = ProjectService()
        project = await service.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting project", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/start")
async def start_project(project_id: str):
    """Start project execution"""
    try:
        service = ProjectService()
        result = await service.start_project(project_id)
        return {"status": "started", "project_id": project_id}
    except Exception as e:
        logger.error("Error starting project", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/cancel")
async def cancel_project(project_id: str):
    """Cancel a running project"""
    try:
        service = ProjectService()
        await service.cancel_project(project_id)
        return {"status": "cancelled", "project_id": project_id}
    except Exception as e:
        logger.error("Error cancelling project", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
