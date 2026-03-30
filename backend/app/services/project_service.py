from typing import List, Optional
from app.models.project import (
    ProjectCreate, ProjectResponse, ProjectDetail, ProjectPlan,
    ProjectStatus, ProjectComplexity
)
from datetime import datetime
import uuid
import structlog

logger = structlog.get_logger()

class ProjectService:
    """Service for managing projects"""
    
    async def create_project(self, project: ProjectCreate) -> ProjectDetail:
        """Create a new project and generate agent team"""
        logger.info("Creating project", name=project.name)
        
        # Generate project ID
        project_id = str(uuid.uuid4())
        
        # Analyze project and create plan
        plan = await self._generate_project_plan(project_id, project)
        
        # Create project response
        result = ProjectDetail(
            id=project_id,
            name=project.name,
            description=project.description,
            status=ProjectStatus.CREATED,
            complexity=self._determine_complexity(plan.complexity_score),
            user_id=project.user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            agent_count=len(plan.required_agents),
            completion_percentage=0.0,
            estimated_cost=self._estimate_cost(plan),
            plan=plan,
            active_agents=[],
            completed_agents=[],
            deliverables=[]
        )

        try:
            from app.db.models import Project as ProjectModel
            await ProjectModel.create(
                id=project_id,
                user_id=project.user_id,
                name=project.name,
                description=project.description,
                status="active",
                project_type=None,
                industry=None,
                config={},
            )
            logger.info("Project saved to database", project_id=project_id)
        except Exception as e:
            logger.error("Failed to save project to database", project_id=project_id, error=str(e))

        logger.info("Project created", project_id=project_id, agent_count=len(plan.required_agents))
        return result
    
    async def _generate_project_plan(self, project_id: str, project: ProjectCreate) -> ProjectPlan:
        """Use Orchestrator Agent to generate project plan"""
        # TODO: Implement actual orchestrator agent
        # For now, return a sample plan
        
        from app.models.project import AgentSpec
        
        return ProjectPlan(
            project_id=project_id,
            objective=project.description,
            timeline=project.timeline or "5 days",
            complexity_score=7.5,
            required_agents=[
                AgentSpec(
                    role="Research Agent",
                    responsibilities=["Market research", "Competitor analysis"],
                    tools=["web_browser", "data_analyzer"],
                    dependencies=[]
                ),
                AgentSpec(
                    role="Strategy Agent",
                    responsibilities=["Positioning", "Messaging"],
                    tools=["document_writer", "strategy_frameworks"],
                    dependencies=["Research Agent"]
                ),
                AgentSpec(
                    role="Copywriter Agent",
                    responsibilities=["Copy writing", "Content creation"],
                    tools=["document_writer", "brand_voice_analyzer"],
                    dependencies=["Strategy Agent"]
                )
            ],
            execution_plan={
                "phase_1": ["Research Agent"],
                "phase_2": ["Strategy Agent"],
                "phase_3": ["Copywriter Agent"]
            },
            estimated_completion="4 days, 6 hours",
            checkpoints=[
                {"day": "2", "deliverable": "Research findings"},
                {"day": "4", "deliverable": "Final deliverables"}
            ]
        )
    
    def _determine_complexity(self, score: float) -> ProjectComplexity:
        """Determine project complexity from score"""
        if score < 4.0:
            return ProjectComplexity.SIMPLE
        elif score < 7.0:
            return ProjectComplexity.MEDIUM
        elif score < 9.0:
            return ProjectComplexity.COMPLEX
        else:
            return ProjectComplexity.ENTERPRISE
    
    def _estimate_cost(self, plan: ProjectPlan) -> float:
        """Estimate project cost"""
        # Simple estimation: $50 per agent
        return len(plan.required_agents) * 50.0
    
    async def list_projects(self, user_id: str, skip: int = 0, limit: int = 20) -> List[ProjectResponse]:
        """List projects for a user"""
        try:
            from app.db.models import Project as ProjectModel
            projects = await ProjectModel.find_many(
                where={"user_id": user_id},
                skip=skip,
                take=limit,
                order={"created_at": "desc"},
            )
            return [
                ProjectResponse(
                    id=p.id,
                    name=p.name,
                    description=p.description or "",
                    status=p.status or "active",
                    complexity=p.complexity or "medium",
                    user_id=p.user_id,
                    created_at=p.created_at.isoformat() if p.created_at else "",
                    updated_at=p.updated_at.isoformat() if p.updated_at else "",
                    agent_count=0,
                    completion_percentage=0.0,
                    estimated_cost=0.0,
                )
                for p in projects
            ]
        except Exception as e:
            logger.warning("Failed to list projects", user_id=user_id, error=str(e))
            return []

    async def get_project(self, project_id: str) -> Optional[ProjectDetail]:
        """Get project details"""
        try:
            from app.db.models import Project as ProjectModel
            p = await ProjectModel.find_first(where={"id": project_id})
            if not p:
                return None
            return ProjectDetail(
                id=p.id,
                name=p.name,
                description=p.description or "",
                status=p.status or "active",
                complexity=p.complexity or "medium",
                user_id=p.user_id,
                created_at=p.created_at.isoformat() if p.created_at else "",
                updated_at=p.updated_at.isoformat() if p.updated_at else "",
                agent_count=0,
                completion_percentage=0.0,
                estimated_cost=0.0,
            )
        except Exception as e:
            logger.warning("Failed to get project", project_id=project_id, error=str(e))
            return None

    async def start_project(self, project_id: str):
        """Start project execution"""
        logger.info("Starting project", project_id=project_id)
        try:
            from app.db.models import Project as ProjectModel
            await ProjectModel.update(
                where={"id": project_id},
                data={"status": "in_progress"},
            )
            logger.info("Project started", project_id=project_id)
        except Exception as e:
            logger.error("Failed to start project", project_id=project_id, error=str(e))

    async def cancel_project(self, project_id: str):
        """Cancel a running project"""
        logger.info("Cancelling project", project_id=project_id)
        try:
            from app.db.models import Project as ProjectModel
            await ProjectModel.update(
                where={"id": project_id},
                data={"status": "cancelled"},
            )
            logger.info("Project cancelled", project_id=project_id)
        except Exception as e:
            logger.error("Failed to cancel project", project_id=project_id, error=str(e))
