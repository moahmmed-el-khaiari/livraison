import httpx
from pydantic import BaseModel
from typing import Optional

from app.config import settings


class TrackingEventCreate(BaseModel):
    tracking_number: str
    status: str                 # string pour interop
    source: str                 # DOIT etre: SYSTEM | COURIER | HUB
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
    def __init__(self, base_url: str | None = None, timeout: float = 5.0):
        self.base_url = (base_url or settings.TRACKING_BASE_URL).rstrip("/")
        self.timeout = httpx.Timeout(timeout=timeout, connect=2.0)

    def add_event(self, payload: TrackingEventCreate) -> TrackingEventOut:
        url = f"{self.base_url}/tracking/events"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(url, json=payload.model_dump())
        except httpx.RequestError as e:
            raise RuntimeError(f"tracking-service unreachable: {str(e)}") from e

        if resp.status_code >= 400:
            raise RuntimeError(f"tracking-service error {resp.status_code}: {resp.text}")

        return TrackingEventOut(**resp.json())

    def get_latest_status(self, tracking_number: str) -> str:
        # endpoint existe dans tracking-service: GET /tracking/{tracking_number}/latest
        # et il retourne un TrackingEventOut (champ "status") :contentReference[oaicite:4]{index=4}
        url = f"{self.base_url}/tracking/{tracking_number}/latest"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.get(url)
        except httpx.RequestError as e:
            raise RuntimeError(f"tracking-service unreachable: {str(e)}") from e

        if resp.status_code >= 400:
            raise RuntimeError(f"tracking-service error {resp.status_code}: {resp.text}")

        data = resp.json()
        return data["status"]
