from fastapi import APIRouter, Query
from app.services.reporting_service import ReportingService
from app.schemas.report_schema import DashboardReport, OrdersReport, DeliveriesReport, ShipmentReport, TrackingReport, PodsReport
from fastapi import APIRouter, Query
from app.services.reporting_service import ReportingService
router = APIRouter(prefix="/reports", tags=["Reports"])
service = ReportingService()


@router.get("/dashboard", response_model=DashboardReport)
def dashboard(include_raw: bool = Query(default=False, description="Inclure les données brutes (DEV)")):
    return service.dashboard(include_raw=include_raw)


@router.get("/orders", response_model=OrdersReport)
def orders():
    return service.orders_report()

@router.get("/deliveries", response_model=DeliveriesReport)
def deliveries():
    return service.deliveries_report()

@router.get("/tracking")
def tracking_report(tracking_number: str = Query(..., description="Tracking number")):
    return service.tracking_report(tracking_number)


@router.get("/pods", response_model=PodsReport)
def pods():
    return service.pods_report()

@router.get("/shipment/{tracking_number}/", response_model=ShipmentReport)
def shipment(tracking_number: str):
    return service.shipment_report(tracking_number)