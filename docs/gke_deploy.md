# Deploying MAXX-AI to GKE

This guide outlines the minimal steps to deploy the stack onto a Google Kubernetes Engine cluster.

## Prerequisites

- `gcloud` CLI configured with a project
- Docker daemon authenticated to `gcr.io`
- A GKE cluster

## Environment variables

Set the following variables before running the deployment script:

```bash
export GCP_PROJECT=<your-gcp-project>
export GKE_CLUSTER=<your-cluster-name>
export GKE_ZONE=<cluster-zone>
```

## Build and Deploy

Run the helper script from the repository root:

```bash
./scripts/deploy_gke.sh
```

The script builds images, pushes them to `gcr.io/$GCP_PROJECT`, and applies the manifests in `infra/gke/`.

Verify container signatures before rollout:

```bash
cosign verify "$GCP_PROJECT"/backend:latest
cosign verify "$GCP_PROJECT"/orchestrator:latest
cosign verify "$GCP_PROJECT"/frontend:latest
```
