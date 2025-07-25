"""Simplistic order routing and execution simulator."""

from __future__ import annotations

import asyncio
import random
from typing import Iterable

from .risk_manager import Fill
from ..models.plan_v2 import Leg


class Router:
    """Route orders to the best venue and simulate fills."""

    def __init__(self, venues: Iterable[str] | None = None) -> None:
        self.venues = list(venues or ["binance", "coinbase", "bybit"])

    def best_venue(self, symbol: str) -> str:  # noqa: D401 - simple wrapper
        """Return the best venue for symbol."""
        return random.choice(self.venues)

    async def execute(self, leg: Leg) -> Fill:
        await asyncio.sleep(0.1)  # simulate network delay
        price = leg.price or 0.0
        return Fill(
            order_id=f"{leg.symbol}-{random.randint(1, 999999)}",
            symbol=leg.symbol,
            side=leg.side,
            qty=leg.qty,
            price=price,
        )
