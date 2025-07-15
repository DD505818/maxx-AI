#!/usr/bin/env bash
# build, push & deploy MAXX-AI on GKE
set -euo pipefail

PROJECT="${1?PROJECT_ID missing}"
REGION="${2?REGION missing}"
PREFIX="${3?IMAGE prefix missing}"
CLUSTER="${4?GKE CLUSTER missing}"
ZONE="${5?GKE ZONE missing}"

# 0) housekeeping
gcloud config set project "$PROJECT"
gcloud auth configure-docker "$REGION-docker.pkg.dev" -q

# 1) Build & push images
BACKEND_IMAGE="$REGION-docker.pkg.dev/$PROJECT/${PREFIX}-backend:latest"
FRONTEND_IMAGE="$REGION-docker.pkg.dev/$PROJECT/${PREFIX}-frontend:latest"

gcloud builds submit ./backend --tag "$BACKEND_IMAGE"
gcloud builds submit ./frontend --tag "$FRONTEND_IMAGE"

# 2) Get GKE credentials
gcloud container clusters get-credentials "$CLUSTER" --zone "$ZONE"

# 3) Create namespace if absent
kubectl get ns maxx-ai || kubectl create ns maxx-ai

# 4) Generate k8s manifests
mkdir -p k8s

cat > k8s/backend-deployment.yaml <<EOM
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: maxx-ai
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: $BACKEND_IMAGE
        ports:
        - containerPort: 8000
        env:
        - name: PYTHONUNBUFFERED
          value: "1"
---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: maxx-ai
spec:
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 8000
EOM

cat > k8s/frontend-deployment.yaml <<EOM
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: maxx-ai
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: $FRONTEND_IMAGE
        ports:
        - containerPort: 3000
        env:
        - name: PORT
          value: "3000"
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: maxx-ai
spec:
  type: ClusterIP
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 3000
EOM

cat > k8s/ingress.yaml <<EOM
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: maxx-ai-ingress
  namespace: maxx-ai
  annotations:
    kubernetes.io/ingress.class: "gce"
spec:
  defaultBackend:
    service:
      name: frontend
      port:
        number: 80
EOM

# 5) Deploy
kubectl apply -f k8s

