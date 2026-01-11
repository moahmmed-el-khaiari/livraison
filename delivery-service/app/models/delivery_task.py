from sqlalchemy import Column, String, DateTime, Float, Text
from app.db import Base


class DeliveryTask(Base):
    __tablename__ = "delivery_tasks"

    id = Column(String(36), primary_key=True)
    tracking_number = Column(String(64), unique=True, nullable=False, index=True)

    # IMPORTANT: le champ s'appelle "status"
    status = Column(String(32), nullable=False, index=True)

    courier_id = Column(String(64), nullable=True)
    last_lat = Column(Float, nullable=True)
    last_lng = Column(Float, nullable=True)

    note = Column(Text, nullable=True)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
