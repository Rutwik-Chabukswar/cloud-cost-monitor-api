from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from app.crud import crud_resource
from app.api.deps import get_db

router = APIRouter()

@router.get("/total-cost/{resource_id}")
def get_resource_total_cost(resource_id: int, db: Session = Depends(get_db)):
    cost = crud_resource.get_resource_total_cost(db, resource_id=resource_id)
    return {"resource_id": resource_id, "total_cost": cost}

@router.get("/service-summary")
def get_service_summary(db: Session = Depends(get_db)):
    return crud_resource.get_service_summary(db)

@router.get("/top-expensive")
def get_top_expensive(limit: int = 5, db: Session = Depends(get_db)):
    return crud_resource.get_top_expensive_resources(db, limit=limit)
