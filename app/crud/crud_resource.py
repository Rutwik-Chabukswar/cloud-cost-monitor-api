from sqlalchemy.orm import Session
from app.models.resource import Resource, UsageRecord
from app.schemas.resource import ResourceCreate, ResourceUpdate, UsageRecordCreate
from datetime import datetime
from sqlalchemy import func

# CRUD operations for Resources
def create_resource(db: Session, resource: ResourceCreate) -> Resource:
    db_resource = Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def get_resources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Resource).offset(skip).limit(limit).all()

def get_resource(db: Session, resource_id: int):
    return db.query(Resource).filter(Resource.id == resource_id).first()

def delete_resource(db: Session, resource_id: int):
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if db_resource:
        db.delete(db_resource)
        db.commit()
    return db_resource

# CRUD operations for Usage Records
def record_usage(db: Session, usage: UsageRecordCreate) -> UsageRecord:
    db_usage = UsageRecord(**usage.model_dump())
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage

# Analytics helpers
def get_resource_total_cost(db: Session, resource_id: int) -> float:
    from sqlalchemy import func
    total_hours = db.query(func.sum(UsageRecord.hours)).filter(UsageRecord.resource_id == resource_id).scalar() or 0.0
    resource = get_resource(db, resource_id)
    return total_hours * resource.unit_price if resource else 0.0

def get_service_summary(db: Session):
    # This is a bit complex for a simple CRUD file, might move later
    results = db.query(
        Resource.service_type,
        func.sum(UsageRecord.hours * Resource.unit_price)
    ).join(UsageRecord).group_by(Resource.service_type).all()
    return [{"service_type": s[0], "total_cost": s[1]} for s in results]

def get_top_expensive_resources(db: Session, limit: int = 5):
    results = db.query(
        Resource.id,
        Resource.name,
        func.sum(UsageRecord.hours).label("total_hours"),
        Resource.unit_price,
        (func.sum(UsageRecord.hours) * Resource.unit_price).label("total_cost")
    ).join(UsageRecord).group_by(Resource.id).order_by(func.sum(UsageRecord.hours * Resource.unit_price).desc()).limit(limit).all()
    
    return [
        {
            "resource_id": r[0],
            "name": r[1],
            "total_hours": r[2],
            "unit_price": r[3],
            "total_cost": r[4]
        } for r in results
    ]
