from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException
from fastapi.security import SecurityScopes
from jose.exceptions import JWTError

from scripts.shared.http_exc import CONIFGS
from scripts.shared.security import get_payload_from_token
from scripts.shared.security.oauth import oauth2_scheme
from scripts.shared.security.permission_checks import (
    check_admin_exist, check_maintainer_permission)


@dataclass
class UsernameWithToken:
    username: str
    token: str


async def token_checker(security_scopes: SecurityScopes, token: str) -> UsernameWithToken:
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

    return UsernameWithToken(username, token)

async def user_checked_token(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
):
    username_with_token = await token_checker(security_scopes, token)

    return username_with_token.token

async def admin_checked_token(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
) -> str:
    username_with_token = await token_checker(security_scopes, token)
    await check_admin_exist(username_with_token.username)

    return username_with_token.token

async def twofactor_maintainer_checked_token(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
) -> str:
    username_with_token = await token_checker(security_scopes, token)
    await check_maintainer_permission(username_with_token.username)

    return username_with_token.token

async def full_maintainer_checked_token(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
) -> str:
    username_with_token = await token_checker(security_scopes, token)
    await check_maintainer_permission(username_with_token.username)

    return username_with_token.token