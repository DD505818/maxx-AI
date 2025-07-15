from backend.services.alpha_ensemble import AlphaEngine


def test_alpha_score() -> None:
    engine = AlphaEngine(["BTCUSD"])
    for _ in range(60):
        engine.update("BTCUSD", 100.0)
    assert isinstance(engine.score("BTCUSD"), float)
