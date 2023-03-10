from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, Path, Security

from pydantic_models.event import EventModelWithId
from scripts.dependencies import checked_token
from scripts.shared.security import Token, create_access_token
from scripts.v1.add_new_record import new_record
from scripts.v1.get_event_details import (active_event,
                                          is_correct_password_for_event)

router = APIRouter()

@router.get("/event", response_model = Optional[EventModelWithId])
def get_ongoin_event():
    return active_event()

@router.post("/event_login/{event_id}", response_model = Token)
def try_to_login_to_event(
    event_id: UUID = Path(...),
    user_random_id: str = Body(min_length = 6),
    event_password: str = Body()
):
    if not is_correct_password_for_event(event_id, event_password):
        raise HTTPException(
            status_code = HTTPStatus.UNAUTHORIZED,
            detail = "Incorrect password",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data = {
            "sub": user_random_id,
            "scopes": ["user"]
        }
    )

    return Token(access_token = access_token)

@router.post("/record_request/{event_id}")
def send_record_request(
    event_id: UUID = Path(...),
    record_request: str = Body(...),
    token: str = Security(checked_token, scopes = ["user"])
):
    new_record(event_id, record_request)