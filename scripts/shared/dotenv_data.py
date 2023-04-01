from enum import Enum
from os import getenv
from pathlib import Path
from typing import Any, List


class AllowedEnvKey(Enum):
    DATABASE_URL = "DATABASE_URL"
    DATABASE_BACKUP = "DATABASE_BACKUP" 
    DB_BACKUP_STRATEGY = "DB_BACKUP_STRATEGY"

    # JWT
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ALGORITHM = "JWT_ALGORITHM"
    JWT_EXPIRE_MINS = "JWT_EXPIRE_MINS"

    # CORS
    ALLOW_ORIGINS = "ALLOW_ORIGINS"
    ALLOW_CREDENTIALS = "ALLOW_CREDENTIALS"
    ALLOW_METHODS = "ALLOW_METHODS"
    ALLOW_HEADERS = "ALLOW_HEADERS"

    # 2f
    INITIAL_WEBHOOKS_2F_URL = "INITIAL_WEBHOOKS_2F_URL"

    ENV_FILE_PATH = "ENV_FILE_PATH" # this must be provided by the runner

def get_env_data(env_key: AllowedEnvKey) -> Any:
    "Returns env data based on the provided key"
    # NOTE: to be able to get data from dotenv file too it must be loaded! 

    assert env_key in AllowedEnvKey
    
    return getenv(env_key.value)

def get_cors_conf(env_key: AllowedEnvKey) -> List[str]:
    "Returns cors data from .env file"
    return get_env_data(env_key).split()

def get_env_file_path(env_key: AllowedEnvKey = AllowedEnvKey.ENV_FILE_PATH) -> Path:
    dotenv_file_path = Path(get_env_data(env_key))

    if not dotenv_file_path.exists():
        raise AttributeError(".env file was not found!")

    return dotenv_file_path