from fastapi.responses import Response
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_health():
    r: Response = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


