import pytest

from tests.factories import create_course


@pytest.mark.anyio
async def test_list_courses(client, session):
    for i in range(5):
        await create_course(session, name=f"Course {i}", code=f"C{i}")
    r = await client.get("/v1/courses", params={"page": 1, "size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["total"] == 5
    assert len(data["items"]) == 2


@pytest.mark.anyio
async def test_get_course(client, session):
    course = await create_course(session)
    r = await client.get(f"/v1/courses/{course.id}")
    assert r.status_code == 200
    assert r.json()["id"] == course.id


@pytest.mark.anyio
async def test_create_course(client):
    payload = {
        "name": "New Course",
        "description": "Desc",
        "code": "NC101",
        "professor_name": "Prof",
        "professor_email": "prof@example.com",
        "credits": 3,
        "semester": "Fall",
        "year": 2025,
        "department": "CS",
        "campus": "Main",
        "location": "Bldg",
        "final_grade": 0.0,
    }
    r = await client.post("/v1/courses", json=payload)
    assert r.status_code == 201
    assert r.json()["code"] == "NC101"


@pytest.mark.anyio
async def test_update_course(client, session):
    course = await create_course(session)
    payload = {
        "name": course.name,
        "description": "New Desc",
        "code": course.code,
        "professor_name": "Prof",
        "professor_email": "prof@example.com",
        "credits": 4,
        "semester": "Spring",
        "year": 2026,
        "department": "CS",
        "campus": "Main",
        "location": "Bldg",
        "final_grade": 1.0,
    }
    r = await client.put(f"/v1/courses/{course.id}", json=payload)
    assert r.status_code == 200
    assert r.json()["credits"] == 4


@pytest.mark.anyio
async def test_delete_course(client, session):
    course = await create_course(session)
    r = await client.delete(f"/v1/courses/{course.id}")
    assert r.status_code == 200
    assert r.json()["message"] == "Course deleted successfully"
