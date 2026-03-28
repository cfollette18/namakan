from typing import Callable, Any
from datetime import datetime, timedelta
from enum import Enum
import structlog

logger = structlog.get_logger()

class CircuitState(str, Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failures detected, blocking calls
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """
    Circuit breaker pattern for agent operations
    Prevents cascading failures and enables graceful degradation
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        success_threshold: int = 2
    ):
        """
        Initialize circuit breaker
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before trying again
            success_threshold: Successes needed to close circuit from half-open
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: datetime | None = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection
        
        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Function result
        
        Raises:
            Exception: If circuit is open or function fails
        """
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker transitioning to HALF_OPEN")
            else:
                raise Exception("Circuit breaker is OPEN - operation blocked")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        
        except Exception as e:
            self._on_failure()
            raise
    
    async def call_async(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute async function with circuit breaker protection
        
        Args:
            func: Async function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Function result
        
        Raises:
            Exception: If circuit is open or function fails
        """
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker transitioning to HALF_OPEN")
            else:
                raise Exception("Circuit breaker is OPEN - operation blocked")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful operation"""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                logger.info("Circuit breaker CLOSED - service recovered")
    
    def _on_failure(self):
        """Handle failed operation"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(
                "Circuit breaker OPENED",
                failure_count=self.failure_count,
                threshold=self.failure_threshold
            )
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        
        time_since_failure = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return time_since_failure >= self.recovery_timeout
    
    def reset(self):
        """Manually reset the circuit breaker"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        logger.info("Circuit breaker manually reset")
    
    def get_state(self) -> dict:
        """Get current circuit breaker state"""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure": self.last_failure_time.isoformat() if self.last_failure_time else None
        }


class AgentCircuitBreaker:
    """
    Circuit breaker specifically for agent operations
    Tracks failures per agent and escalates to human when needed
    """
    
    def __init__(self):
        self.breakers: dict[str, CircuitBreaker] = {}
    
    def get_breaker(self, agent_id: str) -> CircuitBreaker:
        """Get or create circuit breaker for an agent"""
        if agent_id not in self.breakers:
            self.breakers[agent_id] = CircuitBreaker(
                failure_threshold=3,  # Lower threshold for agents
                recovery_timeout=30,
                success_threshold=2
            )
        
        return self.breakers[agent_id]
    
    async def execute_with_protection(
        self,
        agent_id: str,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute agent function with circuit breaker protection
        
        Args:
            agent_id: Agent identifier
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Function result
        """
        breaker = self.get_breaker(agent_id)
        
        try:
            result = await breaker.call_async(func, *args, **kwargs)
            return result
        
        except Exception as e:
            # Check if we should escalate to human
            if breaker.state == CircuitState.OPEN:
                logger.error(
                    "Agent circuit breaker open - escalating to human",
                    agent_id=agent_id,
                    error=str(e)
                )
                # In production, this would trigger human notification
                raise Exception(f"Agent {agent_id} requires human intervention")
            
            raise
    
    def get_all_states(self) -> dict:
        """Get state of all circuit breakers"""
        return {
            agent_id: breaker.get_state()
            for agent_id, breaker in self.breakers.items()
        }
    
    def reset_all(self):
        """Reset all circuit breakers"""
        for breaker in self.breakers.values():
            breaker.reset()
        logger.info("All circuit breakers reset")


# Global agent circuit breaker
agent_circuit_breaker = AgentCircuitBreaker()
