"""Simple broker service for order execution."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict

logger = logging.getLogger("BrokerService")


class BrokerService:
    """Execute and track orders against a simulated broker."""

    def __init__(self) -> None:
        self.health_status: Dict[str, str] = {}
        self._order_id = 0

    async def check_health(self) -> None:
        """Update internal broker health status."""
        await asyncio.sleep(0)
        self.health_status = {"status": "ok"}

    async def execute_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        stop_loss: float,
        take_profit: float,
        leverage: float = 1.0,
    ) -> Dict[str, Any]:
        """Simulate order execution and return confirmation."""
        await asyncio.sleep(0)
        self._order_id += 1
        logger.info(
            "Executed order %s %s %s @ %s", self._order_id, side, symbol, price
        )
        return {
            "id": self._order_id,
            "symbol": symbol,
            "side": side,
            "qty": quantity,
            "price": price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "leverage": leverage,
        }
