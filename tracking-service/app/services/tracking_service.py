from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.tracking_event import TrackingEvent
from app.models.enums import TrackingStatus
from app.repositories.tracking_repository import TrackingRepository

from app.schemas.event_schema import  TrackingEventCreate,TrackingEventOut 
from app.schemas.tracking_schema import TrackingTimelineOut

from app.utils.time_utils import now_utc
from app.utils.id_utils import new_uuid
from app.utils.state_machine import is_transition_allowed, FINAL_STATES


class TrackingService:
    def __init__(self):
        self.repo = TrackingRepository()

    def add_event(self, db: Session, payload: TrackingEventCreate) -> TrackingEvent:
        last = self.repo.latest_event(db, payload.tracking_number)

        if last is None:
            if payload.status != TrackingStatus.CREATED:
                raise HTTPException(status_code=400, detail="First event must be CREATED")
        else:
            current_status = TrackingStatus(last.status)

            if current_status in FINAL_STATES:
                raise HTTPException(
                    status_code=409,
                    detail=f"Shipment already in final state: {current_status.value}"
                )

            if not is_transition_allowed(current_status, payload.status):
                raise HTTPException(
                    status_code=409,
                    detail=f"Invalid transition: {current_status.value} -> {payload.status.value}"
                )

        event = TrackingEvent(
            id=new_uuid(),
            tracking_number=payload.tracking_number,
            status=payload.status.value,
            source=payload.source.value,
            city=payload.city,
            message=payload.message,
            lat=payload.lat,
            lng=payload.lng,
            event_time=now_utc(),
        )

        self.repo.add_event(db, event)
        db.commit()
        db.refresh(event)
        return event

    def get_timeline(self, db: Session, tracking_number: str) -> TrackingTimelineOut:
        events = self.repo.list_events(db, tracking_number)

        if not events:
            raise HTTPException(status_code=404, detail="Tracking number not found")

        latest = events[-1]

        return TrackingTimelineOut(
            tracking_number=tracking_number,
            latest_status=latest.status,
            latest_lat=latest.lat,
            latest_lng=latest.lng,
            events=[TrackingEventOut.model_validate(e) for e in events],
        )

    def get_latest(self, db: Session, tracking_number: str) -> TrackingEvent:
        latest = self.repo.latest_event(db, tracking_number)
        if not latest:
            raise HTTPException(status_code=404, detail="Tracking number not found")
        return latest
