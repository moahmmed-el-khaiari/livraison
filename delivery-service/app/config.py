from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "delivery-service"
    APP_VERSION: str = "1.0.0"

    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "db_deliveries"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""

    TRACKING_BASE_URL: str = "http://127.0.0.1:9001"

    class Config:
        env_file = ".env"


settings = Settings()
