import pytest
from httpx import AsyncClient, ASGITransport

from app.main import create_app
from app.db.base import get_session


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
async def client(app, db_session):
    async def _get_session_override():
        yield db_session
    app.dependency_overrides[get_session] = _get_session_override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c