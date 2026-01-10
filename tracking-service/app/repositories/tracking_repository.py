from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.tracking_event import TrackingEvent

class TrackingRepository:
    def add_event(self, db: Session, event: TrackingEvent) -> TrackingEvent:
        db.add(event)
        db.flush()
        return event

    def list_events(self, db: Session, tracking_number: str) -> list[TrackingEvent]:
        return (
            db.query(TrackingEvent)
            .filter(TrackingEvent.tracking_number == tracking_number)
            .order_by(TrackingEvent.event_time.asc())
            .all()
        )

    def latest_event(self, db: Session, tracking_number: str) -> TrackingEvent | None:
        return (
            db.query(TrackingEvent)
            .filter(TrackingEvent.tracking_number == tracking_number)
            .order_by(desc(TrackingEvent.event_time))
            .first()
        )
