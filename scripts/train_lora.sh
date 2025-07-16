#!/bin/bash
# Trigger LoRA fine-tuning for the model.
# TODO: add actual training script invocation when available.

set -euo pipefail
python -m lora_training "$@"
