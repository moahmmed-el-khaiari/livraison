from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.report_router import router as report_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # TODO Security (Keycloak):
    # - plus tard: validation JWT au niveau gateway ou ici via Depends()
    yield
    # Shutdown


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Microservice de reporting (agrégation des données des autres MS).",
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

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": str(exc),
                "path": str(request.url.path),
            },
        )

    app.include_router(report_router)
    return app


app = create_app()
