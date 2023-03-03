from http import HTTPStatus
from typing import Final, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext

from scripts.shared.security import get_payload_from_token

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = "token", scopes = {
        "user": "Normal user privilige, add records to current event",
        "admin": "Admin priviliges"
    }
)

CREDENTIAL_EXC: Final[HTTPException] = HTTPException(
    status_code = HTTPStatus.UNAUTHORIZED,
    detail = "Could not validate credentials",
    headers = {"WWW-Authenticate": "Bearer"},
)

async def checked_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = get_payload_from_token(token)
        username: Optional[str] = payload.get("sub")

        if username is None:
            raise CREDENTIAL_EXC
        
    except ExpiredSignatureError:
        raise CREDENTIAL_EXC

    return token