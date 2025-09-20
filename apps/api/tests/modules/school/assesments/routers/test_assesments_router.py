import pytest

from tests.factories import create_course, create_assesment


@pytest.mark.anyio
async def test_list_assesments(client, session):
    course = await create_course(session)
    for i in range(5):
        await create_assesment(session, course_id=course.id, name=f"Assesment {i}")
    r = await client.get("/v1/assesments", params={"page": 1, "size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2


@pytest.mark.anyio
async def test_get_assesment(client, session):
    a = await create_assesment(session)
    r = await client.get(f"/v1/assesments/{a.id}")
    assert r.status_code == 200
    assert r.json()["id"] == a.id


@pytest.mark.anyio
async def test_create_assesment(client, session):
    course = await create_course(session)
    payload = {
        "course_id": course.id,
        "name": "New",
        "description": "Desc",
        "type": "exam",
        "start_date": "2025-01-01T00:00:00",
        "end_date": "2025-01-01T01:00:00",
        "weight": 0.4,
        "final_grade": 0.0,
    }
    r = await client.post("/v1/assesments", json=payload)
    assert r.status_code == 201
    assert r.json()["name"] == "New"


@pytest.mark.anyio
async def test_update_assesment(client, session):
    a = await create_assesment(session)
    payload = {
        "course_id": a.course_id,
        "name": a.name,
        "description": "Updated",
        "type": "quiz",
        "start_date": "2025-01-01T00:00:00",
        "end_date": "2025-01-01T01:00:00",
        "weight": 0.5,
        "final_grade": 1.0,
    }
    r = await client.put(f"/v1/assesments/{a.id}", json=payload)
    assert r.status_code == 200
    assert r.json()["type"] == "quiz"


@pytest.mark.anyio
async def test_delete_assesment(client, session):
    a = await create_assesment(session)
    r = await client.delete(f"/v1/assesments/{a.id}")
    assert r.status_code == 200
    assert r.json()["message"] == "Assesment deleted successfully"
