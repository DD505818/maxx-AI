from importlib import reload

import backend.utils.settings as settings_module


def test_settings_override(monkeypatch) -> None:
    monkeypatch.setenv("ORCH_URL", "http://example.org")
    reload(settings_module)
    assert str(settings_module.settings.orch_url).rstrip("/") == "http://example.org"
