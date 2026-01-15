from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.notification_schema import NotificationEventIn, NotificationOut, NotificationListOut
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])
service = NotificationService()

def to_out(n) -> NotificationOut:
    return NotificationOut(
        id=n.id,
        event_type=n.event_type,
        channel=n.channel,
        recipient=n.recipient,
        tracking_number=n.tracking_number,
        order_id=n.order_id,
        title=n.title,
        message=n.message,
        status=n.status,
        sent=n.sent,
        created_at=n.created_at.isoformat(),
        sent_at=n.sent_at.isoformat() if n.sent_at else None,
    )

@router.post("/events", response_model=NotificationOut, status_code=201)
def receive_event(payload: NotificationEventIn, db: Session = Depends(get_db)):
    n = service.receive_event(db, payload)
    return to_out(n)

@router.get("/tracking/{tracking_number}", response_model=NotificationListOut)
def list_by_tracking(tracking_number: str, limit: int = 50, db: Session = Depends(get_db)):
    items = service.list_by_tracking(db, tracking_number, limit)
    return {"items": [to_out(x) for x in items]}

@router.get("/recipient/{recipient}", response_model=NotificationListOut)
def list_by_recipient(recipient: str, limit: int = 50, db: Session = Depends(get_db)):
    items = service.list_by_recipient(db, recipient, limit)
    return {"items": [to_out(x) for x in items]}
