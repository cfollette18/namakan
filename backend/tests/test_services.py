import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime


@pytest.mark.asyncio
async def test_agent_service_list_project_agents():
    """Test listing agents for a project"""
    from app.services.agent_service import AgentService

    service = AgentService()

    # Mock the Prisma Agent model
    with patch("app.services.agent_service.AgentModel") as MockAgent:
        mock_agent = MagicMock()
        mock_agent.id = "agent-1"
        mock_agent.role = "Research Agent"
        mock_agent.project_id = "project-1"
        mock_agent.status = "active"
        mock_agent.created_at = datetime.now()
        mock_agent.updated_at = datetime.now()

        MockAgent.filter = AsyncMock(return_value=[mock_agent])

        result = await service.list_project_agents("project-1")

        assert len(result) == 1
        assert result[0].name == "Research Agent"
        assert result[0].project_id == "project-1"


@pytest.mark.asyncio
async def test_agent_service_get_agent():
    """Test getting a single agent"""
    from app.services.agent_service import AgentService

    service = AgentService()

    with patch("app.services.agent_service.AgentModel") as MockAgent:
        mock_agent = MagicMock()
        mock_agent.id = "agent-1"
        mock_agent.role = "Strategy Agent"
        mock_agent.project_id = "project-1"
        mock_agent.status = "idle"
        mock_agent.created_at = datetime.now()
        mock_agent.updated_at = datetime.now()

        MockAgent.find_first = AsyncMock(return_value=mock_agent)

        result = await service.get_agent("agent-1")

        assert result is not None
        assert result.id == "agent-1"
        assert result.role == "Strategy Agent"


@pytest.mark.asyncio
async def test_agent_service_get_agent_not_found():
    """Test getting a non-existent agent returns None"""
    from app.services.agent_service import AgentService

    service = AgentService()

    with patch("app.services.agent_service.AgentModel") as MockAgent:
        MockAgent.find_first = AsyncMock(return_value=None)

        result = await service.get_agent("non-existent")

        assert result is None


@pytest.mark.asyncio
async def test_agent_service_process_feedback():
    """Test processing user feedback"""
    from app.services.agent_service import AgentService
    from app.core.event_store import EventStore

    service = AgentService()

    with patch("app.core.event_store.EventStore") as MockStore:
        mock_store = MagicMock()
        mock_store.append = AsyncMock(return_value=MagicMock())
        mock_store.close = MagicMock()
        MockStore.return_value = mock_store

        await service.process_feedback(
            "agent-1",
            {"project_id": "project-1", "rating": 5, "comment": "Great work"}
        )

        mock_store.append.assert_called_once()
        mock_store.close.assert_called_once()