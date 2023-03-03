from datetime import datetime, timedelta
from typing import Any, Dict, Final, Optional

from jose import jwt
from pydantic import BaseModel, Field

from scripts.shared.dotenv_data import AllowedEnvKey, get_env_data

__DEFAULT_EXP_MINS: Final[int] = int(get_env_data(AllowedEnvKey.JWT_EXPIRE_MINS))
__JWT_SECRET_KEY: Final[str] = get_env_data(AllowedEnvKey.JWT_SECRET_KEY)
__JWT_ALGORITHM: Final[str] = get_env_data(AllowedEnvKey.JWT_ALGORITHM)

class Token(BaseModel):
    access_token: str
    token_type: str = Field(default = "bearer")

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta is None:
        expires_delta = timedelta(minutes = __DEFAULT_EXP_MINS) 

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, __JWT_SECRET_KEY, algorithm = __JWT_ALGORITHM)

    return encoded_jwt

def get_payload_from_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, __JWT_SECRET_KEY, algorithms = [__JWT_ALGORITHM])
