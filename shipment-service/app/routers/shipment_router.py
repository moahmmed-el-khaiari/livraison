from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.shipment_schema import ShipmentCreate, ShipmentOut
from app.services.shipment_service import ShipmentService

router = APIRouter(prefix="/shipments", tags=["Shipments"])
service = ShipmentService()


@router.post("", response_model=ShipmentOut, status_code=201)
def create_shipment(payload: ShipmentCreate, db: Session = Depends(get_db)):
    shipment = service.create_shipment(db, payload)
    return shipment


@router.get("/{tracking_number}", response_model=ShipmentOut)
def get_shipment(tracking_number: str, db: Session = Depends(get_db)):
    shipment = service.get_shipment(db, tracking_number)
    return shipment
