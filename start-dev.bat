@echo off
echo Starting Namakan Development Environment...
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Start infrastructure services
echo Starting Docker services (PostgreSQL, Redis)...
docker-compose up -d

REM Wait for services to be healthy
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check if services are healthy
docker-compose ps
echo.

REM Create new terminals for frontend and backend
echo Creating development terminals...

REM Frontend Terminal (Next.js)
start "Frontend Dev Server" cmd /k "cd frontend && npm run dev"

REM Backend Terminal (FastAPI)
start "Backend API Server" cmd /k "cd backend && set DATABASE_URL=postgresql://namakan_user:namakan_password@localhost:5432/namakan_dev && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Development environment started successfully!
echo.
echo Services available at:
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo.
echo PostgreSQL: localhost:5432 (namakan_user / namakan_password)
echo Redis: localhost:6379
echo.
pause
