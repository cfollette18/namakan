from typing import List, Dict, Any, Optional
from datetime import datetime
from app.db.models import AgentEvent
from app.core.database import prisma
import structlog
import json

logger = structlog.get_logger()

class EventStore:
    """
    Immutable event store for agent actions and outputs
    Implements event sourcing pattern for shared context
    """

    def __init__(self):
        self.db = prisma
    
    async def append(
        self,
        project_id: str,
        agent_id: str,
        event_type: str,
        event_data: Dict[str, Any],
        confidence_score: Optional[float] = None
    ) -> AgentEvent:
        """
        Append an immutable event to the store

        Args:
            project_id: Project UUID
            agent_id: Agent UUID
            event_type: Type of event (e.g., 'research_complete', 'strategy_proposed')
            event_data: Event payload as JSON
            confidence_score: Confidence level (0.0 to 1.0)

        Returns:
            Created AgentEvent
        """
        try:
            # Get current version for this project
            latest_version = await self.db.agent_event.find_first(
                where={"projectId": project_id},
                order={"version": "desc"}
            )

            next_version = (latest_version.version + 1) if latest_version else 1

            # Create event using Prisma
            event = await self.db.agent_event.create(
                data={
                    "projectId": project_id,
                    "agentId": agent_id,
                    "eventType": event_type,
                    "eventData": json.dumps(event_data),  # Prisma expects JSON as dict
                    "confidenceScore": confidence_score,
                    "version": next_version,
                    "createdAt": datetime.utcnow()
                }
            )

            logger.info(
                "Event appended",
                project_id=project_id,
                agent_id=agent_id,
                event_type=event_type,
                version=next_version
            )

            return event

        except Exception as e:
            logger.error("Error appending event", error=str(e))
            raise
    
    async def get_events(
        self,
        project_id: str,
        agent_id: Optional[str] = None,
        event_types: Optional[List[str]] = None,
        since_version: Optional[int] = None
    ) -> List[AgentEvent]:
        """
        Retrieve events from the store

        Args:
            project_id: Project UUID
            agent_id: Filter by agent (optional)
            event_types: Filter by event types (optional)
            since_version: Get events after this version (optional)

        Returns:
            List of AgentEvent objects ordered by version
        """
        try:
            where_clause = {"projectId": project_id}

            if agent_id:
                where_clause["agentId"] = agent_id

            if event_types:
                where_clause["eventType"] = {"in": event_types}

            if since_version:
                where_clause["version"] = {"gt": since_version}

            events = await self.db.agent_event.find_many(
                where=where_clause,
                order={"version": "asc"}
            )

            logger.debug(
                "Events retrieved",
                project_id=project_id,
                count=len(events)
            )

            return events

        except Exception as e:
            logger.error("Error retrieving events", error=str(e))
            raise
    
    async def get_latest_events(
        self,
        project_id: str,
        limit: int = 50
    ) -> List[AgentEvent]:
        """Get the most recent events for a project"""
        try:
            events = await self.db.agent_event.find_many(
                where={"projectId": project_id},
                order={"createdAt": "desc"},
                take=limit
            )

            return list(reversed(events))  # Return in chronological order

        except Exception as e:
            logger.error("Error retrieving latest events", error=str(e))
            raise

    async def get_events_by_type(
        self,
        project_id: str,
        event_type: str
    ) -> List[AgentEvent]:
        """Get all events of a specific type for a project"""
        try:
            events = await self.db.agent_event.find_many(
                where={
                    "projectId": project_id,
                    "eventType": event_type
                },
                order={"version": "asc"}
            )

            return events

        except Exception as e:
            logger.error("Error retrieving events by type", error=str(e))
            raise
    
    # Note: Prisma handles connection management automatically
    # No need for explicit close method


class ContextBuilder:
    """
    Builds agent-specific context from event stream
    Each agent gets a filtered, relevant view of the project context
    """
    
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
    
    async def build_for_agent(
        self,
        agent_role: str,
        project_id: str,
        max_tokens: int = 8000
    ) -> Dict[str, Any]:
        """
        Build agent-specific context from event stream
        
        Args:
            agent_role: Role of the agent (e.g., "Research Agent")
            project_id: Project UUID
            max_tokens: Maximum context size in tokens
        
        Returns:
            Filtered context dictionary
        """
        # Get all events for this project
        all_events = await self.event_store.get_events(project_id)
        
        # Filter events relevant to this agent role
        relevant_events = self._filter_relevant_events(agent_role, all_events)
        
        # Rank by importance
        ranked_events = self._rank_events(relevant_events)
        
        # Pack into token budget
        context = self._pack_events_into_context(
            events=ranked_events,
            max_tokens=max_tokens
        )
        
        return context
    
    def _filter_relevant_events(
        self,
        agent_role: str,
        events: List[AgentEvent]
    ) -> List[AgentEvent]:
        """
        Filter events based on agent role
        Different agents need different context
        """
        relevance_rules = {
            "Research Agent": [
                "project_created",
                "user_feedback",
                "research_*"
            ],
            "Strategist Agent": [
                "project_created",
                "user_feedback",
                "research_complete",
                "strategy_*"
            ],
            "Copywriter Agent": [
                "project_created",
                "user_feedback",
                "strategy_approved",
                "copywriting_*"
            ],
            "Email Marketing Agent": [
                "project_created",
                "user_feedback",
                "strategy_approved",
                "copywriting_complete",
                "email_*"
            ]
        }
        
        patterns = relevance_rules.get(agent_role, ["*"])
        
        filtered = []
        for event in events:
            for pattern in patterns:
                # Simple wildcard matching
                if pattern == "*" or \
                   pattern.replace("*", "") in event.event_type:
                    filtered.append(event)
                    break
        
        return filtered
    
    def _rank_events(self, events: List[AgentEvent]) -> List[AgentEvent]:
        """
        Rank events by importance
        Recent + high-confidence events rank higher
        """
        # Simple ranking: recent events first, then by confidence
        return sorted(
            events,
            key=lambda e: (
                e.created_at.timestamp(),
                e.confidence_score or 0.0
            ),
            reverse=True
        )
    
    def _pack_events_into_context(
        self,
        events: List[AgentEvent],
        max_tokens: int
    ) -> Dict[str, Any]:
        """
        Pack events into context within token budget
        Rough estimation: 1 event ≈ 100 tokens
        """
        max_events = max_tokens // 100
        
        context = {
            "events": [],
            "summary": {}
        }
        
        for event in events[:max_events]:
            context["events"].append({
                "type": event.event_type,
                "data": event.event_data,
                "confidence": event.confidence_score,
                "timestamp": event.created_at.isoformat()
            })
        
        # Build summary
        context["summary"] = self._build_summary(events[:max_events])
        
        return context
    
    def _build_summary(self, events: List[AgentEvent]) -> Dict[str, Any]:
        """Build a summary of key information from events"""
        summary = {
            "total_events": len(events),
            "event_types": {},
            "key_decisions": [],
            "user_feedback": []
        }
        
        for event in events:
            # Count event types
            event_type = event.event_type
            summary["event_types"][event_type] = \
                summary["event_types"].get(event_type, 0) + 1
            
            # Extract key decisions
            if "approved" in event_type or "decision" in event_type:
                summary["key_decisions"].append({
                    "type": event_type,
                    "data": event.event_data
                })
            
            # Extract user feedback
            if "user_feedback" in event_type:
                summary["user_feedback"].append(event.event_data)
        
        return summary
