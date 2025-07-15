#!/bin/bash
set -euo pipefail

: "${GCP_PROJECT:?GCP_PROJECT not set}"
: "${GKE_CLUSTER:?GKE_CLUSTER not set}"
: "${GKE_ZONE:?GKE_ZONE not set}"

REGISTRY="gcr.io/${GCP_PROJECT}"
BACKEND_IMG="${REGISTRY}/backend:latest"
ORCH_IMG="${REGISTRY}/orchestrator:latest"
FRONTEND_IMG="${REGISTRY}/frontend:latest"

# Build images
docker build -t "$BACKEND_IMG" -f backend/Dockerfile backend
docker build -t "$ORCH_IMG" -f Dockerfile.orchestrator .
docker build -t "$FRONTEND_IMG" -f frontend/Dockerfile frontend

# Push images
docker push "$BACKEND_IMG"
docker push "$ORCH_IMG"
docker push "$FRONTEND_IMG"

# Update manifests with project images
sed "s~myrepo/backend:latest~$BACKEND_IMG~" infra/gke/backend-deployment.yaml > /tmp/backend.yaml
sed "s~myrepo/orchestrator:latest~$ORCH_IMG~" infra/gke/orchestrator-deployment.yaml > /tmp/orchestrator.yaml
sed "s~myrepo/frontend:latest~$FRONTEND_IMG~" infra/gke/frontend-deployment.yaml > /tmp/frontend.yaml

# Configure kubectl
gcloud container clusters get-credentials "$GKE_CLUSTER" --zone "$GKE_ZONE" --project "$GCP_PROJECT"

# Deploy resources
kubectl apply -f infra/gke/namespace.yaml
kubectl apply -f infra/gke/redpanda-deployment.yaml
kubectl apply -f infra/gke/risingwave-deployment.yaml
kubectl apply -f infra/gke/llama3-deployment.yaml
kubectl apply -f /tmp/orchestrator.yaml
kubectl apply -f /tmp/backend.yaml
kubectl apply -f /tmp/frontend.yaml
