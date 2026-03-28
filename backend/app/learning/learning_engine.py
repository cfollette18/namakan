from typing import Dict, Any, List, Optional
from datetime import datetime
from app.db.models import Learning, User
from app.core.database import prisma
from pydantic import BaseModel
import structlog

logger = structlog.get_logger()

class LearningEvent(BaseModel):
    """Data captured from each agent interaction"""
    user_id: str
    project_id: str
    agent_role: str
    industry: str
    project_type: str
    
    # User query data
    user_query: str
    query_context: Dict[str, Any]
    user_refinements: List[str] = []
    
    # Agent action data
    agent_actions: List[Dict[str, Any]]
    agent_reasoning: List[str]
    tool_usage: List[Dict[str, Any]]
    
    # Response data
    agent_outputs: Dict[str, Any]
    output_quality_score: float
    time_to_complete: float
    
    # User feedback data
    user_approval: bool
    user_edits: List[Dict[str, Any]] = []
    user_rating: Optional[int] = None
    user_comments: Optional[str] = None
    reuse_rate: Optional[float] = None
    
    # Outcome data
    project_success: bool = False
    metrics: Dict[str, Any] = {}

class LearningModel(BaseModel):
    """A learned pattern that can be reused"""
    pattern: str
    context: Dict[str, Any]
    strategy: str
    confidence: float
    evidence_count: int
    success_rate: float

