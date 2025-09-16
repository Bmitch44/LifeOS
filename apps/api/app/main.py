from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.middleware.setup import setup_middleware
from app.db.base import init_db
from app.modules.users.router import router as users_router
from app.modules.school.courses.router import router as courses_router
from app.modules.school.assesments.router import router as assesments_router
from app.modules.school.lectures.router import router as lectures_router
from app.modules.integrations.snaptrade.routers import (
    connection_router as snaptrade_connection_router,
    account_router as snaptrade_account_router,
    auth_router as snaptrade_auth_router
)
from app.modules.integrations.plaid.routers import (
    item_router as plaid_item_router,
    account_router as plaid_account_router,
    auth_router as plaid_auth_router
)

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
    app.include_router(lectures_router)

    app.include_router(snaptrade_connection_router)
    app.include_router(snaptrade_account_router)
    app.include_router(snaptrade_auth_router)
    app.include_router(plaid_item_router)
    app.include_router(plaid_account_router)
    app.include_router(plaid_auth_router)

    @app.get("/health", tags=["health"])  # simple readiness probe
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


