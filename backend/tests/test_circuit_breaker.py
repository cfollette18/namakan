import pytest
from app.agents.circuit_breaker import CircuitBreaker, CircuitState, AgentCircuitBreaker

def test_circuit_breaker_closed_state():
    """Test circuit breaker in closed state"""
    breaker = CircuitBreaker(failure_threshold=3)
    
    def success_func():
        return "success"
    
    result = breaker.call(success_func)
    assert result == "success"
    assert breaker.state == CircuitState.CLOSED

def test_circuit_breaker_opens_on_failures():
    """Test circuit breaker opens after threshold failures"""
    breaker = CircuitBreaker(failure_threshold=3)
    
    def failing_func():
        raise Exception("Test failure")
    
    # Trigger failures
    for i in range(3):
        try:
            breaker.call(failing_func)
        except Exception:
            pass
    
    assert breaker.state == CircuitState.OPEN
    assert breaker.failure_count == 3

def test_circuit_breaker_blocks_when_open():
    """Test circuit breaker blocks calls when open"""
    breaker = CircuitBreaker(failure_threshold=2)
    
    def failing_func():
        raise Exception("Test failure")
    
    # Open the circuit
    for i in range(2):
        try:
            breaker.call(failing_func)
        except Exception:
            pass
    
    # Try to call when open
    with pytest.raises(Exception) as exc_info:
        breaker.call(lambda: "test")
    
    assert "Circuit breaker is OPEN" in str(exc_info.value)

def test_circuit_breaker_reset():
    """Test manual circuit breaker reset"""
    breaker = CircuitBreaker(failure_threshold=2)
    
    def failing_func():
        raise Exception("Test failure")
    
    # Open the circuit
    for i in range(2):
        try:
            breaker.call(failing_func)
        except Exception:
            pass
    
    assert breaker.state == CircuitState.OPEN
    
    # Reset
    breaker.reset()
    
    assert breaker.state == CircuitState.CLOSED
    assert breaker.failure_count == 0

@pytest.mark.asyncio
async def test_agent_circuit_breaker():
    """Test agent-specific circuit breaker"""
    agent_breaker = AgentCircuitBreaker()
    
    async def success_func():
        return "success"
    
    result = await agent_breaker.execute_with_protection(
        "agent-1",
        success_func
    )
    
    assert result == "success"
    
    # Check state
    states = agent_breaker.get_all_states()
    assert "agent-1" in states
    assert states["agent-1"]["state"] == "closed"
