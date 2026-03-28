# Testing Rules

## Backend (Python)

**Framework**: `pytest`

```bash
cd backend
pytest                    # Run all tests
pytest -v                 # Verbose
pytest tests/test_agents.py  # Specific file
```

**Structure**:
```
backend/
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_routers.py
│   └── test_services.py
```

**Requirements**:
- Unit tests for all service functions
- Integration tests for all API routes
- Mock external dependencies (DB, Redis, LLM APIs)
- Minimum 80% code coverage for critical paths

**Example**:
```python
def test_create_agent(db_session):
    from ..services.agent_service import create_agent
    
    agent = create_agent(
        db=db_session,
        name="Test Agent",
        role="coder"
    )
    
    assert agent.id is not None
    assert agent.name == "Test Agent"
    assert agent.role == "coder"
```

## Frontend (TypeScript)

**Framework**: Jest + React Testing Library

```bash
cd frontend
npm test                  # Run all tests
npm test -- --watch      # Watch mode
npm test -- coverage     # With coverage
```

**Requirements**:
- Component tests for all UI components
- Test user interactions (clicks, form submissions)
- Mock API calls with MSW or `fetch-mock`
- No implementation detail tests — test behavior only

## CI/CD

All tests must pass before merge:
```yaml
- name: Run tests
  run: |
    docker-compose run backend pytest
    docker-compose run frontend npm test
```

## What to Test

| Type | Examples |
|------|----------|
| Unit | Pure functions, data transformations |
| API | All route handlers, request validation |
| Integration | DB operations, Redis cache |
| E2E | Critical user flows (signup, create project) |
