from app.modules.integrations.snaptrade.mappers.snaptrade_account_mapper import SnaptradeAccountMapper


def test_snaptrade_mapper_maps_basic_fields():
    mapper = SnaptradeAccountMapper("user_test")

    class Obj:
        def get(self, k, d=None):
            data = {
                "id": "sa_1",
                "brokerage_authorization": "conn_1",
                "name": "A",
                "number": "****1111",
                "institution_name": "Broker One",
                "status": "ACTIVE",
                "raw_type": "cash",
                "balance": {"total": {"amount": 5000.0, "currency": "CAD"}},
            }
            return data.get(k, d)

    payload = mapper.map_api_account_to_snaptrade_account(Obj())
    assert payload.account_id == "sa_1"
    assert payload.currency == "CAD"