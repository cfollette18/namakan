from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = ""
    
    # Redis
    REDIS_URL: str = ""
    
    # API Keys
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    
    # Environment
    NODE_ENV: str = "development"
    PYTHON_ENV: str = "development"
    
    # JWT & Security
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Logging
    LOG_LEVEL: str = "DEBUG"
    
    # AI Model Configuration
    DEFAULT_ORCHESTRATOR_MODEL: str = "claude-3-opus-20240229"
    DEFAULT_AGENT_MODEL: str = "claude-3-sonnet-20240229"
    FALLBACK_MODEL: str = "gpt-4-turbo-preview"
    
    # Cost Limits
    MAX_PROJECT_COST: float = 50.00
    MAX_MONTHLY_COST: float = 500.00
    
    # Feature Flags
    ENABLE_AGENT_COLLABORATION: bool = True
    ENABLE_LEARNING_SYSTEM: bool = True
    ENABLE_ANALYTICS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
