# Security Rules

## Client Data (MOST IMPORTANT)

All client data handling must follow `namakan-technical/SECURE-DATA-PIPELINE.md`.

**ABSOLUTE RULES**:
- Client data NEVER leaves the designated secure environment
- No client data in logs, error messages, or Sentry
- No client data in Git commits
- All data pipelines encrypted at rest (AES-256) and in transit (TLS 1.2+)
- Client data deleted within 30 days of project completion

## Authentication & Authorization

- All API endpoints require authentication unless explicitly public
- Role-based access control (RBAC) for all resources
- JWT tokens with 1-hour expiry, refresh tokens with 7-day expiry
- Never expose user IDs in URLs — use UUIDs

## API Security

- Input validation on ALL endpoints (Pydantic models)
- SQL injection prevention — always use parameterized queries (SQLAlchemy)
- Rate limiting on all public endpoints (Redis-based)
- CORS configured for known origins only
- No sensitive data in error responses (don't leak stack traces)

## Secrets Management

- NEVER hardcode secrets in code
- Use environment variables loaded from `.env`
- `.env` is in `.gitignore`
- Rotate API keys quarterly
- Use a secrets manager (AWS Secrets Manager, HashiCorp Vault) in production

## AI-Specific Security

- **Prompt injection**: Never trust client-provided content as system prompts
- **Data exfiltration**: AI outputs must only come from retrieved context or model weights
- **Hallucination mitigation**: Always ground responses in retrieved documents
- **Audit logging**: Log all AI agent actions and decisions

## Scanning

Run security checks before deploying:
```bash
# Python
pip install bandit safety
bandit -r backend/app/
safety check -r backend/requirements.txt

# JavaScript
npm audit
```
