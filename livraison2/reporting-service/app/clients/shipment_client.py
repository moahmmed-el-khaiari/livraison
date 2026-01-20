from app.clients.base_client import BaseClient
from app.config import settings


class ShipmentClient(BaseClient):
    def __init__(self):
        super().__init__(settings.SHIPMENT_BASE_URL)

    def get_shipment(self, tracking_number: str):
        # GET /shipments/{tracking_number}
        return self._get(f"/shipments/{tracking_number}")
