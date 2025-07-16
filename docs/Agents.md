# MAXX-Ai Agents Overview

This document summarizes agent roles defined in the MAXX-Ai Agents Specification.
Refer to the root `AGENTS.md` for the full specification and update both files when adding or modifying agents.

| Agent | Description |
|-------|-------------|
| MarketDataAgent | Normalizes exchange feeds and publishes ticks to the bus |
| AlphaAgent | Generates trading signals using momentum, mean reversion, breakout and sentiment models |
| RiskSentinel | Provides real-time risk controls and kill switch functionality |
| ExecutionAgent | Routes orders to brokers and reconciles fills |
| MetaGovernor | Performs RL/AutoML to adjust AlphaAgent weights |
| PortfolioAgent | Aggregates PnL and manages payouts |
| SessionClock | Emits global session events |
| SentimentAgent | Processes news and social feeds to produce sentiment scores |
