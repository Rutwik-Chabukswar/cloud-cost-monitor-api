from fastapi import APIRouter
from app.api.v1.endpoints import resources, usage, analytics, health, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(health.router, prefix="/health", tags=["monitoring"])
api_router.include_router(resources.router, prefix="/resources", tags=["resources"])
api_router.include_router(usage.router, prefix="/usage", tags=["usage"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
