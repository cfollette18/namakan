from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, END
from app.agents.orchestrator_agent import OrchestratorAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.worker_agent import WorkerAgent, ResearchAgent, StrategyAgent, CopywriterAgent
from app.agents.base_agent import AgentContext
import structlog

logger = structlog.get_logger()

class ProjectState(TypedDict):
    """State that flows through the workflow"""
    project_id: str
    current_phase: str
    phase_outputs: Dict[str, Any]
    user_approvals: Dict[str, bool]
    error_count: int
    context: AgentContext


class MultiAgentWorkflow:
    """
    LangGraph-based workflow for multi-agent coordination
    Manages phase transitions and agent execution
    """
    
    def __init__(self, project_id: str, task_description: str):
        self.project_id = project_id
        self.task_description = task_description
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(ProjectState)
        
        # Add nodes (each is a phase supervisor)
        workflow.add_node("orchestration", self._orchestration_phase)
        workflow.add_node("research_phase", self._research_phase)
        workflow.add_node("strategy_phase", self._strategy_phase)
        workflow.add_node("creative_phase", self._creative_phase)
        workflow.add_node("user_checkpoint", self._user_checkpoint)
        workflow.add_node("error_handler", self._error_handler)
        
        # Add edges (routing logic)
        workflow.set_entry_point("orchestration")
        workflow.add_edge("orchestration", "research_phase")
        workflow.add_edge("research_phase", "user_checkpoint")
        
        workflow.add_conditional_edges(
            "user_checkpoint",
            self._route_after_checkpoint,
            {
                "approved_research": "strategy_phase",
                "approved_strategy": "creative_phase",
                "approved_creative": END,
                "revision_requested": "error_handler",
                "abandoned": END
            }
        )
        
        workflow.add_edge("strategy_phase", "user_checkpoint")
        workflow.add_edge("creative_phase", "user_checkpoint")
        workflow.add_edge("error_handler", "research_phase")
        
        return workflow.compile()
    
    async def _orchestration_phase(self, state: ProjectState) -> ProjectState:
        """Orchestrator analyzes task and creates plan"""
        logger.info("Starting orchestration phase", project_id=state["project_id"])
        
        # Create orchestrator agent
        orchestrator = OrchestratorAgent(agent_id="orchestrator-1")
        
        # Execute orchestration
        context = AgentContext(
            project_id=state["project_id"],
            task_description=self.task_description,
            shared_context={}
        )
        
        result = await orchestrator.execute(context)
        
        # Update state
        state["phase_outputs"]["orchestration"] = result.content
        state["current_phase"] = "research"
        state["context"] = context
        
        logger.info("Orchestration complete", agents_created=len(result.content.get("required_agents", [])))
        
        return state
    
    async def _research_phase(self, state: ProjectState) -> ProjectState:
        """Research phase with supervisor coordinating workers"""
        logger.info("Starting research phase", project_id=state["project_id"])
        
        # Create research workers
        research_agent = ResearchAgent(agent_id="research-1")
        
        # Create supervisor
        supervisor = SupervisorAgent(
            agent_id="supervisor-research",
            phase_name="Research",
            worker_agents=[research_agent],
            quality_criteria={"has_sources": True, "confidence_above": 0.7}
        )
        
        # Execute phase
        result = await supervisor.execute(state["context"])
        
        # Update state
        state["phase_outputs"]["research"] = result.content
        state["current_phase"] = "research_review"
        
        logger.info("Research phase complete", confidence=result.confidence)
        
        return state
    
    async def _strategy_phase(self, state: ProjectState) -> ProjectState:
        """Strategy phase"""
        logger.info("Starting strategy phase", project_id=state["project_id"])
        
        # Create strategy workers
        strategy_agent = StrategyAgent(agent_id="strategy-1")
        
        # Update context with research results
        state["context"].dependencies_outputs["research"] = state["phase_outputs"]["research"]
        
        # Create supervisor
        supervisor = SupervisorAgent(
            agent_id="supervisor-strategy",
            phase_name="Strategy",
            worker_agents=[strategy_agent],
            quality_criteria={"has_positioning": True, "confidence_above": 0.7}
        )
        
        # Execute phase
        result = await supervisor.execute(state["context"])
        
        # Update state
        state["phase_outputs"]["strategy"] = result.content
        state["current_phase"] = "strategy_review"
        
        logger.info("Strategy phase complete", confidence=result.confidence)
        
        return state
    
    async def _creative_phase(self, state: ProjectState) -> ProjectState:
        """Creative phase (copywriting, design, etc.)"""
        logger.info("Starting creative phase", project_id=state["project_id"])
        
        # Create creative workers
        copywriter_agent = CopywriterAgent(agent_id="copywriter-1")
        
        # Update context with strategy results
        state["context"].dependencies_outputs["strategy"] = state["phase_outputs"]["strategy"]
        
        # Create supervisor
        supervisor = SupervisorAgent(
            agent_id="supervisor-creative",
            phase_name="Creative",
            worker_agents=[copywriter_agent],
            quality_criteria={"has_copy": True, "confidence_above": 0.7}
        )
        
        # Execute phase
        result = await supervisor.execute(state["context"])
        
        # Update state
        state["phase_outputs"]["creative"] = result.content
        state["current_phase"] = "creative_review"
        
        logger.info("Creative phase complete", confidence=result.confidence)
        
        return state
    
    async def _user_checkpoint(self, state: ProjectState) -> ProjectState:
        """User reviews and provides feedback"""
        logger.info("User checkpoint", phase=state["current_phase"])
        
        # In production, this would wait for user input
        # For now, auto-approve
        current_phase = state["current_phase"].replace("_review", "")
        state["user_approvals"][current_phase] = True
        
        logger.info("User approved", phase=current_phase)
        
        return state
    
    async def _error_handler(self, state: ProjectState) -> ProjectState:
        """Handle errors and retries"""
        logger.warning("Error handler triggered", project_id=state["project_id"])
        
        state["error_count"] += 1
        
        if state["error_count"] > 3:
            logger.error("Max retries exceeded", project_id=state["project_id"])
            state["current_phase"] = "failed"
        
        return state
    
    def _route_after_checkpoint(self, state: ProjectState) -> str:
        """Decide routing after user checkpoint"""
        current_phase = state["current_phase"]
        
        if current_phase == "research_review":
            if state["user_approvals"].get("research"):
                return "approved_research"
            else:
                return "revision_requested"
        
        elif current_phase == "strategy_review":
            if state["user_approvals"].get("strategy"):
                return "approved_strategy"
            else:
                return "revision_requested"
        
        elif current_phase == "creative_review":
            if state["user_approvals"].get("creative"):
                return "approved_creative"
            else:
                return "revision_requested"
        
        return "abandoned"
    
    async def run(self) -> Dict[str, Any]:
        """Execute the workflow"""
        logger.info("Starting workflow", project_id=self.project_id)
        
        # Initialize state
        initial_state: ProjectState = {
            "project_id": self.project_id,
            "current_phase": "orchestration",
            "phase_outputs": {},
            "user_approvals": {},
            "error_count": 0,
            "context": AgentContext(
                project_id=self.project_id,
                task_description=self.task_description,
                shared_context={}
            )
        }
        
        # Run workflow
        final_state = await self.workflow.ainvoke(initial_state)
        
        logger.info("Workflow complete", project_id=self.project_id)
        
        return {
            "status": "completed",
            "outputs": final_state["phase_outputs"],
            "approvals": final_state["user_approvals"]
        }


class WorkflowFactory:
    """Factory for creating workflows based on project type"""
    
    @staticmethod
    def create_workflow(
        project_id: str,
        task_description: str,
        project_type: str = "standard"
    ) -> MultiAgentWorkflow:
        """
        Create appropriate workflow for project type
        
        Args:
            project_id: Project UUID
            task_description: User's task description
            project_type: Type of project (standard, rapid, comprehensive)
        
        Returns:
            Configured MultiAgentWorkflow
        """
        # For now, return standard workflow
        # In future, can create different workflows for different project types
        return MultiAgentWorkflow(project_id, task_description)
