#!/bin/bash
# Deploy MAXX-AI services to an existing GKE cluster.
# Requires gcloud and kubectl to be installed and authenticated.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

: "${GCP_PROJECT:?Set GCP_PROJECT}"
: "${GKE_CLUSTER:?Set GKE_CLUSTER}"
: "${GKE_ZONE:?Set GKE_ZONE}"
: "${IMAGE_TAG:=latest}"

# Get cluster credentials
"$(command -v gcloud)" container clusters get-credentials "$GKE_CLUSTER" \
    --zone "$GKE_ZONE" --project "$GCP_PROJECT"

# Apply manifests
kubectl apply -f "$ROOT_DIR/infra/gke/namespace.yaml"
for f in "$ROOT_DIR"/infra/gke/*.yaml; do
    [ "$f" != "$ROOT_DIR/infra/gke/namespace.yaml" ] || continue
    kubectl apply -f "$f"
done

echo "Deployment complete."
