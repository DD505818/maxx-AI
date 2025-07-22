"""Build and deploy the frontend to Cloud Run.

This script expects the following environment variables:
- ``GCP_PROJECT``: Google Cloud project ID.
- ``REGION``: Deployment region (default: ``us-central1``).
- ``SERVICE_NAME``: Optional Cloud Run service name (default: ``maxx-frontend``).

It builds the container image using ``gcloud builds submit`` and deploys it
with ``gcloud run deploy``. All gcloud commands must be installed and
authenticated.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    """Run a subprocess command and raise if it fails."""
    subprocess.run(cmd, check=True)


def main() -> None:
    project = os.environ["GCP_PROJECT"]
    region = os.environ.get("REGION", "us-central1")
    service = os.environ.get("SERVICE_NAME", "maxx-frontend")

    repo = f"gcr.io/{project}/{service}"
    frontend_dir = Path(__file__).resolve().parents[1] / "frontend"

    run(["gcloud", "builds", "submit", str(frontend_dir), "--tag", repo])
    run([
        "gcloud",
        "run",
        "deploy",
        service,
        "--image",
        repo,
        "--region",
        region,
        "--platform",
        "managed",
        "--allow-unauthenticated",
    ])


if __name__ == "__main__":
    main()
