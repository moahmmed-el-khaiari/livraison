from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.routers.pod_router import router as pod_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DEV: create tables automatically
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Microservice de preuve de livraison (Proof Of Delivery).",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # =========================
    # (OPTION) Keycloak / Security
    # =========================
    # Quand tu activeras security-service + Keycloak dans tout le projet:
    # 1) Au niveau GATEWAY: tu protèges les routes /pod/** (JWT)
    # 2) Ici dans POD: tu peux soit laisser "trust gateway" (pas de JWT ici),
    #    soit vérifier le JWT côté POD aussi.
    #
    # Exemple (plus tard) si tu veux vérifier JWT dans FastAPI:
    # - Ajouter une dépendance "get_current_user" qui valide le token
    # - Appliquer Depends(get_current_user) sur les endpoints
    #
    # Pour l'instant: on laisse ouvert (comme shipment/tracking/delivery).

    @app.get("/", tags=["System"])
    def root():
        return {"service": settings.APP_NAME, "status": "running", "version": settings.APP_VERSION}

    @app.get("/health", tags=["System"])
    def health():
        return {"status": "UP"}

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": "INTERNAL_SERVER_ERROR", "message": "Erreur interne", "path": request.url.path},
        )

    app.include_router(pod_router)
    return app


app = create_app()
