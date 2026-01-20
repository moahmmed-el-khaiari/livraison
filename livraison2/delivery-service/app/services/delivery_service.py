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

    # =========================
    # ASSIGN DELIVERY
    # =========================
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
            status=DeliveryStatus.CREATED,
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

        # IMPORTANT:
        # l'event CREATED est déjà créé par shipment-service (ou manuellement).
        # Donc on ne le renvoie JAMAIS ici (sinon 409 CREATED -> CREATED).
        return task
    # =========================
    # LIST ALL DELIVERIES   
    # =========================
    def list_all(self, db: Session) -> list[DeliveryTask]:
        return self.repo.list_all(db)
    
    # =========================
    # START DELIVERY
    # =========================
    def start(self, db: Session, tracking_number: str, req: StartDeliveryRequest) -> DeliveryTask:
        task = self.repo.find_by_tracking(db, tracking_number)
        if not task:
            raise HTTPException(status_code=404, detail="Delivery task not found")

        if task.status not in (DeliveryStatus.CREATED, DeliveryStatus.FAILED_ATTEMPT):
            raise HTTPException(
                status_code=409,
                detail=f"Cannot start delivery from status: {task.status}",
            )

        # 1) Update delivery-task local
        task.status = DeliveryStatus.OUT_FOR_DELIVERY
        task.last_lat = req.lat
        task.last_lng = req.lng
        task.updated_at = now_utc()

        self.repo.save(db)
        self.repo.refresh(db, task)

        # 2) Tracking: on respecte la machine à états du tracking-service
        # CREATED -> PICKED_UP -> IN_TRANSIT -> OUT_FOR_DELIVERY
        latest = self.tracking.get_latest_status(tracking_number)

        # Si tracking-service est déjà OUT_FOR_DELIVERY ou DELIVERED, on ne pousse rien
        if latest in (TrackingStatus.OUT_FOR_DELIVERY.value, TrackingStatus.DELIVERED.value):
            return task

        # Si tracking est CREATED, on envoie PICKED_UP
        if latest == TrackingStatus.CREATED.value:
            self.tracking.add_event(
                TrackingEventCreate(
                    tracking_number=tracking_number,
                    status=TrackingStatus.PICKED_UP.value,
                    source="COURIER",
                    city=req.city,
                    lat=req.lat,
                    lng=req.lng,
                    message="Package picked up by courier",
                )
            )
            latest = TrackingStatus.PICKED_UP.value  # on avance localement

        # Si tracking est PICKED_UP, on envoie IN_TRANSIT
        if latest == TrackingStatus.PICKED_UP.value:
            self.tracking.add_event(
                TrackingEventCreate(
                    tracking_number=tracking_number,
                    status=TrackingStatus.IN_TRANSIT.value,
                    source="HUB",
                    city=req.city,
                    lat=req.lat,
                    lng=req.lng,
                    message="Package in transit",
                )
            )
            latest = TrackingStatus.IN_TRANSIT.value

        # Si tracking est IN_TRANSIT, on envoie OUT_FOR_DELIVERY
        if latest == TrackingStatus.IN_TRANSIT.value:
            self.tracking.add_event(
                TrackingEventCreate(
                    tracking_number=tracking_number,
                    status=TrackingStatus.OUT_FOR_DELIVERY.value,
                    source="COURIER",
                    city=req.city,
                    lat=req.lat,
                    lng=req.lng,
                    message="Out for delivery",
                )
            )

        return task

    # =========================
    # ATTEMPT FAILED
    # =========================
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
                source="COURIER",
                lat=req.lat,
                lng=req.lng,
                message=f"Delivery failed: {req.reason}",
            )
        )

        return task

    # =========================
    # COMPLETE DELIVERY
    # =========================
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
                source="COURIER",
                city=req.city,
                lat=req.lat,
                lng=req.lng,
                message="Delivered",
            )
        )

        return task

    # =========================
    # GET DELIVERY
    # =========================
    def get_one(self, db: Session, tracking_number: str) -> DeliveryTask:
        task = self.repo.find_by_tracking(db, tracking_number)
        if not task:
            raise HTTPException(status_code=404, detail="Delivery task not found")
        return task
