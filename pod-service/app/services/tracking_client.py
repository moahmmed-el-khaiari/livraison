import httpx
from pydantic import BaseModel
from typing import Optional

from app.config import settings


class TrackingEventCreate(BaseModel):
    tracking_number: str
    status: str                 # string pour interop
    source: str = "POD_SERVICE"
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


class TrackingClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or settings.TRACKING_BASE_URL).rstrip("/")

    def add_event(self, payload: TrackingEventCreate) -> TrackingEventOut:
        url = f"{self.base_url}/tracking/events"

        with httpx.Client(timeout=5.0) as client:
            resp = client.post(url, json=payload.model_dump())

        if resp.status_code >= 400:
            raise RuntimeError(f"tracking-service error {resp.status_code}: {resp.text}")

        return TrackingEventOut(**resp.json())
