from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.services.delivery_service import DeliveryService
from app.schemas.delivery_schema import (
    AssignDeliveryRequest, StartDeliveryRequest,
    AttemptDeliveryRequest, CompleteDeliveryRequest,
    DeliveryTaskOut
)

router = APIRouter(prefix="/delivery", tags=["Delivery"])
service = DeliveryService()


def to_out(task) -> DeliveryTaskOut:
    return DeliveryTaskOut(
        id=task.id,
        tracking_number=task.tracking_number,
        status=task.status,
        courier_id=task.courier_id,
        last_lat=task.last_lat,
        last_lng=task.last_lng,
        note=task.note,
        created_at=str(task.created_at),
        updated_at=str(task.updated_at),
    )


@router.post("/assign", response_model=DeliveryTaskOut, status_code=201)
def assign(req: AssignDeliveryRequest, db: Session = Depends(get_db)):
    task = service.assign(db, req)
    return to_out(task)


@router.patch("/{tracking_number}/start", response_model=DeliveryTaskOut)
def start(tracking_number: str, req: StartDeliveryRequest, db: Session = Depends(get_db)):
    task = service.start(db, tracking_number, req)
    return to_out(task)


@router.patch("/{tracking_number}/attempt-failed", response_model=DeliveryTaskOut)
def attempt_failed(tracking_number: str, req: AttemptDeliveryRequest, db: Session = Depends(get_db)):
    task = service.attempt_failed(db, tracking_number, req)
    return to_out(task)


@router.patch("/{tracking_number}/complete", response_model=DeliveryTaskOut)
def complete(tracking_number: str, req: CompleteDeliveryRequest, db: Session = Depends(get_db)):
    task = service.complete(db, tracking_number, req)
    return to_out(task)

@router.get("/deliveries", response_model=List[DeliveryTaskOut])
def list_deliveries(db: Session = Depends(get_db)):
    tasks = service.list_all(db)
    return [to_out(t) for t in tasks]

@router.get("/{tracking_number}", response_model=DeliveryTaskOut)
def get_one(tracking_number: str, db: Session = Depends(get_db)):
    task = service.get_one(db, tracking_number)
    return to_out(task)
