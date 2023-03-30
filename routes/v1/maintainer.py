from datetime import timedelta
from functools import lru_cache
from http import HTTPStatus
from typing import Final, List

from fastapi import APIRouter, Body, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from requests.exceptions import ConnectionError

from pydantic_models.admin import AdminModel, DetailedAdminConfigModel
from scripts.dependencies import checked_token
from scripts.shared.http_exc import get_http_exc_with_detail
from scripts.shared.security import (Token, create_access_token,
                                     get_payload_from_token,
                                     is_admin_credentials_ok)
from scripts.shared.twofactor import (CodeHandler, get_secure_code,
                                      send_code_over_2f)
from scripts.v1.admin_handling import add_admin_to_db, get_all_admins

TWOFACTOR_EXPIRE_TIME_IN_MINS: Final[int] = 3

base_maintainer_router = APIRouter(prefix = "/maintainer", tags = ["maintainer"])
twofactor_router = APIRouter(prefix = "/2f_auth", dependencies = [
        Security(checked_token, scopes = ["maintainer_2f"])
    ]
)
maintainer_router = APIRouter(dependencies = [
        Security(checked_token, scopes = ["maintainer"])
    ]
)

#region twofactor login
@lru_cache # by caching I can make simple singleton here
def get_2f_code_handler() -> CodeHandler:
    return CodeHandler()

@base_maintainer_router.post("/token")
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
        expires_delta = timedelta(minutes = TWOFACTOR_EXPIRE_TIME_IN_MINS)
    )

    return Token(access_token = access_token)

@twofactor_router.post("/send_code")
async def send_code(twofactor_code_handler: CodeHandler = Depends(get_2f_code_handler)):
    "Sends out twofactor token via webhooks" # TODO: google authenticator ?
    #! WARNING: at the first startup, env link will be used but then
    #! it is going to be added to the db and env won't be checked again
    secure_code = get_secure_code()
    twofactor_code_handler.add(secure_code, "")

    try:
        response = send_code_over_2f(secure_code)
        
        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                HTTPStatus.CONFLICT,
                "Unknown error during 2f notification sending"
            )
    except ConnectionError:
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            "Connection outage"
        )

async def get_current_user_from_jwt(token: str = Security(checked_token, scopes = ["maintainer_2f"])) -> str:
    jwt_payload = get_payload_from_token(token)
    username = jwt_payload.get("sub")

    if username is None:
        raise get_http_exc_with_detail(
            HTTPStatus.UNAUTHORIZED,
            "Incorrect data"
        )

    return username

@twofactor_router.post("/login", response_model = Token) 
async def login_with_2f_token(
    twofactor_token: str = Body(...),
    twofactor_code_handler: CodeHandler = Depends(get_2f_code_handler),
    current_user: str = Depends(get_current_user_from_jwt)
):
    "Accepts twofactor token from user and compares it to the saved one"
    if not twofactor_code_handler.checkIfCodeIsCorrect(twofactor_token):
        raise get_http_exc_with_detail(
            HTTPStatus.UNAUTHORIZED,
            "Incorrect credential"
        )

    access_token = create_access_token(
        data = {
            "sub": current_user,
            "scopes": ["user, admin, maintainer"]
        }
    )

    return Token(access_token = access_token)
#endregion

@base_maintainer_router.post("/admins/add")
def add_admin(admin_credentials: DetailedAdminConfigModel):
    add_admin_to_db(admin_credentials)

@maintainer_router.get("/admins/get_all", response_model = List[AdminModel])
def get_admins():
    return get_all_admins()

@maintainer_router.get("/admins/get")
def get_particular_admin():
    ...

@maintainer_router.put("/admins/update")
def update_admin():
    ...

@maintainer_router.delete("/admins/delete")
def delete_admin():
    ...

@maintainer_router.put("/change_webhook_url")
def change_webhook_url(new_webhook_url: str = Body(...)):
    #! DANGER: if the webhook url gets changed here but the updated url gets removed from the db 
    #! in a way when no other left, then the url in the .env will be used again!
    #! This could be a security risk.
    ...