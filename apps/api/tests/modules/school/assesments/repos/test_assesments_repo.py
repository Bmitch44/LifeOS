import pytest
from datetime import datetime

from app.modules.school.assesments.repo import AssesmentsRepo
from tests.factories import create_course, create_assesment


@pytest.mark.anyio
async def test_paginate(session):
    course = await create_course(session)
    for i in range(3):
        await create_assesment(session, course_id=course.id, name=f"A{i}")
    repo = AssesmentsRepo(session)
    page = await repo.paginate(1, 2)
    assert page.total == 3
    assert len(page.items) == 2


@pytest.mark.anyio
async def test_create_get_update_delete(session):
    course = await create_course(session)
    repo = AssesmentsRepo(session)
    created = await repo.create(type("Obj", (), {
        "course_id": course.id,
        "name": "N",
        "description": "D",
        "type": "exam",
        "start_date": datetime(2025, 1, 1, 0, 0, 0),
        "end_date": datetime(2025, 1, 1, 1, 0, 0),
        "weight": 0.4,
        "final_grade": 0.0,
    })())
    assert created.id is not None
    got = await repo.get(created.id)
    assert got.id == created.id

    updated = await repo.update(created.id, type("Obj", (), {
        "course_id": course.id,
        "name": "N2",
        "description": "D2",
        "type": "quiz",
        "start_date": datetime(2025, 1, 1, 0, 0, 0),
        "end_date": datetime(2025, 1, 1, 1, 0, 0),
        "weight": 0.5,
        "final_grade": 1.0,
    })())
    assert updated.type == "quiz"

    res = await repo.delete(created.id)
    assert res["message"] == "Assesment deleted successfully"


