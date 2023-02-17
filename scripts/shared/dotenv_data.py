from enum import Enum
from os import getenv
from typing import Any


class AllowedEnvKey(Enum):
    DATABASE_URL = "DATABASE_URL"

def get_env_data(env_key: AllowedEnvKey) -> Any:
    "Returns env data based on the provided key"
    # NOTE: to be able to get data from dotenv file too it must be loaded! 

    assert env_key in AllowedEnvKey
    
    return getenv(env_key.value)