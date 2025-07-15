from backend.services.session_clock import session_active


def test_session_active() -> None:
    assert isinstance(session_active(), bool)
