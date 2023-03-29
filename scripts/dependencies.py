from http import HTTPStatus
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose.exceptions import JWTError

from scripts import __version__
from scripts.shared.http_exc import CONIFGS
from scripts.shared.security import get_payload_from_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = f"{__version__}/admin/token", scopes = {
        "user": "Normal user privilige, add records to current event",
        "admin": "Admin priviliges",
        "maintainer_2f": "Maintainer 2 factor auth page access",
        "maintainer": "Handle admins"
    }
)
# TODO: add multiple OAuth2PasswordBearer objects to separate scopes, via this, Swagger will work again

async def checked_token(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
) -> str:
    credential_exc_conf: Dict[str, Any] = {
        **CONIFGS[HTTPStatus.UNAUTHORIZED],
        "detail": "Could not validate credentials",
    }

    if security_scopes.scopes:
        credential_exc_conf["headers"]["WWW-Authenticate"] = f'Bearer scope="{security_scopes.scope_str}"'

    try:
        payload = get_payload_from_token(token)
        username: Optional[str] = payload.get("sub")
        token_scopes = payload.get("scopes", [])

        if username is None:
            raise HTTPException(**credential_exc_conf)
    except JWTError:
        raise HTTPException(**credential_exc_conf)

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(**credential_exc_conf)

    return token