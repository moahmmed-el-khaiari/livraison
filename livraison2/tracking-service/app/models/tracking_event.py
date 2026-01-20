from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, BigInteger

from app.db import Base


class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    # ✅ ordre DB fiable (auto-increment)
    db_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # ✅ identifiant métier/API (inchangé)
    id: Mapped[str] = mapped_column(String(36), unique=True, index=True, nullable=False)

    tracking_number: Mapped[str] = mapped_column(String(50), index=True, nullable=False)

    status: Mapped[str] = mapped_column(String(30), nullable=False)
    source: Mapped[str] = mapped_column(String(30), nullable=False)

    city: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    message: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lng: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    event_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
