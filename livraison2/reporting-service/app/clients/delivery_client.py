from app.clients.base_client import BaseClient
from app.config import settings

class DeliveryClient(BaseClient):
    def __init__(self):
        super().__init__(settings.DELIVERY_BASE_URL)

    def list_deliveries(self):
        return self._get("/delivery/deliveries")

    def get_one(self, tracking_number: str):
        return self._get(f"/delivery/{tracking_number}")
