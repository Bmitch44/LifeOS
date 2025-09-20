import pytest

from app.modules.school.courses.repo import CoursesRepo
from tests.factories import create_course


@pytest.mark.anyio
async def test_paginate(session):
    for i in range(3):
        await create_course(session, name=f"C{i}", code=f"X{i}")
    repo = CoursesRepo(session)
    page = await repo.paginate(1, 2)
    assert page.total == 3
    assert len(page.items) == 2


@pytest.mark.anyio
async def test_create_get_update_delete(session):
    repo = CoursesRepo(session)
    created = await repo.create(type("Obj", (), {
        "name": "N",
        "description": "D",
        "code": "CD",
        "professor_name": "P",
        "professor_email": "p@ex.com",
        "credits": 3,
        "semester": "Fall",
        "year": 2025,
        "department": "CS",
        "campus": "Main",
        "location": "Bldg",
        "final_grade": 0.0,
    })())
    assert created.id is not None
    got = await repo.get(created.id)
    assert got.id == created.id

    updated = await repo.update(created.id, type("Obj", (), {
        "name": "N2",
        "description": "D2",
        "code": "CD",
        "professor_name": "P",
        "professor_email": "p@ex.com",
        "credits": 4,
        "semester": "Spring",
        "year": 2026,
        "department": "CS",
        "campus": "Main",
        "location": "Bldg",
        "final_grade": 1.0,
    })())
    assert updated.credits == 4

    res = await repo.delete(created.id)
    assert res["message"] == "Course deleted successfully"


