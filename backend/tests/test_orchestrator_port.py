from backend.api.orchestrator import server_port


def test_server_port_env(monkeypatch):
    monkeypatch.setenv("PORT", "5555")
    assert server_port() == 5555
    monkeypatch.delenv("PORT", raising=False)
    assert server_port() == 8080

