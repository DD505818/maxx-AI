#!/bin/bash
# Deploy MAXX-AI services to Google Kubernetes Engine.
set -euo pipefail

: "${PROJECT_ID:?Set PROJECT_ID}"
: "${GKE_CLUSTER_NAME:?Set GKE_CLUSTER_NAME}"
: "${GKE_REGION:?Set GKE_REGION}"
:GKE_NODE_COUNT="${GKE_NODE_COUNT:-3}"

# Configure gcloud and create cluster if missing.
gcloud config set project "$PROJECT_ID"
if ! gcloud container clusters describe "$GKE_CLUSTER_NAME" --region "$GKE_REGION" >/dev/null 2>&1; then
  gcloud container clusters create "$GKE_CLUSTER_NAME" \
    --region "$GKE_REGION" \
    --num-nodes "$GKE_NODE_COUNT" \
    --machine-type "e2-standard-4"
fi

# Build and push images.
gcloud auth configure-docker gcr.io --quiet
gcloud builds submit --tag "gcr.io/${PROJECT_ID}/maxx-backend:latest" backend
gcloud builds submit --tag "gcr.io/${PROJECT_ID}/maxx-frontend:latest" frontend

# Deploy to cluster.
gcloud container clusters get-credentials "$GKE_CLUSTER_NAME" --region "$GKE_REGION"
kubectl apply -f infra/k8s

echo "Deployment complete."
