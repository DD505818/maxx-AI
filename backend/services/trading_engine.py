"""Asynchronous trading engine orchestrating signals, orders, and risk."""

import asyncio
import logging
import time
from typing import Dict, List

from .alpha_ensemble import AlphaEngine
from .market_data import Tick, TickSubscriber
from .order_router import Router
from .risk_manager import RiskSentinel
from .sentiment_bridge import sentiment_factor
from .session_clock import session_active
from ..models.plan_v2 import Leg, PlanV2

logger = logging.getLogger("MAXXAI_ENGINE")


class TradingEngine:
    """Main trading engine."""

    def __init__(self) -> None:
        self.tick_sub = TickSubscriber(["BTCUSD", "ETHUSD", "EURUSD"])
        self.alpha = AlphaEngine()
        self.router = Router()
        self.risk = RiskSentinel()
        self.ws_queues: List[asyncio.Queue] = []

    async def state_stream(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self.ws_queues.append(q)
        try:
            while True:
                yield await q.get()
        finally:
            self.ws_queues.remove(q)

    async def _broadcast(self, state: Dict) -> None:
        for q in self.ws_queues:
            await q.put(state)

    async def start(self) -> None:
        async for tick in self.tick_sub.stream():
            if not session_active():
                continue
            sent = await sentiment_factor()
            self.alpha.update(tick.symbol, tick.price)
            alpha = self.alpha.score(tick.symbol) * (1 + 0.5 * sent)
            if abs(alpha) < 0.25:
                continue
            if self.risk.halt:
                continue
            qty = self.alpha.size(tick.price, self.risk.balance, alpha)
            plan = PlanV2(
                timestamp=time.time(),
                legs=[
                    Leg(
                        symbol=tick.symbol,
                        side="BUY" if alpha > 0 else "SELL",
                        qty=qty,
                        price=tick.price,
                        broker=self.router.best_venue(tick.symbol),
                    )
                ],
            )
            fill = await self.router.execute(plan.legs[0])
            self.risk.update(fill)
            await self._broadcast(
                {
                    "symbol": tick.symbol,
                    "balance": self.risk.balance,
                    "unrealized_pnl": self.risk.unrealized_pnl(),
                    "status": "LIVE",
                }
            )
