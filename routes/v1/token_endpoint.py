from datetime import timedelta
from http import HTTPStatus
from typing import Final, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from scripts.shared.http_exc import get_http_exc_with_detail
from scripts.shared.security import (Roles, Token, create_access_token,
                                     is_admin_credentials_ok)
from scripts.static import code_handler
from scripts.v1.get_event_details import is_correct_password_for_event

token_router = APIRouter()
TWOFACTOR_EXPIRE_TIME_IN_MINS: Final[int] = 3


@token_router.post("/token", response_model = Token)
async def token_endpoint(form_data: OAuth2PasswordRequestForm = Depends()):
    _sub = "random_id_generated" # FIXME
    wanted_roles: List[str] = []
    _expires_delta: Optional[timedelta] = None
    unauthorized_exc = get_http_exc_with_detail(
        HTTPStatus.UNAUTHORIZED,
        "Incorrect credential"
    )

    if Roles.MAINTAINER in form_data.scopes:
        # form_data.password is the sent out twofactor code here
        if not code_handler.checkIf2FCodeIsCorrect(form_data.username, form_data.password):
            raise unauthorized_exc

        code_handler.forget(form_data.username)

        _sub = form_data.username
        wanted_roles.extend((Roles.MAINTAINER, Roles.ADMIN, Roles.USER))

    elif Roles.MAINTAINER_2F in form_data.scopes:
        if not is_admin_credentials_ok(form_data.username, form_data.password, maintainer = True):
            raise unauthorized_exc

        _sub = form_data.username
        _expires_delta = timedelta(minutes = TWOFACTOR_EXPIRE_TIME_IN_MINS)
        wanted_roles.append(Roles.MAINTAINER_2F)

    elif Roles.ADMIN in form_data.scopes:
        if not is_admin_credentials_ok(form_data.username, form_data.password):
            raise unauthorized_exc

        _sub = form_data.username
        wanted_roles.extend((Roles.ADMIN, Roles.USER))

    elif Roles.USER in form_data.scopes:
        # form_data.username is the event_id here
        try:
            event_id = UUID(form_data.username)
        except ValueError:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect format")

        if not is_correct_password_for_event(event_id, form_data.password):
            raise unauthorized_exc

        wanted_roles.append(Roles.USER)

    else:
        raise HTTPException(HTTPStatus.NOT_FOUND)


    return Token(
        access_token = create_access_token(
            data = {
                "sub": _sub,
                "scopes": wanted_roles
            },
            expires_delta = _expires_delta
        )
    )
