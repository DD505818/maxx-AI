
# MAXX-AI

Full-stack async trading platform using FastAPI backend and Next.js frontend.

## Running Locally

```bash
cd docker && docker-compose up --build -d
```

Then open http://localhost:3000 to view the dashboard.

# MAXX-AI Sample Package

This archive contains a minimal yet runnable slice of the MAXX-AI stack:

- **backend/api/orchestrator.py** — AutoGen multi-agent orchestrator.
- **backend/services/trading_engine.py** — Async trading loop core.
- **backend/services/risk_manager.py** — Drawdown and position risk guard.
- **docker/backend.Dockerfile** + **requirements.agent.txt** — container.
- **docker/docker-compose.yml** — Compose file with `models:` block.

## Quick start

```bash
cd docker && docker-compose up --build -d
```

This will spin vLLM (GPU), orchestrator, Redpanda, RisingWave, and the backend in seconds.

## Environment variables

Copy `.env.example` to `.env` and provide values for the listed variables. Never commit real secrets to the repository.


See `docs/gke_deploy.md` for Kubernetes deployment instructions.
