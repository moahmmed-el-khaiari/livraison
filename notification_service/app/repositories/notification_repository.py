from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.notification import Notification

class NotificationRepository:

    def create(self, db: Session, n: Notification) -> None:
        db.add(n)

    def commit(self, db: Session) -> None:
        db.commit()

    def refresh(self, db: Session, n: Notification) -> None:
        db.refresh(n)

    def list_by_tracking(self, db: Session, tracking_number: str, limit: int = 50):
        stmt = (
            select(Notification)
            .where(Notification.tracking_number == tracking_number)
            .order_by(desc(Notification.created_at))
            .limit(limit)
        )
        return list(db.scalars(stmt))

    def list_by_recipient(self, db: Session, recipient: str, limit: int = 50):
        stmt = (
            select(Notification)
            .where(Notification.recipient == recipient)
            .order_by(desc(Notification.created_at))
            .limit(limit)
        )
        return list(db.scalars(stmt))

    def list_pending(self, db: Session, limit: int = 20):
        stmt = (
            select(Notification)
            .where(Notification.status == "PENDING")
            .order_by(Notification.created_at.asc())
            .limit(limit)
        )
        return list(db.scalars(stmt))
