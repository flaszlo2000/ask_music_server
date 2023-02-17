#!/bin/bash

gunicorn main:app --workers $SERVICE_WORKERS --worker-class uvicorn.workers.UvicornWorker