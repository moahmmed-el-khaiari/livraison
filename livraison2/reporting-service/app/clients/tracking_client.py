from app.clients.base_client import BaseClient
from app.config import settings


class TrackingClient(BaseClient):
    def __init__(self):
        super().__init__(settings.TRACKING_BASE_URL)

    def timeline(self, tracking_number: str):
        # GET /tracking/{tracking_number}
        return self._get(f"/tracking/{tracking_number}")

    def latest(self, tracking_number: str):
        # GET /tracking/{tracking_number}/latest
        return self._get(f"/tracking/{tracking_number}/latest")
