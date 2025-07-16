from backend.services.risk_manager import RiskSentinel, Fill


def test_intraday_drawdown() -> None:
    risk = RiskSentinel()
    fill = Fill(symbol="BTCUSD", side="SELL", qty=1, price=100)
    risk.update(fill)
    assert risk.intraday_dd() >= 0
