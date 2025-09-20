import pytest
from types import SimpleNamespace

from app.modules.school.courses.service import CoursesService


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
        return {"message": "Course deleted successfully"}


@pytest.mark.anyio
async def test_list_create_get_update_delete_unit(session, monkeypatch):
    svc = CoursesService(session)
    monkeypatch.setattr(svc, "repo", FakeRepo())
    page = await svc.list_courses(1, 10)
    assert page.total == 0

    created = await svc.create_course(SimpleNamespace(name="N", description="D", code="C", professor_name="P", professor_email="p@ex.com", credits=3, semester="Fall", year=2025, department="CS", campus="Main", location="Bldg", final_grade=0.0))
    assert created.id == 1

    got = await svc.get_course(1)
    assert got.id == 1

    updated = await svc.update_course(1, SimpleNamespace(name="N2", description="D2", code="C", professor_name="P", professor_email="p@ex.com", credits=4, semester="Spring", year=2026, department="CS", campus="Main", location="Bldg", final_grade=1.0))
    assert updated.credits == 4

    res = await svc.delete_course(1)
    assert res["message"] == "Course deleted successfully"


