from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
import structlog

logger = structlog.get_logger()

class CollaborationStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    DECLINED = "declined"
    EXPIRED = "expired"

class PermissionLevel(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"

class CollaborationRequest(BaseModel):
    """Request to collaborate between agents from different users"""
    request_id: str
    from_user_id: str
    to_user_id: str
    project_id: str
    agent_roles: List[str]
    purpose: str
    requested_permissions: Dict[str, List[PermissionLevel]]
    expires_at: datetime

class CollaborationSession(BaseModel):
    """Active collaboration session between user agents"""
    session_id: str
    participants: List[Dict[str, str]]  # [{user_id, agent_team}]
    shared_data: Dict[str, Any]
    permissions: Dict[str, Dict[str, List[str]]]  # {user_id: {can_share: [fields]}}
    audit_log: List[Dict[str, Any]]
    created_at: datetime
    expires_at: Optional[datetime] = None

class AgentCollaborationNetwork:
    """
    Manages cross-user agent collaboration
    Enables agents from different users to work together
    """
    
    def __init__(self):
        self.active_sessions: Dict[str, CollaborationSession] = {}
        self.pending_requests: Dict[str, CollaborationRequest] = {}
    
    async def create_collaboration_request(
        self,
        from_user_id: str,
        to_user_id: str,
        project_id: str,
        agent_roles: List[str],
        purpose: str,
        requested_permissions: Dict[str, List[str]]
    ) -> CollaborationRequest:
        """
        Create a collaboration request
        
        Args:
            from_user_id: Requesting user
            to_user_id: Target user
            project_id: Project ID
            agent_roles: Roles of agents to collaborate
            purpose: Purpose of collaboration
            requested_permissions: What data can be shared
        
        Returns:
            CollaborationRequest
        """
        import uuid
        
        request_id = str(uuid.uuid4())
        
        request = CollaborationRequest(
            request_id=request_id,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            project_id=project_id,
            agent_roles=agent_roles,
            purpose=purpose,
            requested_permissions=requested_permissions,
            expires_at=datetime.utcnow()  # + timedelta(days=7)
        )
        
        self.pending_requests[request_id] = request
        
        logger.info(
            "Collaboration request created",
            request_id=request_id,
            from_user=from_user_id,
            to_user=to_user_id
        )
        
        return request
    
    async def approve_collaboration_request(
        self,
        request_id: str,
        approved_permissions: Dict[str, List[str]]
    ) -> CollaborationSession:
        """
        Approve a collaboration request and create session
        
        Args:
            request_id: Request ID
            approved_permissions: Approved permissions (may differ from requested)
        
        Returns:
            CollaborationSession
        """
        import uuid
        
        request = self.pending_requests.get(request_id)
        if not request:
            raise ValueError(f"Request not found: {request_id}")
        
        session_id = str(uuid.uuid4())
        
        session = CollaborationSession(
            session_id=session_id,
            participants=[
                {"user_id": request.from_user_id, "agent_team": "team_a"},
                {"user_id": request.to_user_id, "agent_team": "team_b"}
            ],
            shared_data={},
            permissions={
                request.from_user_id: approved_permissions.get(request.from_user_id, {}),
                request.to_user_id: approved_permissions.get(request.to_user_id, {})
            },
            audit_log=[],
            created_at=datetime.utcnow()
        )
        
        self.active_sessions[session_id] = session
        del self.pending_requests[request_id]
        
        logger.info(
            "Collaboration session created",
            session_id=session_id,
            participants=len(session.participants)
        )
        
        return session
    
    async def share_data(
        self,
        session_id: str,
        from_user_id: str,
        data_type: str,
        data: Any
    ) -> bool:
        """
        Share data in collaboration session
        
        Args:
            session_id: Session ID
            from_user_id: User sharing data
            data_type: Type of data
            data: Data to share
        
        Returns:
            True if successful
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        # Check permissions
        user_perms = session.permissions.get(from_user_id, {})
        can_share = user_perms.get("can_share", [])
        
        if data_type not in can_share:
            logger.warning(
                "Permission denied",
                user_id=from_user_id,
                data_type=data_type
            )
            return False
        
        # Store shared data
        if data_type not in session.shared_data:
            session.shared_data[data_type] = []
        
        session.shared_data[data_type].append({
            "from_user": from_user_id,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Audit log
        session.audit_log.append({
            "action": "data_shared",
            "user_id": from_user_id,
            "data_type": data_type,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        logger.info(
            "Data shared",
            session_id=session_id,
            from_user=from_user_id,
            data_type=data_type
        )
        
        return True
    
    async def get_shared_data(
        self,
        session_id: str,
        user_id: str,
        data_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get shared data from collaboration session
        
        Args:
            session_id: Session ID
            user_id: User requesting data
            data_type: Specific data type (None for all)
        
        Returns:
            Shared data
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        # Check permissions
        user_perms = session.permissions.get(user_id, {})
        can_read = user_perms.get("can_read", [])
        
        # Filter by permissions
        filtered_data = {}
        for dtype, items in session.shared_data.items():
            if data_type and dtype != data_type:
                continue
            
            if dtype in can_read or "all" in can_read:
                filtered_data[dtype] = items
        
        logger.info(
            "Data retrieved",
            session_id=session_id,
            user_id=user_id,
            data_types=list(filtered_data.keys())
        )
        
        return filtered_data
    
    async def agent_to_agent_message(
        self,
        session_id: str,
        from_agent_role: str,
        to_agent_role: str,
        message: str
    ) -> bool:
        """
        Send message between agents in collaboration
        
        Args:
            session_id: Session ID
            from_agent_role: Sender agent role
            to_agent_role: Recipient agent role
            message: Message content
        
        Returns:
            True if successful
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        # Store in shared data
        if "agent_messages" not in session.shared_data:
            session.shared_data["agent_messages"] = []
        
        session.shared_data["agent_messages"].append({
            "from": from_agent_role,
            "to": to_agent_role,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Audit log
        session.audit_log.append({
            "action": "agent_message",
            "from_agent": from_agent_role,
            "to_agent": to_agent_role,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        logger.info(
            "Agent message sent",
            session_id=session_id,
            from_agent=from_agent_role,
            to_agent=to_agent_role
        )
        
        return True
    
    async def end_collaboration(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """
        End collaboration session
        
        Args:
            session_id: Session ID
        
        Returns:
            Session summary
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        # Generate summary
        summary = {
            "session_id": session_id,
            "duration": (datetime.utcnow() - session.created_at).total_seconds(),
            "participants": session.participants,
            "data_shared_count": sum(len(items) for items in session.shared_data.values()),
            "messages_exchanged": len(session.shared_data.get("agent_messages", [])),
            "audit_log_entries": len(session.audit_log)
        }
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        logger.info(
            "Collaboration ended",
            session_id=session_id,
            duration=summary["duration"]
        )
        
        return summary
    
    def get_active_collaborations(self, user_id: str) -> List[CollaborationSession]:
        """Get all active collaborations for a user"""
        active = []
        
        for session in self.active_sessions.values():
            for participant in session.participants:
                if participant["user_id"] == user_id:
                    active.append(session)
                    break
        
        return active
    
    def get_pending_requests(self, user_id: str) -> List[CollaborationRequest]:
        """Get all pending collaboration requests for a user"""
        pending = []
        
        for request in self.pending_requests.values():
            if request.to_user_id == user_id:
                pending.append(request)
        
        return pending


# Global instance
agent_network = AgentCollaborationNetwork()
