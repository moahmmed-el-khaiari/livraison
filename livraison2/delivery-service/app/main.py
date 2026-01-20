from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.routers.delivery_router import router as delivery_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Microservice de gestion de livraison (delivery tasks + intégration tracking).",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", tags=["System"])
    def root():
        return {"service": settings.APP_NAME, "version": settings.APP_VERSION, "status": "running"}

    @app.get("/health", tags=["System"])
    def health():
        return {"status": "UP"}

    app.include_router(delivery_router)
    return app


app = create_app()
