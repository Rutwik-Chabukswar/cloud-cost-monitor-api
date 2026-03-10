from fastapi import APIRouter
from app.api.v1.endpoints import resources, usage, analytics

api_router = APIRouter()

api_router.include_router(resources.router, prefix="/resources", tags=["resources"])
api_router.include_router(usage.router, prefix="/usage", tags=["usage"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
