import asyncio
from backend.models.plan_v2 import Leg
from backend.services.order_router import Router
from backend.services.risk_manager import Fill


def test_execute_order() -> None:
    router = Router(["binance"])
    leg = Leg(symbol="BTCUSD", side="BUY", qty=0.1, broker=router.best_venue("BTCUSD"), price=100)
    fill = asyncio.run(router.execute(leg))
    assert isinstance(fill, Fill)
    assert fill.symbol == "BTCUSD"
    assert fill.qty == 0.1

