import httpx
from app.config import settings
from app.schemas.tracking_external_schema import TrackingEventCreate, TrackingEventOut


class TrackingClient:
    def __init__(self, base_url: str | None = None, timeout: float = 5.0):
        self.base_url = (base_url or settings.TRACKING_BASE_URL).rstrip("/")
        self.timeout = httpx.Timeout(timeout=timeout, connect=2.0)

    def add_event(self, payload: TrackingEventCreate) -> TrackingEventOut:
        url = f"{self.base_url}/tracking/events"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(url, json=payload.model_dump())
        except httpx.RequestError as e:
            raise RuntimeError(f"tracking-service unreachable: {str(e)}") from e

        if resp.status_code >= 400:
            raise RuntimeError(f"tracking-service error {resp.status_code}: {resp.text}")

        return TrackingEventOut(**resp.json())

    def get_latest_status(self, tracking_number: str) -> str:
        """
        Appelle tracking-service et retourne latest_status.
        Endpoint utilisé: GET /tracking/{tracking_number}
        (car ta réponse contient: latest_status)
        """
        url = f"{self.base_url}/tracking/{tracking_number}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.get(url)
        except httpx.RequestError as e:
            raise RuntimeError(f"tracking-service unreachable: {str(e)}") from e

        if resp.status_code >= 400:
            raise RuntimeError(f"tracking-service error {resp.status_code}: {resp.text}")

        data = resp.json()
        # attendu: {"tracking_number": "...", "latest_status": "...", "events": [...]}
        return data.get("latest_status") or data.get("status")
