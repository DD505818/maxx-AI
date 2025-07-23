from backend.services.risk_manager import RiskSentinel, Fill


def test_drawdown_halt() -> None:
    risk = RiskSentinel(max_dd=0.02)
    fill = Fill(order_id="1", symbol="BTCUSD", side="BUY", qty=50, price=100)
    risk.update(fill)
    assert risk.halt


def test_start_balance() -> None:
    risk = RiskSentinel(start_balance=500)
    assert risk.balance == 500


def test_value_at_risk() -> None:
    risk = RiskSentinel()
    risk.update(Fill(order_id="1", symbol="BTCUSD", side="BUY", qty=1, price=100))
    risk.update(Fill(order_id="2", symbol="BTCUSD", side="SELL", qty=1, price=90))
    assert risk.value_at_risk(confidence=0.95) > 0
