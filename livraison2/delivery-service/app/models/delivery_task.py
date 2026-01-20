from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Float, Text, Enum
from app.db import Base
from app.models.enums import DeliveryStatus
from datetime import datetime

class DeliveryTask(Base):
    __tablename__ = "delivery_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    tracking_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)

    # ✅ LA LIGNE MAGIQUE
    status: Mapped[DeliveryStatus] = mapped_column(Enum(DeliveryStatus), nullable=False)

    courier_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_lng: Mapped[float | None] = mapped_column(Float, nullable=True)

    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)