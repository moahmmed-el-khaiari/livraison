from collections import Counter
from typing import Any

from app.clients.order_client import OrderClient
from app.clients.delivery_client import DeliveryClient
from app.clients.tracking_client import TrackingClient
from app.clients.pod_client import PodClient
from app.schemas.report_schema import (
    DashboardReport, OrdersReport, DeliveriesReport, TrackingReport, PodsReport
)
from app.utils.date_utils import now_utc_iso


class ReportingService:
    def __init__(self):
        self.orders = OrderClient()
        self.deliveries = DeliveryClient()
        self.tracking = TrackingClient()
        self.pods = PodClient()

    @staticmethod
    def _count_by_status(items: list[dict[str, Any]], field: str = "status") -> dict[str, int]:
        c = Counter()
        for it in items:
            s = (it.get(field) or "UNKNOWN")
            c[str(s)] += 1
        return dict(c)

    def dashboard(self, include_raw: bool = False) -> DashboardReport:
        orders_data = self.orders.list_orders() or []
        deliveries_data = self.deliveries.list_deliveries() or []
        tracking_data = self.tracking.list_events() or []

        orders_report = OrdersReport(
            total=len(orders_data),
            by_status=self._count_by_status(orders_data, "status"),
        )

        deliveries_report = DeliveriesReport(
            total=len(deliveries_data),
            by_status=self._count_by_status(deliveries_data, "status"),
        )

        # Tracking: on compte nombre total d’events et (option) latest_status_count si tu exposes latest par tracking_number
        # Ici simple: count events by status
        tracking_report = TrackingReport(
            total_events=len(tracking_data),
            latest_status_count=self._count_by_status(tracking_data, "status"),
        )

        # POD optionnel
        pods_report = None
        try:
            pods_data = self.pods.list_pods() or []
            pods_report = PodsReport(total=len(pods_data))
        except Exception:
            pods_data = None  # si pod-service pas prêt

        raw_sources = None
        if include_raw:
            raw_sources = {
                "orders": orders_data,
                "deliveries": deliveries_data,
                "tracking": tracking_data,
                "pods": pods_data,
            }

        return DashboardReport(
            generated_at=now_utc_iso(),
            orders=orders_report,
            deliveries=deliveries_report,
            tracking=tracking_report,
            pods=pods_report,
            raw_sources=raw_sources,
        )

    def orders_report(self) -> OrdersReport:
        data = self.orders.list_orders() or []
        return OrdersReport(total=len(data), by_status=self._count_by_status(data, "status"))

    def deliveries_report(self) -> DeliveriesReport:
        data = self.deliveries.list_deliveries() or []
        return DeliveriesReport(total=len(data), by_status=self._count_by_status(data, "status"))

    def tracking_report(self) -> TrackingReport:
        data = self.tracking.list_events() or []
        return TrackingReport(total_events=len(data), latest_status_count=self._count_by_status(data, "status"))

    def pods_report(self) -> PodsReport:
        data = self.pods.list_pods() or []
        return PodsReport(total=len(data))
