from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import text
from app.api.deps import get_db

router = APIRouter()

@router.get("/")
def check_health(db: Session = Depends(get_db)):
    """
    Check the health of the service and database connectivity.
    """
    try:
        # Check database connectivity
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"unreachable: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }
