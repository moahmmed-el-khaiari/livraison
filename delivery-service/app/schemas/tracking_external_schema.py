from pydantic import BaseModel
from enum import Enum
from typing import Optional

class TrackingStatus(str, Enum):
    CREATED = "CREATED"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    EXCEPTION = "EXCEPTION"

class TrackingEventCreate(BaseModel):
    tracking_number: str
    status: str  # ✅ interop microservices
    source: str = "DELIVERY_SERVICE"
    city: Optional[str] = None
    message: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class TrackingEventOut(BaseModel):
    id: str
    tracking_number: str
    status: str
    source: str
    city: Optional[str] = None
    message: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    event_time: str
