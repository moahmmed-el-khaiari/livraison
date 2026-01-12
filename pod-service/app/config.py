from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "pod-service"
    APP_VERSION: str = "1.0.0"

    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "db_pod"

    TRACKING_BASE_URL: str = "http://127.0.0.1:9002"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
