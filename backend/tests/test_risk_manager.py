from backend.services.risk_manager import RiskSentinel, Fill


def test_drawdown_halt() -> None:
    risk = RiskSentinel(max_dd=0.02)
    fill = Fill(order_id="1", symbol="BTCUSD", side="BUY", qty=50, price=100)
    risk.update(fill)
    assert risk.halt
