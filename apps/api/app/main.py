from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.middleware.setup import setup_middleware
from app.db.base import init_db
from app.modules.users.router import router as users_router
from app.modules.school.courses.router import router as courses_router
from app.modules.school.assesments.router import router as assesments_router
from app.modules.school.documents.router import router as documents_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="LifeOS API", version="0.1.0", lifespan=lifespan)
    setup_middleware(app)

    # Routers
    app.include_router(users_router)
    app.include_router(courses_router)
    app.include_router(assesments_router)
    app.include_router(documents_router)

    @app.get("/health", tags=["health"])  # simple readiness probe
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


