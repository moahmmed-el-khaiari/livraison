from app.clients.base_client import BaseClient
from app.config import settings


def _resolve_base() -> str:
    if settings.POD_BASE_URL:
        return settings.POD_BASE_URL
    return settings.POD_BASE_URL


class PodClient(BaseClient):
    def __init__(self):
        super().__init__(_resolve_base())

    def list_pods(self):
        # Adapte selon ton pod-service
        path = "/pod/pods" if settings.POD_BASE_URL else "/pods"
        return self._get(path)
