#!/bin/bash
set -e

gcloud builds submit .. --tag gcr.io/myproject/maxx-backend
