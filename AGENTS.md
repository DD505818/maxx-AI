# MAXX‑Ai Agents Specification

*Version 1.0 · Last updated: 2025‑07‑13*

---
Here’s your enhanced, future-proof, and production-ready MAXX-Ai Agents Specification—fully aligned with best practices, modern agent design, and today’s AI/infra stack. This revision sharpens security, extensibility, and composability, and tightly integrates new features for observability and automated recovery. Each section is direct and actionable for devs, ops, and researchers.


---

MAXX-Ai Agents Specification

Version 1.1 · Last updated: 2025‑07‑13


---

1 Purpose

This specification defines all runtime agents for MAXX-Ai’s autonomous trading platform.
It covers agent roles, composition patterns, lifecycle and recovery, inter-agent contracts (API and message bus), config schemas, health checks, observability hooks, extension best practices, and compliance/security notes.
Treat this as the definitive, reviewable, and extensible reference for anyone building, modifying, or auditing MAXX-Ai’s agent fabric.


---

2 Taxonomy & Responsibilities

Agent Name	Container Tag	Core Role	API Endpoints	Scaling / Placement

MarketDataAgent	maxx-marketdata	Ingests/normalizes exchange tick feeds, forwards to bus	/healthz, /reload	1/market (binance, coinbase, etc)
AlphaAgent	maxx-alpha	Runs ensemble signal (momentum, mean-rev, breakout, sentiment, NLP)	/signal/{symbol}	HPA, CPU>60%
RiskSentinel	maxx-risk	Real-time risk, per-trade/session guards, kill switch, Kelly clamp	/risk/state, /risk/trim	Singleton (leader election)
ExecutionAgent	maxx-exec	Broker/order routing, smart maker/taker, fill reconciliation	/order, /cancel, /quote	HPA on pending_orders metric
MetaGovernor	maxx-governor	RL/AutoML agent: reweights AlphaAgent signals, deploys new configs	/govern/reweight, /govern/validate	GPU node, singleton
PortfolioAgent	maxx-portfolio	Aggregates PnL, tracks lockbox, manages payouts/reporting	/pnl, /sweep, /balance	Singleton
SessionClock	maxx-sessionclock	Emits global session open/close events (London/NY/Asia)	/now, /calendar	Singleton, ultra-high-uptime
SentimentAgent	maxx-sentiment	Ingests news/social, scores sentiment, feeds AlphaAgent	/score, /stream, /reload	1–N (HPA on news volume)


> Security Note: All agents must use readOnlyRootFilesystem: true, only least-privileged service accounts, and all container images must be cosign-verified before deployment.




---

3 Agent Lifecycle, State, and Coordination

┌──────────┐  Init      ┌──────────────┐   Ready   ┌─────────────┐
│   Init   ├──────────►│   Running    ├──────────►│ Recycling   │
└──────────┘           └──────────────┘           └─────────────┘
     ▲                       │▲        ▲                  │
     │   fatal/error         │└────┐   │ done             │ done
     └───────── CrashLoop ◄──┘    │   └─────╮             ▼
                                   │         │       ┌────────────┐
                              graceful stop  │       │  Shutdown  │
                                             └──────►└────────────┘

Agents broadcast transitions (agent.state:<name> channel, value: {state,ts,reason})

Health checks: /healthz (HTTP 200/500), plus OTel metrics at :4317 (gRPC, Prometheus scrape).



---

4 Message Bus (Idempotent, Traceable)

Stream	Producer	Consumers	Payload Schema	Notes

ticks:<symbol>	MarketDataAgent	AlphaAgent	{ts,price,volume,exchange}	1:many
signals:<symbol>	AlphaAgent	ExecutionAgent	{score,side,confidence}	Always includes agent-version
orders	ExecutionAgent	RiskSentinel, PortfolioAgent	{id,symbol,qty,side,meta}	Det-IDed, fully auditable
fills	ExecutionAgent	PortfolioAgent	{order_id,price,fee,venue}	Each fill triggers PnL/lockbox update
pnl	PortfolioAgent	MetaGovernor	{equity,realized,unrealized}	MetaGovernor recalibrates signal blend
session_events	SessionClock	All agents	{event,start_ts,end_ts,session}	Drives schedule/sleep/active transition


