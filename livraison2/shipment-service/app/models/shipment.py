from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db import Base
from app.models.enums import ShipmentStatus, ServiceLevel

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(String(36), primary_key=True, index=True)
    tracking_number = Column(String(32), unique=True, index=True, nullable=False)

    status = Column(String(40), nullable=False, default=ShipmentStatus.CREATED.value)
    service_level = Column(String(30), nullable=False, default=ServiceLevel.STANDARD.value)

    weight_kg = Column(Float, nullable=False)

    pickup_address_id = Column(String(36), ForeignKey("addresses.id"), nullable=False)
    delivery_address_id = Column(String(36), ForeignKey("addresses.id"), nullable=False)

    pickup_address = relationship("Address", foreign_keys=[pickup_address_id])
    delivery_address = relationship("Address", foreign_keys=[delivery_address_id])

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
