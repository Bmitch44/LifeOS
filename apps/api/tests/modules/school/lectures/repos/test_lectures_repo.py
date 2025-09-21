import pytest
from datetime import datetime

from app.modules.school.lectures.repo import LecturesRepo
from tests.factories import create_course, create_lecture


@pytest.mark.anyio
async def test_paginate(session):
    course = await create_course(session)
    for i in range(3):
        await create_lecture(session, course_id=course.id, name=f"L{i}")
    repo = LecturesRepo(session)
    page = await repo.paginate(1, 2)
    assert page.total == 3
    assert len(page.items) == 2


@pytest.mark.anyio
async def test_create_get_update_delete(session):
    course = await create_course(session)
    repo = LecturesRepo(session)
    created = await repo.create(type("Obj", (), {
        "course_id": course.id,
        "name": "N",
        "description": "D",
        "start_date": datetime(2025, 1, 1, 0, 0, 0),
        "end_date": datetime(2025, 1, 1, 1, 0, 0)
    })())
    assert created.id is not None
    got = await repo.get(created.id)
    assert got.id == created.id

    updated = await repo.update(created.id, type("Obj", (), {
        "course_id": course.id,
        "name": "N2",
        "description": "D2",
        "start_date": datetime(2025, 1, 1, 0, 0, 0),
        "end_date": datetime(2025, 1, 1, 1, 0, 0),
    })())
    assert updated.id == created.id

    res = await repo.delete(created.id)
    assert res["message"] == "Lecture deleted successfully"


