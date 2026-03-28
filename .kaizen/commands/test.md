# Test Command

Run all tests for backend and frontend.

## Usage

```bash
/test
/test backend
/test frontend
/test --coverage
```

## Options

| Flag | Description |
|------|-------------|
| `backend` | Run backend tests only |
| `frontend` | Run frontend tests only |
| `--coverage` | Generate coverage report |

## Backend

```bash
cd backend
pytest                    # All tests
pytest -v                 # Verbose
pytest tests/test_*.py    # Specific file
pytest --cov=app         # With coverage
```

## Frontend

```bash
cd frontend
npm test                  # All tests
npm test -- --watch      # Watch mode
npm test -- --coverage   # With coverage
```

## CI Mode

```bash
/test --ci
# Fails on first error, no watch mode, XML output for CI
```
