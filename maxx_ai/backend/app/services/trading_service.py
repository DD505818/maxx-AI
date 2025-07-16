"""Trading service coordinating strategies and broker."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd
import pandas_ta as ta

from .broker_service import BrokerService
from .real_time_data_service import RealTimeDataService
from .stock_selection_service import StockSelectionService
from ..strategies.triple_ma_crossover import TripleMACrossover
from ..strategies.stochastic_double_cross import StochasticDoubleCross
from ..strategies.ichimoku_cloud import IchimokuCloud
from ..strategies.crypto_channel_breakout import CryptoChannelBreakout
from ..strategies.macd_histogram import MACDHistogram
from ..strategies.bollinger_squeeze import BollingerSqueeze
from ..strategies.momentum_strategy import MomentumStrategy
from ..strategies.mean_reversion_strategy import MeanReversionStrategy
from ..strategies.breakout_strategy import BreakoutStrategy
from ..strategies.orb_strategy import ORBStrategy

logger = logging.getLogger("TradingService")


class TradingService:
    """Core trading logic handling position management and backtests."""

    def __init__(
        self,
        broker_service: BrokerService,
        real_time_data_service: RealTimeDataService,
        stock_selection_service: StockSelectionService,
        capital: float = 100_000.0,
    ) -> None:
        self.broker_service = broker_service
        self.data_service = real_time_data_service
        self.stock_selection_service = stock_selection_service
        self.capital = capital
        self.portfolio: Dict[str, any] = {
            "cash": capital,
            "positions": {},
            "equity_history": [capital],
            "trade_log": [],
        }
        self.daily_pnl = 0.0
        self.max_drawdown = 0.0
        self.strategies = {
            "triple_ma": TripleMACrossover(),
            "stochastic": StochasticDoubleCross(),
            "ichimoku": IchimokuCloud(),
            "channel": CryptoChannelBreakout(),
            "macd_histogram": MACDHistogram(),
            "bollinger_squeeze": BollingerSqueeze(),
            "momentum": MomentumStrategy(),
            "mean_reversion": MeanReversionStrategy(),
            "breakout": BreakoutStrategy(),
            "orb": ORBStrategy(real_time_data_service),
        }
        self.strategy_weights = {
            "triple_ma": 0.25,
            "stochastic": 0.20,
            "ichimoku": 0.20,
            "channel": 0.15,
            "macd_histogram": 0.10,
            "bollinger_squeeze": 0.10,
            "momentum": 0.05,
            "mean_reversion": 0.05,
            "breakout": 0.05,
            "orb": 0.05,
        }
        self.risk_params = {
            s: {
                "position_size": 0.02,
                "daily_loss_limit": 0.05,
                "max_drawdown": 0.10,
                "leverage": 2.0 if s in {"triple_ma", "stochastic", "ichimoku"} else 1.5,
                "stop_loss_factor": 0.005,
            }
            for s in self.strategies
        }

    async def main_loop(self) -> None:
        """Run trading loop for selected stocks and crypto."""
        crypto_symbols = ["BTC/USDT", "ETH/USDT"]
        while True:
            stocks = self.stock_selection_service.select_stocks()
            tasks = [self.run_trading_cycle(s) for s in stocks]
            tasks += [self.run_trading_cycle(sym) for sym in crypto_symbols]
            await asyncio.gather(*tasks)
            await asyncio.sleep(60)

    async def run_trading_cycle(self, symbol: str) -> List[Tuple[str, float, str, float]]:
        data = await self.data_service.get_15min_data(symbol)
        if data.empty:
            logger.warning("No data for %s", symbol)
            return []
        data["atr"] = ta.atr(data.high, data.low, data.close, length=14)
        signals: List[Tuple[str, float, str, float]] = []
        for name, strat in self.strategies.items():
            signal, confidence = (
                strat.generate_signal(symbol)
                if name == "orb"
                else strat.generate_signal(data)
            )
            if signal:
                weighted = confidence * self.strategy_weights[name]
                price = data.close.iloc[-1]
                signals.append((signal, weighted, name, price))
        if signals:
            signal, _conf, name, price = max(signals, key=lambda x: x[1])
            params = self.risk_params[name]
            if (
                self.daily_pnl <= -self.capital * params["daily_loss_limit"]
                or self.max_drawdown >= params["max_drawdown"]
            ):
                logger.warning("Risk limit reached for %s", name)
                return signals
            atr = data["atr"].iloc[-1]
            stop_loss = (
                price - price * params["stop_loss_factor"]
                if signal == "buy"
                else price + price * params["stop_loss_factor"]
            )
            take_profit = (
                price + atr * params["stop_loss_factor"] * 3.5
                if signal == "buy"
                else price - atr * params["stop_loss_factor"] * 3.5
            )
            size = self.calculate_position_size(
                price, stop_loss, params["position_size"], params["leverage"]
            )
            if size > 0:
                await self.execute_trade(
                    symbol, signal, price, size, stop_loss, take_profit, name
                )
        return signals

    def calculate_position_size(
        self, price: float, stop_loss: float, position_size: float, leverage: float
    ) -> float:
        risk_amount = self.capital * position_size * leverage
        stop_distance = abs(price - stop_loss)
        return risk_amount / stop_distance if stop_distance > 0 else 0.0

    async def execute_trade(
        self,
        symbol: str,
        signal: str,
        price: float,
        size: float,
        stop_loss: float,
        take_profit: float,
        strategy_name: str,
    ) -> None:
        try:
            order = await self.broker_service.execute_order(
                symbol, signal, size, price, stop_loss, take_profit, leverage=self.risk_params[strategy_name]["leverage"]
            )
            if signal == "buy":
                self.portfolio["positions"][symbol] = {
                    "size": size,
                    "price": price,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit,
                    "strategy": strategy_name,
                }
                self.portfolio["trade_log"].append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "symbol": symbol,
                        "side": signal,
                        "price": price,
                        "size": size,
                        "strategy": strategy_name,
                    }
                )
            elif signal == "sell" and symbol in self.portfolio["positions"]:
                buy_price = self.portfolio["positions"][symbol]["price"]
                profit = (price - buy_price) * size
                self.portfolio["cash"] += profit
                self.daily_pnl += profit
                self.portfolio["trade_log"].append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "symbol": symbol,
                        "side": signal,
                        "price": price,
                        "size": size,
                        "strategy": strategy_name,
                        "profit": profit,
                    }
                )
                del self.portfolio["positions"][symbol]
                self.update_equity()
                logger.info("Sell %s of %s at %s", size, symbol, price)
        except Exception as exc:  # pragma: no cover - network/async errors
            logger.error("Trade execution failed: %s", exc)

    def update_equity(self) -> None:
        current = self.portfolio["cash"] + sum(
            pos["size"] * pos["price"] for pos in self.portfolio["positions"].values()
        )
        self.portfolio["equity_history"].append(current)
        peak = max(self.portfolio["equity_history"])
        self.max_drawdown = (peak - current) / peak if peak > 0 else 0.0

    def run_backtest(
        self, df: pd.DataFrame, strategy_obj: Any, strategy_name: str
    ) -> Tuple[List[float], List[dict]]:
        """Backtest a given strategy on historical data."""
        cash = self.capital
        positions: Dict[str, Tuple[float, float]] = {}
        equity_curve = [cash]
        trades: List[dict] = []
        df = df.copy()
        df["atr"] = ta.atr(df.high, df.low, df.close, length=14)
        for i in range(2, len(df)):
            data_slice = df.iloc[: i + 1]
            signal, _conf = strategy_obj.generate_signal(data_slice)
            price = data_slice.close.iloc[-1]
            if signal == "buy" and not positions:
                stop_loss = price - price * self.risk_params[strategy_name]["stop_loss_factor"]
                take_profit = price + data_slice.atr.iloc[-1] * self.risk_params[strategy_name]["stop_loss_factor"] * 3.5
                size = self.calculate_position_size(
                    price,
                    stop_loss,
                    self.risk_params[strategy_name]["position_size"],
                    self.risk_params[strategy_name]["leverage"],
                )
                if size > 0:
                    positions["open"] = (price, size)
                    trades.append({"timestamp": str(data_slice.index[-1]), "side": "buy", "price": price, "size": size})
            elif signal == "sell" and "open" in positions:
                buy_price, size = positions["open"]
                profit = (price - buy_price) * size
                cash += profit
                trades.append(
                    {
                        "timestamp": str(data_slice.index[-1]),
                        "side": "sell",
                        "price": price,
                        "size": size,
                        "profit": profit,
                    }
                )
                positions = {}
            equity = cash + sum(pos[1] * price for pos in positions.values()) if positions else cash
            equity_curve.append(equity)
        return equity_curve, trades
