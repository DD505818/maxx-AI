#!/bin/bash
cd "$(dirname "$0")/../infra/docker" && docker compose up --build -d
