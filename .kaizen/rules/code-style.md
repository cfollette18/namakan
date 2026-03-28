# Code Style Rules

## Python (Backend)

**Linter/Formatter**: `ruff`

```bash
ruff check .          # Lint
ruff format .         # Format
```

**Style**:
- 4-space indentation
- Max line length: 100
- Snake_case for functions/variables, PascalCase for classes
- Type hints required on all public functions
- Docstrings on all classes and public methods

**Example**:
```python
def get_agent_by_id(agent_id: int, db: Session) -> Agent | None:
    """Fetch an agent by ID, returns None if not found."""
    return db.query(Agent).filter(Agent.id == agent_id).first()
```

**Imports**:
```python
# stdlib
import os
import json
from typing import Optional

# third-party
from fastapi import APIRouter
from sqlalchemy.orm import Session

# local
from ..core.database import get_db
from ..models.agent import Agent
```

## TypeScript (Frontend)

**Linter**: `eslint`, **Formatter**: `prettier`

```bash
npm run lint    # ESLint
npm run format  # Prettier
```

**Style**:
- 2-space indentation
- Max line length: 100
- camelCase for variables/functions, PascalCase for components
- Explicit types on all props and function signatures
- No `any` type

**Example**:
```typescript
interface AgentCardProps {
  agent: Agent
  onSelect: (id: string) => void
}

export function AgentCard({ agent, onSelect }: AgentCardProps) {
  return (
    <div className="p-4 border rounded" onClick={() => onSelect(agent.id)}>
      <h3>{agent.name}</h3>
    </div>
  )
}
```

## General

- No commented-out code — delete it
- Small functions (< 40 lines ideal)
- Single responsibility per function
- No magic numbers — use named constants
- Error handling — never let exceptions propagate silently
