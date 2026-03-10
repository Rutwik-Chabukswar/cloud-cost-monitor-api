from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.resource import UsageRecord, UsageRecordCreate
from app.crud import crud_resource
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=UsageRecord)
def record_usage(usage_in: UsageRecordCreate, db: Session = Depends(get_db)):
    # Check if resource exists
    db_resource = crud_resource.get_resource(db, resource_id=usage_in.resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return crud_resource.record_usage(db, usage_in)
