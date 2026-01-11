from pydantic import BaseModel
from typing import Optional
from app.models.enums import DeliveryStatus


class AssignDeliveryRequest(BaseModel):
    tracking_number: str
    courier_id: Optional[str] = None


class StartDeliveryRequest(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None
    city: Optional[str] = None


class AttemptDeliveryRequest(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None
    reason: str


class CompleteDeliveryRequest(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None
    city: Optional[str] = None
    note: Optional[str] = None


class DeliveryTaskOut(BaseModel):
    id: str
    tracking_number: str
    status: str  # ✅ SIMPLE
    courier_id: Optional[str] = None
    last_lat: Optional[float] = None
    last_lng: Optional[float] = None
    note: Optional[str] = None
    created_at: str
    updated_at: str
