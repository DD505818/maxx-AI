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

    def __init__(
        self,
        symbols: Iterable[str] | None = None,
        *,
        weights: Mapping[str, float] | None = None,
        config_path: str | None = None,
    ) -> None:
        symbols = symbols or ["BTCUSD", "ETHUSD", "EURUSD"]
        self.prices = {sym: deque(maxlen=200) for sym in symbols}
        self.weights = self._load_weights(weights, config_path)

    def _load_weights(
        self, weights: Mapping[str, float] | None, config_path: str | None
    ) -> Mapping[str, float]:
        if weights:
            return {
                "momentum": float(weights.get("momentum", 0.5)),
                "sentiment": float(weights.get("sentiment", 0.3)),
                "mean_reversion": float(weights.get("mean_reversion", 0.2)),
            }

        path = config_path or os.getenv("STRATEGY_CONFIG", "config/strategies.yml")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            cfg = data.get("weights", {})
            return {
                "momentum": float(cfg.get("momentum", 0.5)),
                "sentiment": float(cfg.get("sentiment", 0.3)),
                "mean_reversion": float(cfg.get("mean_reversion", 0.2)),
            }
        except FileNotFoundError:
            return self.DEFAULT_WEIGHTS

    def update(self, symbol: str, price: float) -> None:
        self.prices[symbol].append(price)

    def score(self, symbol: str, *, sentiment: float = 0.0) -> float:
        p: List[float] = list(self.prices[symbol])
        if len(p) < 50:
            return 0.0
        mom = np.tanh(np.polyfit(range(len(p)), p, 1)[0] * 100)
        mean_rev = -np.tanh((p[-1] - np.mean(p[-20:])) / (np.std(p[-20:]) + 1e-9))
        return (
            self.weights["momentum"] * mom
            + self.weights["mean_reversion"] * mean_rev
            + self.weights["sentiment"] * sentiment
        )

    def size(self, price: float, balance: float, alpha: float, vix: float = 18) -> float:
        btc_prices = list(self.prices["BTCUSD"])[-50:]
        if len(btc_prices) < 10:
            return 0.0
        kelly = max(0.01, min(0.5 / (1 + vix / 20), alpha / (np.std(btc_prices) ** 2)))
        risk_dollars = balance * 0.003
        qty = abs(kelly) * risk_dollars / price
        return round(qty, 6)
