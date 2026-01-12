from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.delivery_task import DeliveryTask
from app.models.enums import DeliveryStatus
from app.repositories.delivery_repository import DeliveryRepository
from app.schemas.delivery_schema import (
    AssignDeliveryRequest,
    StartDeliveryRequest,
    AttemptDeliveryRequest,
    CompleteDeliveryRequest,
)
from app.schemas.tracking_external_schema import TrackingEventCreate, TrackingStatus
from app.services.tracking_client import TrackingClient
from app.utils.id_utils import new_uuid
from app.utils.time_utils import now_utc


class DeliveryService:
    def __init__(self):
        self.repo = DeliveryRepository()
        self.tracking = TrackingClient()

    def assign(self, db: Session, req: AssignDeliveryRequest) -> DeliveryTask:
        existing = self.repo.find_by_tracking(db, req.tracking_number)
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Delivery task already exists for this tracking number",
            )

        task = DeliveryTask(
            id=new_uuid(),
            tracking_number=req.tracking_number,
            status=DeliveryStatus.CREATED,  # ✅ Enum SQLAlchemy
            courier_id=req.courier_id,
            last_lat=None,
            last_lng=None,
            note=None,
            created_at=now_utc(),
            updated_at=now_utc(),
        )

        self.repo.create(db, task)
        self.repo.save(db)
        self.repo.refresh(db, task)

        # Event tracking (API externe → string)
        self.tracking.add_event(
            TrackingEventCreate(
                tracking_number=req.tracking_number,
                status=TrackingStatus.CREATED.value,
                message="Delivery task created",
            )
        )

        return task

    def start(self, db: Session, tracking_number: str, req: StartDeliveryRequest) -> DeliveryTask:
        task = self.repo.find_by_tracking(db, tracking_number)
        if not task:
            raise HTTPException(status_code=404, detail="Delivery task not found")

        if task.status not in (
            DeliveryStatus.CREATED,
            DeliveryStatus.FAILED_ATTEMPT,
        ):
            raise HTTPException(
                status_code=409,
                detail=f"Cannot start delivery from status: {task.status}",
            )

        task.status = DeliveryStatus.OUT_FOR_DELIVERY
        task.last_lat = req.lat
        task.last_lng = req.lng
        task.updated_at = now_utc()

        self.repo.save(db)
        self.repo.refresh(db, task)

        self.tracking.add_event(
            TrackingEventCreate(
                tracking_number=tracking_number,
                status=TrackingStatus.OUT_FOR_DELIVERY.value,
                city=req.city,
                lat=req.lat,
                lng=req.lng,
                message="Out for delivery",
            )
        )

        return task

    def attempt_failed(self, db: Session, tracking_number: str, req: AttemptDeliveryRequest) -> DeliveryTask:
        task = self.repo.find_by_tracking(db, tracking_number)
        if not task:
            raise HTTPException(status_code=404, detail="Delivery task not found")

        if task.status != DeliveryStatus.OUT_FOR_DELIVERY:
            raise HTTPException(
                status_code=409,
                detail="Delivery attempt allowed only when OUT_FOR_DELIVERY",
            )

        task.status = DeliveryStatus.FAILED_ATTEMPT
        task.last_lat = req.lat
        task.last_lng = req.lng
        task.note = req.reason
        task.updated_at = now_utc()

        self.repo.save(db)
        self.repo.refresh(db, task)

        self.tracking.add_event(
            TrackingEventCreate(
                tracking_number=tracking_number,
                status=TrackingStatus.EXCEPTION.value,
                lat=req.lat,
                lng=req.lng,
                message=f"Delivery failed: {req.reason}",
            )
        )

        return task

    def complete(self, db: Session, tracking_number: str, req: CompleteDeliveryRequest) -> DeliveryTask:
        task = self.repo.find_by_tracking(db, tracking_number)
        if not task:
            raise HTTPException(status_code=404, detail="Delivery task not found")

        if task.status != DeliveryStatus.OUT_FOR_DELIVERY:
            raise HTTPException(
                status_code=409,
                detail="Complete allowed only when OUT_FOR_DELIVERY",
            )

        task.status = DeliveryStatus.DELIVERED
        task.last_lat = req.lat
        task.last_lng = req.lng
        task.note = req.note
        task.updated_at = now_utc()

        self.repo.save(db)
        self.repo.refresh(db, task)

        self.tracking.add_event(
            TrackingEventCreate(
                tracking_number=tracking_number,
                status=TrackingStatus.DELIVERED.value,
                city=req.city,
                lat=req.lat,
                lng=req.lng,
                message="Delivered",
            )
        )

        return task

    def get_one(self, db: Session, tracking_number: str) -> DeliveryTask:
        task = self.repo.find_by_tracking(db, tracking_number)
        if not task:
            raise HTTPException(status_code=404, detail="Delivery task not found")
        return task
