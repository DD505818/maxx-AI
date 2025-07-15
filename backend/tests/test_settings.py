from importlib import reload

import backend.utils.settings as settings_module


def test_settings_override(monkeypatch) -> None:
    monkeypatch.setenv("ORCH_URL", "http://example.org")
    monkeypatch.setenv("MAX_DRAWDOWN_PCT", "0.1")
    reload(settings_module)
    assert str(settings_module.settings.orch_url).rstrip("/") == "http://example.org"
    assert settings_module.settings.max_drawdown_pct == 0.1

