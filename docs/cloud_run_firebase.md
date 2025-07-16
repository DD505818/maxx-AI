# Deploying the Frontend on Cloud Run with Firebase Hosting

This guide explains how to build the frontend container and expose it through Firebase Hosting. The setup uses Cloud Run as the backend for dynamic requests and Firebase Hosting for TLS termination and CDN caching.

## Prerequisites
- `gcloud` and `firebase` CLIs installed and authenticated
- A Google Cloud project with billing enabled
- Firebase project initialized (`firebase init`)

## Build & Deploy

1. Set environment variables:
   ```bash
   export GCP_PROJECT=<your-project-id>
   export REGION=us-central1
   ```
2. Run the helper script:
   ```bash
   python scripts/deploy_cloud_run.py
   ```
   This builds the image `gcr.io/$GCP_PROJECT/maxx-frontend` and deploys a Cloud Run service named `maxx-frontend`.
3. Deploy Firebase Hosting:
   ```bash
   firebase deploy --only hosting
   ```

The `firebase.json` configuration rewrites all requests to the Cloud Run service, enabling seamless Next.js routing.
