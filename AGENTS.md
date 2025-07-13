# MAXX‑Ai Agents Specification

*Version 1.0 · Last updated: 2025‑07‑13*

---

## 1  Purpose

This document defines every **runtime agent** that powers MAXX‑Ai’s autonomous trading platform.  It covers agent roles, life‑cycle events, inter‑agent messaging, configuration schema, health probes, observability hooks, and extension guidelines.  Treat it as the single source of truth when adding, modifying, or debugging an agent.

---

## 2  Taxonomy of Agents

| Code Name           | Container Image Tag | Responsibility                                                      | Key Endpoints               | Scaling Rule                                         |
| ------------------- | ------------------- | ------------------------------------------------------------------- | --------------------------- | ---------------------------------------------------- |
| **MarketDataAgent** | `maxx-marketdata`   | Connects to exchange WebSockets, normalises ticks → Redis stream.   | `/healthz`, `/reload`       | 1 replica per feed (binance, coinbase, bybit, oanda) |
| **AlphaAgent**      | `maxx-alpha`        | Runs ensemble signals (momentum / mean‑rev / breakout / sentiment). | `/signal/{symbol}`          | Horizontal HPA on CPU 60 %                           |
| **RiskSentinel**    | `maxx-risk`         | Enforces per‑trade & session risk, kill‑switch, Kelly damp.         | `/risk/state`, `/risk/trim` | Singleton (leader election)                          |
| **ExecutionAgent**  | `maxx-exec`         | Smart‑routes orders, handles maker/taker logic, writes fills.       | `/order`, `/cancel`         | HPA on pending orders metric                         |
| **MetaGovernor**    | `maxx-governor`     | RL policy selector, re‑weights AlphaAgent ensembles nightly.        | `/govern/reweight`          | GPU‑node, 1 replica                                  |
| **PortfolioAgent**  | `maxx-portfolio`    | Aggregates PnL, handles PnL lock‑box & payouts.                     | `/pnl`, `/sweep`            | 1 replica                                            |

> **Note:** All agents expose an OpenTelemetry gRPC endpoint at `:4317` for traces + metrics.

---

## 3  Life‑Cycle States

```
┌──────────┐  start   ┌──────────────┐  healthy   ┌───────────┐
│   Init   ├────────►│   Running    ├───────────►│ Recycling │
└──────────┘          └──────────────┘            └───────────┘
     ▲                    │▲  error/retry               │
     │  fatal/error       │└──────────────┐            │ done
     └─────────── CrashLoopBackoff ◄──────┘            ▼
                                                 ┌────────────┐
                                                 │  Shutdown  │
                                                 └────────────┘
```

* Agents publish life‑cycle transitions to Redis channel `agent.events` (`{agent}:{state}:{timestamp}`).

---

## 4  Message Bus (Redis Streams)

| Stream             | Producer        | Consumers                    | Payload Schema                 |
| ------------------ | --------------- | ---------------------------- | ------------------------------ |
| `ticks:<symbol>`   | MarketDataAgent | AlphaAgent                   | `{ts,price,volume}`            |
| `signals:<symbol>` | AlphaAgent      | ExecutionAgent               | `{score,side,confidence}`      |
| `orders`           | ExecutionAgent  | RiskSentinel, PortfolioAgent | `{id,symbol,qty,side}`         |
| `fills`            | ExecutionAgent  | PortfolioAgent               | `{order_id,price,fee}`         |
| `pnl`              | PortfolioAgent  | MetaGovernor                 | `{equity,realized,unrealized}` |

Streams are id‑empotent; message keys are deterministic UUIDv7.

---

## 5  Configuration Reference (`agent_config.yaml`)

```yaml
market_data:
  retry_backoff_ms: 250
  resubscribe_sec: 300
alpha:
  weights: { momentum: 0.5, mean_reversion: 0.3, breakout: 0.2, sentiment: 0.0 }
  reweight_cron: "10 0 * * *"   # 00:10 UTC daily
risk:
  max_trade_risk_pct: 0.3       # ‰ of balance
  daily_drawdown_pct: 5.0
exec:
  slip_tolerance_pct: 0.2
  maker_rebate_threshold_bps: 1.0
```

All agents mount `/config/agent_config.yaml` read‑only; hot‑reload is via `SIGHUP`.

---

## 6  Health & Observability

* **HTTP `/healthz`** → 200 OK if agent internal probe passes.
* **Prometheus metrics** at `:9100/metrics` (latency, cpu, queue length).
* **Structured logs** (JSON) with `level`, `ts`, `msg`, `symbol`, `order_id`.

Example log:

```json
{"level":"info","ts":"2025-07-13T18:42:12Z","msg":"order executed","order_id":"01H…","symbol":"BTCUSD","qty":0.004,"price":62650.2}
```

---

## 7  Extending with a New Agent

1. Scaffold class inheriting `BaseAgent` in `services/new_agent.py`.
2. Add deployment YAML → `k8s/new-agent-deployment.yaml`.
3. Update Helm values & CI Matrix (`.github/workflows/ci-cd.yml`).
4. Write unit tests in `backend/tests/test_new_agent.py`.
5. Run `pnpm turbo run test --filter backend` and CI must pass.

---

## 8  Failure Modes & Recovery

| Failure                  | Detection                 | Automatic Action                                                     |
| ------------------------ | ------------------------- | -------------------------------------------------------------------- |
| WebSocket feed drops     | no tick for 5 s           | MarketDataAgent reconnects & raises alert Slack channel `#feed`      |
| Order reject ratio > 2 % | RiskSentinel metric       | Router shifts to next broker with better fill rate                   |
| Intraday drawdown > 5 %  | PortfolioAgent monitoring | MetaGovernor sets Kelly clip to 0.25 & RiskSentinel halts new trades |

---

## 9  Appendix A – gRPC IDL Snippet

```proto
service ExecutionService {
  rpc SubmitOrder(OrderRequest) returns (OrderAck) {}
  rpc CancelOrder(CancelRequest) returns (CancelAck) {}
}
```

Refer to `proto/` for full schema.

---

*End of Agents Spec*
