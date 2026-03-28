# Build Command

Build all services for production.

## Usage

```bash
/build
```

## What It Does

```bash
# 1. Backend
cd backend
pip install -r requirements.txt
python -m pytest tests/ -q

# 2. Frontend
cd frontend
npm install
npm run build

# 3. Docker (production)
docker build -t namakan-backend ./backend
```

## Files Checked

- Backend: `backend/requirements.txt`, `backend/app/`
- Frontend: `frontend/package.json`, `frontend/app/`

## Fail Conditions

- Any pytest test fails
- Frontend build errors (TypeScript, ESLint)
- Docker build fails
