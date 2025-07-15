"""CashEquivalentSwapAgent places cash-equivalent swap positions with risk controls."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MarketEstimate:
    """Represents market expectations for a swap leg."""

    spread: float  # expected annualized spread vs. cash
    variance: float  # variance of spread estimate


class RiskLimitError(Exception):
    """Raised when order sizing exceeds the agent's risk limit."""


class CashEquivalentSwapAgent:
    """Basic agent sizing cash-equivalent swap exposure using Kelly criterion."""

    def __init__(self, capital: float, risk_limit: float = 0.05) -> None:
        if capital <= 0:
            raise ValueError("capital must be positive")
        if not 0 < risk_limit <= 1:
            raise ValueError("risk_limit must be between 0 and 1")
        self.capital = capital
        self.risk_limit = risk_limit

    def position_size(self, estimate: MarketEstimate) -> float:
        """Return position size respecting Kelly sizing and risk limits."""
        if estimate.variance <= 0:
            raise ValueError("variance must be positive")
        kelly_fraction = estimate.spread / estimate.variance
        suggested = kelly_fraction * self.capital
        limit = self.capital * self.risk_limit
        if abs(suggested) > limit:
            raise RiskLimitError(
                f"Position size {suggested:.2f} exceeds risk limit {limit:.2f}"
            )
        return suggested
