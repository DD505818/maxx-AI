import pandas as pd
from fastapi.testclient import TestClient

from maxx_ai.backend.app.main import app


def test_backtest_endpoint() -> None:
    client = TestClient(app)
    dates = pd.date_range("2024-01-01", periods=60, freq="15min")
    df = pd.DataFrame(
        {
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.0,
            "volume": 1.0,
        },
        index=dates,
    )
    csv_bytes = df.to_csv().encode()
    resp = client.post(
        "/backtest",
        files={"file": ("data.csv", csv_bytes, "text/csv")},
        data={"strategy": "triple_ma"},
    )
    assert resp.status_code == 200
    payload = resp.json()
    assert "equity_curve" in payload
    assert "trades" in payload
