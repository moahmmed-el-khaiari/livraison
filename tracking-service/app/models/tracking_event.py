from sqlalchemy import Column, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.db import Base

class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    id = Column(String(36), primary_key=True, index=True)
    tracking_number = Column(String(64), index=True, nullable=False)

    status = Column(String(40), nullable=False)
    source = Column(String(20), nullable=False)

    city = Column(String(100), nullable=True)
    message = Column(Text, nullable=True)

    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    event_time = Column(DateTime(timezone=True), server_default=func.now(), index=True)
