from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent, AgentContext, AgentOutput
from app.models.project import AgentSpec, ProjectPlan
from app.services.ai_service import ai_service
from datetime import datetime
import structlog
import json

logger = structlog.get_logger()

class OrchestratorAgent(BaseAgent):
    """
    The CEO - Meta-agent that understands user goals and creates optimal teams
    Uses Claude Opus for maximum intelligence
    """
    
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            role="Orchestrator Agent",
            responsibilities=[
                "Analyze user requests",
                "Break down complex projects",
                "Design optimal agent teams",
                "Create execution plans",
                "Monitor overall progress"
            ],
            tools=[
                "domain_research",
                "task_decomposition",
                "agent_designer",
                "workflow_optimizer"
            ],
            personality="Strategic, analytical, decisive",
            constraints=[
                "Must create achievable plans",
                "Optimize for cost and time",
                "Ensure proper dependencies"
            ]
        )
    
    async def execute(self, context: AgentContext) -> AgentOutput:
        """Analyze task and create agent team"""
        logger.info("Orchestrator analyzing task", project_id=context.project_id)

        try:
            # Step 1: Understand the domain
            domain = await self._analyze_domain(context.task_description)
            logger.info("Domain analyzed", domain=domain)

            # Step 2: Decompose the task
            task_breakdown = await ai_service.decompose_task(context.task_description, domain)
            logger.info("Task decomposed", phases=len(task_breakdown.get("phases", [])))

            # Step 3: Identify required expertise
            expertise = task_breakdown.get("required_expertise", await self._identify_expertise(domain, {}))
            logger.info("Expertise identified", expertise=expertise)

            # Step 4: Design agent team
            agents = await self._design_agent_team(expertise)
            logger.info("Agent team designed", agent_count=len(agents))

            # Step 5: Create execution workflow
            workflow = await self._design_workflow(agents)
            logger.info("Workflow designed", phases=len(workflow))

            return AgentOutput(
                agent_id=self.agent_id,
                agent_role=self.role,
                content={
                    "domain": domain,
                    "task_breakdown": task_breakdown,
                    "required_agents": agents,
                    "execution_plan": workflow,
                    "estimated_timeline": task_breakdown.get("timeline", self._estimate_timeline(agents, workflow)),
                    "risks": task_breakdown.get("risks", [])
                },
                confidence=0.9,
                timestamp=datetime.utcnow(),
                event_type="project_plan_created",
                reasoning="Analyzed domain, decomposed task, identified required expertise, and designed optimal team with workflow"
            )
        except Exception as e:
            logger.error("Orchestrator execution failed, using fallback", error=str(e))
            # Fallback to simple analysis
            domain = await self._analyze_domain(context.task_description)
            expertise = await self._identify_expertise(domain, {})
            agents = await self._design_agent_team(expertise)
            workflow = await self._design_workflow(agents)

            return AgentOutput(
                agent_id=self.agent_id,
                agent_role=self.role,
                content={
                    "domain": domain,
                    "required_agents": agents,
                    "execution_plan": workflow,
                    "estimated_timeline": self._estimate_timeline(agents, workflow),
                    "fallback_used": True
                },
                confidence=0.6,
                timestamp=datetime.utcnow(),
                event_type="project_plan_created",
                reasoning="Used fallback analysis due to AI service issues"
            )
    
    async def reason(self, context: AgentContext) -> Dict[str, Any]:
        """Decide how to decompose the project"""
        return {
            "action": "analyze_and_plan",
            "steps": [
                "Understand domain",
                "Research requirements",
                "Design team",
                "Create workflow"
            ]
        }
    
    async def _analyze_domain(self, task_description: str) -> str:
        """Analyze what domain this task belongs to"""
        try:
            return await ai_service.analyze_domain(task_description)
        except Exception as e:
            logger.warning("AI domain analysis failed, using fallback", error=str(e))
            # Fallback heuristic
            if "marketing" in task_description.lower():
                return "marketing"
            elif "product" in task_description.lower():
                return "product_development"
            elif "research" in task_description.lower():
                return "research"
            else:
                return "general"
    
    async def _research_domain(self, domain: str) -> Dict[str, Any]:
        """Research domain-specific knowledge"""
        try:
            prompt = f"""
            Research the {domain} domain and provide key insights:

            Return a JSON object with:
            - key_concepts: array of 5-7 core concepts
            - methodologies: array of 3-5 common methodologies
            - tools: array of 4-6 commonly used tools
            - best_practices: array of 4-6 best practices

            Format: JSON only, no additional text.
            """

            response = await ai_service.generate_response(prompt, provider="deepseek", temperature=0.3)
            return json.loads(response)
        except Exception as e:
            logger.warning("AI domain research failed, using fallback", error=str(e))
            return {
                "key_concepts": ["Domain expertise required"],
                "methodologies": ["Standard practices"],
                "tools": ["Web browser", "Document writer"],
                "best_practices": ["Follow industry standards"]
            }
    
    async def _identify_expertise(self, domain: str, knowledge: Dict[str, Any]) -> List[str]:
        """Identify required expertise areas"""
        try:
            prompt = f"""
            Based on this {domain} project, identify the specific expertise areas needed.

            Domain knowledge: {json.dumps(knowledge)}

            Return a JSON array of 3-6 specific expertise roles needed for this type of project.
            Examples: "Market Research Specialist", "Content Strategy Expert", "Technical Writer", etc.

            Format: JSON array only, no additional text.
            """

            response = await ai_service.generate_response(prompt, provider="deepseek", temperature=0.4)
            return json.loads(response)
        except Exception as e:
            logger.warning("AI expertise identification failed, using fallback", error=str(e))
            return [
                "Research Specialist",
                "Strategy Expert",
                "Content Creator"
            ]
    
    async def _design_agent_team(self, expertise: List[str]) -> List[AgentSpec]:
        """Design specific agents for each expertise area"""
        try:
            agents_data = await ai_service.design_agent_team(expertise, await self._analyze_domain(""))

            agents = []
            for agent_data in agents_data:
                spec = AgentSpec(
                    role=agent_data.get("role", "General Agent"),
                    responsibilities=agent_data.get("responsibilities", ["Handle assigned tasks"]),
                    tools=agent_data.get("tools", ["web_browser", "document_writer"]),
                    dependencies=[]
                )
                agents.append(spec)

            return agents
        except Exception as e:
            logger.warning("AI agent design failed, using fallback", error=str(e))
            # Fallback to simple agent creation
            agents = []
            for expert_role in expertise:
                spec = AgentSpec(
                    role=expert_role,
                    responsibilities=self._get_responsibilities(expert_role),
                    tools=self._get_tools(expert_role),
                    dependencies=[]
                )
                agents.append(spec)

            return agents
    
    # ── Tool registry ──────────────────────────────────────────────────────────
    
    ROLE_TO_TOOLS: dict[str, list[str]] = {
        "research": ["web_browser", "data_analyzer"],
        "analysis": ["data_analyzer", "web_browser"],
        "analytics": ["data_analyzer"],
        "strategy": ["document_writer", "data_analyzer"],
        "content": ["document_writer"],
        "writing": ["document_writer"],
        "marketing": ["document_writer", "web_browser"],
        "technical": ["web_browser"],
        "engineering": ["web_browser"],
        "design": ["document_writer"],
        "creative": ["document_writer"],
        "data": ["data_analyzer"],
        "qa": ["data_analyzer"],
        "testing": ["data_analyzer"],
        "default": ["web_browser", "document_writer"],
    }
    
    RESPONSIBILITY_TEMPLATES: dict[str, list[str]] = {
        "research": [
            "Conduct thorough web and document research",
            "Synthesize findings into structured reports",
            "Verify facts and cite sources",
        ],
        "analysis": [
            "Analyze data for patterns and anomalies",
            "Interpret results in domain context",
            "Produce actionable insights from complex datasets",
        ],
        "strategy": [
            "Develop actionable strategic recommendations",
            "Evaluate options against business constraints",
            "Present clear rationale for proposed decisions",
        ],
        "content": [
            "Write clear, on-brand content for target audience",
            "Align messaging with business objectives",
            "Iterate based on feedback and brand guidelines",
        ],
        "technical": [
            "Research and document technical approaches",
            "Evaluate feasibility of technical solutions",
            "Communicate technical details to stakeholders",
        ],
    }
    
    def _get_responsibilities(self, role: str) -> List[str]:
        """Get responsibilities for a role using templates or LLM fallback"""
        role_lower = role.lower()
        for key, responsibilities in self.RESPONSIBILITY_TEMPLATES.items():
            if key in role_lower:
                return responsibilities
        # Fallback: derive from role name
        return [f"Execute {role} tasks with quality and precision"]
    
    def _get_tools(self, role: str) -> List[str]:
        """Map role to available tools"""
        role_lower = role.lower()
        for key, tools in self.ROLE_TO_TOOLS.items():
            if key in role_lower:
                return tools
        return self.ROLE_TO_TOOLS["default"]
    
    async def _design_workflow(self, agents: List[AgentSpec]) -> Dict[str, List[str]]:
        """Design execution workflow with phases"""
        try:
            agent_roles = [agent.role for agent in agents]
            prompt = f"""
            Design an optimal workflow for these agents working together: {", ".join(agent_roles)}

            Consider dependencies, parallel execution opportunities, and logical flow.

            Return a JSON object where keys are phase names and values are arrays of agent roles that work in that phase.
            Example: {{"research_phase": ["Research Agent"], "strategy_phase": ["Strategy Agent"], "execution_phase": ["Content Creator", "Marketing Agent"]}}

            Format: JSON object only, no additional text.
            """

            response = await ai_service.generate_response(prompt, provider="deepseek", temperature=0.3)
            return json.loads(response)
        except Exception as e:
            logger.warning("AI workflow design failed, using fallback", error=str(e))
            # Fallback to simple sequential workflow
            workflow = {}
            for i, agent in enumerate(agents):
                workflow[f"phase_{i+1}"] = [agent.role]
            return workflow
    
    def _estimate_timeline(self, agents: List[AgentSpec], workflow: Dict[str, List[str]]) -> str:
        """Estimate project timeline"""
        # Simple estimation: 1 day per phase
        num_phases = len(workflow)
        return f"{num_phases} days"
