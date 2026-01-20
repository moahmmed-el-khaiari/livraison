from collections import Counter
from typing import Any, Optional

from app.clients.order_client import OrderClient
from app.clients.delivery_client import DeliveryClient
from app.clients.tracking_client import TrackingClient
from app.clients.shipment_client import ShipmentClient
from app.clients.pod_client import PodClient
from app.schemas.report_schema import (
    DashboardReport, OrdersReport, DeliveriesReport, TrackingReport, PodsReport , ShipmentReport
)
from app.utils.date_utils import now_utc_iso


class ReportingService:
    def __init__(self):
        self.orders = OrderClient()
        self.deliveries = DeliveryClient()
        self.tracking = TrackingClient()
        self.pods = PodClient()
        self.shipment = ShipmentClient()
        

    @staticmethod
    def _count_by_status(items: list[dict[str, Any]], field: str = "status") -> dict[str, int]:
        c = Counter()
        for it in items:
            s = it.get(field) or "UNKNOWN"
            c[str(s)] += 1
        return dict(c)

    def dashboard(self, include_raw: bool = False) -> DashboardReport:
        # -------- ORDERS --------
        orders_data = self.orders.list_orders() or []
        orders_report = OrdersReport(
            total=len(orders_data),
            by_status=self._count_by_status(orders_data, "status"),
        )

        # -------- DELIVERIES --------
        deliveries_data = self.deliveries.list_deliveries() or []
        deliveries_report = DeliveriesReport(
            total=len(deliveries_data),
            by_status=self._count_by_status(deliveries_data, "status"),
        )

        # -------- TRACKING (best effort) --------
        # Tracking-service n'a pas un endpoint "list all events" global.
        # Donc on agrège via les tracking_number qu'on connaît déjà (orders/deliveries).
        tracking_numbers = []

        for o in orders_data:
            tn = o.get("tracking_number")
            if tn:
                tracking_numbers.append(tn)

        for d in deliveries_data:
            tn = d.get("tracking_number")
            if tn:
                tracking_numbers.append(tn)

        tracking_numbers = list(dict.fromkeys(tracking_numbers))  # unique + preserve order

        all_events: list[dict[str, Any]] = []
        for tn in tracking_numbers:
            try:
                timeline = self.tracking.timeline(tn)
                # ton endpoint retourne souvent un dict { tracking_number, events, latest_status... }
                if isinstance(timeline, dict) and "events" in timeline:
                    all_events.extend(timeline.get("events") or [])
                elif isinstance(timeline, list):
                    all_events.extend(timeline)
            except Exception:
                # si un tracking_number n'existe pas encore dans tracking-service -> on ignore
                continue

        tracking_report = TrackingReport(
            total_events=len(all_events),
            latest_status_count=self._count_by_status(all_events, "status"),
        )

        # -------- PODS --------
        pods_report: Optional[PodsReport] = None
        pods_data = None
        try:
            pods_data = self.pods.list_pods() or []
            pods_report = PodsReport(total=len(pods_data))
        except Exception:
            pods_data = None

        # -------- RAW --------
        raw_sources = None
        if include_raw:
            raw_sources = {
                "orders": orders_data,
                "deliveries": deliveries_data,
                "tracking_events": all_events,
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
    
    def shipment_report(self, tracking_number: str) -> dict[str, Any]:
        shipment = self.shipment.get_shipment(tracking_number)

        delivery = None
        latest_tracking = None
        pod = None

        try:
            delivery = self.deliveries.get_one(tracking_number)
        except Exception:
            pass

        try:
            latest_tracking = self.tracking.latest(tracking_number)
        except Exception:
            pass

        try:
            pod = self.pods.list_pods()
        except Exception:
            pass

        return {
            "tracking_number": tracking_number,
            "shipment": shipment,
            "delivery": delivery,
            "latest_tracking": latest_tracking,
            "pod": pod,
        }

    def orders_report(self) -> OrdersReport:
        data = self.orders.list_orders() or []
        return OrdersReport(total=len(data), by_status=self._count_by_status(data, "status"))

    def deliveries_report(self) -> DeliveriesReport:
        data = self.deliveries.list_deliveries() or []
        return DeliveriesReport(total=len(data), by_status=self._count_by_status(data, "status"))

    def tracking_report(self, tracking_number: str) -> dict[str, Any]:
        timeline = self.tracking.timeline(tracking_number)
        latest = self.tracking.latest(tracking_number)

        return {
            "tracking_number": tracking_number,
            "latest": latest,
            "timeline": timeline,
        }
    
    def pods_report(self) -> PodsReport:
        data = self.pods.list_pods() or []
        return PodsReport(total=len(data))
