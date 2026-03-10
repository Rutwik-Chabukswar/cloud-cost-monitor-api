import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cloud Resource Cost Monitoring API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
