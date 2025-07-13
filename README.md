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
