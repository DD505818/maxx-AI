
# MAXX-AI

Full-stack async trading platform using FastAPI backend and Next.js frontend.

## Running Locally

```bash
./scripts/build_local.sh
```

# Then open the dashboard

Then open http://localhost:3000.

# MAXX-AI Sample Package

This archive contains a minimal yet runnable slice of the MAXX-AI stack:

- **backend/services/agent_orchestrator.py** — AutoGen multi-agent orchestrator.
- **backend/services/trading_engine.py** — Async trading loop core.
- **backend/Dockerfile.agents** + **requirements.agent.txt** — container.
- **infra/docker/docker-compose.yml** — Compose file with `models:` block.

## Quick start

```bash
docker compose -f infra/docker/docker-compose.yml up --build
```

This will spin vLLM (GPU), orchestrator, Redpanda, RisingWave, and the backend in seconds.

## Environment variables

Copy `.env.example` to `.env` and provide values for the listed variables. Never commit real secrets to the repository.

