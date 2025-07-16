"""Trade plan data models."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Leg:
    symbol: str
    side: str
    qty: float
    price: float
    broker: str


@dataclass
class PlanV2:
    timestamp: float
    legs: List[Leg] = field(default_factory=list)
