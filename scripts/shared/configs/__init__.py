from typing import Callable, Dict, Final

from db.app_config import get_jwt_secret_key_from_db
from scripts.shared.configs.security_config_names import SecurityConfigNames
from scripts.shared.configs.smart_config import SmartConfig
from scripts.shared.dotenv_data import AllowedEnvKey, get_env_data

__security_config: Final[Dict[SecurityConfigNames, Callable[[], str]]] = {
        SecurityConfigNames.DEFAULT_EXP_MINS: lambda: get_env_data(AllowedEnvKey.JWT_EXPIRE_MINS),
        SecurityConfigNames.JWT_SECRET_KEY: get_jwt_secret_key_from_db,
        SecurityConfigNames.JWT_ALGORITHM: lambda: get_env_data(AllowedEnvKey.JWT_ALGORITHM)
    }

GlobalSecurityConfig = SmartConfig[SecurityConfigNames](__security_config)

__all__ = ["SmartConfig"]
