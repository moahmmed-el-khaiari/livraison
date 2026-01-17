from app.clients.base_client import BaseHttpClient
from app.config import settings


def _resolve_base() -> str:
    if settings.USE_GATEWAY:
        # Exemple route gateway: /order/...
        return settings.GATEWAY_BASE_URL
    return settings.ORDER_BASE_URL


class OrderClient(BaseHttpClient):
    def __init__(self):
        super().__init__(_resolve_base())

    def list_orders(self):
        # Adapte ces paths selon ton order-service
        # Via gateway: GET http://localhost:8080/order/orders
        # Direct:      GET http://localhost:9002/orders
        path = "/order/orders" if settings.USE_GATEWAY else "/orders"
        return self._get(path)
