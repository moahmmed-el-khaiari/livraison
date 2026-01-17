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


class DashboardReport(BaseModel):
    generated_at: str
    orders: OrdersReport
    deliveries: DeliveriesReport
    tracking: TrackingReport
    pods: Optional[PodsReport] = None
    raw_sources: Optional[Dict[str, Any]] = None  # utile en dev
