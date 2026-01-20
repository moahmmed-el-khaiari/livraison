from sqlalchemy.orm import Session
from app.models.delivery_task import DeliveryTask


class DeliveryRepository:
    def create(self, db: Session, task: DeliveryTask) -> DeliveryTask:
        db.add(task)
        return task

    def save(self, db: Session) -> None:
        db.commit()

    def refresh(self, db: Session, task: DeliveryTask) -> None:
        db.refresh(task)

    def find_by_tracking(self, db: Session, tracking_number: str) -> DeliveryTask | None:
        return db.query(DeliveryTask).filter(DeliveryTask.tracking_number == tracking_number).first()
    
    def list_all(self, db: Session) -> list[DeliveryTask]:
        return db.query(DeliveryTask).order_by(DeliveryTask.created_at.desc()).all()
