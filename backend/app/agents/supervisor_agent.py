from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent, AgentContext, AgentOutput
from datetime import datetime
import asyncio
import structlog

logger = structlog.get_logger()

class SupervisorAgent(BaseAgent):
    """
    Phase Supervisor - Manages 2-5 worker agents in a single phase
    Uses Claude Sonnet for balance of intelligence and speed
    """
    
    def __init__(
        self,
        agent_id: str,
        phase_name: str,
        worker_agents: List[BaseAgent],
        quality_criteria: Dict[str, Any]
    ):
        super().__init__(
            agent_id=agent_id,
            role=f"Supervisor - {phase_name}",
            responsibilities=[
                "Manage worker agents",
                "Monitor progress",
                "Ensure quality",
                "Handle retries",
                "Escalate blockers"
            ],
            tools=[
                "worker_coordinator",
                "quality_checker",
                "progress_tracker"
            ],
            personality="Supportive but demanding",
            constraints=[
                "Maximum 3 retries per worker",
                "Timeout: 10 minutes per worker",
                "Must meet quality criteria"
            ]
        )
        self.phase_name = phase_name
        self.workers = worker_agents
        self.quality_criteria = quality_criteria
        self.max_retries = 3
    
    async def execute(self, context: AgentContext) -> AgentOutput:
        """Execute all workers in this phase with supervision"""
        logger.info("Supervisor starting phase", phase=self.phase_name)
        
        results = {}
        retry_count = 0
        
        while retry_count < self.max_retries:
            try:
                # Run workers in parallel with timeout
                tasks = []
                for worker in self.workers:
                    task = asyncio.wait_for(
                        worker.execute(context),
                        timeout=600  # 10 minutes
                    )
                    tasks.append(task)
                
                # Wait for all workers
                worker_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results
                for i, result in enumerate(worker_results):
                    if isinstance(result, Exception):
                        logger.error("Worker failed", worker=self.workers[i].role, error=str(result))
                        # Retry logic would go here
                    else:
                        results[self.workers[i].role] = result
                
                # Quality gate check
                quality_check = await self._check_quality(results)
                
                if quality_check["passed"]:
                    return AgentOutput(
                        agent_id=self.agent_id,
                        agent_role=self.role,
                        content={
                            "phase_name": self.phase_name,
                            "outputs": results,
                            "quality_score": quality_check["score"]
                        },
                        confidence=quality_check["score"],
                        timestamp=datetime.utcnow(),
                        event_type="phase_complete"
                    )
                else:
                    logger.warning("Quality check failed", issues=quality_check["issues"])
                    retry_count += 1
            
            except asyncio.TimeoutError:
                logger.error("Phase timeout", phase=self.phase_name)
                retry_count += 1
        
        # Max retries exceeded
        return AgentOutput(
            agent_id=self.agent_id,
            agent_role=self.role,
            content={
                "phase_name": self.phase_name,
                "status": "failed",
                "error": f"Phase failed after {self.max_retries} retries"
            },
            confidence=0.0,
            timestamp=datetime.utcnow(),
            event_type="phase_failed"
        )
    
    async def reason(self, context: AgentContext) -> Dict[str, Any]:
        """Decide how to coordinate workers"""
        return {
            "action": "coordinate_workers",
            "strategy": "parallel_execution",
            "workers": [w.role for w in self.workers]
        }
    
    async def _check_quality(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check if results meet quality criteria"""
        # TODO: Implement actual quality checking
        # For now, simple check
        if results:
            return {
                "passed": True,
                "score": 0.85,
                "issues": []
            }
        else:
            return {
                "passed": False,
                "score": 0.0,
                "issues": ["No results produced"]
            }