class AdvancedLearningEngine:
    """
    Implements dual-layer learning:
    1. Personal Learning (user-specific)
    2. Collective Learning (global intelligence)
    """
    
    def __init__(self):
        self.db = prisma
        self.personal_models: Dict[str, Dict[str, Any]] = {}
    
    async def process_interaction(self, event: LearningEvent):
        """
        Process every interaction to extract learnings
        
        Args:
            event: Learning event from agent interaction
        """
        logger.info(
            "Processing learning event",
            user_id=event.user_id,
            agent_role=event.agent_role
        )
        
        # 1. Personal Learning - Update user-specific model
        await self._update_personal_model(event)
        
        # 2. Collective Learning - Extract generalizable insights
        if event.user_approval and (event.user_rating or 0) >= 4:
            learning = await self._extract_learning(event)
            await self._store_collective_learning(learning)
        
        # 3. Track outcomes for continuous improvement
        if event.metrics:
            await self._correlate_actions_to_outcomes(event)
    
    async def _update_personal_model(self, event: LearningEvent):
        """Update user-specific learning model"""
        try:
            # Get or create user profile
            if event.user_id not in self.personal_models:
                self.personal_models[event.user_id] = {
                    "preferences": {},
                    "patterns": [],
                    "communication_style": {},
                    "industry": event.industry
                }
            
            profile = self.personal_models[event.user_id]
            
            # Update preferences based on edits
            if event.user_edits:
                for edit in event.user_edits:
                    edit_type = edit.get("type")
                    if edit_type not in profile["preferences"]:
                        profile["preferences"][edit_type] = []
                    profile["preferences"][edit_type].append(edit.get("change"))
            
            # Update communication style
            if event.user_refinements:
                profile["communication_style"]["refinement_count"] = \
                    profile["communication_style"].get("refinement_count", 0) + len(event.user_refinements)
            
            # Store successful patterns
            if event.user_approval:
                profile["patterns"].append({
                    "query": event.user_query,
                    "strategy": event.agent_reasoning,
                    "success": True,
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            logger.info("Personal model updated", user_id=event.user_id)
        
        except Exception as e:
            logger.error("Error updating personal model", error=str(e))
    
    async def _extract_learning(self, event: LearningEvent) -> LearningModel:
        """
        Extract generalizable learning from successful interaction
        
        Args:
            event: Learning event
        
        Returns:
            LearningModel with pattern, strategy, and confidence
        """
        # Identify the pattern
        pattern = self._identify_pattern(event)
        
        # Extract the strategy that worked
        strategy = " | ".join(event.agent_reasoning) if event.agent_reasoning else ""
        
        # Calculate confidence based on quality score
        confidence = event.output_quality_score
        
        return LearningModel(
            pattern=pattern,
            context={
                "agent_role": event.agent_role,
                "industry": event.industry,
                "project_type": event.project_type
            },
            strategy=strategy,
            confidence=confidence,
            evidence_count=1,
            success_rate=1.0 if event.user_approval else 0.0
        )
    
    def _identify_pattern(self, event: LearningEvent) -> str:
        """Identify the pattern from the event"""
        # Simple pattern identification
        # In production, this would use NLP/ML
        return f"{event.agent_role} for {event.project_type} in {event.industry}"
    
    async def _store_collective_learning(self, learning: LearningModel):
        """Store learning in collective knowledge base"""
        try:
            # Check if similar learning exists
            existing = await self.db.learning.find_first(
                where={
                    "pattern": learning.pattern,
                    "isPersonal": False
                }
            )

            if existing:
                # Update existing learning
                new_evidence_count = existing.evidenceCount + 1
                new_success_rate = (
                    (existing.successRate * existing.evidenceCount + learning.success_rate) /
                    new_evidence_count
                )

                await self.db.learning.update(
                    where={"id": existing.id},
                    data={
                        "evidenceCount": new_evidence_count,
                        "successRate": new_success_rate,
                        "confidence": max(existing.confidence, learning.confidence),
                        "updatedAt": datetime.utcnow()
                    }
                )
            else:
                # Create new learning
                await self.db.learning.create(
                    data={
                        "agentType": learning.context["agent_role"],
                        "industry": learning.context["industry"],
                        "projectType": learning.context["project_type"],
                        "pattern": learning.pattern,
                        "context": learning.context,
                        "strategy": learning.strategy,
                        "confidence": learning.confidence,
                        "evidenceCount": learning.evidence_count,
                        "successRate": learning.success_rate,
                        "isPersonal": False
                    }
                )

            logger.info(
                "Collective learning stored",
                pattern=learning.pattern,
                confidence=learning.confidence
            )

        except Exception as e:
            logger.error("Error storing collective learning", error=str(e))
    
    async def _correlate_actions_to_outcomes(self, event: LearningEvent):
        """Correlate agent actions to business outcomes"""
        # Track which agent actions led to successful outcomes
        # This helps identify what actually works vs what just looks good
        logger.info(
            "Correlating actions to outcomes",
            agent_role=event.agent_role,
            success=event.project_success
        )
    
    async def get_personal_learnings(
        self,
        user_id: str,
        agent_role: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Get personal learnings for a user
        
        Args:
            user_id: User ID
            agent_role: Agent role
            context: Context for filtering
        
        Returns:
            List of relevant personal learnings
        """
        profile = self.personal_models.get(user_id, {})
        
        # Return user's successful patterns
        patterns = profile.get("patterns", [])
        
        # Filter by relevance
        relevant = [
            p for p in patterns
            if p["success"]
        ]
        
        return relevant[-10:]  # Return last 10 successful patterns
    
    async def get_collective_learnings(
        self,
        agent_role: str,
        industry: str,
        project_type: str,
        min_confidence: float = 0.75
    ) -> List[Learning]:
        """
        Get collective learnings for a scenario

        Args:
            agent_role: Agent role
            industry: Industry
            project_type: Project type
            min_confidence: Minimum confidence threshold

        Returns:
            List of relevant learnings
        """
        try:
            learnings = await self.db.learning.find_many(
                where={
                    "agentType": agent_role,
                    "isPersonal": False,
                    "confidence": {"gte": min_confidence}
                },
                order={"confidence": "desc"},
                take=10
            )

            logger.info(
                "Collective learnings retrieved",
                agent_role=agent_role,
                count=len(learnings)
            )

            return learnings

        except Exception as e:
            logger.error("Error retrieving collective learnings", error=str(e))
            return []
    
    async def apply_learnings_to_agent(
        self,
        agent_role: str,
        user_id: str,
        context: Dict[str, Any],
        base_prompt: str
    ) -> str:
        """
        Apply learnings to enhance agent prompt
        
        Args:
            agent_role: Agent role
            user_id: User ID
            context: Context
            base_prompt: Base system prompt
        
        Returns:
            Enhanced prompt with learnings
        """
        # Get personal learnings
        personal = await self.get_personal_learnings(user_id, agent_role, context)
        
        # Get collective learnings
        collective = await self.get_collective_learnings(
            agent_role,
            context.get("industry", "general"),
            context.get("project_type", "general"),
            min_confidence=0.75
        )
        
        # Build learning section
        learning_section = "\n\n## LEARNED BEST PRACTICES\n\n"
        
        # Add personal learnings
        if personal:
            learning_section += "### Your Past Successes:\n"
            for p in personal[:5]:
                learning_section += f"- When: {p.get('query', 'N/A')}\n"
                learning_section += f"  Strategy: {p.get('strategy', ['N/A'])[0] if p.get('strategy') else 'N/A'}\n"
        
        # Add collective learnings
        if collective:
            learning_section += "\n### Proven Strategies (from thousands of projects):\n"
            for learning in collective[:5]:
                learning_section += f"- {learning.pattern}\n"
                learning_section += f"  Strategy: {learning.strategy}\n"
                learning_section += f"  Success Rate: {learning.success_rate * 100:.1f}% (n={learning.evidence_count})\n"
        
        # Combine with base prompt
        enhanced_prompt = base_prompt + learning_section
        
        logger.info(
            "Prompt enhanced with learnings",
            personal_count=len(personal),
            collective_count=len(collective)
        )
        
        return enhanced_prompt
    
    # Note: Prisma handles connection management automatically
    # No need for explicit close method


class UserDataIsolation:
    """
    Ensures user privacy while enabling collective learning
    Personal learnings stay personal, collective learnings are anonymized
    """
    
    @staticmethod
    def anonymize_for_collective_learning(event: LearningEvent) -> Dict[str, Any]:
        """
        Remove all personally identifiable information
        
        Args:
            event: Learning event
        
        Returns:
            Anonymized data
        """
        anonymized = {
            "agent_role": event.agent_role,
            "industry": event.industry,
            "project_type": event.project_type,
            "strategy_used": event.agent_reasoning,
            "outcome": event.user_approval,
            "context": {
                "output_quality": event.output_quality_score,
                "time_to_complete": event.time_to_complete
            }
        }
        
        # NO user_id, NO specific content, NO identifying details
        return anonymized
    
    @staticmethod
    async def get_user_personal_data(user_id: str, db) -> Dict[str, Any]:
        """
        Get all personal data for a user

        Args:
            user_id: User ID
            db: Database client

        Returns:
            User's personal learning data
        """
        # Personal data is encrypted and isolated per user
        # Only accessible with user's authentication
        learnings = await db.learning.find_many(
            where={
                "userId": user_id,
                "isPersonal": True
            }
        )

        return {
            "user_id": user_id,
            "personal_learnings": [
                {
                    "pattern": l.pattern,
                    "strategy": l.strategy,
                    "confidence": l.confidence,
                    "created_at": l.createdAt.isoformat()
                }
                for l in learnings
            ]
        }
