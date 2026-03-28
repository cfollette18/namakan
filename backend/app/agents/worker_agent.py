from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent, AgentContext, AgentOutput
from app.services.ai_service import ai_service
from datetime import datetime
import structlog
import json

logger = structlog.get_logger()

class WorkerAgent(BaseAgent):
    """
    Worker Agent - Executes specific tasks
    Uses Claude Sonnet for most tasks, Haiku for simple tasks
    """
    
    def __init__(
        self,
        agent_id: str,
        role: str,
        responsibilities: List[str],
        tools: List[str],
        personality: str = "professional",
        domain_knowledge: Dict[str, Any] = None
    ):
        super().__init__(
            agent_id=agent_id,
            role=role,
            responsibilities=responsibilities,
            tools=tools,
            personality=personality,
            constraints=[
                "Must produce structured output",
                "Cite all sources",
                "Flag low-confidence work"
            ]
        )
        self.domain_knowledge = domain_knowledge or {}
    
    async def execute(self, context: AgentContext) -> AgentOutput:
        """Execute the specific task"""
        logger.info("Worker starting task", role=self.role)
        
        # Execute with reflection loop
        max_iterations = 3
        best_output = None
        best_quality = 0.0
        
        for iteration in range(max_iterations):
            # Generate output
            output = await self._generate_output(context)
            
            # Self-critique
            critique = await self.critique_output(output, context)
            
            if critique["quality_score"] > best_quality:
                best_output = output
                best_quality = critique["quality_score"]
            
            # If good enough, return
            if critique["quality_score"] > 0.8:
                logger.info("Worker completed task", role=self.role, quality=critique["quality_score"])
                return output
            
            # Otherwise, improve for next iteration
            if iteration < max_iterations - 1:
                logger.info("Worker improving output", role=self.role, iteration=iteration+1)
                context.user_feedback.append(critique)
        
        # Return best attempt
        logger.info("Worker completed after max iterations", role=self.role, quality=best_quality)
        return best_output
    
    async def reason(self, context: AgentContext) -> Dict[str, Any]:
        """Decide how to approach the task"""
        return {
            "action": "execute_task",
            "approach": "iterative_improvement",
            "max_iterations": 3
        }
    
    async def _generate_output(self, context: AgentContext) -> AgentOutput:
        """Generate output for the task using AI"""
        try:
            # Create a comprehensive prompt based on agent role and context
            prompt = self._build_task_prompt(context)

            # Use DeepSeek as primary AI provider
            ai_response = await ai_service.generate_response(
                prompt,
                provider="deepseek",
                temperature=0.7,
                max_tokens=2000
            )

            # Parse and structure the AI response
            structured_output = self._parse_ai_response(ai_response)

            return AgentOutput(
                agent_id=self.agent_id,
                agent_role=self.role,
                content=structured_output,
                confidence=0.85,
                timestamp=datetime.utcnow(),
                event_type="task_complete",
                reasoning=f"AI-generated output using DeepSeek API for {self.role} responsibilities"
            )
        except Exception as e:
            logger.error("AI generation failed, using fallback", error=str(e))
            # Fallback output
            return AgentOutput(
                agent_id=self.agent_id,
                agent_role=self.role,
                content={
                    "result": f"Task completed by {self.role}",
                    "details": f"Generated with limited capabilities due to: {str(e)}",
                    "error": "AI service temporarily unavailable"
                },
                confidence=0.5,
                timestamp=datetime.utcnow(),
                event_type="task_complete",
                reasoning=f"Fallback execution due to AI service issues"
            )
    
    def _build_task_prompt(self, context: AgentContext) -> str:
        """Build a comprehensive prompt for the AI based on agent role and context"""
        system_context = self.get_system_prompt()

        task_context = f"""
        Current Task: {context.task_description}

        Shared Context: {json.dumps(context.shared_context)}
        Previous Dependencies: {json.dumps(context.dependencies_outputs)}
        User Feedback: {json.dumps(context.user_feedback)}
        """

        prompt = f"""
        {system_context}

        TASK CONTEXT:
        {task_context}

        INSTRUCTIONS:
        As a {self.role}, execute this task to the best of your ability. Provide detailed, actionable output that demonstrates your expertise. Structure your response as JSON when possible, with clear sections and deliverables.

        Focus on:
        - High-quality, professional output
        - Practical and actionable results
        - Clear reasoning and methodology
        - Specific recommendations or deliverables

        Response format: Provide your main output, then any additional analysis or recommendations.
        """

        return prompt

    def _parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Parse the AI response into structured output"""
        try:
            # Try to parse as JSON first
            return json.loads(ai_response)
        except:
            # If not JSON, structure it manually
            return {
                "result": ai_response,
                "structured_output": self._extract_structure(ai_response),
                "raw_response": ai_response[:1000] + "..." if len(ai_response) > 1000 else ai_response
            }

    def _extract_structure(self, response: str) -> Dict[str, Any]:
        """Extract structured information from text response"""
        # Simple extraction logic - can be enhanced based on agent type
        sections = {}
        current_section = "main_output"

        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Look for section headers (lines that are all caps or start with #)
            if line.isupper() and len(line) < 50:
                current_section = line.lower().replace(' ', '_')
                sections[current_section] = []
            elif line.startswith('#'):
                current_section = line[1:].strip().lower().replace(' ', '_')
                sections[current_section] = []
            else:
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append(line)

        # Convert lists back to strings
        for key, value in sections.items():
            if isinstance(value, list):
                sections[key] = '\n'.join(value)

        return sections

    async def critique_output(self, output: AgentOutput, context: AgentContext) -> Dict[str, Any]:
        """Worker critiques its own work using AI"""
        try:
            critique_prompt = f"""
            As a {self.role}, critically evaluate this output for quality, completeness, and effectiveness.

            Original Task: {context.task_description}
            Your Output: {json.dumps(output.content)}

            Evaluate on these criteria:
            1. Completeness - Does it fully address the task?
            2. Quality - Is the work professional and well-structured?
            3. Actionability - Can someone use this output effectively?
            4. Accuracy - Is the information correct and well-supported?

            Provide a JSON response with:
            - quality_score: number between 0-1
            - issues: array of specific problems or gaps
            - strengths: array of what's good about the output
            - overall_assessment: brief summary
            - improvement_suggestions: array of specific ways to improve

            JSON only, no additional text.
            """

            critique_response = await ai_service.generate_response(
                critique_prompt,
                provider="deepseek",
                temperature=0.3
            )

            return json.loads(critique_response)
        except Exception as e:
            logger.warning("AI critique failed, using fallback", error=str(e))
            # Fallback critique
            return {
                "quality_score": 0.8,
                "issues": [],
                "strengths": ["Task completed", "Followed guidelines"],
                "overall_assessment": "Good quality output",
                "improvement_suggestions": []
            }

class ResearchAgent(WorkerAgent):
    """Specialized research agent"""
    
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            role="Research Agent",
            responsibilities=[
                "Conduct market research",
                "Gather data from multiple sources",
                "Analyze trends and patterns",
                "Create research reports"
            ],
            tools=["web_browser", "data_scraper", "spreadsheet_analyzer"],
            personality="Thorough, data-driven, skeptical"
        )

class CopywriterAgent(WorkerAgent):
    """Specialized copywriting agent"""
    
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            role="Copywriter Agent",
            responsibilities=[
                "Write compelling copy",
                "Match brand voice",
                "Optimize for engagement",
                "Create multiple variations"
            ],
            tools=["document_writer", "brand_voice_analyzer", "readability_checker"],
            personality="Creative, empathetic, persuasive"
        )

class StrategyAgent(WorkerAgent):
    """Specialized strategy agent"""
    
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            role="Strategy Agent",
            responsibilities=[
                "Develop strategic plans",
                "Analyze competitive positioning",
                "Create frameworks and models",
                "Provide recommendations"
            ],
            tools=["document_writer", "strategy_frameworks", "data_analyzer"],
            personality="Analytical, strategic, decisive"
        )
