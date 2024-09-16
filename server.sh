#!/bin/bash
set -euf -o pipefail

uvicorn main:app --workers $SERVICE_WORKERS --host $HOST --port $PORT