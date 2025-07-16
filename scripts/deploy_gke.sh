#!/bin/bash
# Deploy the stack to a GKE cluster.
# TODO: replace sample cluster values with real project settings.

set -euo pipefail
PROJECT=${PROJECT:-my-project}
CLUSTER=${CLUSTER:-my-cluster}
REGION=${REGION:-us-central1}

gcloud container clusters get-credentials "$CLUSTER" --region "$REGION" --project "$PROJECT"
kubectl apply -f infra/helm/
