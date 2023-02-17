#!/bin/bash

export ENV_FILE_PATH=.env
gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
