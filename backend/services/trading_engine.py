"""Core asynchronous trading engine."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

from .alpha_ensemble import AlphaEngine
from .market_data import TickSubscriber
from .order_router import Router
from .risk_manager import RiskSentinel
from .sentiment_bridge import sentiment_factor
from .session_clock import session_active
from ..models.plan_v2 import Leg, PlanV2

logger = logging.getLogger("MAXXAI_ENGINE")


class TradingEngine:
    """End-to-end trade loop."""

    def __init__(
        self,
        tick_sub: TickSubscriber | None = None,
        risk: RiskSentinel | None = None,
    ) -> None:
        """Create a trading engine with optional dependencies."""

        self.tick_sub = tick_sub or TickSubscriber(
            ["BTCUSD", "ETHUSD", "EURUSD"]
        )
        self.alpha = AlphaEngine()
        self.router = Router()
        self.risk = risk or RiskSentinel()
        self.start_time = time.monotonic()
        self.last_tick = self.start_time
        self.ws_queues: list[asyncio.Queue[Any]] = []

    @property
    def uptime(self) -> float:
        """Return engine uptime in seconds."""
        return time.monotonic() - self.start_time

    @property
    def lag(self) -> float:
        """Return seconds since last processed tick."""
        return time.monotonic() - self.last_tick

    async def state_stream(self) -> Any:
        """Yield engine state for websocket clients."""
        q: asyncio.Queue[Any] = asyncio.Queue()
        self.ws_queues.append(q)
        try:
            while True:
                yield await q.get()
        finally:
            self.ws_queues.remove(q)

    async def _broadcast(self, state: dict[str, Any]) -> None:
        for q in self.ws_queues:
            await q.put(state)

    async def start(self) -> None:
        async for tick in self.tick_sub.stream():
            self.last_tick = time.monotonic()
            self.alpha.update(tick.symbol, tick.price)
            if not session_active():
                continue
            sent = await sentiment_factor()
            alpha = self.alpha.score(tick.symbol) * (1 + 0.5 * sent)
            if abs(alpha) < 0.25:
                continue
            if self.risk.halt:
                continue
            qty = self.alpha.size(tick.price, self.risk.balance, alpha)
            if qty <= 0:
                continue
            plan = PlanV2(
                timestamp=time.time(),
                legs=[
                    Leg(
                        symbol=tick.symbol,
                        side="BUY" if alpha > 0 else "SELL",
                        qty=qty,
                        broker=self.router.best_venue(tick.symbol),
                        price=tick.price,
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

    async def run(self, max_ticks: int) -> None:
        """Run the trading loop for a finite number of ticks."""

        count = 0
        async for tick in self.tick_sub.stream():
            self.last_tick = time.monotonic()
            self.alpha.update(tick.symbol, tick.price)
            sent = await sentiment_factor()
            alpha = self.alpha.score(tick.symbol) * (1 + 0.5 * sent)
            if abs(alpha) >= 0.25 and not self.risk.halt:
                qty = self.alpha.size(tick.price, self.risk.balance, alpha)
                if qty > 0:
                    plan = PlanV2(
                        timestamp=time.time(),
                        legs=[
                            Leg(
                                symbol=tick.symbol,
                                side="BUY" if alpha > 0 else "SELL",
                                qty=qty,
                                broker=self.router.best_venue(tick.symbol),
                                price=tick.price,
                            )
                        ],
                    )
                    fill = await self.router.execute(plan.legs[0])
                    self.risk.update(fill)
            count += 1
            if count >= max_ticks:
                break
