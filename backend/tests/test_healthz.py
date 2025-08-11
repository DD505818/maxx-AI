from fastapi.testclient import TestClient
from backend.api.main import app


def test_healthz_fields() -> None:
    client = TestClient(app)
    resp = client.get("/healthz")
    assert resp.status_code == 200
    data = resp.json()
    assert all(k in data for k in ["uptime", "lag", "reason"])
