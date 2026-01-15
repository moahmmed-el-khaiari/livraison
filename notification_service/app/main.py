import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.routers.notification_router import router as notification_router
from app.services.dispatcher import Dispatcher

dispatcher = Dispatcher()
_dispatch_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables (DEV)
    Base.metadata.create_all(bind=engine)

    # background dispatcher (optionnel)
    global _dispatch_task
    _dispatch_task = asyncio.create_task(dispatcher.run())

    yield

    # shutdown
    dispatcher.stop()
    if _dispatch_task:
        _dispatch_task.cancel()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Microservice de notifications (events) pour order/shipment/tracking/delivery/pod.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.CORS_ORIGINS] if settings.CORS_ORIGINS != "*" else ["*"],
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

    # ============================
    # Keycloak / JWT (COMMENTÉ)
    # ============================
    # Plus tard tu feras :
    # - Gateway valide JWT
    # - Chaque MS valide JWT (resource server)
    #
    # Exemple (Spring) : oauth2ResourceServer().jwt()
    # Exemple (FastAPI) : middleware + JWKS Keycloak
    #
    # Ici on laisse désactivé pour dev.

    app.include_router(notification_router)
    return app

app = create_app()
