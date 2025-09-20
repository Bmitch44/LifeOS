import pytest
from types import SimpleNamespace

from app.modules.finances.services.financial_account_service import FinancialAccountService


class FakeRepo:
    def __init__(self, session, user):
        self._session = session
        self._user = user
        self.created = []

    async def paginate(self, page, size):
        return type("Obj", (), {"items": [], "page": page, "size": size, "total": 0})()

    async def create(self, payload):
        self.created.append(payload)
        payload_dict = {
            "clerk_user_id": getattr(payload, "clerk_user_id", None),
            "type": getattr(payload, "type", None),
            "name": getattr(payload, "name", None),
            "institution_name": getattr(payload, "institution_name", None),
            "currency": getattr(payload, "currency", None),
            "current_balance": getattr(payload, "current_balance", None),
            "source": getattr(payload, "source", None),
            "source_account_id": getattr(payload, "source_account_id", None),
        }
        return SimpleNamespace(id=1, **payload_dict)

    async def get(self, id):
        return SimpleNamespace(id=id)

    async def update(self, id, payload):
        payload_dict = {
            "clerk_user_id": getattr(payload, "clerk_user_id", None),
            "type": getattr(payload, "type", None),
            "name": getattr(payload, "name", None),
            "institution_name": getattr(payload, "institution_name", None),
            "currency": getattr(payload, "currency", None),
            "current_balance": getattr(payload, "current_balance", None),
            "source": getattr(payload, "source", None),
            "source_account_id": getattr(payload, "source_account_id", None),
        }
        return SimpleNamespace(id=id, **payload_dict)

    async def delete(self, id):
        return {"message": "Financial account deleted successfully"}


class FakePlaidSvc:
    async def sync_accounts(self):
        return {"message": "ok"}


class FakeSnaptradeSvc:
    async def sync_accounts(self):
        return {"message": "ok"}


@pytest.mark.anyio
async def test_list_financial_accounts_unit(session, monkeypatch):
    svc = FinancialAccountService(session, "test_user")
    fake_repo = FakeRepo(session, "test_user")
    monkeypatch.setattr(svc, "repo", fake_repo)
    result = await svc.list_financial_accounts(1, 10)
    assert result.total == 0


@pytest.mark.anyio
async def test_create_get_update_delete_unit(session, monkeypatch):
    svc = FinancialAccountService(session, "test_user")
    fake_repo = FakeRepo(session, "test_user")
    monkeypatch.setattr(svc, "repo", fake_repo)

    created = await svc.create_financial_account(type("Obj", (), {
        "clerk_user_id": "test_user",
        "type": "bank",
        "name": "Name",
        "institution_name": "Inst",
        "currency": "USD",
        "current_balance": 1.0,
        "source": "plaid",
        "source_account_id": "src_1",
    })())
    assert created.id == 1

    got = await svc.get_financial_account(1)
    assert got.id == 1

    updated = await svc.update_financial_account(1, type("Obj", (), {
        "clerk_user_id": "test_user",
        "type": "bank",
        "name": "Name2",
        "institution_name": "Inst",
        "currency": "USD",
        "current_balance": 2.0,
        "source": "plaid",
        "source_account_id": "src_1",
    })())
    assert updated.name == "Name2"

    res = await svc.delete_financial_account(1)
    assert res["message"] == "Financial account deleted successfully"


@pytest.mark.anyio
async def test_sync_financial_accounts_unit(session, monkeypatch):
    svc = FinancialAccountService(session, "test_user")
    monkeypatch.setattr(svc, "plaid_account_service", FakePlaidSvc())
    monkeypatch.setattr(svc, "snaptrade_account_service", FakeSnaptradeSvc())
    res = await svc.sync_financial_accounts()
    assert res["message"] == "Financial accounts synced successfully"


