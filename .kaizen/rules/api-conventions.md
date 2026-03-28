# API Conventions

## REST Standards

| Method | Path | Description |
|--------|------|-------------|
| GET | `/agents` | List all agents |
| GET | `/agents/{id}` | Get agent by ID |
| POST | `/agents` | Create new agent |
| PATCH | `/agents/{id}` | Update agent |
| DELETE | `/agents/{id}` | Delete agent |

## Request/Response

**Request** — JSON body, Pydantic model validated:
```python
class AgentCreate(BaseModel):
    name: str
    role: str
    system_prompt: str | None = None
```

**Response** — Always JSON:
```python
# Success
return {"id": 1, "name": "Agent", "role": "coder"}

# Error
return {"error": "Not found", "detail": "Agent with ID 1 not found"}
```

## Status Codes

| Code | When |
|------|------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (validation error) |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not found |
| 500 | Internal server error |

## Error Format

```json
{
  "error": "Human-readable error title",
  "detail": "Specific error message",
  "code": "ERROR_CODE"
}
```

## Versioning

```
/api/v1/agents
/api/v1/projects
```

## Rate Limiting

- Public: 100 req/min
- Authenticated: 1000 req/min
- Webhooks: 60 req/min
