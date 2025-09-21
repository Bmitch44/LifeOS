import pytest

from tests.factories import create_course, create_lecture


@pytest.mark.anyio
async def test_list_lectures(client, session):
    course = await create_course(session)
    for i in range(5):
        await create_lecture(session, course_id=course.id, name=f"Lecture {i}")
    r = await client.get("/v1/lectures", params={"page": 1, "size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2


@pytest.mark.anyio
async def test_get_lecture(client, session):
    lecture = await create_lecture(session)
    r = await client.get(f"/v1/lectures/{lecture.id}")
    assert r.status_code == 200
    assert r.json()["id"] == lecture.id


@pytest.mark.anyio
async def test_create_lecture(client, session):
    course = await create_course(session)
    payload = {
        "course_id": course.id,
        "name": "New Lecture",
        "description": "Desc",
        "start_date": "2025-01-01T00:00:00",
        "end_date": "2025-01-01T01:00:00",
        "weight": 0.2,
        "final_grade": 0.0,
    }
    r = await client.post("/v1/lectures", json=payload)
    assert r.status_code == 201
    assert r.json()["name"] == "New Lecture"


@pytest.mark.anyio
async def test_update_lecture(client, session):
    lecture = await create_lecture(session)
    payload = {
        "course_id": lecture.course_id,
        "name": lecture.name,
        "description": "Updated",
        "start_date": "2025-01-01T00:00:00",
        "end_date": "2025-01-01T01:00:00",
    }
    r = await client.put(f"/v1/lectures/{lecture.id}", json=payload)
    assert r.status_code == 200
    assert r.json()["id"] == lecture.id


@pytest.mark.anyio
async def test_delete_lecture(client, session):
    lecture = await create_lecture(session)
    r = await client.delete(f"/v1/lectures/{lecture.id}")
    assert r.status_code == 200
    assert r.json()["message"] == "Lecture deleted successfully"
