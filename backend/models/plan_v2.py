"""Trade plan data models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Leg:
    symbol: str
    side: str
    qty: float
    broker: str
    price: float | None = None


@dataclass
class PlanV2:
    timestamp: float
    legs: List[Leg]
