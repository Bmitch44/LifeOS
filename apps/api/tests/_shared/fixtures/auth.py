import pytest
from app.core.auth import AuthenticatedUser
from app.deps import get_current_user


@pytest.fixture
def auth_user() -> AuthenticatedUser:
    return AuthenticatedUser(
        sub="sub_test",
        user_id="user_test",
        email="user@test.dev",
        first_name="Test",
        last_name="User",
        phone=None,
        raw={"sub": "sub_test"},
    )


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}


@pytest.fixture(autouse=True)
def override_current_user(app, auth_user):
    def _override():
        return auth_user
    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.pop(get_current_user, None)