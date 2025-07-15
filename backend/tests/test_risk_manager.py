from backend.services.risk_manager import RiskSentinel, Fill


def test_can_trade_position_limit() -> None:
    risk = RiskSentinel(max_position_pct=0.01)
    # initial exposure is zero; should allow trade
    assert risk.can_trade("BTCUSD", 0.01, 50_000.0)
    # update with a fill to reach limit
    risk.update(Fill("1", "BTCUSD", "BUY", 0.02, 50_000.0))
    # additional trade would exceed limit
    assert not risk.can_trade("BTCUSD", 0.05, 50_000.0)
