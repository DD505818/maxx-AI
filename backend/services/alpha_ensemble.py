"""Signal generation via ensemble methods."""

from __future__ import annotations

from collections import deque
from typing import Iterable, List, Mapping

import os
import yaml

import numpy as np


class AlphaEngine:
    """Blend momentum, sentiment, and mean reversion signals."""

    DEFAULT_WEIGHTS = {
        "momentum": 0.5,
        "sentiment": 0.3,
        "mean_reversion": 0.2,
    }

<<<<
        mean_rev = -np.tanh((p[-1] - np.mean(p[-20:])) / (np.std(p[-20:]) + 1e-9))
        return (
            self.weights["momentum"] * mom
            + self.weights["mean_reversion"] * mean_rev
            + self.weights["sentiment"] * sentiment
        

    def size(
        self,
        price: float,
        balance: float,
        alpha: float,
        vix: float = 18,
    ) -> float:
        btc_prices = list(self.prices["BTCUSD"])[-50:]
        if len(btc_prices) < 10:
            return 0.0
        vol = float(np.std(btc_prices))
        kelly = max(0.01, min(0.5 / (1 + vix / 20), alpha / (vol ** 2)))
        risk_dollars = balance * 0.003
        qty = abs(kelly) * risk_dollars / price
        return round(qty, 6)