All messages are UUIDv7 keyed, JSON encoded, trace-annotated.

Replay and checkpointing supported via Redis Streams or Redpanda (for scale).



---

5 Config Schema (agent_config.yaml)

market_data:
  retry_backoff_ms: 250
  resubscribe_sec: 300
  feeds: ["binance", "coinbase", "bybit", "oanda"]
alpha:
  weights: { momentum: 0.5, mean_reversion: 0.3, breakout: 0.2, sentiment: 0.1 }
  reweight_cron: "10 0 * * *"
  nlp_model: "llama3-lora-trading"
risk:
  max_trade_risk_pct: 0.3
  daily_drawdown_pct: 5.0
  slippage_limit_pct: 0.2
  hard_kill_pct: 7.0
exec:
  maker_rebate_threshold_bps: 1.0
  fallback_on_reject: true
sentiment:
  score_feed: "risingwave://sentiment_30m"
  news_apis: ["newsapi.org", "twitter", "reddit"]
meta_governor:
  enable_rl: true
  retrain_cron: "5 1 * * *"

Mount as /config/agent_config.yaml (read-only).

Hot-reload: SIGHUP or /reload POST.



---

6 Health, Observability, and Auditability

HTTP /healthz → 200 OK or 500 error, always includes JSON {uptime, lag, reason}.

OpenTelemetry: Expose gRPC at :4317 for distributed traces (latency, errors, queue length).

Prometheus: /metrics endpoint on :9100 (container resource, agent custom KPIs).

Structured logging: All logs JSON with level, ts, msg, context, agent, order_id, user_id if relevant.


Example:

{"level":"info","ts":"2025-07-13T18:42:12Z","msg":"order executed","agent":"maxx-exec","order_id":"01H...","symbol":"BTCUSD","qty":0.004,"price":62650.2}

Critical errors: sent to Slack/Teams, tagged for auto-issue creation.



---

7 Agent Extension: Best Practices

1. Scaffold: inherit from BaseAgent (backend/services/base_agent.py).


2. Define config schema and default values.


3. Add deployment spec (k8s/new-agent-deployment.yaml), helm chart if needed.


4. Register API endpoints, log health/OTel hooks.


5. Write/extend integration and contract tests (tests/test_<agent>.py).


6. Update CI Matrix; ensure plan-schema and security checks pass.


7. Peer-review for message/trace compliance.


8. Document role and interactions in docs/Agents.md with version.




---

8 Fault Handling & Self-Recovery

Failure	Detection	Automated Response

WS feed drop	No tick 5s	MarketDataAgent auto-reconnects, logs incident, notifies #feed
Order reject ratio >2%	Metric/Prometheus	ExecutionAgent switches broker route, notifies RiskSentinel
Intraday DD >5%	PortfolioAgent	MetaGovernor clamps Kelly, RiskSentinel halts all new trades
Latency p95 >80ms	Prometheus	Koordinator auto-scales pods, or triggers HPA burst
Healthz probe fail	K8s/liveness	Pod restart; crashloop triggers escalation if 3+ in 15 min



---

9 Security & Compliance

Image signing: cosign verified before rollout.

Role-based access: no container has unneeded creds; each pod gets least privilege.

Network: Egress firewall, restricts agents to only broker and whitelisted APIs.

Audit logs: Immutable, encrypted at rest, streamed to SIEM.

CI/CD: All PRs run contract and security tests before merge.



---

10 gRPC Example (Execution Agent IDL)

syntax = "proto3";
service ExecutionService {
  rpc SubmitOrder(OrderRequest) returns (OrderAck) {}
  rpc CancelOrder(CancelRequest) returns (CancelAck) {}
  rpc GetQuote(QuoteRequest) returns (Quote) {}
}

Full proto in /proto/.


---

End of MAXX-Ai Agents Specification v1.1
For all changes, update this doc and the API/contract tests.


---

This version is ready for production, open for agent plug-ins, and built for scale, compliance, and auditability.

