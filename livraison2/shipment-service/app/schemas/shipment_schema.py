from pydantic import BaseModel, Field, ConfigDict
from app.schemas.address_schema import AddressCreate, AddressOut
from app.models.enums import ServiceLevel


class ShipmentCreate(BaseModel):
    service_level: ServiceLevel = ServiceLevel.STANDARD
    weight_kg: float = Field(gt=0)

    pickup_address: AddressCreate
    delivery_address: AddressCreate


class ShipmentOut(BaseModel):
    id: str
    tracking_number: str
    status: str
    service_level: str
    weight_kg: float

    pickup_address: AddressOut
    delivery_address: AddressOut

    # Pydantic v2: permet de retourner directement l'objet Shipment (ORM)
    model_config = ConfigDict(from_attributes=True)
