from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import settings
from api.v1 import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: add DB migrations check, connection pool warm-up here (Phase 2)
    yield
    # Shutdown: cleanup resources (e.g., close Redis, flush queues)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
        docs_url="/docs" if settings.DEBUG else None,  # Hide docs in production
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.DEBUG else [],  # Lock down in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(v1_router, prefix=settings.API_V1_PREFIX)

    # Health check — always mounted, no auth required
    @app.get("/health", tags=["System"])
    async def health():
        return {"status": "ok", "version": settings.APP_VERSION, "env": settings.ENV}

    return app


app = create_app()
