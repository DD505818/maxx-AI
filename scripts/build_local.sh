#!/bin/bash
# Build and start the local stack using Docker Compose.

set -euo pipefail

cd "$(dirname "$0")/../infra/docker" && docker compose up --build -d
