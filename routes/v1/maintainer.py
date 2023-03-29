from datetime import timedelta
from http import HTTPStatus
from typing import Final

import requests
from fastapi import APIRouter, Body, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm

from scripts.dependencies import checked_token
from scripts.shared.http_exc import get_http_exc_with_detail
from scripts.shared.security import (Token, create_access_token,
                                     is_admin_credentials_ok)
from scripts.shared.twofactor import get_secure_code, send_code_over_2f

EXPIRE_TIME_IN_MINS_2F: Final[int] = 2

base_maintainer_router = APIRouter(prefix = "/maintainer", tags = ["maintainer"])

twofactor_router = APIRouter(prefix = "/2f_auth", dependencies = [
        Security(checked_token, scopes = "maintainer_2f")
    ]
)

maintainer_router = APIRouter(dependencies = [
        Security(checked_token, scopes = ["maintainer"])
    ]
)

@base_maintainer_router.get("/token")
async def login_for_2f_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if not is_admin_credentials_ok(form_data.username, form_data.password, maintainer = True):
        raise get_http_exc_with_detail(
            HTTPStatus.UNAUTHORIZED,
            "Incorrect username or password"
        )

    access_token = create_access_token(
        data = {
            "sub": form_data.username,
            "scopes": ["maintainer_2f"]
        },
        expires_delta = timedelta(minutes = EXPIRE_TIME_IN_MINS_2F)
    )

    return Token(access_token = access_token)

@base_maintainer_router.post("/send_code") #! it must be twofactor_router
async def send_code():
    # twofactor_code_handler.setNewCode(get_secure_code())
    send_code_over_2f(get_secure_code())

@twofactor_router.get("/login", response_model = Token)
async def login_with_2f_token(two_factor_token: str = Body(...)):...

@maintainer_router.post("/admins/add")
async def add_admin():
    ...

@maintainer_router.post("/admins/get_all")
async def get_admins():
    ...

@maintainer_router.post("/admins/get")
async def get_particular_admin():
    ...

@maintainer_router.post("/admins/update")
async def update_admin():
    ...

@maintainer_router.delete("/admins/delete")
async def delete_admin():
    ...
