"""Engine state message model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentState:
    symbol: str
    balance: float
    unrealized_pnl: float
    status: str
