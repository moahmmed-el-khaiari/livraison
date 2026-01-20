import httpx
from app.config import settings


class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str, params: dict | None = None):
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client(timeout=settings.HTTP_TIMEOUT_SECONDS) as client:
                resp = client.get(url, params=params)
        except httpx.RequestError as e:
            raise RuntimeError(f"Connection error calling {url}: {e}") from e

        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code} calling {url}: {resp.text}")

        return resp.json()
