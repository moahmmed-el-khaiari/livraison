from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.routers.shipment_router import router as shipment_router


# =========================
# Lifespan (startup/shutdown)
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    # Création des tables (DEV / projet master)
    # En production, on préfère Alembic, mais pour ton projet c'est OK.
    Base.metadata.create_all(bind=engine)

    yield

    # --- Shutdown ---
    # (rien à fermer ici, SQLAlchemy engine gère le pool)
    # Tu pourrais fermer des connexions externes ici.
    pass


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Microservice de création et consultation des expéditions (Shipments).",
        lifespan=lifespan
    )

    # =========================
    # CORS (Angular)
    # =========================
    # En dev: autoriser tout. En prod: mettre le domaine exact du front/gateway.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # =========================
    # Routes système
    # =========================
    @app.get("/", tags=["System"])
    def root():
        return {
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running"
        }

    @app.get("/health", tags=["System"])
    def health():
        return {"status": "UP"}

    # =========================
    # Handlers d'erreurs (propre)
    # =========================
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # Tu peux logger ici si tu veux (logging)
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "Une erreur interne est survenue.",
                "path": str(request.url.path),
            },
        )

    # =========================
    # Routers métier
    # =========================
    app.include_router(shipment_router)

    return app


app = create_app()
