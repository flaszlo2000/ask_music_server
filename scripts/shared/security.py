from datetime import datetime, timedelta
from typing import Any, Dict, Final, Optional

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from db.models.admins import DBAdmins
from db.singleton_handler import global_db_handler
from scripts.shared.dotenv_data import (AllowedEnvKey, get_env_data,
                                        get_env_file_path)

load_dotenv(get_env_file_path())
__DEFAULT_EXP_MINS: Final[int] = int(get_env_data(AllowedEnvKey.JWT_EXPIRE_MINS))
__JWT_SECRET_KEY: Final[str] = get_env_data(AllowedEnvKey.JWT_SECRET_KEY)
__JWT_ALGORITHM: Final[str] = get_env_data(AllowedEnvKey.JWT_ALGORITHM)

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default = "bearer")

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta is None:
        expires_delta = timedelta(minutes = __DEFAULT_EXP_MINS) 

    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, __JWT_SECRET_KEY, algorithm = __JWT_ALGORITHM)

    return encoded_jwt

def get_payload_from_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, __JWT_SECRET_KEY, algorithms = [__JWT_ALGORITHM])

def is_admin_credentials_ok(username: str, password: str) -> bool:
    db_handler = global_db_handler()

    with db_handler.session() as session:
        orm_inst = session.query(DBAdmins.password).filter(DBAdmins.username == username).first()

        if orm_inst is None: return False


    return pwd_context.verify(password, orm_inst[0])