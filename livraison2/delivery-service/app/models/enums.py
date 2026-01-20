from enum import Enum


class DeliveryStatus(str, Enum):
    CREATED = "CREATED"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    FAILED_ATTEMPT = "FAILED_ATTEMPT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
