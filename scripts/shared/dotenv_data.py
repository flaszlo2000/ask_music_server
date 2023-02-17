from enum import Enum
from os import getenv
from typing import Any, List


class AllowedEnvKey(Enum):
    DATABASE_URL = "DATABASE_URL"
    ALLOW_ORIGINS = "ALLOW_ORIGINS"
    ALLOW_CREDENTIALS = "ALLOW_CREDENTIALS"
    ALLOW_METHODS = "ALLOW_METHODS"
    ALLOW_HEADERS = "ALLOW_HEADERS"

def get_env_data(env_key: AllowedEnvKey) -> Any:
    "Returns env data based on the provided key"
    # NOTE: to be able to get data from dotenv file too it must be loaded! 

    assert env_key in AllowedEnvKey
    
    return getenv(env_key.value)

def get_cors_conf(env_key: AllowedEnvKey) -> List[str]:
    return get_env_data(env_key).split()