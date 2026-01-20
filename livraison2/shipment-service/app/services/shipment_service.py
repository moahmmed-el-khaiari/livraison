from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.address import Address
from app.models.shipment import Shipment
from app.models.enums import ShipmentStatus
from app.repositories.address_repository import AddressRepository
from app.repositories.shipment_repository import ShipmentRepository
from app.schemas.shipment_schema import ShipmentCreate
from app.utils.id_utils import new_uuid
from app.utils.tracking_utils import generate_tracking_number

class ShipmentService:
    def __init__(self):
        self.ship_repo = ShipmentRepository()
        self.addr_repo = AddressRepository()

    def create_shipment(self, db: Session, payload: ShipmentCreate) -> Shipment:
        # 1) Créer adresses
        pickup = Address(id=new_uuid(), **payload.pickup_address.dict())
        delivery = Address(id=new_uuid(), **payload.delivery_address.dict())

        self.addr_repo.create(db, pickup)
        self.addr_repo.create(db, delivery)

        # 2) Générer tracking unique (retry simple)
        tracking = None
        for _ in range(5):
            candidate = generate_tracking_number()
            if not self.ship_repo.find_by_tracking(db, candidate):
                tracking = candidate
                break
        if not tracking:
            raise HTTPException(status_code=500, detail="Cannot generate unique tracking number")

        # 3) Créer shipment
        shipment = Shipment(
            id=new_uuid(),
            tracking_number=tracking,
            status=ShipmentStatus.CREATED.value,
            service_level=payload.service_level.value,
            weight_kg=payload.weight_kg,
            pickup_address_id=pickup.id,
            delivery_address_id=delivery.id
        )

        self.ship_repo.create(db, shipment)
        db.commit()
        db.refresh(shipment)
        return shipment

    def get_shipment(self, db: Session, tracking_number: str) -> Shipment:
        shipment = self.ship_repo.find_by_tracking(db, tracking_number)
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        return shipment
