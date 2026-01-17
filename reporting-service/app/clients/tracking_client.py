from app.clients.base_client import BaseHttpClient
from app.config import settings


def _resolve_base() -> str:
    if settings.USE_GATEWAY:
        return settings.GATEWAY_BASE_URL
    return settings.TRACKING_BASE_URL


class TrackingClient(BaseHttpClient):
    def __init__(self):
        super().__init__(_resolve_base())

    def list_events(self):
        # Adapte selon ton tracking-service
        path = "/tracking/events" if settings.USE_GATEWAY else "/tracking/events"
        return self._get(path)
