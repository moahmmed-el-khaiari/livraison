from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.routers.tracking_router import router as tracking_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DEV: création auto des tables
    Base.metadata.create_all(bind=engine)
    yield
    # shutdown: rien à fermer ici


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Microservice de gestion des événements de suivi (tracking timeline).",
        lifespan=lifespan
    )

    # CORS (Angular / Gateway)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # en prod: mets l'URL exacte du front/gateway
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes système
    @app.get("/", tags=["System"])
    def root():
        return {"service": "tracking-service", "status": "running"}

    @app.get("/health", tags=["System"])
    def health():
        return {"status": "UP"}

    # Routes métier
    app.include_router(tracking_router)

    return app


app = create_app()
