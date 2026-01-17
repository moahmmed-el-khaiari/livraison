from app.clients.base_client import BaseHttpClient
from app.config import settings


def _resolve_base() -> str:
    if settings.USE_GATEWAY:
        return settings.GATEWAY_BASE_URL
    return settings.POD_BASE_URL


class PodClient(BaseHttpClient):
    def __init__(self):
        super().__init__(_resolve_base())

    def list_pods(self):
        # Adapte selon ton pod-service
        path = "/pod/pods" if settings.USE_GATEWAY else "/pods"
        return self._get(path)
