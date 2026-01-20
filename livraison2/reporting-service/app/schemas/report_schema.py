from pydantic import BaseModel
from typing import Optional, Dict, Any


class OrdersReport(BaseModel):
    total: int
    by_status: Dict[str, int]


class DeliveriesReport(BaseModel):
    total: int
    by_status: Dict[str, int]


class TrackingReport(BaseModel):
    total_events: int
    latest_status_count: Dict[str, int]


class PodsReport(BaseModel):
    total: int



class ShipmentReport(BaseModel):
    tracking_number: str
    shipment: dict[str, Any]
    delivery: Optional[dict[str, Any]] = None
    latest_tracking: Optional[dict[str, Any]] = None
    pod: Optional[dict[str, Any]] = None



class DashboardReport(BaseModel):
    generated_at: str
    orders: OrdersReport
    deliveries: DeliveriesReport
    tracking: TrackingReport
    pods: Optional[PodsReport] = None
    raw_sources: Optional[Dict[str, Any]] = None  # utile en dev
