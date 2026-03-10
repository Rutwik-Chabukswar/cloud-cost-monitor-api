from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# Resource Schemas
class ResourceBase(BaseModel):
    name: str = Field(..., examples=["AWS-EC2-Main"])
    service_type: str = Field(..., examples=["EC2"])
    unit_price: float = Field(..., examples=[0.05])

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(ResourceBase):
    name: Optional[str] = None
    service_type: Optional[str] = None
    unit_price: Optional[float] = None

class Resource(ResourceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Usage Record Schemas
class UsageRecordBase(BaseModel):
    resource_id: int
    hours: float = Field(..., gt=0)

class UsageRecordCreate(UsageRecordBase):
    pass

class UsageRecord(UsageRecordBase):
    id: int
    recorded_at: datetime

    class Config:
        from_attributes = True

# Analytics Schemas
class ResourceCost(BaseModel):
    resource_id: int
    name: str
    total_hours: float
    unit_price: float
    total_cost: float

class ServiceSummary(BaseModel):
    service_type: str
    total_cost: float

class CostSummary(BaseModel):
    total_cost: float
    resources_summary: List[ResourceCost]
    service_summary: List[ServiceSummary]
