# Deploying MAXX-AI on Google Kubernetes Engine

This guide outlines the steps to launch the MAXX-AI stack on GKE. It assumes you have `gcloud` and `kubectl` installed and authenticated.

1. **Create a Cluster**
   ```bash
   gcloud container clusters create "$GKE_CLUSTER" \
     --zone "$GKE_ZONE" --project "$GCP_PROJECT"
   ```

2. **Build and Push Images**
   ```bash
   IMAGE_TAG=latest
   docker build -t gcr.io/$GCP_PROJECT/maxx-orchestrator:$IMAGE_TAG -f backend/Dockerfile .
   docker build -t gcr.io/$GCP_PROJECT/maxx-backend:$IMAGE_TAG -f backend/Dockerfile backend
   docker build -t gcr.io/$GCP_PROJECT/maxx-frontend:$IMAGE_TAG -f frontend/Dockerfile frontend
   docker push gcr.io/$GCP_PROJECT/maxx-orchestrator:$IMAGE_TAG
   docker push gcr.io/$GCP_PROJECT/maxx-backend:$IMAGE_TAG
   docker push gcr.io/$GCP_PROJECT/maxx-frontend:$IMAGE_TAG
   ```

3. **Deploy Manifests**
   ```bash
   ./scripts/deploy_gke.sh
   ```

The script retrieves cluster credentials and applies all manifests from `infra/gke/`. Ensure your `.env` file defines the required variables (`GCP_PROJECT`, `GKE_CLUSTER`, `GKE_ZONE`, `IMAGE_TAG`).
