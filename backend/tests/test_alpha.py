from backend.services.alpha_ensemble import AlphaEngine


def test_alpha_score() -> None:
    engine = AlphaEngine(
        ["BTCUSD"],
        weights={"momentum": 0.5, "sentiment": 0.3, "mean_reversion": 0.2},
    )
    for _ in range(60):
        engine.update("BTCUSD", 100.0)
    assert isinstance(engine.score("BTCUSD", sentiment=0.1), float)
