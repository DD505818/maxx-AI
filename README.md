
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
- **docker/backend.Dockerfile** + **requirements.agent.txt** — container.
- **docker/docker-compose.yml** — Compose file with `models:` block.

## Quick start

```bash
cd docker && docker-compose up --build -d
```

This will spin vLLM (GPU), orchestrator, Redpanda, RisingWave, and the backend in seconds.

## Environment variables

Copy `.env.example` to `.env` and provide values for the listed variables. Never commit real secrets to the repository.

| Variable | Purpose | Default |
|----------|---------|---------|
| `ORCH_URL` | Base URL of the orchestrator service | `http://localhost:8080` |
| `NEXT_PUBLIC_WS_URL` | WebSocket endpoint for frontend updates | `ws://localhost:8000/ws/agents` |
| `MAX_DRAWDOWN_PCT` | Max intraday drawdown before halt | `0.05` |


See `docs/gke_deploy.md` for Kubernetes deployment instructions.
For Cloud Run and Firebase setup, see `docs/cloud_run_firebase.md`.
