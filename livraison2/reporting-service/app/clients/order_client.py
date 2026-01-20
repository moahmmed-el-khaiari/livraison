from app.clients.base_client import BaseClient
from app.config import settings


def _resolve_base() -> str:
    if settings.ORDER_BASE_URL:
        # Exemple route gateway: /order/...
        return settings.ORDER_BASE_URL
    return settings.ORDER_BASE_URL


class OrderClient(BaseClient):
    def __init__(self):
        super().__init__(_resolve_base())

    def list_orders(self):
      
        path = "/order/orders" if settings.ORDER_BASE_URL else "/orders"
        return self._get(path)
