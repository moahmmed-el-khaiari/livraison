from app.clients.base_client import BaseHttpClient
from app.config import settings


def _resolve_base() -> str:
    if settings.USE_GATEWAY:
        return settings.GATEWAY_BASE_URL
    return settings.DELIVERY_BASE_URL


class DeliveryClient(BaseHttpClient):
    def __init__(self):
        super().__init__(_resolve_base())

    def list_deliveries(self):
        # Adapte selon ton delivery-service
        path = "/delivery/deliveries" if settings.USE_GATEWAY else "/deliveries"
        return self._get(path)
