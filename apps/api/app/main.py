from fastapi import FastAPI

from .middleware.setup import setup_middleware
from .modules.users.router import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(title="LifeOS API", version="0.1.0")
    setup_middleware(app)

    # Routers
    app.include_router(users_router)

    @app.get("/health", tags=["health"])  # simple readiness probe
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


