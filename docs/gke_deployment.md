# GKE Deployment Guide

This document outlines the steps to run MAXX-AI on Google Kubernetes Engine.

1. Set up a Google Cloud project and enable the GKE API.
2. Populate `.env` with your `PROJECT_ID`, `GKE_CLUSTER_NAME`, and `GKE_REGION`.
3. Authenticate with `gcloud auth login` and `gcloud auth application-default login`.
4. Execute:

```bash
source .env
./scripts/deploy_gke.sh
```

The script creates the cluster if needed, builds and pushes container images, and applies the manifests located in `infra/k8s`.
