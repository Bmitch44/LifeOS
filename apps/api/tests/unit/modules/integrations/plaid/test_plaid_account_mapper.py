from app.modules.integrations.plaid.mappers import PlaidAccountToFinancialAccountMapper


def test_mapper_maps_basic_fields():
    mapper = PlaidAccountToFinancialAccountMapper("user_test")

    class Obj:
        def get(self, k, d=None):
            data = {
                "account_id": "pa_1",
                "name": "N",
                "official_name": "ON",
                "type": "T",
                "subtype": "ST",
                "mask": "1111",
            }
            return data.get(k, d)

        balances = type("B", (), {"current": 10.0, "available": 8.0, "iso_currency_code": "CAD"})()

    payload = mapper.map_api_account_to_plaid_account(Obj())
    assert payload.account_id == "pa_1"
    assert payload.iso_currency_code == "CAD"