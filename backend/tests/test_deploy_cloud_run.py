import pytest

import scripts.deploy_cloud_run as deploy


def test_env_required(monkeypatch: pytest.MonkeyPatch) -> None:
    """The script should raise KeyError when GCP_PROJECT is missing."""
    monkeypatch.delenv("GCP_PROJECT", raising=False)
    with pytest.raises(KeyError):
        deploy.main()
