from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    service_type = Column(String, index=True) # e.g., EC2, S3, etc.
    unit_price = Column(Float) # Hourly rate
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    usage_records = relationship("UsageRecord", back_populates="resource", cascade="all, delete-orphan")

class UsageRecord(Base):
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"))
    hours = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    resource = relationship("Resource", back_populates="usage_records")
