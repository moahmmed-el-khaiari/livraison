import os
from dotenv import load_dotenv

load_dotenv()  # charge .env

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "shipment-service")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "db_shipments")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASS: str = os.getenv("DB_PASS", "")

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
