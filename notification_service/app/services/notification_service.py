from sqlalchemy.orm import Session
from app.repositories.notification_repository import NotificationRepository
from app.models.notification import Notification
from app.schemas.notification_schema import NotificationEventIn
from app.utils.id_utils import new_uuid
from app.utils.time_utils import now_utc

class NotificationService:
    def __init__(self):
        self.repo = NotificationRepository()

    def receive_event(self, db: Session, payload: NotificationEventIn) -> Notification:
        n = Notification(
            id=new_uuid(),
            event_type=payload.event_type,
            channel=payload.channel,
            recipient=payload.recipient,
            tracking_number=payload.tracking_number,
            order_id=payload.order_id,
            title=payload.title,
            message=payload.message,
            status="PENDING",
            sent=False,
            created_at=now_utc(),
            sent_at=None,
        )

        self.repo.create(db, n)
        self.repo.commit(db)
        self.repo.refresh(db, n)
        return n

    def list_by_tracking(self, db: Session, tracking_number: str, limit: int = 50):
        return self.repo.list_by_tracking(db, tracking_number, limit)

    def list_by_recipient(self, db: Session, recipient: str, limit: int = 50):
        return self.repo.list_by_recipient(db, recipient, limit)
