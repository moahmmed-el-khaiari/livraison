from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "reporting-service"
    APP_VERSION: str = "1.0.0"
    CORS_ORIGINS: str = "*"

    # ✅ AJOUTE CA
    USE_GATEWAY: bool = False
    SHIPMENT_BASE_URL: str = "http://127.0.0.1:9001"
    ORDER_BASE_URL: str = "http://127.0.0.1:9009"
    DELIVERY_BASE_URL: str = "http://127.0.0.1:9003"
    TRACKING_BASE_URL: str = "http://127.0.0.1:9002"
    POD_BASE_URL: str = "http://127.0.0.1:9004"

    HTTP_TIMEOUT_SECONDS: float = Field(default=5.0)

settings = Settings()
