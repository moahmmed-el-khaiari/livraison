from sqlalchemy.orm import Session
from app.models.shipment import Shipment

class ShipmentRepository:
    def create(self, db: Session, shipment: Shipment) -> Shipment:
        db.add(shipment)
        db.flush()
        return shipment

    def find_by_tracking(self, db: Session, tracking_number: str) -> Shipment | None:
        return db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
