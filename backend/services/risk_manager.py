"""Intraday and per-trade risk controls."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Fill:
    order_id: str
    symbol: str
    side: str
    qty: float
    price: float


class RiskSentinel:
    """Risk management with drawdown and position limits."""

    def __init__(self, max_position_pct: float = 0.1) -> None:
        self.balance = 100_000.0
        self.day_start = self.balance
        self.halt = False
        self.fills: List[Fill] = []
        self.positions: Dict[str, float] = {}
        self.max_position_pct = max_position_pct

    def update(self, fill: Fill | None) -> None:
        if not fill:
            return
        self.fills.append(fill)
        qty = fill.qty if fill.side == "BUY" else -fill.qty
        self.positions[fill.symbol] = self.positions.get(fill.symbol, 0.0) + qty
        delta = -qty * fill.price
        self.balance += delta
        if self.intraday_dd() >= 0.05:
            self.halt = True

    def unrealized_pnl(self) -> float:
        return sum(f.qty * f.price for f in self.fills)

    def intraday_dd(self) -> float:
        return max(0.0, 1 - self.balance / self.day_start)

    def position_exposure(self, symbol: str, price: float) -> float:
        """Return notional exposure for ``symbol`` at ``price``."""
        return abs(self.positions.get(symbol, 0.0)) * price

    def can_trade(self, symbol: str, qty: float, price: float) -> bool:
        """Return True if trade keeps exposure under the limit and no halt."""
        if self.halt:
            return False
        exposure = abs(self.positions.get(symbol, 0.0) + qty) * price
        limit = self.day_start * self.max_position_pct
        return exposure <= limit
