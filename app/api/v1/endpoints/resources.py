from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.schemas.resource import Resource, ResourceCreate, ResourceUpdate
from app.crud import crud_resource
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Resource)
def create_resource(
    resource_in: ResourceCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_resource.create_resource(db, resource_in)

@router.get("/", response_model=List[Resource])
def list_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_resource.get_resources(db, skip=skip, limit=limit)

@router.get("/{resource_id}", response_model=Resource)
def view_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = crud_resource.get_resource(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@router.put("/{resource_id}", response_model=Resource)
def update_resource(
    resource_id: int, 
    resource_in: ResourceUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_resource = crud_resource.get_resource(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Update resource fields
    for field, value in resource_in.model_dump(exclude_unset=True).items():
        setattr(db_resource, field, value)
    
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.delete("/{resource_id}")
def delete_resource(
    resource_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_resource = crud_resource.delete_resource(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"message": "Resource deleted successfully"}
