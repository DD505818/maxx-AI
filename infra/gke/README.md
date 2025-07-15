# GKE Deployment Manifests

This directory contains Kubernetes manifests for running MAXX-AI on Google Kubernetes Engine.

Apply them with:

```bash
scripts/deploy_gke.sh
```

Ensure the container images referenced in the manifests are built and pushed to
your Google Container Registry before applying.
