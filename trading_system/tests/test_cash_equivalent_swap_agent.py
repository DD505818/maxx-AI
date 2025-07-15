import os, sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import pytest

from backend.app.agents.cash_equivalent_swap_agent import (
    CashEquivalentSwapAgent,
    MarketEstimate,
    RiskLimitError,
)


def test_position_size_within_limit():
    agent = CashEquivalentSwapAgent(capital=100_000, risk_limit=0.3)
    estimate = MarketEstimate(spread=0.01, variance=0.04)
    size = agent.position_size(estimate)
    assert size == pytest.approx(25_000.0)


def test_position_size_exceeds_limit():
    agent = CashEquivalentSwapAgent(capital=50_000, risk_limit=0.3)
    estimate = MarketEstimate(spread=0.10, variance=0.01)
    with pytest.raises(RiskLimitError):
        agent.position_size(estimate)
