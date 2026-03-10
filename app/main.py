import uvicorn
import time
import logging
from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine, Base
from app.core.logging import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger("cloud-cost-monitor")

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    ## Cloud Resource Cost Monitoring API
    A production-ready system for tracking cloud infrastructure costs:
    - **Resources**: Manage cloud assets (EC2, S3, RDS, etc.) with custom pricing.
    - **Usage**: Track and record hourly usage logs.
    - **Analytics**: Generate detailed cost reports and identify top spending resources.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    contact={
        "name": "Cloud Cost Team",
        "url": "http://api.cloud-cost-monitor.com/support",
    }
)

# 1. Middleware: Request Logging & Processing Time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    
    # Log the incoming request
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log the completion
    logger.info(
        f"Request completed: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.4f}s"
    )
    
    return response

# 2. Global Error Handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please contact support." if settings.ENVIRONMENT == "production" else str(exc)
        }
    )

# 3. Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, refine this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["root"])
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": "1.0.0",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
