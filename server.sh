#!/bin/bash

gunicorn main:app --worker-class uvicorn.workers.UvicornWorker