from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.event_schema import TrackingEventCreate, TrackingEventOut
from app.schemas.tracking_schema import TrackingTimelineOut
from app.services.tracking_service import TrackingService

router = APIRouter(prefix="/tracking", tags=["Tracking"])
service = TrackingService()


@router.post("/events", response_model=TrackingEventOut, status_code=201)
def add_event(payload: TrackingEventCreate, db: Session = Depends(get_db)):
    return service.add_event(db, payload)


@router.get("/{tracking_number}", response_model=TrackingTimelineOut)
def timeline(tracking_number: str, db: Session = Depends(get_db)):
    return service.get_timeline(db, tracking_number)


@router.get("/{tracking_number}/latest", response_model=TrackingEventOut)
def latest(tracking_number: str, db: Session = Depends(get_db)):
    return service.get_latest(db, tracking_number)
