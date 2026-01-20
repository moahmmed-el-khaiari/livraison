from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from app.models.enums import TrackingStatus, EventSource


class TrackingEventCreate(BaseModel):
    tracking_number: str = Field(min_length=6, max_length=50)
    status: TrackingStatus
    source: EventSource
    city: Optional[str] = Field(default=None, max_length=120)
    message: Optional[str] = Field(default=None, max_length=255)
    lat: Optional[float] = None
    lng: Optional[float] = None


class TrackingEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tracking_number: str
    status: str
    source: str
    city: Optional[str] = None
    message: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    event_time: datetime
