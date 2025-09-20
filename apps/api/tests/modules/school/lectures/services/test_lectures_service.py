import pytest
from types import SimpleNamespace

from app.modules.school.lectures.service import LecturesService


class FakeRepo:
    async def paginate(self, page, size):
        return SimpleNamespace(items=[], page=page, size=size, total=0)

    async def create(self, payload):
        return SimpleNamespace(id=1, **payload.__dict__)

    async def get(self, id):
        return SimpleNamespace(id=id)

    async def update(self, id, payload):
        return SimpleNamespace(id=id, **payload.__dict__)

    async def delete(self, id):
        return {"message": "Lecture deleted successfully"}


@pytest.mark.anyio
async def test_list_create_get_update_delete_unit(session, monkeypatch):
    svc = LecturesService(session)
    monkeypatch.setattr(svc, "repo", FakeRepo())
    page = await svc.list_lectures(1, 10)
    assert page.total == 0

    created = await svc.create_lecture(SimpleNamespace(course_id=1, name="N", description="D", start_date="2025-01-01T00:00:00", end_date="2025-01-01T01:00:00", weight=0.3, final_grade=0.0))
    assert created.id == 1

    got = await svc.get_lecture(1)
    assert got.id == 1

    updated = await svc.update_lecture(1, SimpleNamespace(course_id=1, name="N2", description="D2", start_date="2025-01-01T00:00:00", end_date="2025-01-01T01:00:00", weight=0.5, final_grade=1.0))
    assert updated.weight == 0.5

    res = await svc.delete_lecture(1)
    assert res["message"] == "Lecture deleted successfully"


