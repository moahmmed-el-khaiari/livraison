from enum import Enum

class ShipmentStatus(str, Enum):
    CREATED = "CREATED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    EXCEPTION = "EXCEPTION"

class ServiceLevel(str, Enum):
    STANDARD = "STANDARD"
    EXPRESS = "EXPRESS"
