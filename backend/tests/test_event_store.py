import pytest
from app.core.event_store import EventStore, ContextBuilder
from app.db.models import AgentEvent
from datetime import datetime

@pytest.mark.asyncio
async def test_event_store_append():
    """Test appending events to the store"""
    store = EventStore()
    
    event = await store.append(
        project_id="test-project-1",
        agent_id="test-agent-1",
        event_type="research_complete",
        event_data={"findings": ["Finding 1", "Finding 2"]},
        confidence_score=0.95
    )
    
    assert event.project_id == "test-project-1"
    assert event.agent_id == "test-agent-1"
    assert event.event_type == "research_complete"
    assert event.confidence_score == 0.95
    assert event.version == 1
    
    store.close()

@pytest.mark.asyncio
async def test_event_store_get_events():
    """Test retrieving events from the store"""
    store = EventStore()
    
    # Append multiple events
    await store.append(
        project_id="test-project-2",
        agent_id="agent-1",
        event_type="research_start",
        event_data={"query": "market research"}
    )
    
    await store.append(
        project_id="test-project-2",
        agent_id="agent-1",
        event_type="research_complete",
        event_data={"findings": ["Result 1"]}
    )
    
    # Retrieve events
    events = await store.get_events("test-project-2")
    
    assert len(events) >= 2
    assert events[0].version < events[1].version
    
    store.close()

@pytest.mark.asyncio
async def test_context_builder():
    """Test building agent-specific context"""
    store = EventStore()
    builder = ContextBuilder(store)
    
    # Add events
    await store.append(
        project_id="test-project-3",
        agent_id="research-agent",
        event_type="research_complete",
        event_data={"findings": ["Market size: $1B"]},
        confidence_score=0.9
    )
    
    # Build context for Strategy Agent
    context = await builder.build_for_agent(
        agent_role="Strategy Agent",
        project_id="test-project-3",
        max_tokens=1000
    )
    
    assert "events" in context
    assert "summary" in context
    assert len(context["events"]) > 0
    
    store.close()
