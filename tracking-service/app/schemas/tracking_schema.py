from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.schemas.event_schema import TrackingEventOut

class TrackingTimelineOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tracking_number: str
    latest_status: str
    latest_lat: Optional[float] = None
    latest_lng: Optional[float] = None
    events: List[TrackingEventOut]
