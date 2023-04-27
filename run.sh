#!/bin/bash
set -euf -o pipefail

export ENV_FILE_PATH=.env
export DB_BACKUP_STRATEGY=0 # WARNING: this must be 0/1 bc it is used as index, see db_backup.py

export SERVICE_WORKERS=1
export HOST=localhost
export PORT=8080

if [[ ! -v TEST_BACKUP ]]; then
    ./server.sh
else
    echo "[*] Generating random data and testing backup"
    python3 ./generate_random_db_content.py && python3 ./db_backup.py
fi