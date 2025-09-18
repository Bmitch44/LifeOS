import pytest

from tests.factories import create_user


@pytest.mark.anyio
async def test_list_users_pagination(client, session):
    # seed
    for i in range(1, 6):
        await create_user(session, clerk_user_id=f"user_{i}", email=f"u{i}@ex.com")

    r = await client.get("/v1/users", params={"page": 1, "size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2


@pytest.mark.anyio
async def test_get_user(client, session):
    user = await create_user(session)
    r = await client.get(f"/v1/users/{user.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == user.id
    assert data["email"] == user.email


@pytest.mark.anyio
async def test_update_user(client, session):
    user = await create_user(session)
    payload = {
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "Name",
        "phone": "123",
    }
    r = await client.put(f"/v1/users/{user.id}", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]


@pytest.mark.anyio
async def test_delete_user(client, session):
    user = await create_user(session)
    r = await client.delete(f"/v1/users/{user.id}")
    assert r.status_code == 200
    assert r.json()["message"] == "User deleted successfully"


