#!/bin/bash
set -euf -o pipefail

export ENV_FILE_PATH=.env
export SERVICE_WORKERS=4
export DB_BACKUP_STRATEGY=0 # WARNING: this must be 0/1 bc it is used as index, see db_backup.py
export JWT_SECRET_KEY=testsecretkey
export JWT_ALGORITHM=HS256
export JWT_EXPIRE_MINS=30

if [[ ! -v TEST_BACKUP ]]; then
    # ./server.sh
    uvicorn main:app --reload
else
    echo "[*] Generating random data and testing backup"
    python3 ./generate_random_db_content.py && python3 ./db_backup.py
fi