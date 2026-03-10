import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cloud Resource Cost Monitoring API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    # Use os.getenv as fallback for direct env access or default to sqlite
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-it-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"

    # Pydantic Settings will automatically look for .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
    )

settings = Settings()
