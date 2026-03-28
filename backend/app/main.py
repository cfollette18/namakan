from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import connect_db, disconnect_db
from app.routers import projects, agents, users, websocket, marketplace
import structlog

logger = structlog.get_logger()

app = FastAPI(
    title="Namakan API",
    description="Multi-Agent Orchestration Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(websocket.router, prefix="/api/ws", tags=["websocket"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["marketplace"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Namakan API")
    await connect_db()
    logger.info("Database connected")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Namakan API")
    await disconnect_db()
    logger.info("Database disconnected")

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "namakan-api",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
