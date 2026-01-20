from enum import Enum

class TrackingStatus(str, Enum):
    CREATED = "CREATED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    EXCEPTION = "EXCEPTION"

class EventSource(str, Enum):
    SYSTEM = "SYSTEM"
    COURIER = "COURIER"
    HUB = "HUB"
